import requests
import time
from error_handling import handle_error

def check_ollama_available():
    """Verifica se o servidor Ollama está disponível."""
    try:
        response = requests.get("http://localhost:11434/api/version", timeout=2)
        return response.status_code == 200
    except requests.exceptions.RequestException:
        return False

def wait_for_ollama(max_retries=3, retry_interval=2):
    """Espera que o Ollama esteja disponível, com número máximo de tentativas."""
    for i in range(max_retries):
        if check_ollama_available():
            return True
        print(f"Esperando pelo servidor Ollama... Tentativa {i+1}/{max_retries}")
        time.sleep(retry_interval)
    return False

def get_settings():
    """Carrega as configurações do arquivo settings.json."""
    try:
        import json
        with open('settings.json', 'r') as f:
            return json.load(f)
    except Exception as e:
        print(f"Aviso: Não foi possível carregar as configurações: {e}")
        return {"model": "deepseek-coder:1.3b", "endpoint": "http://localhost:11434/api/generate"}

def query_ai(context, model=None):
    try:
        settings = get_settings()
        model = model or settings.get("model", "deepseek-coder:1.3b")
        
        # Verifica se o Ollama está disponível
        if not check_ollama_available():
            return "Erro: Servidor Ollama não está disponível. Verifique se o Ollama está em execução."
        
        response = requests.post(
            settings.get("endpoint", "http://localhost:11434/api/generate"),
            json={
                "model": model,
                "prompt": context,
                "stream": False,
                "options": {
                    "temperature": 0.7,
                    "max_tokens": 2000
                }
            },
            timeout=30  # Adicionando timeout para evitar espera infinita
        )
        
        
        if response.status_code == 200:
            return response.json().get("response", "Resposta vazia da IA")
        else:
            return f"Erro na resposta do servidor: {response.status_code}"
    except Exception as e:
        handle_error("IA Query", e)
        return f"Erro na comunicação com a IA: {str(e)}"