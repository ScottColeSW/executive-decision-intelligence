from typing import Dict, List
from data.cases import DecisionCase

class GovernanceEngine:
    """
    Ensures SME projects respect strategic business policies, budget constraints,
    and classic risk-mitigation criteria. Each check returns a status so the UI can
    render a structured policy review instead of a flat list of strings.
    """

    MIN_HURDLE_RATE = 0.05

    CATEGORY_NOTES = {
        "CAPEX": "Equipment insurance and liability coverage must be confirmed before asset purchase.",
        "SUNK": "Vendor/agency performance clause should be reviewed before authorizing a final milestone payment.",
        "AI": "Third-party data handling and customer-consent policy review required before deployment.",
        "VENDOR": "Independently verify vendor-claimed performance figures before signing a multi-year contract; treat urgency-driven pricing as a red flag, not a reason to skip review.",
        "LEASE": "Confirm early-termination penalties and total cost of ownership across every financing structure before signing.",
    }

    CATEGORY_LABELS = {
        "CAPEX": "CapEx",
        "SUNK": "Sunk Cost",
        "AI": "AI",
        "VENDOR": "Vendor Contract",
        "LEASE": "Financing",
    }

    def review(self, case: DecisionCase) -> List[Dict[str, str]]:
        checks: List[Dict[str, str]] = []

        # Policy Rule 1: Investment Limits
        if case.investment > 100000.0:
            checks.append({
                "check": "Budget Cap",
                "status": "review",
                "detail": "Capital allocation exceeds standard discretionary thresholds ($100k). Requires multi-partner signature."
            })
        else:
            checks.append({
                "check": "Budget Cap",
                "status": "pass",
                "detail": "Investment capital falls within standard SME working limits ($100k discretionary ceiling)."
            })

        # Policy Rule 2: Approval routing, synthesized from investment size
        if case.investment < 10000:
            routing = "Owner sign-off only."
        elif case.investment <= 100000:
            routing = "Owner + Financial Advisor sign-off required."
        else:
            routing = "Multi-partner signature required before funds release."
        checks.append({
            "check": "Approval Routing",
            "status": "pass",
            "detail": routing
        })

        # Policy Rule 3: Decoupled Sunk Costs
        if case.sunk_costs > 0:
            checks.append({
                "check": "Sunk Cost Decoupling",
                "status": "pass",
                "detail": f"Emotional sunk costs (${case.sunk_costs:,.2f}) successfully flagged and decoupled from future planning math."
            })

        # Policy Rule 4: Time Horizon Check
        if case.horizon_years > 5:
            checks.append({
                "check": "Forecast Horizon",
                "status": "flag",
                "detail": "Projections past 5 years introduce high estimation risk. Requesting annual reviews."
            })
        else:
            checks.append({
                "check": "Forecast Horizon",
                "status": "pass",
                "detail": "Horizon parameters sit inside reliable, near-term modeling buffers."
            })

        # Policy Rule 5: Hurdle Rate Compliance
        if case.discount_rate < self.MIN_HURDLE_RATE:
            checks.append({
                "check": "Hurdle Rate Compliance",
                "status": "flag",
                "detail": (
                    f"Discount rate ({case.discount_rate * 100:.1f}%) is below the {self.MIN_HURDLE_RATE * 100:.0f}% "
                    f"policy minimum for risk-adjusted capital decisions. Basis: {case.discount_rate_basis}"
                )
            })
        else:
            checks.append({
                "check": "Hurdle Rate Compliance",
                "status": "pass",
                "detail": (
                    f"Discount rate ({case.discount_rate * 100:.1f}%) meets or exceeds the {self.MIN_HURDLE_RATE * 100:.0f}% "
                    f"policy minimum. Basis: {case.discount_rate_basis}"
                )
            })

        # Policy Rule 6: Assumption Documentation
        if len(case.assumptions) < 2:
            checks.append({
                "check": "Assumption Documentation",
                "status": "flag",
                "detail": "Fewer than 2 assumptions logged. Insufficient documentation to support a defensible decision trail."
            })
        else:
            checks.append({
                "check": "Assumption Documentation",
                "status": "pass",
                "detail": f"{len(case.assumptions)} assumptions logged and available for audit review."
            })

        # Policy Rule 7: Case-category-specific review
        category = case.case_id.split("-")[1] if case.case_id.count("-") >= 2 else ""
        if category in self.CATEGORY_NOTES:
            checks.append({
                "check": f"{self.CATEGORY_LABELS[category]} Category Review",
                "status": "review",
                "detail": self.CATEGORY_NOTES[category]
            })

        return checks
