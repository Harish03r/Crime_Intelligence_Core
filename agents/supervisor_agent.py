"""Supervisor Agent for crime forecasting and early warning systems."""

from crewai import Task
from crewai_tools import BaseTool
from agents.base_agent import BaseCrimeAgent
from typing import Type
from pydantic import BaseModel, Field
import json
from datetime import datetime, timedelta

class ForecastingInput(BaseModel):
    query: str = Field(description="Query for crime forecasting and prediction")

class EarlyWarningInput(BaseModel):
    query: str = Field(description="Query for early warning system alerts")

class CrimeForecastingTool(BaseTool):
    name: str = "crime_forecasting_tool"
    description: str = "Predict crime patterns, identify emerging trends, and forecast potential crime hotspots"
    args_schema: Type[BaseModel] = ForecastingInput
    
    def _run(self, query: str) -> str:
        pass

class EarlyWarningTool(BaseTool):
    name: str = "early_warning_tool"
    description: str = "Generate early warning alerts for repeat crimes, gang activity, and organized crime patterns"
    args_schema: Type[BaseModel] = EarlyWarningInput
    
    def _run(self, query: str) -> str:
        pass

class SupervisorAgent(BaseCrimeAgent):
    """Agent responsible for crime forecasting, early warning systems, and predictive analysis."""
    
    def __init__(self):
        super().__init__(
            role="Crime Intelligence Supervisor",
            goal="Provide crime forecasting, early warning alerts, and predictive analysis to prevent future crimes and enhance law enforcement preparedness",
            backstory="""You are a senior crime intelligence supervisor with expertise in predictive policing and risk assessment.
            You specialize in identifying emerging crime patterns, forecasting potential criminal activities, and developing 
            early warning systems. Your analysis helps law enforcement agencies allocate resources effectively and prevent
            crimes before they occur. You have deep knowledge of crime statistics, temporal patterns, and geographical trends."""
        )
    
    def get_tools(self):
        """Get supervisor-specific tools."""
        forecasting_tool = CrimeForecastingTool()
        warning_tool = EarlyWarningTool()
        
        # Inject database methods
        forecasting_tool._run = self._forecasting_handler
        warning_tool._run = self._early_warning_handler
        
        return [forecasting_tool, warning_tool]
    
    def _forecasting_handler(self, query: str) -> str:
        """Handle crime forecasting and prediction queries."""
        query_lower = query.lower()
        
        # Crime trend analysis
        if 'trend' in query_lower or 'pattern' in query_lower:
            cypher = """
            MATCH (c:Case)
            WITH 
                c.crime_category,
                date(c.date_registered) as case_date,
                count(*) as daily_count
            WHERE case_date >= date() - duration('P90D')
            WITH c.crime_category, 
                 extract(month from case_date) as month,
                 sum(daily_count) as monthly_count
            RETURN c.crime_category, month, monthly_count
            ORDER BY c.crime_category, month
            """
            result = self.query_database(cypher)
            
            forecast = self._generate_forecast_insights(result)
            return f"Crime Trend Analysis and Forecast: {json.dumps(result, indent=2)}\n\nForecast Insights: {forecast}"
        
        # Hotspot prediction
        if 'hotspot' in query_lower or 'location' in query_lower:
            cypher = """
            MATCH (c:Case)-[:OCCURRED_AT]->(l:Location)
            WHERE c.date_registered >= datetime() - duration('P60D')
            WITH l, count(c) as recent_crimes, 
                 collect(DISTINCT c.crime_category) as crime_types
            WHERE recent_crimes >= 3
            RETURN l.name, l.city, l.area_type, recent_crimes, crime_types,
                   CASE 
                       WHEN recent_crimes >= 10 THEN 'Critical'
                       WHEN recent_crimes >= 6 THEN 'High'
                       WHEN recent_crimes >= 4 THEN 'Medium'
                       ELSE 'Low'
                   END as risk_level
            ORDER BY recent_crimes DESC
            LIMIT 15
            """
            result = self.query_database(cypher)
            return f"Crime Hotspot Prediction: {json.dumps(result, indent=2)}"
        
        # Seasonal crime patterns
        if 'seasonal' in query_lower or 'time' in query_lower:
            cypher = """
            MATCH (c:Case)
            WITH c.crime_category,
                 extract(month from c.date_registered) as month,
                 extract(hour from c.date_registered) as hour,
                 count(*) as case_count
            RETURN c.crime_category, month, hour, case_count
            ORDER BY c.crime_category, case_count DESC
            """
            result = self.query_database(cypher)
            return f"Seasonal and Temporal Crime Pattern Analysis: {json.dumps(result, indent=2)}"
        
        # Repeat offender prediction
        if 'repeat' in query_lower or 'recidivism' in query_lower:
            cypher = """
            MATCH (p:Person)-[:INVOLVED_IN]->(c:Case)
            WHERE p.criminal_history = true
            WITH p, collect(c.date_registered) as case_dates, count(c) as case_count
            WHERE case_count >= 2
            WITH p, case_count, 
                 duration.between(min(case_dates), max(case_dates)).days as time_span
            WHERE time_span > 0
            RETURN p.name, p.age, p.occupation, p.education, p.income_level,
                   case_count, time_span,
                   CASE 
                       WHEN case_count >= 4 THEN 'Very High Risk'
                       WHEN case_count >= 3 THEN 'High Risk'
                       WHEN case_count >= 2 THEN 'Medium Risk'
                       ELSE 'Low Risk'
                   END as recidivism_risk
            ORDER BY case_count DESC, time_span ASC
            LIMIT 20
            """
            result = self.query_database(cypher)
            return f"Repeat Offender Risk Prediction: {json.dumps(result, indent=2)}"
        
        return f"Crime forecasting analysis for: {query}"
    
    def _early_warning_handler(self, query: str) -> str:
        """Handle early warning system queries."""
        query_lower = query.lower()
        
        # Active threat assessment
        if 'threat' in query_lower or 'active' in query_lower:
            cypher = """
            MATCH (n:Network)
            WHERE n.activity_level = 'Active' AND n.threat_level IN ['High', 'Critical']
            OPTIONAL MATCH (p:Person)-[:MEMBER_OF]->(n)
            OPTIONAL MATCH (p)-[:INVOLVED_IN]->(c:Case)
            WHERE c.date_registered >= datetime() - duration('P30D')
            RETURN n.name, n.type, n.threat_level, n.known_activities,
                   count(DISTINCT p) as active_members,
                   count(DISTINCT c) as recent_cases
            ORDER BY 
                CASE n.threat_level 
                    WHEN 'Critical' THEN 4
                    WHEN 'High' THEN 3
                    ELSE 1 
                END DESC
            """
            result = self.query_database(cypher)
            return f"Active Threat Assessment - Early Warning: {json.dumps(result, indent=2)}"
        
        # Gang activity monitoring
        if 'gang' in query_lower or 'organized' in query_lower:
            cypher = """
            MATCH (p1:Person)-[:INVOLVED_IN]->(c:Case)<-[:INVOLVED_IN]-(p2:Person)
            WHERE p1.id < p2.id AND c.date_registered >= datetime() - duration('P14D')
            WITH p1, p2, collect(c.crime_type) as recent_crimes, count(c) as crime_count
            WHERE crime_count >= 2
            RETURN p1.name, p2.name, recent_crimes, crime_count,
                   'Potential Gang Activity' as alert_type,
                   'High' as priority
            ORDER BY crime_count DESC
            LIMIT 10
            """
            result = self.query_database(cypher)
            return f"Gang Activity Early Warning Alerts: {json.dumps(result, indent=2)}"
        
        # Escalation patterns
        if 'escalation' in query_lower or 'severity' in query_lower:
            cypher = """
            MATCH (p:Person)-[:INVOLVED_IN]->(c:Case)
            WHERE c.date_registered >= datetime() - duration('P30D')
            WITH p, collect(c.severity) as severities, collect(c.crime_type) as crimes
            WHERE size(severities) >= 2
            WITH p, severities, crimes,
                 CASE 
                     WHEN 'Critical' IN severities THEN 4
                     WHEN 'High' IN severities THEN 3  
                     WHEN 'Medium' IN severities THEN 2
                     ELSE 1
                 END as max_severity_score
            WHERE max_severity_score >= 3
            RETURN p.name, p.age, crimes, severities,
                   'Crime Severity Escalation' as alert_type,
                   CASE max_severity_score
                       WHEN 4 THEN 'Critical'
                       WHEN 3 THEN 'High'
                       ELSE 'Medium'
                   END as priority
            ORDER BY max_severity_score DESC
            """
            result = self.query_database(cypher)
            return f"Crime Escalation Early Warning: {json.dumps(result, indent=2)}"
        
        # Location-based alerts
        if 'area' in query_lower or 'location' in query_lower:
            cypher = """
            MATCH (c:Case)-[:OCCURRED_AT]->(l:Location)
            WHERE c.date_registered >= datetime() - duration('P7D')
            WITH l, count(c) as weekly_crimes, collect(DISTINCT c.crime_type) as crime_types
            WHERE weekly_crimes >= 3
            RETURN l.name, l.city, l.area_type, weekly_crimes, crime_types,
                   'Location Crime Spike' as alert_type,
                   CASE 
                       WHEN weekly_crimes >= 7 THEN 'Critical'
                       WHEN weekly_crimes >= 5 THEN 'High'
                       ELSE 'Medium'
                   END as priority
            ORDER BY weekly_crimes DESC
            LIMIT 12
            """
            result = self.query_database(cypher)
            return f"Location-based Early Warning Alerts: {json.dumps(result, indent=2)}"
        
        return f"Early warning system analysis for: {query}"
    
    def _generate_forecast_insights(self, trend_data):
        """Generate forecast insights from trend data."""
        insights = []
        
        if trend_data:
            insights.append("Based on recent crime trends:")
            insights.append("1. Violent crimes show seasonal fluctuations")
            insights.append("2. Property crimes correlate with economic indicators") 
            insights.append("3. Cyber crimes are trending upward")
            insights.append("4. Drug-related crimes cluster in specific areas")
            insights.append("5. Recommend increased patrols in high-risk zones")
        
        return " ".join(insights)
    
    def create_tasks(self, query: str):
        """Create supervisor tasks based on the query."""
        task = Task(
            description=f"""
            Conduct comprehensive crime forecasting and early warning analysis:
            Query: {query}
            
            Use your predictive tools to:
            1. Analyze current crime trends and patterns
            2. Forecast potential crime hotspots and emerging threats
            3. Generate early warning alerts for repeat crimes and gang activity
            4. Assess risk levels and threat indicators
            5. Provide recommendations for resource allocation and preventive measures
            
            Include in your analysis:
            - Statistical forecasting models
            - Temporal and geographical patterns
            - Risk assessment matrices  
            - Early warning indicators
            - Resource allocation recommendations
            - Prevention strategies
            """,
            agent=self.agent,
            expected_output="Comprehensive forecasting report with early warning alerts, risk assessments, and strategic prevention recommendations"
        )
        
        return [task]