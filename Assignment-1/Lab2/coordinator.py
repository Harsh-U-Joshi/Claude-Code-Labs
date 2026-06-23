from subagents import (
    run_classifier,
    run_crm_enricher,
    run_drafter,
    run_validator,
)


def main():
    ticket = """
    Subject: Cannot access SSO login — entire 
    team locked out Our team of 40 has been unable to log in via SSO since 09:00 this morning. 
    We have a client demo in 3 hours. This is completely blocking us.
    """

    customer_email = "sarah.chen@globalcorp.com"

    # Step 1: Classifier
    classification = run_classifier(ticket)
    print("\n=== CLASSIFIER ===")
    print(classification)

    # Step 2: CRM Enricher
    crm = run_crm_enricher(customer_email, classification)
    print("\n=== CRM ENRICHER ===")
    print(crm)

    # Step 3: Drafter
    draft = run_drafter(ticket, classification, crm)
    print("\n=== DRAFTER ===")
    print(draft)

    # Step 4: Validator
    validation = run_validator(draft, classification, crm,ticket)
    print("\n=== VALIDATOR ===")
    print(validation)


if __name__ == "__main__":
    main()