"""
Mind Map Visualization utilities.
Creates beautiful, interactive mind map visualizations.
"""
import plotly.graph_objects as go
import networkx as nx
import math


def create_mindmap_visualization(mindmap_data: dict) -> go.Figure:
    """
    Create an interactive mind map visualization using Plotly.
    
    Args:
        mindmap_data: Mind map dictionary with 'topic' and 'nodes'
        
    Returns:
        Plotly Figure object
    """
    # Create a directed graph
    G = nx.DiGraph()
    
    # Add nodes
    topic = mindmap_data.get("topic", "Mind Map")
    nodes = mindmap_data.get("nodes", [])
    
    # Build node mapping
    node_map = {}
    for node in nodes:
        node_id = node["id"]
        node_map[node_id] = node
        G.add_node(node_id, text=node["text"], parent=node["parent"])
    
    # Add edges
    for node in nodes:
        if node["parent"] != 0:
            G.add_edge(node["parent"], node["id"])
    
    # Calculate positions using hierarchical layout
    pos = _hierarchical_layout(G, nodes)
    
    # Define colors for different levels
    colors = [
        '#7B68EE',  # Purple - Level 1
        '#4A90E2',  # Blue - Level 2
        '#51CF66',  # Green - Level 3
        '#FFD93D',  # Yellow - Level 4
        '#FF6B6B',  # Red - Level 5+
    ]
    
    # Calculate node levels
    node_levels = _calculate_node_levels(nodes)
    
    # Create edge traces
    edge_traces = []
    for edge in G.edges():
        x0, y0 = pos[edge[0]]
        x1, y1 = pos[edge[1]]
        
        edge_trace = go.Scatter(
            x=[x0, x1, None],
            y=[y0, y1, None],
            mode='lines',
            line=dict(width=2, color='#888'),
            hoverinfo='none',
            showlegend=False
        )
        edge_traces.append(edge_trace)
    
    # Create node traces by level
    node_traces = []
    for level in range(5):
        node_x = []
        node_y = []
        node_text = []
        node_hover = []
        
        for node_id, (x, y) in pos.items():
            if node_levels.get(node_id, 0) == level:
                node_x.append(x)
                node_y.append(y)
                text = node_map[node_id]["text"]
                node_text.append(text[:30] + "..." if len(text) > 30 else text)
                node_hover.append(text)
        
        if node_x:  # Only create trace if there are nodes at this level
            node_trace = go.Scatter(
                x=node_x,
                y=node_y,
                mode='markers+text',
                hoverinfo='text',
                text=node_text,
                hovertext=node_hover,
                textposition="middle center",
                textfont=dict(size=10, color='white', family='Arial Black'),
                marker=dict(
                    size=60,
                    color=colors[level],
                    line=dict(width=2, color='white'),
                    symbol='hexagon'
                ),
                name=f'Level {level + 1}',
                showlegend=True
            )
            node_traces.append(node_trace)
    
    # Create figure
    fig = go.Figure(data=edge_traces + node_traces)
    
    # Update layout
    fig.update_layout(
        title=dict(
            text=f"<b>{topic}</b>",
            x=0.5,
            xanchor='center',
            font=dict(size=24, color='white')
        ),
        showlegend=True,
        hovermode='closest',
        margin=dict(b=20, l=5, r=5, t=60),
        plot_bgcolor='#2E2E2E',
        paper_bgcolor='#2E2E2E',
        xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
        yaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
        height=700,
        legend=dict(
            font=dict(color='white'),
            bgcolor='rgba(0,0,0,0.5)'
        )
    )
    
    return fig


def _calculate_node_levels(nodes: list) -> dict:
    """Calculate the level of each node in the hierarchy."""
    node_levels = {}
    node_map = {node["id"]: node for node in nodes}
    
    def get_level(node_id):
        if node_id in node_levels:
            return node_levels[node_id]
        
        node = node_map.get(node_id)
        if not node or node["parent"] == 0:
            node_levels[node_id] = 0
            return 0
        
        level = get_level(node["parent"]) + 1
        node_levels[node_id] = level
        return level
    
    for node in nodes:
        get_level(node["id"])
    
    return node_levels


def _hierarchical_layout(G: nx.DiGraph, nodes: list) -> dict:
    """
    Create a hierarchical layout for the mind map.
    Positions nodes in a radial/circular pattern around the center.
    """
    pos = {}
    node_levels = _calculate_node_levels(nodes)
    
    # Group nodes by level
    levels = {}
    for node in nodes:
        level = node_levels[node["id"]]
        if level not in levels:
            levels[level] = []
        levels[level].append(node["id"])
    
    # Position nodes level by level
    max_level = max(levels.keys()) if levels else 0
    
    for level, node_ids in levels.items():
        num_nodes = len(node_ids)
        radius = (level + 1) * 2  # Increase radius for each level
        
        # Distribute nodes evenly in a circle
        for i, node_id in enumerate(node_ids):
            angle = 2 * math.pi * i / num_nodes if num_nodes > 1 else 0
            x = radius * math.cos(angle)
            y = radius * math.sin(angle)
            pos[node_id] = (x, y)
    
    return pos


def create_simple_tree_visualization(mindmap_data: dict) -> str:
    """
    Create a simple text-based tree visualization.
    Fallback for when Plotly isn't available.
    
    Args:
        mindmap_data: Mind map dictionary
        
    Returns:
        HTML string with tree visualization
    """
    nodes = mindmap_data.get("nodes", [])
    node_map = {node["id"]: node for node in nodes}
    
    # Build tree structure
    children = {}
    for node in nodes:
        parent = node["parent"]
        if parent not in children:
            children[parent] = []
        children[parent].append(node["id"])
    
    # Generate HTML
    html = '<div style="font-family: monospace; color: white;">'
    
    def render_node(node_id, indent=0):
        nonlocal html
        node = node_map.get(node_id)
        if not node:
            return
        
        prefix = "  " * indent + ("└─ " if indent > 0 else "")
        html += f'<div style="margin-left: {indent * 20}px;">{prefix}{node["text"]}</div>'
        
        if node_id in children:
            for child_id in children[node_id]:
                render_node(child_id, indent + 1)
    
    # Start from root nodes (parent = 0)
    if 0 in children:
        for root_id in children[0]:
            render_node(root_id, 0)
    
    html += '</div>'
    return html
