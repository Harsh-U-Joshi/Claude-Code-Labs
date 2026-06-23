from context import TicketContext
from gates import (
    PipelineGateError,
    gate_classification,
    gate_enrichment,
    gate_draft,
)

from subagents import (
    run_classifier,
    run_crm_enricher,
    run_drafter,
    run_validator,
)


def main():
    try:
        ctx = TicketContext(
            ticket_id="INC-1001",
            raw_ticket="Subject: Cannot access SSO login — entire team locked out Our team of 40 has been unable to log in via SSO since 09:00 this morning. We have a client demo in 3 hours. This is completely blocking us",
            customer_email="sarah.chen@globalcorp.com"
        )

        # Step 1 - Classifier
        classification = run_classifier(ctx.raw_ticket)

        ctx.product_area = classification.get("product_area")
        ctx.severity = classification.get("severity")
        ctx.intent = classification.get("intent")

        # Sabotage
        ctx.severity = None

        print("\n=== CLASSIFIER ===")
        print(classification)

        gate_classification(ctx)
        print("Gate 1 passed")

        # Step 2 - CRM Enricher
        crm = run_crm_enricher(
            ctx.customer_email,
            classification
        )

        ctx.account_tier = crm.get("account_tier")
        ctx.sla_tier = crm.get("sla_tier")
        ctx.account_manager = crm.get("account_manager")

        print("\n=== CRM ENRICHER ===")
        print(crm)

        gate_enrichment(ctx)
        print("Gate 2 passed")

        # Step 3 - Drafter
        draft = run_drafter(
            ctx.raw_ticket,
            classification,
            crm
        )

        ctx.draft_response = draft

        print("\n=== DRAFTER ===")
        print(draft)

        gate_draft(ctx)
        print("Gate 3 passed")

        # Step 4 - Validator
        validation = run_validator(
            ctx.draft_response,
            classification,
            crm
        )

        ctx.validation_result = validation

        print("\n=== VALIDATOR ===")
        print(validation)

        print("\n=== FINAL CONTEXT ===")
        print(ctx)

    except PipelineGateError as e:
        print(f"\n[PIPELINE BLOCKED] {e}")


if __name__ == "__main__":
    main()