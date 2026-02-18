import os
import json
import google.generativeai as genai

genai.configure(api_key=os.environ.get("GEMINI_API_KEY"))

model = genai.GenerativeModel("gemini-1.5-flash")


def classify_ticket(description):
    prompt = f"""
    You are a support ticket classifier.

    Choose:
    - category: billing, technical, account, general
    - priority: low, medium, high, critical

    Return ONLY valid JSON like:
    {{
        "category": "...",
        "priority": "..."
    }}

    Description:
    {description}
    """

    try:
        response = model.generate_content(prompt)
        content = response.text.strip()

        result = json.loads(content)

        return {
            "suggested_category": result.get("category", "general"),
            "suggested_priority": result.get("priority", "medium"),
        }

    except Exception:
        return {
            "suggested_category": "general",
            "suggested_priority": "medium",
        }
