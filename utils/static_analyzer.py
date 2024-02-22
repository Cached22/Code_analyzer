```python
import ast
from collections import defaultdict

class StaticAnalyzer:
    def __init__(self):
        self.call_graph = defaultdict(list)

    def analyze_file(self, file_path):
        with open(file_path, 'r') as file:
            node = ast.parse(file.read(), filename=file_path)
            self.visit(node)

    def visit(self, node, parent=None):
        for child in ast.iter_child_nodes(node):
            if isinstance(child, ast.FunctionDef) or isinstance(child, ast.AsyncFunctionDef):
                if parent:
                    self.call_graph[parent].append(child.name)
                self.visit(child, child.name)
            elif isinstance(child, ast.Call) and isinstance(child.func, ast.Name):
                if parent:
                    self.call_graph[parent].append(child.func.id)
            self.visit(child, parent)

    def get_call_graph(self):
        return dict(self.call_graph)

    def save_call_graph(self, output_path):
        with open(output_path, 'w') as file:
            for parent, children in self.call_graph.items():
                file.write(f"{parent} calls: {', '.join(children)}\n")

if __name__ == "__main__":
    analyzer = StaticAnalyzer()
    # Example usage: analyze a single file
    analyzer.analyze_file('example.py')
    call_graph = analyzer.get_call_graph()
    print(call_graph)
    # Save the call graph to a file
    analyzer.save_call_graph('call_graph.txt')
```