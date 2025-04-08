import json
from datetime import datetime
from pathlib import Path
from error_handling import handle_error  # Added import

HISTORY_DIR = Path('conversation_history')

class HistoryManager:
    def __init__(self):
        HISTORY_DIR.mkdir(exist_ok=True)

    def _get_history_file(self, project_id):
        return HISTORY_DIR / f"{project_id}.json"

    def save_conversation(self, project_id, messages):
        try:
            history_file = self._get_history_file(project_id)
            history = []
            if history_file.exists():
                with open(history_file, 'r') as f:
                    history = json.load(f)
            
            history.append({
                'timestamp': datetime.now().isoformat(),
                'messages': messages
            })
            
            with open(history_file, 'w') as f:
                json.dump(history, f)
        except Exception as e:
            handle_error("Salvar Histórico", e)

    def load_history(self, project_id):
        try:
            history_file = self._get_history_file(project_id)
            if history_file.exists():
                with open(history_file, 'r') as f:
                    return json.load(f)
            return []
        except Exception as e:
            handle_error("Carregar Histórico", e)
            return []

    def get_project_history_list(self):
        try:
            return [f.stem for f in HISTORY_DIR.glob("*.json")]
        except Exception as e:
            handle_error("Listar Históricos", e)
            return []