# The idea is to keep Ollama's communication separate from Flask.
import requests

OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL = "qwen2.5:7b"

def analyze_ticket(description):
    prompt = f"""
You are an IT support ticket triage assistant.

Analyze the following ticket:

{description}

Provide:
- Category
- Priority
- Assigned team
- Summary
- Recommended actions
"""
    response = requests.post(
        OLLAMA_URL,
        json={
            "model": MODEL,
            "prompt": prompt,
            "stream": False
        }
    )

    response.raise_for_status()

    result = response.json()

    return result["response"]

if __name__ == "__main__":
    result = analyze_ticket(
        "My laptop cannot connect to the company Wi-Fi"
    )

    print(result)
