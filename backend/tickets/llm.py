import os
from openai import OpenAI

client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))


def classify_ticket(description):
    prompt = f"""
    You are a support ticket classifier.

    Based on the following description, return:
    - category: billing, technical, account, or general
    - priority: low, medium, high, or critical

    Return ONLY valid JSON like:
    {{
        "category": "...",
        "priority": "..."
    }}

    Description:
    {description}
    """

    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}],
        )

        content = response.choices[0].message.content

        import json
        result = json.loads(content)

        return {
            "suggested_category": result.get("category", "general"),
            "suggested_priority": result.get("priority", "medium"),
        }

    except Exception:
        # graceful fallback
        return {
            "suggested_category": "general",
            "suggested_priority": "medium",
        }
