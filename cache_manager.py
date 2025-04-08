import json
import hashlib
from pathlib import Path
import tempfile
import time  # Added import
import shutil  # Added import

CACHE_DIR = Path.home() / '.code_assistant_cache'

class ProjectCache:
    def __init__(self):
        CACHE_DIR.mkdir(exist_ok=True)
        self.cache_index = self._load_index()

    def _load_index(self):
        index_file = CACHE_DIR / 'index.json'
        if index_file.exists():
            with open(index_file, 'r') as f:
                return json.load(f)
        return {}

    def _save_index(self):
        with open(CACHE_DIR / 'index.json', 'w') as f:
            json.dump(self.cache_index, f)

    def get_cache_key(self, repo_url):
        return hashlib.sha256(repo_url.encode()).hexdigest()

    def get_cached_project(self, repo_url):
        key = self.get_cache_key(repo_url)
        return CACHE_DIR / key if key in self.cache_index else None

    def cache_project(self, repo_url, project_path):
        key = self.get_cache_key(repo_url)
        dest = CACHE_DIR / key
        if dest.exists():
            return dest
        
        # Implementation of directory copying
        shutil.copytree(project_path, dest)
        
        self.cache_index[key] = {
            'url': repo_url,
            'timestamp': time.time()
        }
        self._save_index()
        return dest