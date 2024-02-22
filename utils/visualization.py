```python
import os
import json
from graphviz import Digraph
from .file_analyzer import extract_metadata
from .code_parser import parse_code
from .static_analyzer import map_call_relationships

def generate_visualization(codebase_path, output_path):
    # Initialize a directed graph for visualization
    architecture_diagram = Digraph(comment='Architecture Diagram')
    call_graph = Digraph(comment='Call Graph')

    # Traverse the codebase and generate visualizations
    for root, dirs, files in os.walk(codebase_path):
        for file in files:
            file_path = os.path.join(root, file)
            metadata = extract_metadata(file_path)
            ast = parse_code(file_path)
            call_relations = map_call_relationships(ast)

            # Add nodes and edges to the architecture diagram
            architecture_diagram.node(metadata['name'])
            for relation in call_relations:
                architecture_diagram.edge(metadata['name'], relation['callee'])

            # Add nodes and edges to the call graph
            call_graph.node(metadata['name'])
            for relation in call_relations:
                call_graph.edge(relation['caller'], relation['callee'])

    # Save the diagrams to the specified output path
    architecture_diagram.render(os.path.join(output_path, 'architecture_diagram'), format='png')
    call_graph.render(os.path.join(output_path, 'call_graph'), format='png')

    # Save the diagrams data for later use in JSON format
    with open(os.path.join(output_path, 'visualization_data.json'), 'w') as f:
        json.dump({
            'architecture_diagram': architecture_diagram.source,
            'call_graph': call_graph.source
        }, f)

    print("Visualization generated successfully.")

# Function to generate a visualization for a specific file
def generate_file_visualization(file_path, output_path):
    metadata = extract_metadata(file_path)
    ast = parse_code(file_path)
    call_relations = map_call_relationships(ast)

    # Initialize a directed graph for the file visualization
    file_call_graph = Digraph(comment=f'Call Graph for {metadata["name"]}')

    # Add nodes and edges to the call graph
    file_call_graph.node(metadata['name'])
    for relation in call_relations:
        file_call_graph.edge(relation['caller'], relation['callee'])

    # Save the diagram to the specified output path
    file_call_graph.render(os.path.join(output_path, f'{metadata["name"]}_call_graph'), format='png')
    print(f"Visualization for {metadata['name']} generated successfully.")
```