import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt

# Load the Excel file (update the file path to your own)
file_path = r"C:\string_interactions_H1.xlsx"
df = pd.read_excel(file_path)

# Create a MultiGraph object (allows multiple edges between nodes)
G = nx.MultiGraph()

# Add all nodes to ensure they're displayed
nodes = set(df['#node1']).union(set(df['node2']))
G.add_nodes_from(nodes)

# Add edges for database-annotated and experimentally determined interactions
for _, row in df.iterrows():
    db_val = row['database_annotated']
    exp_det_val = row['experimentally_determined_interaction']

    # Add an edge for database-annotated interactions if present
    if db_val > 0:
        G.add_edge(row['#node1'], row['node2'], weight=row['combined_score'],
                   color='cyan', key='database')
    # Add an edge for experimentally determined interactions if present
    if exp_det_val > 0:
        G.add_edge(row['#node1'], row['node2'], weight=row['combined_score'],
                   color='purple', key='experimental')

# Set up the plot
plt.figure(figsize=(12, 10))

# Define positions using spring layout with adjusted parameters
pos = nx.spring_layout(G, seed=42, k=0.8)  # 'k' controls node spacing; 'seed' ensures reproducibility

# Check if edge lists are populated
edges_cyan = [(u, v) for u, v, data in G.edges(data=True) if data['color'] == 'cyan']
edges_purple = [(u, v) for u, v, data in G.edges(data=True) if data['color'] == 'purple']
print(f"Cyan edges: {len(edges_cyan)}, Purple edges: {len(edges_purple)}")  # Debugging

# Draw blue edges for database-annotated interactions
nx.draw_networkx_edges(G, pos, edgelist=edges_cyan, edge_color='blue', width=2)

# Draw purple edges for experimentally determined interactions
nx.draw_networkx_edges(G, pos, edgelist=edges_purple, edge_color='purple', width=2)

# Draw the nodes
nx.draw_networkx_nodes(G, pos, node_color='skyblue', node_size=700)
nx.draw_networkx_labels(G, pos, font_size=8, font_weight='bold')

# Manually add edge weights as labels
for u, v, data in G.edges(data=True):
    x_pos = (pos[u][0] + pos[v][0]) / 2
    y_pos = (pos[u][1] + pos[v][1]) / 2
    weight_label = f"{data['weight']:.3f}"
    plt.text(x_pos, y_pos, weight_label, fontsize=8, color='black', ha='center')

# Show the plot
plt.show()








