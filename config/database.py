"""Database configuration and connection management."""

import os
from neo4j import GraphDatabase
from dotenv import load_dotenv

load_dotenv()

class Neo4jConnection:
    def __init__(self):
        self.uri = os.getenv('NEO4J_URI', 'bolt://localhost:7687')
        self.user = os.getenv('NEO4J_USER', 'neo4j')
        self.password = os.getenv('NEO4J_PASSWORD', 'password')
        self.driver = None
        
    def connect(self):
        """Establish connection to Neo4j database."""
        try:
            self.driver = GraphDatabase.driver(
                self.uri, 
                auth=(self.user, self.password)
            )
            return True
        except Exception as e:
            print(f"Failed to connect to Neo4j: {e}")
            return False
    
    def close(self):
        """Close database connection."""
        if self.driver:
            self.driver.close()
    
    def execute_query(self, query, parameters=None):
        """Execute a Cypher query."""
        with self.driver.session() as session:
            result = session.run(query, parameters or {})
            return result.data()
    
    def create_constraints(self):
        """Create database constraints and indexes."""
        constraints = [
            "CREATE CONSTRAINT person_id IF NOT EXISTS FOR (p:Person) REQUIRE p.id IS UNIQUE",
            "CREATE CONSTRAINT case_id IF NOT EXISTS FOR (c:Case) REQUIRE c.fir_number IS UNIQUE",
            "CREATE CONSTRAINT location_id IF NOT EXISTS FOR (l:Location) REQUIRE l.id IS UNIQUE",
            "CREATE INDEX person_name IF NOT EXISTS FOR (p:Person) ON (p.name)",
            "CREATE INDEX case_date IF NOT EXISTS FOR (c:Case) ON (c.date_registered)",
            "CREATE INDEX location_name IF NOT EXISTS FOR (l:Location) ON (l.name)"
        ]
        
        for constraint in constraints:
            try:
                self.execute_query(constraint)
                print(f"Created constraint/index: {constraint.split()[1]}")
            except Exception as e:
                print(f"Constraint already exists or error: {e}")

# Global database instance
db = Neo4jConnection()