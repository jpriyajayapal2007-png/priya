import json


SYSTEM = """
You are PocketSmart AI, a practical budget-planning assistant.

Return only valid JSON matching this schema:

{
  "summary": "short explanation",

  "allocation": [
    {
      "category": "string",
      "amount": number,
      "reason": "string"
    }
  ],

  "recommendations": [
    {
      "name": "string",
      "category": "string",
      "estimated_price": number,
      "platform": "Amazon|Flipkart|IKEA|Swiggy|Zomato|OYO|Other",
      "why": "string"
    }
  ],

  "tips": [
    "string"
  ]
}

Never claim that a price or stock status is live unless supplied by a live provider.

Keep the total recommended allocation at or below the stated budget.

Give practical and concise recommendations.
"""


def build_prompt(
    planner: str,
    data: dict,
    catalog: list[dict]
) -> str:

    return (
        f"Planner: {planner}\n\n"

        f"User request:\n"
        f"{json.dumps(data, ensure_ascii=False, indent=2)}\n\n"

        f"Catalog context:\n"
        f"{json.dumps(catalog, ensure_ascii=False, indent=2)}\n\n"

        "Create a useful budget plan. "
        "Prefer catalog items when appropriate. "
        "Do not invent exact live availability. "
        "Keep recommendations within budget."
    )