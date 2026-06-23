from subagents import (
    run_classifier,
    run_crm_enricher,
    run_drafter,
    run_validator,
)

from context import TicketContext


def main():
    # Create context
    ctx = TicketContext(
        ticket_id="INC-1001",
        raw_ticket="Subject: Cannot access SSO login — entire team locked out Our team of 40 has been unable to log in via SSO since 09:00 this morning. We have a client demo in 3 hours. This is completely blocking us",
        customer_email="sarah.chen@globalcorp.com"
    )

    # Classifier
    classification = run_classifier(ctx.raw_ticket)

    ctx.product_area = classification.get("product_area")
    ctx.severity = classification.get("severity")
    ctx.intent = classification.get("intent")

    print("\n=== CLASSIFIER ===")
    print(classification)
    print("Classification Complete:", ctx.classification_complete())

    # CRM Enricher
    crm = run_crm_enricher(
        ctx.customer_email,
        classification
    )

    ctx.account_tier = crm.get("account_tier")
    ctx.sla_tier = crm.get("sla_tier")
    ctx.account_manager = crm.get("account_manager")

    print("\n=== CRM ENRICHER ===")
    print(crm)
    print("Enrichment Complete:", ctx.enrichment_complete())

    # Drafter
    draft = run_drafter(
        ctx.raw_ticket,
        classification,
        crm
    )

    ctx.draft_response = draft

    print("\n=== DRAFTER ===")
    print(draft)
    print("Draft Complete:", ctx.draft_complete())

    # Validator
    validation = run_validator(
        ctx.draft_response,
        classification,
        crm
    )

    ctx.validation_result = validation

    print("\n=== VALIDATOR ===")
    print(validation)

    # Final Context
    print("\n=== FINAL CONTEXT ===")
    print(ctx)


if __name__ == "__main__":
    main()