# The idea is to keep Ollama's communication separate from Flask.
import requests
import json

OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL = "qwen2.5:7b"


def analyze_ticket(description):
    prompt = f"""
You are an IT support ticket triage assistant.

Analyze the following ticket:

{description}

Return ONLY valid json.
Do not include markdown, explanations, or ```json code blocks.

Use exactly these fields:

{{
    "category": "Network, Hardware, Software, Access, Security, or Other",
    "priority": "Low, Medium, High, or Critical",
    "assigned_team": "the appropriate IT team",
    "required_department": "IT",
    "preferred_role": "choose one of: Senior System Administrator, Senior Network Administrator, Tech Support L2, Tech Support L3",
    "summary": "a short summary of the problem",
    "recommendations": [
        "recommended action 1",
        "recommended action 2"
    ]
}}
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

    return json.loads(result["response"])


if __name__ == "__main__":
    result = analyze_ticket(
        "My laptop cannot connect to the company Wi-Fi"
    )

    print(result)
    print(type(result))
    print(result["category"])
    print(result["priority"])
    print(result["required_department"])
    print(result["preferred_role"])