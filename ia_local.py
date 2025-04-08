import requests

def query_ai(context, model="deepseek-coder"):
    try:
        response = requests.post(
            "http://localhost:11434/api/generate",
            json={
                "model": model,
                "prompt": context,
                "stream": False,
                "options": {
                    "temperature": 0.7,
                    "max_tokens": 2000
                }
            }
        )
        return response.json()["response"]
    except Exception as e:
        return f"Erro na comunicação com a IA: {str(e)}"