import os
import json
import re
import google.generativeai as genai

genai.configure(api_key=os.environ.get("GEMINI_API_KEY"))
model = genai.GenerativeModel("gemini-1.5-flash")


def classify_ticket(description):
    prompt = f"""
You are a support ticket classifier.

Classify the ticket into:

Categories: billing, technical, account, general
Priorities: low, medium, high, critical

IMPORTANT:
Return ONLY valid JSON.
Do NOT add explanation.
Do NOT use markdown.
Example format:
{{"category": "billing", "priority": "high"}}

Ticket Description:
{description}
"""

    try:
        response = model.generate_content(prompt)
        content = response.text.strip()

        # Remove markdown if Gemini adds it
        content = re.sub(r"```json|```", "", content).strip()

        result = json.loads(content)

        return {
            "suggested_category": result.get("category", "general"),
            "suggested_priority": result.get("priority", "medium"),
        }

    except Exception as e:
        print("LLM ERROR:", e)  # see error in docker logs
        return {
            "suggested_category": "general",
            "suggested_priority": "medium",
        }
