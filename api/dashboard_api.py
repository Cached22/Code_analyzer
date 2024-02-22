```python
from flask import Flask, jsonify, request
from utils.file_analyzer import extract_metadata
from utils.static_analyzer import map_call_relationships
from utils.visualization import generate_visualization
from utils.documentation_generator import format_documentation
from data.file_metadata import FILE_METADATA_SCHEMA
from data.analysis_results import ANALYSIS_RESULTS_SCHEMA
import os
import json

app = Flask(__name__)

@app.route('/dashboard', methods=['GET'])
def dashboard():
    # Load the analysis results and file metadata
    with open('data/analysis_results.json', 'r') as analysis_results_file:
        analysis_results = json.load(analysis_results_file)
    
    with open('data/file_metadata.json', 'r') as file_metadata_file:
        file_metadata = json.load(file_metadata_file)
    
    # Prepare the dashboard data
    dashboard_data = {
        'fileMetadata': file_metadata,
        'analysisResults': analysis_results
    }
    
    return jsonify(dashboard_data)

@app.route('/visualize', methods=['POST'])
def visualize():
    content = request.json
    file_path = content.get('filePath')
    
    if not os.path.exists(file_path):
        return jsonify({'error': 'File does not exist'}), 404
    
    # Extract metadata and perform static analysis
    metadata = extract_metadata(file_path)
    call_relationships = map_call_relationships(file_path)
    
    # Generate visualization
    visualization = generate_visualization(call_relationships)
    
    return jsonify({'visualization': visualization})

@app.route('/documentation', methods=['GET'])
def documentation():
    file_type = request.args.get('type', default='md', type=str)
    
    # Check if the requested documentation type is supported
    if file_type not in ['md', 'html', 'json']:
        return jsonify({'error': 'Unsupported documentation type'}), 400
    
    # Load the documentation data
    documentation_path = f'data/documentation_data.{file_type}'
    if not os.path.exists(documentation_path):
        return jsonify({'error': 'Documentation not found'}), 404
    
    with open(documentation_path, 'r') as documentation_file:
        documentation_data = documentation_file.read()
    
    if file_type == 'json':
        documentation_data = json.loads(documentation_data)
    
    return jsonify({'documentation': documentation_data})

if __name__ == '__main__':
    app.run(debug=True)
```