"""Main Streamlit application for Crime Intelligence Core."""

import streamlit as st
import os
from dotenv import load_dotenv
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import json

# Import agents
from agents.investigator_agent import InvestigatorAgent
from agents.analyst_agent import AnalystAgent
from agents.supervisor_agent import SupervisorAgent
from agents.policy_maker_agent import PolicyMakerAgent
from config.database import db

# Load environment variables
load_dotenv()

# Page configuration
st.set_page_config(
    page_title="Crime Intelligence Core",
    page_icon="🚔",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        color: #1f4e79;
        text-align: center;
        margin-bottom: 2rem;
    }
    .agent-card {
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 4px solid #1f4e79;
        margin: 1rem 0;
    }
    .metric-card {
        background-color: #f8f9fa;
        padding: 1rem;
        border-radius: 0.5rem;
        text-align: center;
    }
</style>
""", unsafe_allow_html=True)

@st.cache_resource
def initialize_agents():
    """Initialize all crime intelligence agents."""
    return {
        "Investigator": InvestigatorAgent(),
        "Analyst": AnalystAgent(), 
        "Supervisor": SupervisorAgent(),
        "Policy Maker": PolicyMakerAgent()
    }

@st.cache_data
def get_dashboard_metrics():
    """Get key metrics for the dashboard."""
    try:
        if not db.driver:
            db.connect()
        
        # Total cases
        total_cases = db.execute_query("MATCH (c:Case) RETURN count(c) as count")[0]['count']
        
        # Active investigations
        active_cases = db.execute_query(
            "MATCH (c:Case) WHERE c.status = 'Under Investigation' RETURN count(c) as count"
        )[0]['count']
        
        # Total persons
        total_persons = db.execute_query("MATCH (p:Person) RETURN count(p) as count")[0]['count']
        
        # Crime networks
        total_networks = db.execute_query("MATCH (n:Network) RETURN count(n) as count")[0]['count']
        
        return {
            "total_cases": total_cases,
            "active_cases": active_cases, 
            "total_persons": total_persons,
            "total_networks": total_networks
        }
    except Exception as e:
        st.error(f"Database connection error: {e}")
        return {"total_cases": 0, "active_cases": 0, "total_persons": 0, "total_networks": 0}

@st.cache_data
def get_crime_statistics():
    """Get crime statistics for visualization."""
    try:
        if not db.driver:
            db.connect()
            
        # Crime by category
        crime_by_category = db.execute_query("""
            MATCH (c:Case)
            RETURN c.crime_category as category, count(*) as count
            ORDER BY count DESC
        """)
        
        # Crime trends (simplified)
        crime_trends = db.execute_query("""
            MATCH (c:Case)
            WITH c.crime_category as category, 
                 extract(month from c.date_registered) as month,
                 count(*) as count
            RETURN category, month, count
            ORDER BY month, category
        """)
        
        return crime_by_category, crime_trends
    except Exception as e:
        st.error(f"Error fetching statistics: {e}")
        return [], []

def create_visualizations(crime_by_category, crime_trends):
    """Create crime data visualizations."""
    col1, col2 = st.columns(2)
    
    with col1:
        if crime_by_category:
            df_category = pd.DataFrame(crime_by_category)
            fig_pie = px.pie(df_category, values='count', names='category', 
                           title="Crime Distribution by Category")
            fig_pie.update_traces(textposition='inside', textinfo='percent+label')
            st.plotly_chart(fig_pie, use_container_width=True)
    
    with col2:
        if crime_trends:
            df_trends = pd.DataFrame(crime_trends)
            fig_line = px.line(df_trends, x='month', y='count', color='category',
                             title="Crime Trends by Month")
            st.plotly_chart(fig_line, use_container_width=True)

def display_agent_interface(selected_agent, agents):
    """Display the interface for the selected agent."""
    agent = agents[selected_agent]
    
    st.markdown(f"### {selected_agent} Agent")
    st.markdown(f"**Role**: {agent.role}")
    st.markdown(f"**Goal**: {agent.goal}")
    
    # Agent-specific descriptions
    descriptions = {
        "Investigator": """
        🔍 **Capabilities:**
        - Query FIR records and case information
        - Search accused, victims, and witness details
        - Check investigation status and criminal history
        - Support English and Indian regional languages
        """,
        "Analyst": """
        📊 **Capabilities:**
        - Criminal network and relationship analysis
        - Identify links between cases and persons
        - Demographic crime pattern analysis
        - Organized crime group detection
        """,
        "Supervisor": """
        ⚠️ **Capabilities:**
        - Crime forecasting and trend prediction
        - Early warning system alerts
        - Hotspot identification and risk assessment
        - Predictive analysis for prevention
        """,
        "Policy Maker": """
        📋 **Capabilities:**
        - Evidence-based policy recommendations
        - Resource allocation strategies
        - Strategic crime prevention initiatives
        - Budget optimization suggestions
        """
    }
    
    st.markdown(descriptions[selected_agent])
    
    # Chat interface
    st.markdown("---")
    st.markdown("#### Ask the Agent")
    
    # Example queries for each agent
    example_queries = {
        "Investigator": [
            "Show me details for FIR001234",
            "Find cases involving theft in Mumbai",
            "Get criminal history for person P0001"
        ],
        "Analyst": [
            "Analyze criminal networks in the database",
            "Show demographic patterns for violent crimes", 
            "Identify repeat offender associations"
        ],
        "Supervisor": [
            "Predict crime trends for next month",
            "Generate early warning alerts",
            "Identify potential crime hotspots"
        ],
        "Policy Maker": [
            "Recommend policies to reduce organized crime",
            "Suggest resource allocation for high crime areas",
            "Provide budget optimization strategies"
        ]
    }
    
    st.markdown("**Example Queries:**")
    for query in example_queries[selected_agent]:
        if st.button(f"📝 {query}", key=f"example_{selected_agent}_{query}"):
            st.session_state['query_input'] = query
    
    # Query input
    query = st.text_area(
        "Enter your query:",
        height=100,
        placeholder=f"Ask the {selected_agent} agent anything...",
        key="query_input"
    )
    
    if st.button("🚀 Execute Query", type="primary"):
        if query:
            with st.spinner(f"Processing with {selected_agent} agent..."):
                try:
                    result = agent.execute(query)
                    
                    st.markdown("### Response:")
                    st.markdown("---")
                    st.write(result)
                    
                    # Optional: Show JSON response in expander
                    with st.expander("View Raw Response"):
                        st.json(str(result))
                        
                except Exception as e:
                    st.error(f"Error executing query: {str(e)}")
        else:
            st.warning("Please enter a query to execute.")

def main():
    """Main application function."""
    
    # Header
    st.markdown('<h1 class="main-header">🚔 Crime Intelligence Core</h1>', unsafe_allow_html=True)
    st.markdown('<p style="text-align: center; color: #666;">AI-Powered Crime Intelligence System with Multi-Agent Architecture</p>', unsafe_allow_html=True)
    
    # Initialize agents
    agents = initialize_agents()
    
    # Sidebar
    st.sidebar.title("🎯 Agent Selection")
    selected_agent = st.sidebar.selectbox(
        "Choose an Intelligence Agent:",
        ["Investigator", "Analyst", "Supervisor", "Policy Maker"],
        help="Select the appropriate agent based on your query type"
    )
    
    st.sidebar.markdown("---")
    st.sidebar.markdown("### 🔧 System Status")
    
    # Database connection status
    try:
        if not db.driver:
            db.connect()
        st.sidebar.success("✅ Database Connected")
    except:
        st.sidebar.error("❌ Database Connection Failed")
    
    # Agent status
    st.sidebar.success(f"✅ {len(agents)} Agents Loaded")
    
    # Main content
    tab1, tab2, tab3 = st.tabs(["🤖 Agent Interface", "📊 Dashboard", "📈 Analytics"])
    
    with tab1:
        display_agent_interface(selected_agent, agents)
    
    with tab2:
        st.markdown("## 📊 Crime Intelligence Dashboard")
        
        # Key metrics
        metrics = get_dashboard_metrics()
        
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Total Cases", metrics["total_cases"], delta="📋")
        with col2:
            st.metric("Active Investigations", metrics["active_cases"], delta="🔍")
        with col3:
            st.metric("Persons in Database", metrics["total_persons"], delta="👥")
        with col4:
            st.metric("Criminal Networks", metrics["total_networks"], delta="🕸️")
        
        st.markdown("---")
        
        # Visualizations
        crime_by_category, crime_trends = get_crime_statistics()
        create_visualizations(crime_by_category, crime_trends)
    
    with tab3:
        st.markdown("## 📈 Advanced Analytics")
        st.markdown("### Network Visualization")
        st.info("🚧 Network visualization with Neo4j integration will be implemented here")
        
        # Placeholder for Neo4j visualization
        st.markdown("### Crime Patterns")
        st.info("🚧 Advanced pattern analysis and ML insights will be displayed here")
    
    # Footer
    st.markdown("---")
    st.markdown(
        '<p style="text-align: center; color: #888;">Crime Intelligence Core v1.0 | '
        'Powered by CrewAI, Neo4j & Google Gemini</p>', 
        unsafe_allow_html=True
    )

if __name__ == "__main__":
    main()