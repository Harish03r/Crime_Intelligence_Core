"""Analyst Agent for criminal network analysis and crime pattern detection."""

from crewai import Task
from crewai_tools import BaseTool
from agents.base_agent import BaseCrimeAgent
from typing import Type
from pydantic import BaseModel, Field
import json

class NetworkAnalysisInput(BaseModel):
    query: str = Field(description="Query for criminal network analysis")

class DemographicAnalysisInput(BaseModel):
    query: str = Field(description="Query for demographic crime pattern analysis")

class NetworkAnalysisTool(BaseTool):
    name: str = "network_analysis_tool"
    description: str = "Analyze criminal networks, relationships between accused, victims, and crime incidents"
    args_schema: Type[BaseModel] = NetworkAnalysisInput
    
    def _run(self, query: str) -> str:
        pass

class DemographicAnalysisTool(BaseTool):
    name: str = "demographic_analysis_tool" 
    description: str = "Analyze crime patterns based on demographic attributes like age, gender, socio-economic background"
    args_schema: Type[BaseModel] = DemographicAnalysisInput
    
    def _run(self, query: str) -> str:
        pass

class AnalystAgent(BaseCrimeAgent):
    """Agent responsible for criminal network analysis and demographic crime insights."""
    
    def __init__(self):
        super().__init__(
            role="Crime Intelligence Analyst",
            goal="Analyze criminal networks, identify patterns, and provide insights on crime trends based on demographic and social factors",
            backstory="""You are a senior crime intelligence analyst specializing in network analysis and pattern recognition.
            You have expertise in identifying connections between criminals, analyzing organized crime structures, and understanding
            socio-economic factors that contribute to criminal behavior. You use advanced analytical techniques to uncover
            hidden relationships and predict criminal network behavior patterns."""
        )
    
    def get_tools(self):
        """Get analyst-specific tools."""
        network_tool = NetworkAnalysisTool()
        demographic_tool = DemographicAnalysisTool()
        
        # Inject database methods
        network_tool._run = self._network_analysis_handler
        demographic_tool._run = self._demographic_analysis_handler
        
        return [network_tool, demographic_tool]
    
    def _network_analysis_handler(self, query: str) -> str:
        """Analyze criminal networks and relationships."""
        query_lower = query.lower()
        
        # Criminal associations analysis
        if 'association' in query_lower or 'network' in query_lower:
            cypher = """
            MATCH (p1:Person)-[:INVOLVED_IN]->(c:Case)<-[:INVOLVED_IN]-(p2:Person)
            WHERE p1.id < p2.id AND 
                  EXISTS((p1)-[:INVOLVED_IN]->(:Case)<-[:INVOLVED_IN]-(p2))
            WITH p1, p2, count(*) as shared_cases
            WHERE shared_cases > 1
            RETURN p1.name, p2.name, shared_cases, 
                   p1.criminal_history, p2.criminal_history
            ORDER BY shared_cases DESC
            LIMIT 20
            """
            result = self.query_database(cypher)
            return f"Criminal Network Analysis - Shared Case Associations: {json.dumps(result, indent=2)}"
        
        # Organized crime groups
        if 'organized' in query_lower or 'gang' in query_lower:
            cypher = """
            MATCH (n:Network)
            OPTIONAL MATCH (p:Person)-[:MEMBER_OF]->(n)
            RETURN n.name, n.type, n.activity_level, n.threat_level, 
                   count(p) as member_count
            ORDER BY 
                CASE n.threat_level 
                    WHEN 'Critical' THEN 4
                    WHEN 'High' THEN 3  
                    WHEN 'Medium' THEN 2
                    ELSE 1 
                END DESC
            """
            result = self.query_database(cypher)
            return f"Organized Crime Groups Analysis: {json.dumps(result, indent=2)}"
        
        # Location-based network analysis
        if 'location' in query_lower or 'geographical' in query_lower:
            cypher = """
            MATCH (c:Case)-[:OCCURRED_AT]->(l:Location)
            MATCH (p:Person)-[:INVOLVED_IN]->(c)
            WHERE p.criminal_history = true
            WITH l, collect(DISTINCT p.name) as criminals, count(DISTINCT c) as case_count
            WHERE case_count >= 3
            RETURN l.name, l.city, l.area_type, case_count, criminals
            ORDER BY case_count DESC
            LIMIT 15
            """
            result = self.query_database(cypher)
            return f"Location-based Criminal Network Analysis: {json.dumps(result, indent=2)}"
        
        # Repeat offender networks
        if 'repeat' in query_lower or 'recurring' in query_lower:
            cypher = """
            MATCH (p:Person)-[:INVOLVED_IN]->(c:Case)
            WHERE p.criminal_history = true
            WITH p, collect(c.crime_type) as crime_types, count(c) as case_count
            WHERE case_count >= 2
            RETURN p.name, p.age, p.occupation, case_count, crime_types,
                   p.income_level, p.education
            ORDER BY case_count DESC
            LIMIT 20
            """
            result = self.query_database(cypher)
            return f"Repeat Offender Analysis: {json.dumps(result, indent=2)}"
        
        return f"Network analysis results for: {query}"
    
    def _demographic_analysis_handler(self, query: str) -> str:
        """Analyze crime patterns based on demographic data."""
        query_lower = query.lower()
        
        # Age-based analysis
        if 'age' in query_lower:
            cypher = """
            MATCH (p:Person)-[:INVOLVED_IN]->(c:Case)
            WITH 
                CASE 
                    WHEN p.age < 25 THEN 'Young (18-24)'
                    WHEN p.age < 35 THEN 'Adult (25-34)' 
                    WHEN p.age < 50 THEN 'Middle-aged (35-49)'
                    ELSE 'Senior (50+)'
                END as age_group,
                c.crime_category,
                count(*) as case_count
            RETURN age_group, c.crime_category, case_count
            ORDER BY case_count DESC
            """
            result = self.query_database(cypher)
            return f"Age-based Crime Pattern Analysis: {json.dumps(result, indent=2)}"
        
        # Gender-based analysis  
        if 'gender' in query_lower:
            cypher = """
            MATCH (p:Person)-[:INVOLVED_IN]->(c:Case)
            WITH p.gender, c.crime_category, count(*) as case_count
            RETURN p.gender, c.crime_category, case_count
            ORDER BY p.gender, case_count DESC
            """
            result = self.query_database(cypher)
            return f"Gender-based Crime Pattern Analysis: {json.dumps(result, indent=2)}"
        
        # Socio-economic analysis
        if 'economic' in query_lower or 'income' in query_lower or 'education' in query_lower:
            cypher = """
            MATCH (p:Person)-[:INVOLVED_IN]->(c:Case)
            WITH p.income_level, p.education, c.crime_category, count(*) as case_count
            RETURN p.income_level, p.education, c.crime_category, case_count
            ORDER BY case_count DESC
            LIMIT 25
            """
            result = self.query_database(cypher)
            return f"Socio-Economic Crime Pattern Analysis: {json.dumps(result, indent=2)}"
        
        # Occupation-based analysis
        if 'occupation' in query_lower or 'job' in query_lower:
            cypher = """
            MATCH (p:Person)-[:INVOLVED_IN]->(c:Case)
            WITH p.occupation, c.crime_type, count(*) as case_count
            WHERE case_count >= 2
            RETURN p.occupation, c.crime_type, case_count
            ORDER BY case_count DESC
            LIMIT 20
            """
            result = self.query_database(cypher)
            return f"Occupation-based Crime Analysis: {json.dumps(result, indent=2)}"
        
        # Comprehensive demographic overview
        cypher = """
        MATCH (p:Person)-[:INVOLVED_IN]->(c:Case)
        RETURN 
            p.gender,
            avg(p.age) as avg_age,
            p.income_level,
            p.education,
            c.crime_category,
            count(*) as case_count
        ORDER BY case_count DESC
        LIMIT 30
        """
        result = self.query_database(cypher)
        return f"Comprehensive Demographic Analysis: {json.dumps(result, indent=2)}"
    
    def create_tasks(self, query: str):
        """Create analyst tasks based on the query."""
        task = Task(
            description=f"""
            Perform comprehensive crime intelligence analysis on the following query:
            Query: {query}
            
            Use your analytical tools to:
            1. Identify criminal networks and associations
            2. Analyze relationships between accused, victims, and locations
            3. Detect patterns based on demographic attributes (age, gender, socio-economic status)
            4. Provide insights on organized crime groups and repeat offenders
            5. Generate actionable intelligence for law enforcement
            
            Present findings with:
            - Statistical analysis and trends
            - Network visualization recommendations
            - Key insights and recommendations
            - Risk assessment of identified networks
            """,
            agent=self.agent,
            expected_output="Comprehensive analytical report with network analysis, demographic insights, and strategic recommendations"
        )
        
        return [task]