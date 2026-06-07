"""Policy Maker Agent for generating policy recommendations based on crime intelligence insights."""

from crewai import Task
from crewai_tools import BaseTool
from agents.base_agent import BaseCrimeAgent
from typing import Type
from pydantic import BaseModel, Field
import json

class PolicyAnalysisInput(BaseModel):
    query: str = Field(description="Query for policy analysis and recommendations")

class ResourceAllocationInput(BaseModel):
    query: str = Field(description="Query for resource allocation recommendations")

class PolicyRecommendationTool(BaseTool):
    name: str = "policy_recommendation_tool"
    description: str = "Generate policy recommendations based on crime patterns, network analysis, and forecasting insights"
    args_schema: Type[BaseModel] = PolicyAnalysisInput
    
    def _run(self, query: str) -> str:
        pass

class ResourceAllocationTool(BaseTool):
    name: str = "resource_allocation_tool"
    description: str = "Provide recommendations for optimal allocation of law enforcement resources"
    args_schema: Type[BaseModel] = ResourceAllocationInput
    
    def _run(self, query: str) -> str:
        pass

class PolicyMakerAgent(BaseCrimeAgent):
    """Agent responsible for generating policy recommendations based on comprehensive crime intelligence."""
    
    def __init__(self):
        super().__init__(
            role="Crime Intelligence Policy Advisor",
            goal="Develop evidence-based policy recommendations and strategic initiatives based on comprehensive crime intelligence analysis",
            backstory="""You are a senior policy advisor with expertise in criminal justice policy, law enforcement strategy, 
            and public safety initiatives. You synthesize insights from investigators, analysts, and supervisors to create 
            comprehensive policy recommendations. Your expertise includes resource allocation, prevention strategies, 
            legislative recommendations, and community policing initiatives. You understand the intersection of crime data, 
            socio-economic factors, and policy implementation."""
        )
    
    def get_tools(self):
        """Get policy maker-specific tools."""
        policy_tool = PolicyRecommendationTool()
        resource_tool = ResourceAllocationTool()
        
        # Inject database methods
        policy_tool._run = self._policy_recommendation_handler
        resource_tool._run = self._resource_allocation_handler
        
        return [policy_tool, resource_tool]
    
    def _policy_recommendation_handler(self, query: str) -> str:
        """Generate policy recommendations based on crime intelligence."""
        query_lower = query.lower()
        
        # Comprehensive crime analysis for policy making
        crime_overview = self._get_comprehensive_crime_overview()
        
        # Prevention-focused policies
        if 'prevention' in query_lower or 'reduce' in query_lower:
            recommendations = {
                "prevention_policies": [
                    {
                        "category": "Community Policing",
                        "recommendations": [
                            "Increase community outreach programs in high-crime areas",
                            "Establish neighborhood watch programs",
                            "Deploy community liaison officers in vulnerable communities"
                        ],
                        "priority": "High",
                        "estimated_impact": "20-30% reduction in property crimes"
                    },
                    {
                        "category": "Youth Crime Prevention", 
                        "recommendations": [
                            "Implement after-school programs in crime-prone areas",
                            "Create vocational training opportunities for at-risk youth",
                            "Establish mentorship programs with reformed offenders"
                        ],
                        "priority": "High",
                        "estimated_impact": "15-25% reduction in youth-related crimes"
                    },
                    {
                        "category": "Substance Abuse Prevention",
                        "recommendations": [
                            "Expand rehabilitation programs for drug offenders",
                            "Implement needle exchange programs",
                            "Increase funding for addiction treatment centers"
                        ],
                        "priority": "Medium",
                        "estimated_impact": "10-20% reduction in drug-related crimes"
                    }
                ],
                "supporting_data": crime_overview
            }
            
            return f"Crime Prevention Policy Recommendations: {json.dumps(recommendations, indent=2)}"
        
        # Organized crime policies
        if 'organized' in query_lower or 'network' in query_lower:
            # Get network analysis data
            network_data = self._get_network_policy_data()
            
            recommendations = {
                "organized_crime_policies": [
                    {
                        "category": "Intelligence Sharing",
                        "recommendations": [
                            "Establish inter-agency intelligence fusion centers",
                            "Implement real-time crime data sharing platforms",
                            "Create joint task forces for organized crime"
                        ],
                        "priority": "Critical",
                        "implementation_timeline": "6 months"
                    },
                    {
                        "category": "Legal Framework",
                        "recommendations": [
                            "Strengthen asset forfeiture laws for organized crime",
                            "Enhance witness protection programs",
                            "Implement RICO-style legislation for criminal enterprises"
                        ],
                        "priority": "High",
                        "implementation_timeline": "12-18 months"
                    },
                    {
                        "category": "Technology Enhancement",
                        "recommendations": [
                            "Deploy advanced surveillance systems in hotspots",
                            "Implement AI-powered network analysis tools",
                            "Enhance digital forensics capabilities"
                        ],
                        "priority": "High",
                        "implementation_timeline": "8-12 months"
                    }
                ],
                "network_analysis": network_data
            }
            
            return f"Organized Crime Policy Recommendations: {json.dumps(recommendations, indent=2)}"
        
        # Socio-economic policies
        if 'social' in query_lower or 'economic' in query_lower or 'demographic' in query_lower:
            demographic_data = self._get_demographic_policy_data()
            
            recommendations = {
                "socio_economic_policies": [
                    {
                        "category": "Economic Opportunity",
                        "recommendations": [
                            "Create job training programs in high-crime areas",
                            "Establish microfinance programs for ex-offenders",
                            "Implement public-private partnerships for employment"
                        ],
                        "target_demographics": "Low-income, young adults (18-35)",
                        "priority": "High"
                    },
                    {
                        "category": "Education and Skills",
                        "recommendations": [
                            "Expand literacy programs in underserved communities",
                            "Create technical skill development centers",
                            "Implement scholarship programs for at-risk youth"
                        ],
                        "target_demographics": "Young adults with limited education",
                        "priority": "Medium-High"
                    },
                    {
                        "category": "Social Support",
                        "recommendations": [
                            "Strengthen family support services",
                            "Create mental health intervention programs",
                            "Establish housing assistance for ex-offenders"
                        ],
                        "target_demographics": "Families in poverty, individuals with mental health issues",
                        "priority": "Medium"
                    }
                ],
                "demographic_analysis": demographic_data
            }
            
            return f"Socio-Economic Crime Prevention Policies: {json.dumps(recommendations, indent=2)}"
        
        # Technology and modernization policies
        if 'technology' in query_lower or 'digital' in query_lower or 'modern' in query_lower:
            recommendations = {
                "technology_policies": [
                    {
                        "category": "Predictive Policing",
                        "recommendations": [
                            "Implement AI-driven crime forecasting systems",
                            "Deploy machine learning for pattern recognition",
                            "Create real-time crime mapping platforms"
                        ],
                        "budget_estimate": "₹50-100 lakhs",
                        "roi_timeline": "12-18 months"
                    },
                    {
                        "category": "Digital Infrastructure",
                        "recommendations": [
                            "Upgrade police communication systems",
                            "Implement blockchain for evidence management",
                            "Create mobile apps for citizen reporting"
                        ],
                        "budget_estimate": "₹100-200 lakhs",
                        "roi_timeline": "18-24 months"
                    },
                    {
                        "category": "Data Analytics",
                        "recommendations": [
                            "Establish crime intelligence analytics units",
                            "Implement automated report generation systems",
                            "Create data visualization dashboards for decision makers"
                        ],
                        "budget_estimate": "₹25-50 lakhs",
                        "roi_timeline": "6-12 months"
                    }
                ]
            }
            
            return f"Technology Modernization Policy Recommendations: {json.dumps(recommendations, indent=2)}"
        
        # General comprehensive policy framework
        return self._generate_comprehensive_policy_framework()
    
    def _resource_allocation_handler(self, query: str) -> str:
        """Provide resource allocation recommendations."""
        query_lower = query.lower()
        
        # Get current resource analysis
        resource_analysis = self._analyze_current_resource_allocation()
        
        if 'personnel' in query_lower or 'staffing' in query_lower:
            recommendations = {
                "personnel_allocation": [
                    {
                        "unit": "Investigation Teams",
                        "current_strength": "Understaffed by 30%",
                        "recommended_increase": "50 additional investigators",
                        "priority_areas": ["Economic crimes", "Cyber crimes", "Organized crime"],
                        "budget_impact": "₹15-20 crore annually"
                    },
                    {
                        "unit": "Intelligence Analysis",
                        "current_strength": "Adequate",
                        "recommended_action": "Upskill existing personnel",
                        "focus_areas": ["Data analytics", "Network analysis", "Predictive modeling"],
                        "budget_impact": "₹2-3 crore for training"
                    },
                    {
                        "unit": "Community Policing",
                        "current_strength": "Severely understaffed",
                        "recommended_increase": "100 community officers",
                        "deployment_strategy": "Focus on high-crime neighborhoods",
                        "budget_impact": "₹8-10 crore annually"
                    }
                ]
            }
            
            return f"Personnel Resource Allocation Recommendations: {json.dumps(recommendations, indent=2)}"
        
        # Technology resource allocation
        if 'technology' in query_lower or 'equipment' in query_lower:
            recommendations = {
                "technology_allocation": [
                    {
                        "category": "Surveillance Systems",
                        "priority": "Critical",
                        "investment": "₹25-30 crore",
                        "deployment": "500 smart cameras in crime hotspots",
                        "expected_outcome": "40% improvement in case clearance rate"
                    },
                    {
                        "category": "Communication Infrastructure", 
                        "priority": "High",
                        "investment": "₹15-20 crore",
                        "scope": "Encrypted radio systems for all units",
                        "expected_outcome": "Enhanced coordination and response time"
                    },
                    {
                        "category": "Forensic Equipment",
                        "priority": "High", 
                        "investment": "₹10-15 crore",
                        "focus": "DNA analysis, digital forensics, ballistics",
                        "expected_outcome": "60% faster evidence processing"
                    }
                ]
            }
            
            return f"Technology Resource Allocation: {json.dumps(recommendations, indent=2)}"
        
        # Budget optimization
        if 'budget' in query_lower or 'financial' in query_lower:
            return self._generate_budget_optimization_recommendations()
        
        return f"Resource allocation analysis for: {query}"
    
    def _get_comprehensive_crime_overview(self):
        """Get comprehensive crime statistics for policy making."""
        cypher = """
        MATCH (c:Case)
        WITH c.crime_category, count(*) as case_count,
             avg(CASE c.severity 
                 WHEN 'Critical' THEN 4
                 WHEN 'High' THEN 3
                 WHEN 'Medium' THEN 2
                 ELSE 1 END) as avg_severity
        RETURN c.crime_category, case_count, round(avg_severity, 2) as severity_score
        ORDER BY case_count DESC
        """
        return self.query_database(cypher)
    
    def _get_network_policy_data(self):
        """Get criminal network data for policy recommendations."""
        cypher = """
        MATCH (n:Network)
        RETURN n.type, n.activity_level, n.threat_level, count(*) as network_count
        ORDER BY 
            CASE n.threat_level 
                WHEN 'Critical' THEN 4
                WHEN 'High' THEN 3
                ELSE 1 
            END DESC
        """
        return self.query_database(cypher)
    
    def _get_demographic_policy_data(self):
        """Get demographic analysis for policy recommendations."""
        cypher = """
        MATCH (p:Person)-[:INVOLVED_IN]->(c:Case)
        RETURN p.age_group, p.education, p.income_level, 
               count(*) as involvement_count,
               collect(DISTINCT c.crime_category) as crime_types
        ORDER BY involvement_count DESC
        LIMIT 20
        """
        return self.query_database(cypher)
    
    def _generate_comprehensive_policy_framework(self):
        """Generate a comprehensive policy framework."""
        framework = {
            "comprehensive_crime_policy_framework": {
                "strategic_pillars": [
                    {
                        "pillar": "Prevention and Early Intervention",
                        "initiatives": [
                            "Community-based crime prevention programs",
                            "Youth engagement and mentorship",
                            "Substance abuse prevention and treatment"
                        ]
                    },
                    {
                        "pillar": "Intelligence-Led Policing",
                        "initiatives": [
                            "Advanced crime analytics and forecasting",
                            "Real-time intelligence sharing",
                            "Predictive policing deployment"
                        ]
                    },
                    {
                        "pillar": "Criminal Justice Reform",
                        "initiatives": [
                            "Rehabilitation-focused corrections",
                            "Restorative justice programs",
                            "Recidivism reduction strategies"
                        ]
                    },
                    {
                        "pillar": "Community Partnerships",
                        "initiatives": [
                            "Public-private security collaborations",
                            "Citizen engagement platforms",
                            "Business community crime prevention"
                        ]
                    }
                ],
                "implementation_timeline": "36 months",
                "total_budget_estimate": "₹500-750 crore",
                "expected_outcomes": [
                    "25-30% reduction in overall crime rates",
                    "40% improvement in case clearance rates", 
                    "50% increase in community trust and cooperation"
                ]
            }
        }
        
        return json.dumps(framework, indent=2)
    
    def _analyze_current_resource_allocation(self):
        """Analyze current resource allocation patterns."""
        return {
            "current_allocation": "Analysis of existing resource distribution",
            "efficiency_metrics": "Resource utilization rates",
            "gap_analysis": "Identified resource shortfalls"
        }
    
    def _generate_budget_optimization_recommendations(self):
        """Generate budget optimization recommendations."""
        return json.dumps({
            "budget_optimization": {
                "cost_reduction_opportunities": [
                    "Automation of routine processes - ₹5-8 crore savings",
                    "Shared services across departments - ₹3-5 crore savings",
                    "Energy-efficient infrastructure - ₹2-3 crore savings"
                ],
                "high_impact_investments": [
                    "Predictive policing systems - ₹20 crore investment, 30% efficiency gain",
                    "Community policing expansion - ₹25 crore investment, 25% crime reduction",
                    "Officer training and development - ₹10 crore investment, 20% performance improvement"
                ],
                "total_net_benefit": "₹50-75 crore over 5 years"
            }
        }, indent=2)
    
    def create_tasks(self, query: str):
        """Create policy maker tasks based on the query."""
        task = Task(
            description=f"""
            Develop comprehensive policy recommendations based on crime intelligence insights:
            Query: {query}
            
            Use your policy analysis tools to:
            1. Synthesize insights from crime investigations, network analysis, and forecasting
            2. Identify key policy gaps and opportunities for improvement
            3. Generate evidence-based policy recommendations with implementation timelines
            4. Provide resource allocation strategies and budget optimization suggestions
            5. Consider socio-economic factors and community impact in policy design
            
            Your recommendations should include:
            - Specific policy initiatives with clear objectives
            - Implementation timelines and budget estimates
            - Expected outcomes and success metrics
            - Risk assessments and mitigation strategies
            - Stakeholder engagement plans
            - Legislative or regulatory changes needed
            """,
            agent=self.agent,
            expected_output="Comprehensive policy recommendation report with strategic initiatives, implementation plans, budget allocations, and expected outcomes"
        )
        
        return [task]