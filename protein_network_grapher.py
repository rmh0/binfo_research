import pandas as pd
import numpy as np
import networkx as nx
import matplotlib.pyplot as plt

# Load the Excel file (update the file path to your own)
file_path = r"C:\string_interactions_H1.xlsx"
ppi_data = pd.read_excel(file_path)

# Create a MultiGraph object (allows multiple edges between nodes)
ppi_graph = nx.MultiGraph()

# Add all nodes to ensure they're displayed
nodes = set(ppi_data['#node1']).union(set(ppi_data['node2']))
ppi_graph.add_nodes_from(nodes)

# Function to determine edge color based on evidence
def edge_color(row):
    db_evidence = row['database_annotated']
    exp_evidence = row['experimentally_determined_interaction']

    if db_evidence > 0 and exp_evidence > 0:
        return "lightsalmon"

    if db_evidence > 0:
        return "lightsteelblue"

    if exp_evidence > 0:
        return "lightgreen"

# Add edges based on evidence type
for _, row in ppi_data.iterrows():
    ppi_graph.add_edge(row['#node1'], row['node2'], weight=row['combined_score'],
                       color=edge_color(row))

# Set up the plot
plt.figure(figsize=(12, 10))

# Define positions using spring layout with adjusted parameters
pos = nx.spring_layout(ppi_graph, seed=42, k=0.8)  # 'k' controls node spacing; 'seed' ensures reproducibility

# Identify edges by color
edges_firebrick = [(u, v) for u, v, data in ppi_graph.edges(data=True) if data['color'] == 'lightsalmon']
edges_steelblue = [(u, v) for u, v, data in ppi_graph.edges(data=True) if data['color'] == 'lightsteelblue']
edges_forestgreen = [(u, v) for u, v, data in ppi_graph.edges(data=True) if data['color'] == 'lightgreen']

# Draw  edges for interactions network
nx.draw_networkx_edges(ppi_graph, pos, edgelist=edges_firebrick, edge_color='lightsalmon', width=2)
nx.draw_networkx_edges(ppi_graph, pos, edgelist=edges_steelblue, edge_color='lightsteelblue', width=2)
nx.draw_networkx_edges(ppi_graph, pos, edgelist=edges_forestgreen, edge_color='lightgreen', width=2)

node_colors = plt.colormaps['Pastel2'](np.linspace(0, 1, len(ppi_graph.nodes)))

# Draw the nodes
nx.draw_networkx_nodes(ppi_graph, pos, node_color=node_colors, node_size=1000)
nx.draw_networkx_labels(ppi_graph, pos, font_size=9, font_weight='bold')

# Manually add edge weights as labels
for u, v, data in ppi_graph.edges(data=True):
    x_pos = (pos[u][0] + pos[v][0]) / 2
    y_pos = (pos[u][1] + pos[v][1]) / 2
    weight_label = f"{data['weight']:.3f}"
    plt.text(x_pos, y_pos, weight_label, fontsize=8, color='black', ha='center')

# Show the plot
plt.title('Protein-Protein Interaction Network of [Protein ID]')
plt.show()