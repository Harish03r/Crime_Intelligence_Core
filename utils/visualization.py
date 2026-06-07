"""Visualization utilities for crime data analysis."""

import plotly.graph_objects as go
import plotly.express as px
import networkx as nx
import pandas as pd
from typing import List, Dict, Any

class CrimeVisualization:
    """Crime data visualization utilities."""
    
    def __init__(self):
        self.color_palette = {
            'Violent Crimes': '#e74c3c',
            'Property Crimes': '#3498db', 
            'Drug Crimes': '#9b59b6',
            'Cyber Crimes': '#e67e22',
            'Organized Crime': '#c0392b'
        }
    
    def create_crime_category_chart(self, data: List[Dict]) -> go.Figure:
        """Create a pie chart for crime categories."""
        df = pd.DataFrame(data)
        
        fig = px.pie(
            df, 
            values='count', 
            names='category',
            title='Crime Distribution by Category',
            color_discrete_map=self.color_palette
        )
        
        fig.update_traces(
            textposition='inside', 
            textinfo='percent+label',
            hovertemplate='<b>%{label}</b><br>Count: %{value}<br>Percentage: %{percent}<extra></extra>'
        )
        
        return fig
    
    def create_temporal_trend_chart(self, data: List[Dict]) -> go.Figure:
        """Create a line chart for crime trends over time."""
        df = pd.DataFrame(data)
        
        fig = px.line(
            df,
            x='month',
            y='count', 
            color='category',
            title='Crime Trends by Month',
            markers=True,
            color_discrete_map=self.color_palette
        )
        
        fig.update_layout(
            xaxis_title='Month',
            yaxis_title='Number of Cases',
            hovermode='x unified'
        )
        
        return fig
    
    def create_location_heatmap(self, data: List[Dict]) -> go.Figure:
        """Create a heatmap for crime by location."""
        df = pd.DataFrame(data)
        
        fig = px.density_heatmap(
            df,
            x='city',
            y='area_type',
            z='case_count',
            title='Crime Heatmap by Location',
            color_continuous_scale='Reds'
        )
        
        return fig
    
    def create_network_graph(self, nodes: List[Dict], edges: List[Dict]) -> go.Figure:
        """Create a network graph for criminal associations."""
        # Create NetworkX graph
        G = nx.Graph()
        
        # Add nodes
        for node in nodes:
            G.add_node(node['id'], **node)
        
        # Add edges
        for edge in edges:
            G.add_edge(edge['source'], edge['target'], weight=edge.get('weight', 1))
        
        # Calculate layout
        pos = nx.spring_layout(G, k=1, iterations=50)
        
        # Prepare node traces
        node_x = []
        node_y = []
        node_info = []
        node_colors = []
        
        for node_id in G.nodes():
            x, y = pos[node_id]
            node_x.append(x)
            node_y.append(y)
            
            node_data = G.nodes[node_id]
            info = f"ID: {node_id}<br>Name: {node_data.get('name', 'Unknown')}<br>Type: {node_data.get('type', 'Person')}"
            node_info.append(info)
            
            # Color by node type
            if node_data.get('type') == 'Network':
                node_colors.append('red')
            elif node_data.get('criminal_history'):
                node_colors.append('orange')
            else:
                node_colors.append('lightblue')
        
        # Prepare edge traces
        edge_x = []
        edge_y = []
        
        for edge in G.edges():
            x0, y0 = pos[edge[0]]
            x1, y1 = pos[edge[1]]
            edge_x.extend([x0, x1, None])
            edge_y.extend([y0, y1, None])
        
        # Create traces
        edge_trace = go.Scatter(
            x=edge_x, y=edge_y,
            line=dict(width=0.5, color='#888'),
            hoverinfo='none',
            mode='lines'
        )
        
        node_trace = go.Scatter(
            x=node_x, y=node_y,
            mode='markers+text',
            hoverinfo='text',
            text=[node['name'] for node in nodes],
            textposition="middle center",
            hovertext=node_info,
            marker=dict(
                size=10,
                color=node_colors,
                line=dict(width=2, color='black')
            )
        )
        
        # Create figure
        fig = go.Figure(data=[edge_trace, node_trace],
                       layout=go.Layout(
                           title='Criminal Network Analysis',
                           titlefont_size=16,
                           showlegend=False,
                           hovermode='closest',
                           margin=dict(b=20,l=5,r=5,t=40),
                           annotations=[ dict(
                               text="Criminal associations and networks",
                               showarrow=False,
                               xref="paper", yref="paper",
                               x=0.005, y=-0.002,
                               xanchor="left", yanchor="bottom",
                               font=dict(color="gray", size=12)
                           )],
                           xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
                           yaxis=dict(showgrid=False, zeroline=False, showticklabels=False)
                       ))
        
        return fig
    
    def create_demographic_analysis_chart(self, data: List[Dict]) -> go.Figure:
        """Create demographic analysis visualization."""
        df = pd.DataFrame(data)
        
        fig = px.sunburst(
            df,
            path=['gender', 'age_group', 'crime_category'],
            values='case_count',
            title='Demographic Crime Analysis',
            color='case_count',
            color_continuous_scale='Viridis'
        )
        
        return fig
    
    def create_risk_assessment_gauge(self, risk_score: float, title: str = "Risk Level") -> go.Figure:
        """Create a gauge chart for risk assessment."""
        fig = go.Figure(go.Indicator(
            mode = "gauge+number+delta",
            value = risk_score,
            domain = {'x': [0, 1], 'y': [0, 1]},
            title = {'text': title},
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
        
        return fig