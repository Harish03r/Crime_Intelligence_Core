"""Base agent class for all crime intelligence agents."""

import os
import google.generativeai as genai
from abc import ABC, abstractmethod
from crewai import Agent, Task, Crew
from langchain_google_genai import ChatGoogleGenerativeAI
from config.database import db
from dotenv import load_dotenv

load_dotenv()

# Configure Gemini
genai.configure(api_key=os.getenv('GOOGLE_API_KEY'))

class BaseCrimeAgent(ABC):
    """Base class for all crime intelligence agents."""
    
    def __init__(self, role: str, goal: str, backstory: str, verbose: bool = True):
        self.role = role
        self.goal = goal
        self.backstory = backstory
        self.verbose = verbose
        
        # Initialize Gemini LLM
        self.llm = ChatGoogleGenerativeAI(
            model="gemini-pro",
            google_api_key=os.getenv('GOOGLE_API_KEY'),
            temperature=0.3
        )
        
        # Create CrewAI agent
        self.agent = Agent(
            role=self.role,
            goal=self.goal,
            backstory=self.backstory,
            verbose=self.verbose,
            allow_delegation=False,
            llm=self.llm,
            tools=self.get_tools()
        )
    
    @abstractmethod
    def get_tools(self):
        """Get tools specific to this agent."""
        pass
    
    @abstractmethod
    def create_tasks(self, query: str):
        """Create tasks for this agent based on the query."""
        pass
    
    def execute(self, query: str):
        """Execute agent tasks."""
        tasks = self.create_tasks(query)
        
        crew = Crew(
            agents=[self.agent],
            tasks=tasks,
            verbose=self.verbose
        )
        
        result = crew.kickoff()
        return result
    
    def query_database(self, cypher_query: str, parameters: dict = None):
        """Execute a Cypher query against the Neo4j database."""
        try:
            if not db.driver:
                db.connect()
            return db.execute_query(cypher_query, parameters)
        except Exception as e:
            return f"Database query error: {str(e)}"
    
    def get_case_info(self, fir_number: str = None, crime_type: str = None):
        """Retrieve case information from database."""
        if fir_number:
            query = """
            MATCH (c:Case {fir_number: $fir_number})
            OPTIONAL MATCH (c)-[:OCCURRED_AT]->(l:Location)
            OPTIONAL MATCH (p:Person)-[r:INVOLVED_IN]->(c)
            RETURN c, l, collect({person: p, relationship: r}) as people
            """
            return self.query_database(query, {'fir_number': fir_number})
        
        elif crime_type:
            query = """
            MATCH (c:Case)
            WHERE c.crime_type CONTAINS $crime_type
            OPTIONAL MATCH (c)-[:OCCURRED_AT]->(l:Location)
            RETURN c, l
            LIMIT 10
            """
            return self.query_database(query, {'crime_type': crime_type})
        
        return "Please provide FIR number or crime type"
    
    def get_person_info(self, person_id: str = None, name: str = None):
        """Retrieve person information from database."""
        if person_id:
            query = """
            MATCH (p:Person {id: $person_id})
            OPTIONAL MATCH (p)-[r:INVOLVED_IN]->(c:Case)
            RETURN p, collect({case: c, relationship: r}) as cases
            """
            return self.query_database(query, {'person_id': person_id})
        
        elif name:
            query = """
            MATCH (p:Person)
            WHERE p.name CONTAINS $name
            OPTIONAL MATCH (p)-[r:INVOLVED_IN]->(c:Case)
            RETURN p, collect({case: c, relationship: r}) as cases
            LIMIT 5
            """
            return self.query_database(query, {'name': name})
        
        return "Please provide person ID or name"