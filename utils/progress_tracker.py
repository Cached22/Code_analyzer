```python
from progress.bar import Bar

class ProgressTracker:
    def __init__(self, total_files):
        self.total_files = total_files
        self.analyzed_files = 0
        self.bar = Bar('Analyzing', max=self.total_files)

    def update_progress(self, file_path):
        self.analyzed_files += 1
        self.bar.next()
        print(f"Completed analysis of {file_path}")

    def is_complete(self):
        return self.analyzed_files == self.total_files

    def finalize(self):
        self.bar.finish()
        print("Analysis complete.")

    def get_progress_percentage(self):
        return (self.analyzed_files / self.total_files) * 100
```