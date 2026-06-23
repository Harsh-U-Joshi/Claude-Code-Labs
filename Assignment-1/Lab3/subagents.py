import json
from anthropic import Anthropic

modelName = 'claude-haiku-4-5-20251001'

client = Anthropic()

def run_classifier(ticket: str) -> dict:
    response = client.messages.create(
        model=modelName,
        max_tokens=300,
        system=(
            "Classify into product_area, severity, intent. "
            "Respond only in JSON."
        ),
        messages=[
            {
                "role": "user",
                "content": ticket
            }
        ]
    )

    text = response.content[0].text.strip()

    # Remove markdown code fences if present
    text = text.replace("```json", "").replace("```", "").strip()

    return json.loads(text)


def run_crm_enricher(customer_email: str, classification: dict) -> dict:
    # Simulated CRM lookup
    return {
        "account_tier": "Enterprise",
        "sla_tier": "4-hour response",
        "account_manager": "Jane Smith",
        "contract_value": 50000
    }


def run_drafter(ticket: str, classification: dict, crm: dict) -> str:
    context = f"""
Ticket:
{ticket}

Classification:
{json.dumps(classification, indent=2)}

CRM:
{json.dumps(crm, indent=2)}
"""

    response = client.messages.create(
        model=modelName,
        max_tokens=500,
        system=(
            "Draft a professional first-response email "
            "referencing the SLA tier."
        ),
        messages=[
            {
                "role": "user",
                "content": context
            }
        ]
    )

    return response.content[0].text


def run_validator(draft: str, classification: dict, crm: dict) -> str:
    validation_context = f"""
                Draft:
                {draft}

                Product Area:
                {classification.get('product_area')}

                Severity:
                {classification.get('severity')}

                Intent:
                {classification.get('intent')}

                Account Tier:
                {crm.get('account_tier')}

                SLA Tier:
                {crm.get('sla_tier')}

                Check:
                1. Product area is reflected correctly.
                2. SLA commitments match the SLA tier.
                3. Tone is professional.

                Reply APPROVED or list issues.
                """

    response = client.messages.create(
        model=modelName,
        max_tokens=300,
        system=(
            "Check product area, SLA match, and tone. "
            "Reply APPROVED or list issues."
        ),
        messages=[
            {
                "role": "user",
                "content": validation_context
            }
        ]
    )

    return response.content[0].text