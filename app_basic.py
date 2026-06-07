"""Basic version of Crime Intelligence Core without database dependency."""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import json
import random
from datetime import datetime, timedelta

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
        background-color: #f8f9fa;
    }
    .metric-card {
        background-color: #f0f8ff;
        padding: 1rem;
        border-radius: 0.5rem;
        text-align: center;
        border: 1px solid #1f4e79;
    }
    .success-response {
        background-color: #d4edda;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 4px solid #28a745;
        margin: 1rem 0;
    }
</style>
""", unsafe_allow_html=True)

class MockAgent:
    """Mock agent class for demonstration."""
    
    def __init__(self, role, capabilities, example_responses):
        self.role = role
        self.capabilities = capabilities
        self.example_responses = example_responses
    
    def execute(self, query):
        """Mock execute method."""
        return random.choice(self.example_responses)

@st.cache_data
def get_mock_data():
    """Generate mock crime data for demonstration."""
    
    # Crime categories data
    crime_by_category = [
        {"category": "Property Crimes", "count": 145},
        {"category": "Violent Crimes", "count": 89},
        {"category": "Drug Crimes", "count": 67},
        {"category": "Cyber Crimes", "count": 34},
        {"category": "Organized Crime", "count": 23}
    ]
    
    # Monthly trends data
    crime_trends = []
    categories = ["Property Crimes", "Violent Crimes", "Drug Crimes", "Cyber Crimes", "Organized Crime"]
    for month in range(1, 13):
        for category in categories:
            count = random.randint(5, 25)
            crime_trends.append({"month": month, "category": category, "count": count})
    
    # Location data
    location_data = [
        {"location": "Mumbai Central", "crimes": 45, "risk_level": "High"},
        {"location": "Delhi NCR", "crimes": 38, "risk_level": "High"},
        {"location": "Bangalore Tech Hub", "crimes": 29, "risk_level": "Medium"},
        {"location": "Chennai Marina", "crimes": 22, "risk_level": "Medium"},
        {"location": "Kolkata Park Street", "crimes": 18, "risk_level": "Low"}
    ]
    
    return crime_by_category, crime_trends, location_data

def initialize_mock_agents():
    """Initialize mock agents with example responses."""
    
    investigator_responses = [
        """**FIR Investigation Results:**
        
📋 **FIR Number:** FIR001234  
📅 **Date Registered:** 2024-11-15  
🏢 **Police Station:** Mumbai Central  
⚖️ **Status:** Under Investigation  
🔍 **Crime Type:** Theft  
📍 **Location:** Dadar Station  
👮 **Investigating Officer:** Inspector Rajesh Kumar  
        
**Case Details:**
- **Accused:** Ramesh Sharma (Age: 28, History: Yes)
- **Victim:** Priya Patel (Age: 34)
- **Evidence:** CCTV footage available
- **Witnesses:** 2 identified
        
**Investigation Progress:**
✅ Complaint registered  
✅ Evidence collected  
🔄 Suspect interrogation in progress  
⏳ Court proceedings pending
        """,
        
        """**Person Search Results:**
        
👤 **Person ID:** P0156  
📛 **Name:** Amit Singh  
📅 **Age:** 32  
🏠 **Address:** Sector 15, Noida, UP  
📱 **Contact:** +91-9876543210  
💼 **Occupation:** Software Engineer  
        
**Criminal History:**
🚫 **Previous Cases:** 2  
📋 **Case 1:** FIR002789 - Cyber Fraud (2023)  
📋 **Case 2:** FIR003456 - Identity Theft (2024)  
⚖️ **Current Status:** On Bail  
        
**Associated Cases:**
- Connected to 3 other cyber crime cases
- Part of organized fraud network
- Known associates: 4 individuals under surveillance
        """,
        
        """**Location Crime Analysis:**
        
📍 **Area:** Connaught Place, Delhi  
🏙️ **Zone:** Central Delhi  
📊 **Crime Rate:** High  
🚨 **Total Incidents:** 67 (Last 6 months)  
        
**Crime Breakdown:**
- Theft: 28 cases
- Fraud: 15 cases  
- Assault: 12 cases
- Drug-related: 8 cases
- Others: 4 cases
        
**Risk Assessment:**
⚠️ **Risk Level:** Critical  
🕐 **Peak Hours:** 8 PM - 12 AM  
📅 **High-risk Days:** Friday-Sunday  
        
**Recommendations:**
- Increase patrol frequency
- Install additional CCTV cameras
- Deploy undercover officers
        """
    ]
    
    analyst_responses = [
        """**Criminal Network Analysis Report:**
        
🕸️ **Network:** Delhi Fraud Ring  
👥 **Active Members:** 12 identified  
🔗 **Connections:** 45 relationships mapped  
📈 **Activity Level:** High  
⚠️ **Threat Level:** Critical  
        
**Key Players:**
🎯 **Leader:** Vikash Yadav (Node centrality: 0.89)  
🤝 **Lieutenant:** Suresh Kumar (Connected to 8 members)  
💰 **Financier:** Deepak Gupta (Money laundering specialist)  
        
**Network Characteristics:**
- **Operational Area:** North India (Delhi, Punjab, Haryana)
- **Primary Activities:** Online fraud, identity theft
- **Financial Impact:** ₹2.3 Crore estimated losses
- **Modus Operandi:** Phishing, fake job portals
        
**Relationship Analysis:**
- Strong ties between core members (family/regional connections)
- Weak ties to peripheral members (recruitment targets)
- Geographic clustering in specific neighborhoods
        
**Recommendations:**
1. Simultaneous raids on core members
2. Financial investigation of money trails
3. Cyber forensics on communication channels
        """,
        
        """**Demographic Crime Pattern Analysis:**
        
📊 **Analysis Period:** January 2024 - November 2024  
🎯 **Focus:** Age and Socio-economic Patterns  
        
**Age Group Analysis:**
👶 **18-25 years:** 34% of offenders  
- Primary crimes: Cyber crimes, theft
- Education level: Mostly graduates
- Employment: Unemployed/underemployed
        
🧑 **26-35 years:** 28% of offenders  
- Primary crimes: Fraud, organized crime
- Education level: Mixed (school to graduate)
- Employment: Various sectors
        
👨 **36-50 years:** 25% of offenders  
- Primary crimes: Financial crimes, corruption
- Education level: Graduate/post-graduate
- Employment: White-collar jobs
        
**Socio-economic Patterns:**
💰 **Low Income:** 45% correlation with property crimes  
💼 **Middle Income:** 35% correlation with white-collar crimes  
🏢 **High Income:** 20% correlation with complex financial crimes  
        
**Gender Analysis:**
👨 **Male:** 78% of cases (Higher in violent crimes)  
👩 **Female:** 22% of cases (Higher in fraud cases)  
        
**Education Impact:**
📚 **Higher Education:** Sophisticated crimes, lower detection rate  
📖 **Limited Education:** Opportunistic crimes, higher detection rate
        """,
        
        """**Crime Association Matrix:**
        
🔗 **Cross-Case Analysis:** 500+ cases analyzed  
📊 **Association Strength:** Statistical correlation  
        
**Strong Associations (>0.7 correlation):**
- Drug trafficking ↔ Money laundering (0.89)
- Cybercrime ↔ Identity theft (0.85)
- Organized theft ↔ Fencing operations (0.82)
        
**Emerging Patterns:**
📱 **Digital-Physical Crime Convergence:**
- Online fraud leading to physical intimidation
- Cryptocurrency used in traditional crimes
- Social media for recruitment and coordination
        
🌐 **Geographic Clustering:**
- Crime hotspots showing network effects
- Cross-border coordination in organized crime
- Transportation hubs as crime convergence points
        
**Predictive Indicators:**
⚡ **Early Warning Signals:**
1. Sudden increase in small-value frauds (precursor to major scams)
2. Multiple identity thefts in same area (organized operation)
3. Recruitment ads in specific online forums (network expansion)
        """
    ]
    
    supervisor_responses = [
        """**Crime Forecasting & Early Warning Report:**
        
📈 **Forecast Period:** Next 30 days  
🎯 **Confidence Level:** 78%  
⚠️ **Alert Status:** MEDIUM-HIGH  
        
**Trend Predictions:**
📊 **Property Crimes:** ↗️ 15% increase expected  
- Reason: Festival season, increased cash transactions
- Risk areas: Market districts, residential areas
- Peak period: November 20-30, 2024
        
💻 **Cyber Crimes:** ↗️ 25% increase expected  
- Reason: Holiday shopping, increased online activity  
- Target demographics: Senior citizens, online shoppers
- Attack vectors: Fake e-commerce, phishing emails
        
**Hotspot Predictions:**
🔥 **Critical Risk Zones:**
1. **Mumbai - Dadar Station Area**
   - Predicted incidents: 12-15
   - Crime types: Pickpocketing, mobile theft
   - Recommended action: Deploy 4 additional officers
        
2. **Delhi - Connaught Place**
   - Predicted incidents: 18-22
   - Crime types: Tourist targeting, fraud
   - Recommended action: Undercover operations
        
**Early Warning Alerts:**
🚨 **ACTIVE ALERTS:**
        
⚠️ **Alert #1: Organized Theft Network**
- Location: Bangalore IT Corridor
- Risk Level: HIGH
- Expected timeline: Next 7-10 days
- Action required: Enhanced surveillance
        
⚠️ **Alert #2: Cyber Fraud Campaign**
- Target: Banking customers
- Risk Level: CRITICAL  
- Expected timeline: Ongoing
- Action required: Public awareness, bank coordination
        
**Resource Allocation Recommendations:**
👮 **Personnel:** Increase night patrol by 30%  
📹 **Technology:** Deploy mobile CCTV units  
🚔 **Vehicles:** 2 additional rapid response teams  
        """,
        
        """**Predictive Analysis Dashboard:**
        
🔮 **AI Model Performance:** 82% accuracy  
📊 **Data Sources:** 15 integrated systems  
⏱️ **Real-time Processing:** Active  
        
**Risk Assessment Matrix:**
        
🟥 **CRITICAL (90-100% Risk):**
- Location: Mumbai Central Station
- Time: 18:00-22:00 today
- Crime Type: Mobile/wallet theft
- Confidence: 94%
        
🟧 **HIGH (70-89% Risk):**
- Location: Delhi Cyber Hub
- Time: Next 48 hours  
- Crime Type: Online fraud
- Confidence: 85%
        
🟨 **MEDIUM (50-69% Risk):**
- Location: Bangalore MG Road
- Time: Weekend (Sat-Sun)
- Crime Type: Vehicle theft
- Confidence: 67%
        
**Behavioral Pattern Analysis:**
🎯 **Repeat Offender Prediction:**
- 23 individuals flagged for high recidivism risk
- Average time to re-offend: 45 days
- Intervention programs recommended for 8 high-risk cases
        
**Seasonal Crime Patterns:**
❄️ **Winter Season Trends (Nov-Jan):**
- Property crimes: +20% (year-over-year)
- Domestic violence: +15% (holiday stress)
- Cyber crimes: +35% (online shopping surge)
        
**Prevention Opportunities:**
✅ **Proactive Measures:**
1. Community awareness programs in high-risk areas
2. Increased lighting in predicted hotspots  
3. Coordination with private security agencies
4. Social media monitoring for threat indicators
        """
    ]
    
    policy_maker_responses = [
        """**Policy Recommendations Report:**
        
📋 **Policy Framework:** Evidence-Based Crime Prevention  
🎯 **Focus Areas:** Prevention, Technology, Community Engagement  
⏱️ **Implementation Timeline:** 6-18 months  
        
**Priority Policy Initiatives:**
        
🏛️ **1. Community Policing Enhancement Act**
**Objective:** Strengthen police-community relationships  
**Budget:** ₹25 crore  
**Timeline:** 12 months  
        
**Key Components:**
- Recruit 200 community liaison officers
- Establish neighborhood watch programs in 50 high-crime areas
- Create citizen advisory committees
- Implement community feedback systems
        
**Expected Impact:** 20-25% reduction in property crimes  
        
🔬 **2. Technology Modernization Initiative**
**Objective:** Upgrade crime fighting capabilities  
**Budget:** ₹75 crore  
**Timeline:** 18 months  
        
**Technology Investments:**
- AI-powered crime prediction system
- Real-time crime mapping platform
- Integrated forensic database
- Mobile crime reporting app
        
**Expected Impact:** 30% faster case resolution  
        
**Legislative Recommendations:**
        
⚖️ **Crime Prevention & Early Intervention Act:**
- Mandatory rehabilitation programs for first-time offenders
- Electronic monitoring for repeat offenders  
- Victim compensation fund enhancement
- Witness protection program expansion
        
📱 **Cyber Crime Prevention Framework:**
- Specialized cyber crime courts
- Public-private partnership for cyber security
- Digital literacy programs
- Online fraud prevention awareness
        
**Budget Allocation Recommendations:**
        
💰 **Total Investment:** ₹150 crore over 3 years  
        
📊 **Allocation Breakdown:**
- Personnel (40%): ₹60 crore
- Technology (35%): ₹52.5 crore  
- Training (15%): ₹22.5 crore
- Infrastructure (10%): ₹15 crore
        
**Success Metrics:**
- 25% reduction in overall crime rate
- 40% improvement in case clearance rate
- 60% increase in community trust scores
- 30% reduction in repeat offenses
        """,
        
        """**Resource Allocation Strategy:**
        
📊 **Current Resource Analysis:**  
🎯 **Optimization Target:** 35% efficiency improvement  
💰 **Budget Impact:** ₹45 crore savings annually  
        
**Personnel Reallocation:**
        
👮 **Field Operations (60% of force):**
- Current: 2,400 officers
- Optimal: 2,600 officers (+200)
- Focus: High-crime areas, community policing
        
🕵️ **Investigation Units (25% of force):**
- Current: 1,000 officers  
- Optimal: 1,100 officers (+100)
- Specialization: Cyber crime, financial crimes
        
📋 **Administrative (15% of force):**
- Current: 600 officers
- Optimal: 500 officers (-100)
- Automation: Reduce paperwork, digitize processes
        
**Technology Investment Strategy:**
        
🚁 **High-Impact Technology (70% of tech budget):**
- Predictive policing systems: ₹30 crore
- CCTV network expansion: ₹25 crore
- Communication systems: ₹15 crore
        
📱 **Supporting Technology (30% of tech budget):**
- Mobile devices and apps: ₹10 crore
- Training simulators: ₹8 crore
- Data analytics tools: ₹7 crore
        
**Performance-Based Allocation:**
        
🏆 **High-Performing Units (Bonus Allocation):**
- Economic Crime Unit: +₹5 crore (85% success rate)
- Cyber Crime Unit: +₹8 crore (90% case closure)
- Community Policing: +₹3 crore (95% satisfaction)
        
⚠️ **Underperforming Units (Restructuring):**
- Traffic Division: Process automation (-₹2 crore)
- Administrative Units: Streamlining (-₹3 crore)
        
**ROI Projections:**
📈 **3-Year Investment Returns:**
- Crime reduction value: ₹200 crore
- Efficiency savings: ₹135 crore  
- Technology ROI: 340%
- Personnel optimization: ₹45 crore annually
        """
    ]
    
    agents = {
        "Investigator": MockAgent(
            "Crime Investigator", 
            ["FIR queries", "Case status", "Criminal history", "Evidence tracking"],
            investigator_responses
        ),
        "Analyst": MockAgent(
            "Crime Intelligence Analyst",
            ["Network analysis", "Pattern recognition", "Demographic insights", "Association mapping"],
            analyst_responses
        ),
        "Supervisor": MockAgent(
            "Crime Intelligence Supervisor", 
            ["Forecasting", "Early warning", "Risk assessment", "Trend analysis"],
            supervisor_responses
        ),
        "Policy Maker": MockAgent(
            "Crime Intelligence Policy Advisor",
            ["Policy recommendations", "Resource allocation", "Strategic planning", "Budget optimization"],
            policy_maker_responses
        )
    }
    
    return agents

def create_visualizations(crime_by_category, crime_trends, location_data):
    """Create crime data visualizations."""
    col1, col2 = st.columns(2)
    
    with col1:
        # Crime distribution pie chart
        df_category = pd.DataFrame(crime_by_category)
        fig_pie = px.pie(df_category, values='count', names='category', 
                       title="Crime Distribution by Category",
                       color_discrete_sequence=px.colors.qualitative.Set3)
        fig_pie.update_traces(textposition='inside', textinfo='percent+label')
        st.plotly_chart(fig_pie, use_container_width=True)
    
    with col2:
        # Crime trends line chart
        df_trends = pd.DataFrame(crime_trends)
        fig_line = px.line(df_trends, x='month', y='count', color='category',
                         title="Monthly Crime Trends",
                         color_discrete_sequence=px.colors.qualitative.Set2)
        fig_line.update_layout(xaxis_title="Month", yaxis_title="Number of Cases")
        st.plotly_chart(fig_line, use_container_width=True)
    
    # Crime hotspots bar chart
    st.markdown("### 🗺️ Crime Hotspots")
    df_locations = pd.DataFrame(location_data)
    fig_bar = px.bar(df_locations, x='location', y='crimes', 
                     color='risk_level',
                     title="Crime Incidents by Location",
                     color_discrete_map={'High': 'red', 'Medium': 'orange', 'Low': 'green'})
    st.plotly_chart(fig_bar, use_container_width=True)

def display_agent_interface(selected_agent, agents):
    """Display the interface for the selected agent."""
    agent = agents[selected_agent]
    
    # Agent info card
    st.markdown(f"""
    <div class="agent-card">
        <h3>🤖 {selected_agent} Agent</h3>
        <p><strong>Role:</strong> {agent.role}</p>
        <p><strong>Capabilities:</strong> {', '.join(agent.capabilities)}</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Agent-specific descriptions and examples
    example_queries = {
        "Investigator": [
            "Show me details for FIR001234",
            "Find cases involving Amit Singh",
            "Get crime statistics for Mumbai Central",
            "Search for theft cases in Delhi"
        ],
        "Analyst": [
            "Analyze criminal networks in the database",
            "Show demographic patterns for cyber crimes", 
            "Identify organized crime associations",
            "Find connections between cases"
        ],
        "Supervisor": [
            "Predict crime trends for next month",
            "Generate early warning alerts",
            "Identify potential crime hotspots",
            "Assess risk levels for different areas"
        ],
        "Policy Maker": [
            "Recommend policies to reduce cyber crime",
            "Suggest resource allocation strategies",
            "Provide budget optimization recommendations",
            "Design community policing initiatives"
        ]
    }
    
    st.markdown("#### 💡 Example Queries")
    
    # Create buttons for example queries
    cols = st.columns(2)
    for i, query in enumerate(example_queries[selected_agent]):
        col = cols[i % 2]
        with col:
            if st.button(f"📝 {query}", key=f"example_{selected_agent}_{i}"):
                st.session_state['selected_query'] = query
    
    # Query input section
    st.markdown("---")
    st.markdown("#### 🔍 Ask the Agent")
    
    # Use session state to populate query if example was clicked
    default_query = st.session_state.get('selected_query', '')
    query = st.text_area(
        "Enter your query:",
        value=default_query,
        height=100,
        placeholder=f"Ask the {selected_agent} agent anything related to crime intelligence...",
        key="query_input"
    )
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button("🚀 Execute Query", type="primary", use_container_width=True):
            if query:
                with st.spinner(f"Processing with {selected_agent} agent..."):
                    # Simulate processing time
                    import time
                    time.sleep(2)
                    
                    try:
                        result = agent.execute(query)
                        
                        # Display response in a nice format
                        st.markdown("### 📊 Agent Response:")
                        st.markdown('<div class="success-response">', unsafe_allow_html=True)
                        st.markdown(result)
                        st.markdown('</div>', unsafe_allow_html=True)
                        
                        # Clear the selected query from session state
                        if 'selected_query' in st.session_state:
                            del st.session_state['selected_query']
                            
                    except Exception as e:
                        st.error(f"Error executing query: {str(e)}")
            else:
                st.warning("Please enter a query to execute.")

def main():
    """Main application function."""
    
    # Header
    st.markdown('<h1 class="main-header">🚔 Crime Intelligence Core</h1>', unsafe_allow_html=True)
    st.markdown('<p style="text-align: center; color: #666; font-size: 1.2em;">AI-Powered Crime Intelligence System with Multi-Agent Architecture</p>', unsafe_allow_html=True)
    st.markdown('<p style="text-align: center; color: #888; font-style: italic;">Demo Version - No Database Required</p>', unsafe_allow_html=True)
    
    # Initialize agents and get mock data
    agents = initialize_mock_agents()
    crime_by_category, crime_trends, location_data = get_mock_data()
    
    # Sidebar
    st.sidebar.title("🎯 Agent Selection")
    selected_agent = st.sidebar.selectbox(
        "Choose an Intelligence Agent:",
        ["Investigator", "Analyst", "Supervisor", "Policy Maker"],
        help="Select the appropriate agent based on your query type"
    )
    
    st.sidebar.markdown("---")
    st.sidebar.markdown("### 🔧 System Status")
    st.sidebar.success("✅ Demo Mode Active")
    st.sidebar.success(f"✅ {len(agents)} Agents Loaded")
    st.sidebar.info("ℹ️ Using Mock Data")
    
    # Agent descriptions in sidebar
    agent_descriptions = {
        "Investigator": "🔍 Query FIR records, case information, and criminal history",
        "Analyst": "📊 Analyze criminal networks and identify crime patterns", 
        "Supervisor": "⚠️ Forecast crimes and generate early warning alerts",
        "Policy Maker": "📋 Recommend policies and optimize resource allocation"
    }
    
    st.sidebar.markdown("### 📋 Agent Capabilities")
    for agent_name, description in agent_descriptions.items():
        if agent_name == selected_agent:
            st.sidebar.markdown(f"**{description}**")
        else:
            st.sidebar.markdown(description)
    
    # Main content tabs
    tab1, tab2, tab3 = st.tabs(["🤖 Agent Interface", "📊 Dashboard", "📈 Analytics"])
    
    with tab1:
        display_agent_interface(selected_agent, agents)
    
    with tab2:
        st.markdown("## 📊 Crime Intelligence Dashboard")
        
        # Key metrics
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.markdown('<div class="metric-card">', unsafe_allow_html=True)
            st.metric("Total Cases", "358", delta="12 this week")
            st.markdown('</div>', unsafe_allow_html=True)
        with col2:
            st.markdown('<div class="metric-card">', unsafe_allow_html=True)
            st.metric("Active Investigations", "89", delta="5 this week")
            st.markdown('</div>', unsafe_allow_html=True)
        with col3:
            st.markdown('<div class="metric-card">', unsafe_allow_html=True)
            st.metric("Persons in Database", "1,247", delta="23 this week")
            st.markdown('</div>', unsafe_allow_html=True)
        with col4:
            st.markdown('<div class="metric-card">', unsafe_allow_html=True)
            st.metric("Criminal Networks", "18", delta="2 this month")
            st.markdown('</div>', unsafe_allow_html=True)
        
        st.markdown("---")
        
        # Visualizations
        create_visualizations(crime_by_category, crime_trends, location_data)
    
    with tab3:
        st.markdown("## 📈 Advanced Analytics")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("### 🎯 Crime Prediction Model")
            
            # Risk gauge
            risk_score = 73
            fig_gauge = go.Figure(go.Indicator(
                mode = "gauge+number+delta",
                value = risk_score,
                domain = {'x': [0, 1], 'y': [0, 1]},
                title = {'text': "Current Risk Level"},
                delta = {'reference': 50},
                gauge = {
                    'axis': {'range': [None, 100]},
                    'bar': {'color': "darkblue"},
                    'steps': [
                        {'range': [0, 25], 'color': "lightgray"},
                        {'range': [25, 50], 'color': "yellow"},
                        {'range': [50, 75], 'color': "orange"},
                        {'range': [75, 100], 'color': "red"}
                    ],
                    'threshold': {
                        'line': {'color': "red", 'width': 4},
                        'thickness': 0.75,
                        'value': 90
                    }
                }
            ))
            fig_gauge.update_layout(height=300)
            st.plotly_chart(fig_gauge, use_container_width=True)
        
        with col2:
            st.markdown("### 📊 Case Resolution Rate")
            
            resolution_data = [
                {"Status": "Solved", "Count": 234},
                {"Status": "Under Investigation", "Count": 89},
                {"Status": "Pending", "Count": 35}
            ]
            df_resolution = pd.DataFrame(resolution_data)
            
            fig_donut = px.pie(df_resolution, values='Count', names='Status', hole=0.4,
                             title="Case Status Distribution",
                             color_discrete_sequence=['#2E8B57', '#FF6347', '#FFD700'])
            st.plotly_chart(fig_donut, use_container_width=True)
        
        # Additional analytics
        st.markdown("### 🔍 Investigation Insights")
        
        insights_col1, insights_col2 = st.columns(2)
        
        with insights_col1:
            st.info("**🎯 Top Crime Patterns:**\n- Property crimes peak during 8-10 PM\n- Cyber crimes increase by 40% during festivals\n- Drug-related crimes cluster in specific neighborhoods")
        
        with insights_col2:
            st.warning("**⚠️ Active Alerts:**\n- Organized theft network detected in Sector 15\n- Cyber fraud campaign targeting senior citizens\n- Vehicle theft pattern identified near metro stations")
    
    # Footer
    st.markdown("---")
    st.markdown(
        '<p style="text-align: center; color: #888; font-size: 0.9em;">'
        'Crime Intelligence Core v1.0 Demo | Powered by CrewAI, Neo4j & Google Gemini<br>'
        'This is a demonstration version with simulated data</p>', 
        unsafe_allow_html=True
    )

if __name__ == "__main__":
    main()