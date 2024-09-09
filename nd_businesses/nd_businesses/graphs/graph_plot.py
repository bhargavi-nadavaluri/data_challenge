import json
import networkx as nx
import matplotlib.pyplot as plt

def build_graph_from_json():

    # Paths to input JSON data and output PNG file
    input_json_path = 'data/nd_businesses.json'
    output_png_path = 'nd_businesses.png'

    # Initialize a new graph
    G = nx.Graph()

    # Load business data from JSON file
    with open(input_json_path, 'r', encoding='utf-8') as file:
        businesses = json.load(file)

    # Process each company and add it to the graph
    for company in businesses:
        company_node = company['business_name']
        G.add_node(company_node, type='company')  # Add company node

        # Add Commercial Registered Agent as a node, if present
        if 'commercial_registered_agent' in company:
            agent_node = company['commercial_registered_agent']
            G.add_node(agent_node, type='agent')
            G.add_edge(company_node, agent_node)  # Connect the company and agent

        # Add Registered Agent as a node, if present
        if 'registered_agent' in company:
            agent_node = company['registered_agent']
            G.add_node(agent_node, type='agent')
            G.add_edge(company_node, agent_node)  # Connect the company and agent

        # Add Owner as a node, if present
        if 'owner_name' in company:
            owner_node = company['owner_name']
            G.add_node(owner_node, type='owner')
            G.add_edge(company_node, owner_node)  # Connect the company and owner

    # Plotting the graph
    plt.figure(figsize=(15, 15))

    # Using spring layout
    pos = nx.spring_layout(G)

    # Assign colors based on node type (company, agent, owner)
    colors = []
    for node in G:
        node_type = G.nodes[node]['type']
        if node_type == 'company':
            colors.append('skyblue')
        elif node_type == 'agent':
            colors.append('orange')
        elif node_type == 'owner':
            colors.append('lightgreen')

    # Draw the graph with customized sizes and labels
    nx.draw(G, pos, with_labels=False, node_color=colors, node_size=50, 
            font_size=0, edge_color='gray', width=1, alpha=1)

    # Save the graph to a file  
    plt.savefig(output_png_path, format="png", dpi=300)
    plt.show()

if __name__ == "__main__":
    build_graph_from_json()
