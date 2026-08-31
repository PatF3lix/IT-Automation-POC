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

Choose the LOWEST appropriate support level.

Role selection rules:

Tech Support L2:
- Standard end-user software issues
- Microsoft Teams, Outlook, Microsoft 365, browser, or application issues
- Password or access problems
- Common workstation issues
- Basic hardware troubleshooting
- Common Wi-Fi or connectivity issues
- Issues that have not yet been escalated or deeply investigated

Tech Support L3:
- Complex technical issues requiring advanced troubleshooting
- Problems explicitly escalated from L2
- Recurring issues where normal troubleshooting has failed
- Advanced operating system or application problems
- Issues involving deeper technical investigation

Senior Network Administrator:
- Routing, switching, VLANs, firewalls, VPN infrastructure
- Network-wide outages
- Advanced network infrastructure problems

Senior System Administrator:
- Active Directory
- Windows or Linux server issues
- Virtualization
- Server infrastructure
- Advanced identity or systems administration issues

Important:
- Do not choose Tech Support L3 simply because the root cause is unknown.
- If both L2 and L3 could handle the issue, choose Tech Support L2.
- Individual user issues should normally start at L2 unless the ticket clearly indicates escalation or advanced complexity.

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