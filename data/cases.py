from typing import Dict, List, Optional

class DecisionCase:
    """Represents a structured operational scenario for small business decision analysis."""
    def __init__(
        self,
        case_id: str,
        title: str,
        question: str,
        company: str,
        investment: float,
        expected_return: float,
        sunk_costs: float = 0.0,
        horizon_years: int = 5,
        discount_rate: float = 0.08,
        assumptions: Optional[List[str]] = None
    ):
        self.case_id = case_id
        self.title = title
        self.question = question
        self.company = company
        self.investment = investment
        self.expected_return = expected_return
        self.sunk_costs = sunk_costs
        self.horizon_years = horizon_years
        self.discount_rate = discount_rate
        self.assumptions = assumptions or []

CASES: Dict[str, DecisionCase] = {
    "Hydro-Jetter Service Van Expansion (CapEx)": DecisionCase(
        case_id="SME-CAPEX-001",
        title="Hydro-Jetter Service Van Expansion",
        question="Should we purchase a secondary service vehicle and hire an assistant technician to handle our 2-week backlog?",
        company="A local plumbing and residential drain services firm. High-margin commercial calls are currently being referred to competitors due to a lack of immediate fleet capacity.",
        investment=85000.0,
        expected_return=140000.0,
        sunk_costs=0.0,
        horizon_years=5,
        discount_rate=0.07,
        assumptions=[
            "Secondary technician can be hired and fully trained within 30 days.",
            "Local commercial call volumes remain steady throughout the fiscal year.",
            "Fuel and maintenance costs do not exceed standard commercial averages."
        ]
    ),
    "Legacy E-Commerce Marketing Dilemma (Sunk Cost)": DecisionCase(
        case_id="SME-SUNK-002",
        title="Custom E-Commerce Platform Overhaul",
        question="Should we pay the local marketing agency a final $6,500 milestone to patch checkout bugs on our custom site, or cut losses?",
        company="A boutique retail store. They have already poured $18,000 into a custom Web App that remains too buggy to launch, leaving them stranded without digital sales.",
        investment=6500.0,
        expected_return=24000.0,
        sunk_costs=18000.0,
        horizon_years=3,
        discount_rate=0.10,
        assumptions=[
            "The final $6,500 payment fully resolves checkout database errors.",
            "The agency completes the project within the proposed 45-day window.",
            "Operational security patches will not require a monthly engineering retainer."
        ]
    ),
    "Automated Review Booster (AI ROI)": DecisionCase(
        case_id="SME-AI-003",
        title="Automated Review Booster & Missed-Call Text-Back System",
        question="Should we deploy a self-hosted automation server to automatically capture lost leads and boost local Google reviews?",
        company="A local service shop. Currently missing 15% of incoming phone calls when out in the field and losing local map rankings due to a lack of recent customer reviews.",
        investment=3500.0,
        expected_return=15000.0,
        sunk_costs=400.0,
        horizon_years=2,
        discount_rate=0.08,
        assumptions=[
            "Instantly texting back missed calls rescues at least two prospects per month.",
            "Google review velocity improves local search ranking within 90 days.",
            "Workflow tooling remains stable without requiring custom developer maintenance."
        ]
    )
}