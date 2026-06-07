# Crime Intelligence Core - Deployment Guide

## 🚀 Quick Start

### Prerequisites
- Python 3.9+
- Docker (recommended)
- Neo4j Database
- Google Gemini API Key

### Option 1: Docker Deployment (Recommended)

1. **Clone and Setup**
```bash
git clone <repository>
cd crime-intelligence-core
cp .env.example .env
```

2. **Configure Environment**
Edit `.env` file:
```bash
GOOGLE_API_KEY=your_gemini_api_key_here
NEO4J_URI=bolt://neo4j:7687
NEO4J_USER=neo4j
NEO4J_PASSWORD=crimedb123
```

3. **Start Services**
```bash
docker-compose up --build
```

4. **Access Application**
- Web Interface: http://localhost:8501
- Neo4j Browser: http://localhost:7474

### Option 2: Manual Installation

1. **Setup Python Environment**
```bash
python -m venv crime-intelligence-env
source crime-intelligence-env/bin/activate  # Linux/Mac
# or
crime-intelligence-env\Scripts\activate  # Windows
```

2. **Install Dependencies**
```bash
pip install -r requirements.txt
```

3. **Setup Neo4j**
```bash
# Using Docker
docker run -d \
  --name neo4j-crime \
  -p 7474:7474 -p 7687:7687 \
  -e NEO4J_AUTH=neo4j/crimedb123 \
  neo4j:5.13
```

4. **Initialize Database**
```bash
python scripts/generate_dummy_data.py
```

5. **Run Application**
```bash
python run_app.py
# or
streamlit run app.py
```

## 🏗️ Architecture Overview

### System Components

```
┌─────────────────────────────────────────────────────────┐
│                   Crime Intelligence Core                │
├─────────────────────────────────────────────────────────┤
│  Frontend: Streamlit Dashboard                          │
│  ├── Agent Selection Interface                          │
│  ├── Query Processing                                   │
│  └── Visualization Components                           │
├─────────────────────────────────────────────────────────┤
│  Multi-Agent System (CrewAI)                           │
│  ├── Investigator Agent (Case Queries)                 │
│  ├── Analyst Agent (Network Analysis)                  │
│  ├── Supervisor Agent (Forecasting)                    │
│  └── Policy Maker Agent (Recommendations)              │
├─────────────────────────────────────────────────────────┤
│  AI Engine: Google Gemini                              │
│  ├── Natural Language Processing                        │
│  ├── Query Understanding                               │
│  └── Response Generation                               │
├─────────────────────────────────────────────────────────┤
│  Data Layer                                            │
│  ├── Neo4j Graph Database                             │
│  ├── Crime Records & FIRs                             │
│  ├── Person & Location Data                           │
│  └── Criminal Networks                                │
└─────────────────────────────────────────────────────────┘
```

### Agent Responsibilities

#### 1. Investigator Agent 🔍
- **Purpose**: Query crime records and case information
- **Capabilities**:
  - FIR search and retrieval
  - Person information lookup
  - Case status tracking
  - Criminal history analysis
- **Tools**: Case Query, Person Query, Location Query

#### 2. Analyst Agent 📊
- **Purpose**: Criminal network and pattern analysis
- **Capabilities**:
  - Network relationship mapping
  - Demographic crime patterns
  - Organized crime detection
  - Association analysis
- **Tools**: Network Analysis, Demographic Analysis

#### 3. Supervisor Agent ⚠️
- **Purpose**: Crime forecasting and early warning
- **Capabilities**:
  - Trend prediction
  - Hotspot identification
  - Risk assessment
  - Early warning alerts
- **Tools**: Crime Forecasting, Early Warning System

#### 4. Policy Maker Agent 📋
- **Purpose**: Policy recommendations and strategy
- **Capabilities**:
  - Evidence-based policy suggestions
  - Resource allocation optimization
  - Strategic initiatives
  - Budget recommendations
- **Tools**: Policy Analysis, Resource Allocation

## 🗄️ Database Schema

### Neo4j Graph Model

```cypher
// Nodes
(:Person {id, name, age, gender, address, criminal_history, ...})
(:Case {fir_number, crime_type, date_registered, status, ...})
(:Location {id, name, city, coordinates, crime_rate, ...})
(:Network {network_id, name, type, threat_level, ...})

// Relationships
(Person)-[:INVOLVED_IN {role}]->(Case)
(Case)-[:OCCURRED_AT]->(Location)
(Person)-[:MEMBER_OF]->(Network)
(Person)-[:ASSOCIATED_WITH]->(Person)
```

### Sample Queries

```cypher
// Find criminal associations
MATCH (p1:Person)-[:INVOLVED_IN]->(c:Case)<-[:INVOLVED_IN]-(p2:Person)
WHERE p1.id < p2.id
RETURN p1.name, p2.name, count(c) as shared_cases

// Crime hotspots
MATCH (c:Case)-[:OCCURRED_AT]->(l:Location)
RETURN l.name, l.city, count(c) as crime_count
ORDER BY crime_count DESC

// Network analysis
MATCH (n:Network)-[:HAS_MEMBER]->(p:Person)-[:INVOLVED_IN]->(c:Case)
RETURN n.name, n.type, count(DISTINCT p) as members, count(c) as cases
```

## 🔧 Configuration

### Environment Variables

| Variable | Description | Example |
|----------|-------------|---------|
| `GOOGLE_API_KEY` | Gemini API key | `AIza...` |
| `NEO4J_URI` | Neo4j connection URI | `bolt://localhost:7687` |
| `NEO4J_USER` | Neo4j username | `neo4j` |
| `NEO4J_PASSWORD` | Neo4j password | `password123` |
| `DEBUG` | Debug mode | `True` |
| `LOG_LEVEL` | Logging level | `INFO` |

### Neo4j Configuration

```yaml
# docker-compose.yml
neo4j:
  environment:
    - NEO4J_AUTH=neo4j/password
    - NEO4J_PLUGINS=["apoc"]
    - NEO4J_dbms_memory_heap_initial__size=1G
    - NEO4J_dbms_memory_heap_max__size=2G
```

## 📈 Performance Optimization

### Database Optimization
- Create appropriate indexes
- Use constraints for data integrity
- Optimize Cypher queries
- Monitor query performance

### Application Optimization
- Use Streamlit caching
- Implement connection pooling
- Optimize agent task execution
- Cache frequently accessed data

## 🔒 Security Considerations

### API Security
- Secure API key storage
- Environment variable protection
- Rate limiting implementation
- Input validation

### Database Security
- Authentication enabled
- Network security
- Data encryption
- Access control

### Application Security
- Input sanitization
- Query parameterization
- Secure communication
- Audit logging

## 📊 Monitoring & Logging

### Application Metrics
- Agent response times
- Query success rates
- Database connection health
- User interaction patterns

### System Monitoring
- Resource utilization
- Database performance
- Error rates
- Response times

## 🚀 Deployment Options

### Local Development
```bash
python run_app.py
```

### Docker Compose
```bash
docker-compose up --build
```

### Cloud Deployment
- **AWS**: ECS, RDS Neo4j
- **GCP**: Cloud Run, Memorystore
- **Azure**: Container Instances, Cosmos DB

### Kubernetes
```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: crime-intelligence-app
spec:
  replicas: 3
  selector:
    matchLabels:
      app: crime-intelligence
  template:
    spec:
      containers:
      - name: app
        image: crime-intelligence:latest
        ports:
        - containerPort: 8501
```

## 🧪 Testing

### Unit Tests
```bash
python -m pytest tests/unit/
```

### Integration Tests
```bash
python -m pytest tests/integration/
```

### Load Testing
```bash
locust -f tests/load/locustfile.py
```

## 📝 API Documentation

### Agent Endpoints
- `/api/investigator` - Investigation queries
- `/api/analyst` - Analysis requests  
- `/api/supervisor` - Forecasting queries
- `/api/policy` - Policy recommendations

### Data Endpoints
- `/api/cases` - Case management
- `/api/persons` - Person data
- `/api/networks` - Network information
- `/api/analytics` - Analytics data

## 🔄 Maintenance

### Regular Tasks
- Database backup and maintenance
- Performance monitoring
- Security updates
- Data quality checks

### Updates
- Agent model updates
- Database schema migrations
- Dependency updates
- Security patches

## 🆘 Troubleshooting

### Common Issues

1. **Database Connection Failed**
   ```bash
   # Check Neo4j status
   docker ps | grep neo4j
   # Restart Neo4j
   docker-compose restart neo4j
   ```

2. **Agent Timeout Errors**
   ```bash
   # Check Gemini API key
   echo $GOOGLE_API_KEY
   # Increase timeout in configuration
   ```

3. **Memory Issues**
   ```bash
   # Increase Docker memory limits
   # Optimize database queries
   # Use pagination for large results
   ```

### Support Contacts
- Technical Issues: [Support Team]
- Feature Requests: [Product Team]
- Security Issues: [Security Team]