"""Generate comprehensive dummy crime data for the intelligence system."""

import random
import pandas as pd
from faker import Faker
from datetime import datetime, timedelta
import json
from config.database import db

# Initialize Faker with Indian locale
fake = Faker(['en_IN', 'hi_IN'])

# Crime categories and types
CRIME_CATEGORIES = {
    'Violent Crimes': ['Murder', 'Assault', 'Robbery', 'Kidnapping', 'Rape'],
    'Property Crimes': ['Theft', 'Burglary', 'Fraud', 'Embezzlement', 'Vandalism'],
    'Drug Crimes': ['Drug Trafficking', 'Drug Possession', 'Drug Manufacturing'],
    'Cyber Crimes': ['Identity Theft', 'Online Fraud', 'Hacking', 'Cyberbullying'],
    'Organized Crime': ['Money Laundering', 'Racketeering', 'Human Trafficking']
}

INDIAN_CITIES = [
    'Mumbai', 'Delhi', 'Bangalore', 'Chennai', 'Kolkata', 'Hyderabad',
    'Pune', 'Ahmedabad', 'Surat', 'Jaipur', 'Lucknow', 'Kanpur',
    'Nagpur', 'Indore', 'Thane', 'Bhopal', 'Visakhapatnam', 'Pimpri'
]

def generate_persons(n=1000):
    """Generate dummy person records (suspects, victims, witnesses)."""
    persons = []
    
    for i in range(n):
        person = {
            'id': f'P{i+1:04d}',
            'name': fake.name(),
            'age': random.randint(18, 80),
            'gender': random.choice(['Male', 'Female']),
            'address': fake.address().replace('\n', ', '),
            'phone': fake.phone_number(),
            'occupation': fake.job(),
            'education': random.choice(['Illiterate', 'Primary', 'Secondary', 'Graduate', 'Post-Graduate']),
            'income_level': random.choice(['Low', 'Medium', 'High']),
            'criminal_history': random.choice([True, False]),
            'created_at': fake.date_time_between(start_date='-5y', end_date='now')
        }
        persons.append(person)
    
    return persons

def generate_locations(n=200):
    """Generate location data with crime hotspot information."""
    locations = []
    
    for i in range(n):
        city = random.choice(INDIAN_CITIES)
        location = {
            'id': f'L{i+1:04d}',
            'name': fake.street_name(),
            'city': city,
            'state': fake.state(),
            'pincode': fake.postcode(),
            'latitude': fake.latitude(),
            'longitude': fake.longitude(),
            'area_type': random.choice(['Residential', 'Commercial', 'Industrial', 'Rural']),
            'crime_rate': random.choice(['Low', 'Medium', 'High']),
            'police_station': f"{city} Police Station"
        }
        locations.append(location)
    
    return locations

def generate_cases(persons, locations, n=500):
    """Generate FIR cases with detailed information."""
    cases = []
    
    for i in range(n):
        crime_category = random.choice(list(CRIME_CATEGORIES.keys()))
        crime_type = random.choice(CRIME_CATEGORIES[crime_category])
        
        case = {
            'fir_number': f'FIR{i+1:06d}',
            'case_title': f"{crime_type} Case",
            'crime_category': crime_category,
            'crime_type': crime_type,
            'date_registered': fake.date_time_between(start_date='-2y', end_date='now'),
            'location_id': random.choice(locations)['id'],
            'investigating_officer': fake.name(),
            'status': random.choice(['Under Investigation', 'Closed', 'Pending', 'Court Trial']),
            'description': f"Case involving {crime_type.lower()} reported on {fake.date()}",
            'severity': random.choice(['Low', 'Medium', 'High', 'Critical']),
            'evidence_collected': random.choice([True, False]),
            'court_proceedings': random.choice([True, False])
        }
        cases.append(case)
    
    return cases

def generate_relationships(persons, cases):
    """Generate relationships between persons and cases."""
    relationships = []
    
    for case in cases:
        # Each case has 1-3 accused, 1-2 victims, 0-3 witnesses
        num_accused = random.randint(1, 3)
        num_victims = random.randint(1, 2)
        num_witnesses = random.randint(0, 3)
        
        case_persons = random.sample(persons, min(len(persons), num_accused + num_victims + num_witnesses))
        
        # Assign roles
        for i, person in enumerate(case_persons):
            if i < num_accused:
                role = 'Accused'
            elif i < num_accused + num_victims:
                role = 'Victim'
            else:
                role = 'Witness'
            
            relationships.append({
                'person_id': person['id'],
                'case_fir': case['fir_number'],
                'role': role,
                'involvement_date': case['date_registered']
            })
    
    return relationships

def generate_criminal_networks():
    """Generate criminal network associations."""
    networks = []
    network_types = ['Drug Cartel', 'Theft Gang', 'Fraud Ring', 'Human Trafficking', 'Cybercrime Group']
    
    for i in range(20):
        network = {
            'network_id': f'NET{i+1:03d}',
            'name': f"{random.choice(network_types)} #{i+1}",
            'type': random.choice(network_types),
            'activity_level': random.choice(['Active', 'Dormant', 'Disbanded']),
            'threat_level': random.choice(['Low', 'Medium', 'High', 'Critical']),
            'established_date': fake.date_between(start_date='-10y', end_date='-1y'),
            'known_activities': random.sample(list(sum(CRIME_CATEGORIES.values(), [])), random.randint(2, 5))
        }
        networks.append(network)
    
    return networks

def store_data_in_neo4j(persons, locations, cases, relationships, networks):
    """Store all generated data in Neo4j database."""
    
    if not db.connect():
        print("Failed to connect to Neo4j database")
        return
    
    # Create constraints first
    db.create_constraints()
    
    # Clear existing data
    db.execute_query("MATCH (n) DETACH DELETE n")
    
    # Create Person nodes
    for person in persons:
        query = """
        CREATE (p:Person {
            id: $id, name: $name, age: $age, gender: $gender,
            address: $address, phone: $phone, occupation: $occupation,
            education: $education, income_level: $income_level,
            criminal_history: $criminal_history, created_at: $created_at
        })
        """
        db.execute_query(query, person)
    
    # Create Location nodes
    for location in locations:
        query = """
        CREATE (l:Location {
            id: $id, name: $name, city: $city, state: $state,
            pincode: $pincode, latitude: $latitude, longitude: $longitude,
            area_type: $area_type, crime_rate: $crime_rate,
            police_station: $police_station
        })
        """
        db.execute_query(query, location)
    
    # Create Case nodes
    for case in cases:
        query = """
        CREATE (c:Case {
            fir_number: $fir_number, case_title: $case_title,
            crime_category: $crime_category, crime_type: $crime_type,
            date_registered: $date_registered, location_id: $location_id,
            investigating_officer: $investigating_officer, status: $status,
            description: $description, severity: $severity,
            evidence_collected: $evidence_collected,
            court_proceedings: $court_proceedings
        })
        """
        db.execute_query(query, case)
    
    # Create Network nodes
    for network in networks:
        query = """
        CREATE (n:Network {
            network_id: $network_id, name: $name, type: $type,
            activity_level: $activity_level, threat_level: $threat_level,
            established_date: $established_date, 
            known_activities: $known_activities
        })
        """
        db.execute_query(query, network)
    
    # Create relationships
    for rel in relationships:
        query = """
        MATCH (p:Person {id: $person_id})
        MATCH (c:Case {fir_number: $case_fir})
        CREATE (p)-[:INVOLVED_IN {role: $role, date: $involvement_date}]->(c)
        """
        db.execute_query(query, rel)
    
    # Connect cases to locations
    for case in cases:
        query = """
        MATCH (c:Case {fir_number: $fir_number})
        MATCH (l:Location {id: $location_id})
        CREATE (c)-[:OCCURRED_AT]->(l)
        """
        db.execute_query(query, {'fir_number': case['fir_number'], 'location_id': case['location_id']})
    
    print(f"✅ Successfully created {len(persons)} persons, {len(locations)} locations, {len(cases)} cases, and {len(networks)} networks")
    db.close()

if __name__ == "__main__":
    print("🔄 Generating dummy crime intelligence data...")
    
    # Generate all data
    persons = generate_persons(1000)
    locations = generate_locations(200)
    cases = generate_cases(persons, locations, 500)
    relationships = generate_relationships(persons, cases)
    networks = generate_criminal_networks()
    
    # Store in Neo4j
    store_data_in_neo4j(persons, locations, cases, relationships, networks)
    
    # Also save as JSON files for backup
    with open('data/persons.json', 'w') as f:
        json.dump(persons, f, indent=2, default=str)
    
    with open('data/locations.json', 'w') as f:
        json.dump(locations, f, indent=2)
    
    with open('data/cases.json', 'w') as f:
        json.dump(cases, f, indent=2, default=str)
    
    with open('data/networks.json', 'w') as f:
        json.dump(networks, f, indent=2, default=str)
    
    print("✅ Data generation completed successfully!")