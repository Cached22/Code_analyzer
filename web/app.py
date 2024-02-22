```python
from flask import Flask, render_template, jsonify, request
from utils.file_analyzer import analyze_files
from utils.documentation_generator import generate_documentation
from utils.visualization import generate_visualization
from utils.progress_tracker import ProgressTracker
from data.file_metadata import FILE_METADATA_SCHEMA
from data.analysis_results import ANALYSIS_RESULTS_SCHEMA
import json
import os

app = Flask(__name__)

# Initialize the progress tracker
progress_tracker = ProgressTracker()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')

@app.route('/analyze', methods=['POST'])
def analyze_codebase():
    # Start the analysis
    progress_tracker.reset()
    directory = request.form.get('directory', '.')
    depth = int(request.form.get('depth', 5))
    analysis_results = analyze_files(directory, depth, progress_tracker)
    return jsonify(analysis_results)

@app.route('/generate-docs', methods=['POST'])
def generate_docs():
    # Generate documentation
    metadata = json.loads(request.form['metadata'], object_hook=FILE_METADATA_SCHEMA)
    results = json.loads(request.form['results'], object_hook=ANALYSIS_RESULTS_SCHEMA)
    docs = generate_documentation(metadata, results)
    return jsonify(docs)

@app.route('/generate-visualization', methods=['GET'])
def visualization():
    # Generate visualization
    file_path = request.args.get('file_path')
    visualization_data = generate_visualization(file_path)
    return jsonify(visualization_data)

@app.route('/progress')
def progress():
    # Get current progress
    return jsonify(progress_tracker.get_progress())

@app.route('/search', methods=['GET'])
def search():
    # Search in the generated documentation
    query = request.args.get('query')
    search_results = []  # This should be replaced with actual search logic
    return jsonify(search_results)

if __name__ == '__main__':
    app.run(debug=True)
```