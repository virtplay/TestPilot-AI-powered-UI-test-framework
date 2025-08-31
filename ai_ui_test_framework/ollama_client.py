import requests, json
OLLAMA_URL = "http://localhost:11434/api/generate"

def ask_ollama(model, prompt, stream=False):
    payload = {"model": model,"prompt": prompt,"stream": False}
    r = requests.post(OLLAMA_URL, json=payload, timeout=120)
    r.raise_for_status()
    return r.json().get("response") or r.text
