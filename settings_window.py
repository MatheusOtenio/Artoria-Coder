import customtkinter as ctk
import json
from error_handling import handle_error  # Added import

class SettingsWindow(ctk.CTkToplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.title("Configurações do Ollama")
        self.geometry("400x300")
        
        self.settings = self._load_settings()
        
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(4, weight=1)
        
        # Modelo
        ctk.CTkLabel(self, text="Modelo:").grid(row=0, column=0, padx=10, pady=5, sticky="w")
        self.model_entry = ctk.CTkEntry(self)
        self.model_entry.insert(0, self.settings.get('model', 'deepseek-coder'))
        self.model_entry.grid(row=1, column=0, padx=10, pady=5, sticky="ew")
        
        # Endpoint
        ctk.CTkLabel(self, text="Endpoint da API:").grid(row=2, column=0, padx=10, pady=5, sticky="w")
        self.endpoint_entry = ctk.CTkEntry(self)
        self.endpoint_entry.insert(0, self.settings.get('endpoint', 'http://localhost:11434/api/generate'))
        self.endpoint_entry.grid(row=3, column=0, padx=10, pady=5, sticky="ew")
        
        # Botões
        self.save_btn = ctk.CTkButton(self, text="Salvar", command=self.save_settings)
        self.save_btn.grid(row=4, column=0, padx=10, pady=10, sticky="se")

    def _load_settings(self):
        try:
            with open('settings.json', 'r') as f:
                return json.load(f)
        except Exception as e:
            print(f"Warning: Could not load settings: {e}")
            return {}

    def save_settings(self):
        try:
            self.settings = {
                'model': self.model_entry.get(),
                'endpoint': self.endpoint_entry.get()
            }
            # Fixed json.load to json.dump and swapped parameters
            with open('settings.json', 'w') as f:
                json.dump(self.settings, f)
            self.destroy()
        except Exception as e:
            handle_error("Salvar Configurações", e)