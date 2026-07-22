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
        discount_rate_basis: str = "",
        assumptions: Optional[List[str]] = None,
        current_state: str = "",
        ai_workflow: str = ""
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
        self.discount_rate_basis = discount_rate_basis or (
            "Manually set; not sourced from a live rate feed. Production version would pull a "
            "current prime or SOFR-based benchmark plus a risk premium instead of a fixed input."
        )
        self.assumptions = assumptions or []
        self.current_state = current_state
        self.ai_workflow = ai_workflow

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
        discount_rate_basis=(
            "Approximates a typical small-business equipment term-loan rate (prime + ~1.5%). "
            "This is debt-financed capex, not equity, so the hurdle is the loan's cost, not the "
            "owner's blended cost of capital. Manually set for this demo, not pulled from a live rate feed."
        ),
        assumptions=[
            "Secondary technician can be hired and fully trained within 30 days.",
            "Local commercial call volumes remain steady throughout the fiscal year.",
            "Fuel and maintenance costs do not exceed standard commercial averages."
        ],
        current_state=(
            "Today the owner decides on gear purchases by feel, after a slow month or a "
            "frustrated phone call, with no NPV, IRR, or payback math run at all. There is no "
            "in-house analyst and no time to build a spreadsheet between service calls, so the "
            "purchase either gets approved on gut instinct or shelved indefinitely. Meanwhile the "
            "2-week backlog keeps quietly costing the business its highest-margin commercial jobs, "
            "which get referred straight to competitors."
        ),
        ai_workflow=(
            "The owner enters the same numbers they already know off the top of their head "
            "(van cost, hire cost, expected new commercial volume) into one intake form. EDI runs "
            "the full financial model, red-team-challenges the assumptions, and flags governance "
            "thresholds automatically. The owner still makes the final call and signs off — EDI "
            "never auto-approves capital, it just gives a $2M-decision-grade analysis to a business "
            "that could never otherwise afford to run one."
        )
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
        discount_rate_basis=(
            "Higher than the CapEx case on purpose: a 3-point risk premium is layered on top of a "
            "typical small-business borrowing rate to reflect this vendor's track record of missed "
            "milestones. Manually set for this demo, not pulled from a live rate feed."
        ),
        assumptions=[
            "The final $6,500 payment fully resolves checkout database errors.",
            "The agency completes the project within the proposed 45-day window.",
            "Operational security patches will not require a monthly engineering retainer."
        ],
        current_state=(
            "The owner is reasoning from \"we've already put $18,000 into this\" rather than "
            "\"what does the next $6,500 actually buy us\" — the textbook sunk-cost trap, made "
            "worse by an agency that has every incentive to ask for one more milestone. There is "
            "no formal separation of past spend from forward economics, so the decision is being "
            "made on frustration and momentum instead of numbers."
        ),
        ai_workflow=(
            "EDI structurally decouples the $18,000 already spent from the forward-looking NPV "
            "of the remaining $6,500, and names the sunk-cost bias explicitly in the Risks tab "
            "instead of leaving it implicit. The owner still decides whether to pay or walk away — "
            "but they decide with the emotional trap labeled, not hidden inside a bigger number."
        )
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
        discount_rate_basis=(
            "A blended small-business hurdle rate for a discretionary opex-like tool purchase — "
            "no dedicated financing behind it, so this approximates prime plus a standard risk "
            "premium. Manually set for this demo, not pulled from a live rate feed."
        ),
        assumptions=[
            "Instantly texting back missed calls rescues at least two prospects per month.",
            "Google review velocity improves local search ranking within 90 days.",
            "Workflow tooling remains stable without requiring custom developer maintenance."
        ],
        current_state=(
            "The owner has a vague sense they're \"missing calls\" but no dollar figure attached "
            "to it, so a $3,500 automation tool gets evaluated on its feature list and a sales "
            "pitch rather than on math — nobody runs a spreadsheet for a decision this size. The "
            "revenue leak from missed calls and stalled review velocity keeps bleeding quietly "
            "because it has never been measured."
        ),
        ai_workflow=(
            "EDI turns a felt-but-unmeasured problem into a calculated NPV, IRR, and payback "
            "period from a handful of inputs, giving a $3,500 decision the same analytical rigor "
            "a company would normally reserve for its largest capital purchases. The owner still "
            "approves the spend; EDI just makes sure the approval is based on numbers instead of "
            "a gut feeling."
        )
    )
}