"""Investigator Agent for crime record queries and case management."""

from crewai import Task
from crewai_tools import BaseTool
from agents.base_agent import BaseCrimeAgent
from typing import Type
from pydantic import BaseModel, Field

class CaseQueryInput(BaseModel):
    query: str = Field(description="Natural language query about cases")

class PersonQueryInput(BaseModel):
    query: str = Field(description="Natural language query about persons")

class LocationQueryInput(BaseModel):
    query: str = Field(description="Natural language query about locations")

class CaseQueryTool(BaseTool):
    name: str = "case_query_tool"
    description: str = "Search and retrieve information about FIR cases, investigation status, and case details"
    args_schema: Type[BaseModel] = CaseQueryInput
    
    def _run(self, query: str) -> str:
        # This tool will be injected with database access
        pass

class PersonQueryTool(BaseTool):
    name: str = "person_query_tool" 
    description: str = "Search for information about accused, victims, witnesses, and their criminal history"
    args_schema: Type[BaseModel] = PersonQueryInput
    
    def _run(self, query: str) -> str:
        # This tool will be injected with database access
        pass

class LocationQueryTool(BaseTool):
    name: str = "location_query_tool"
    description: str = "Search for location-based crime information and geographical data"
    args_schema: Type[BaseModel] = LocationQueryInput
    
    def _run(self, query: str) -> str:
        # This tool will be injected with database access
        pass

class InvestigatorAgent(BaseCrimeAgent):
    """Agent responsible for investigating crime records and case management."""
    
    def __init__(self):
        super().__init__(
            role="Crime Investigator",
            goal="Retrieve and analyze crime records, FIRs, case status, and criminal history to assist in investigations",
            backstory="""You are an experienced crime investigator with deep knowledge of Indian criminal law and investigation procedures. 
            You have access to comprehensive crime databases and can search through FIRs, case records, and criminal histories.
            You can understand queries in English and Indian regional languages. Your expertise lies in finding connections 
            between cases, tracking investigation progress, and providing detailed information about accused persons and victims."""
        )
    
    def get_tools(self):
        """Get investigator-specific tools."""
        # Create custom tools with database access
        case_tool = CaseQueryTool()
        person_tool = PersonQueryTool()
        location_tool = LocationQueryTool()
        
        # Inject database methods
        case_tool._run = self._case_query_handler
        person_tool._run = self._person_query_handler  
        location_tool._run = self._location_query_handler
        
        return [case_tool, person_tool, location_tool]
    
    def _case_query_handler(self, query: str) -> str:
        """Handle case-related queries."""
        query_lower = query.lower()
        
        # Extract FIR number if present
        if 'fir' in query_lower:
            words = query.split()
            for word in words:
                if word.startswith('FIR') or word.startswith('fir'):
                    fir_num = word.upper()
                    result = self.get_case_info(fir_number=fir_num)
                    if result:
                        return f"Case Information for {fir_num}: {result}"
        
        # Search by crime type
        crime_keywords = ['murder', 'theft', 'fraud', 'assault', 'robbery', 'kidnapping']
        for keyword in crime_keywords:
            if keyword in query_lower:
                result = self.get_case_info(crime_type=keyword.title())
                return f"Cases related to {keyword}: {result}"
        
        # General case search
        cypher = """
        MATCH (c:Case)
        WHERE c.case_title CONTAINS $query OR c.description CONTAINS $query
        OPTIONAL MATCH (c)-[:OCCURRED_AT]->(l:Location)
        RETURN c.fir_number, c.case_title, c.status, c.crime_type, l.name as location
        LIMIT 10
        """
        result = self.query_database(cypher, {'query': query})
        return f"Search results: {result}"
    
    def _person_query_handler(self, query: str) -> str:
        """Handle person-related queries."""
        query_lower = query.lower()
        
        # Extract person ID if present
        if query.startswith('P') and query[1:].isdigit():
            result = self.get_person_info(person_id=query)
            return f"Person Information: {result}"
        
        # Search by name
        if any(word in query_lower for word in ['name', 'person', 'accused', 'victim']):
            # Extract potential name from query
            words = query.split()
            name_candidates = [word for word in words if word.istitle() and len(word) > 2]
            if name_candidates:
                result = self.get_person_info(name=name_candidates[0])
                return f"Person search results: {result}"
        
        # Search for criminal history
        if 'criminal history' in query_lower or 'previous cases' in query_lower:
            cypher = """
            MATCH (p:Person {criminal_history: true})
            MATCH (p)-[r:INVOLVED_IN]->(c:Case)
            WHERE r.role = 'Accused'
            RETURN p.name, p.id, count(c) as case_count
            ORDER BY case_count DESC
            LIMIT 10
            """
            result = self.query_database(cypher)
            return f"Persons with criminal history: {result}"
        
        return f"Could not process person query: {query}"
    
    def _location_query_handler(self, query: str) -> str:
        """Handle location-related queries."""
        query_lower = query.lower()
        
        # Search by city or location name
        if any(city in query_lower for city in ['mumbai', 'delhi', 'bangalore', 'chennai', 'kolkata']):
            city_name = next(city for city in ['Mumbai', 'Delhi', 'Bangalore', 'Chennai', 'Kolkata'] 
                           if city.lower() in query_lower)
            cypher = """
            MATCH (l:Location {city: $city})
            OPTIONAL MATCH (c:Case)-[:OCCURRED_AT]->(l)
            RETURN l.name, l.area_type, l.crime_rate, count(c) as case_count
            ORDER BY case_count DESC
            LIMIT 10
            """
            result = self.query_database(cypher, {'city': city_name})
            return f"Location information for {city_name}: {result}"
        
        # Crime hotspots
        if 'hotspot' in query_lower or 'high crime' in query_lower:
            cypher = """
            MATCH (l:Location)
            MATCH (c:Case)-[:OCCURRED_AT]->(l)
            RETURN l.name, l.city, l.crime_rate, count(c) as case_count
            ORDER BY case_count DESC
            LIMIT 15
            """
            result = self.query_database(cypher)
            return f"Crime hotspots: {result}"
        
        return f"Location query results: Processing {query}"
    
    def create_tasks(self, query: str):
        """Create investigation tasks based on the query."""
        task = Task(
            description=f"""
            Analyze the following crime investigation query and provide comprehensive information:
            Query: {query}
            
            Use your tools to:
            1. Search for relevant cases, persons, or locations
            2. Provide detailed information about FIRs and investigation status
            3. Include any relevant criminal history or case connections
            4. Format the response in a clear, professional manner suitable for law enforcement
            
            If the query is in Hindi or regional Indian language, translate and process accordingly.
            """,
            agent=self.agent,
            expected_output="Detailed investigation report with case information, person details, and relevant connections"
        )
        
        return [task]