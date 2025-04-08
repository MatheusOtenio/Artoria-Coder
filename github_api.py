import os
import tempfile
from git import Repo
from error_handling import handle_error  # Added import

def clone_repo(repo_url):
    try:
        clone_dir = tempfile.mkdtemp(prefix="repo_")
        Repo.clone_from(repo_url, clone_dir)
        return clone_dir
    except Exception as e:
        handle_error("Clonagem de Repositório", e)
        print(f"Erro ao clonar repositório: {e}")
        return None