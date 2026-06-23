from context import TicketContext


class PipelineGateError(Exception):
    pass


def gate_classification(ctx: TicketContext) -> None:
    missing = []

    if ctx.product_area is None:
        missing.append("product_area")

    if ctx.severity is None:
        missing.append("severity")

    if ctx.intent is None:
        missing.append("intent")

    if missing:
        raise PipelineGateError(
            f"Classification gate failed. Missing fields: {', '.join(missing)}"
        )


def gate_enrichment(ctx: TicketContext) -> None:
    missing = []

    if ctx.account_tier is None:
        missing.append("account_tier")

    if ctx.sla_tier is None:
        missing.append("sla_tier")

    if ctx.account_manager is None:
        missing.append("account_manager")

    if missing:
        raise PipelineGateError(
            f"Enrichment gate failed. Missing enrichment fields: "
            f"{', '.join(missing)}. "
            f"Please rerun the CRM Enricher."
        )


def gate_draft(ctx: TicketContext) -> None:
    if ctx.draft_response is None:
        raise PipelineGateError(
            "Draft gate failed. draft_response is None. "
            "Please rerun the Drafter."
        )