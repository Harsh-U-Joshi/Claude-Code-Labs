def ticket_classifier(ticket_text, fields_needed):
    text = ticket_text.lower()
    result = {}

    # Product Area
    if "invoice" in text or "payment" in text or "charge" in text or "refund" in text:
        product_area = "Billing"
    elif "api" in text or "integration" in text or "webhook" in text:
        product_area = "Integrations"
    elif "login" in text or "authentication" in text or "security" in text or "breach" in text:
        product_area = "Security"
    elif "setup" in text or "onboarding" in text or "getting started" in text:
        product_area = "Onboarding"
    else:
        product_area = "Platform"

    # Severity
    if any(word in text for word in ["outage", "down", "critical", "cannot access"]):
        severity = "P1-Critical"
    elif any(word in text for word in ["urgent", "blocked", "failure"]):
        severity = "P2-High"
    elif any(word in text for word in ["error", "issue", "problem"]):
        severity = "P3-Medium"
    else:
        severity = "P4-Low"

    # Intent
    if any(word in text for word in ["feature request", "enhancement", "would like"]):
        intent = "Feature Request"
    elif any(word in text for word in ["refund", "incorrect charge", "billing dispute"]):
        intent = "Billing Dispute"
    elif any(word in text for word in ["bug", "error", "not working", "fails"]):
        intent = "Bug"
    else:
        intent = "Question"

    field_values = {
        "product_area": product_area,
        "severity": severity,
        "intent": intent,
    }

    for field in fields_needed:
        if field in field_values:
            result[field] = field_values[field]

    return result