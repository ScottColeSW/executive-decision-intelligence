from types import SimpleNamespace
from typing import List, Optional
from pydantic import BaseModel, Field
from data.cases import DecisionCase

class FinancialAnalysisResult(BaseModel):
    case_id: str
    forward_npv: float = Field(..., description="NPV of future cash flows minus future investment")
    total_project_npv: float = Field(..., description="NPV including sunk costs to date")
    irr: Optional[float] = Field(None, description="Internal Rate of Return for forward cash flows")
    forward_roi: float = Field(..., description="Return on investment based solely on forward capital")
    total_roi: float = Field(..., description="Return on investment factoring in historical sunk costs")
    payback_period_years: Optional[float] = Field(None, description="Time required to recover forward investment")
    forward_cash_flows: List[float] = Field(..., description="Year-indexed forward cash flow stream, year 0 = initial outlay")

class FinancialEngine:
    """Processes DecisionCase models to output standardized corporate finance performance metrics."""

    @staticmethod
    def _calculate_npv(rate: float, cash_flows: List[float]) -> float:
        """Computes Net Present Value using the standard formula: $$NPV = \\sum_{t=0}^{N} \\frac{C_t}{(1 + r)^t}$$"""
        return sum(cf / ((1 + rate) ** t) for t, cf in enumerate(cash_flows))

    @staticmethod
    def _calculate_irr(cash_flows: List[float], max_iterations: int = 100) -> Optional[float]:
        """Finds the Internal Rate of Return where NPV equals zero using the bisection method."""
        # Simple validation: IRR requires at least one negative and one positive cash flow
        if all(cf >= 0 for cf in cash_flows) or all(cf <= 0 for cf in cash_flows):
            return None

        low, high = -0.99, 5.0
        tolerance = 1e-6

        def npv_at(r: float) -> float:
            return sum(cf / ((1 + r) ** t) for t, cf in enumerate(cash_flows))

        if npv_at(low) * npv_at(high) > 0:
            high = 20.0  # Expand upper bound for hyper-profitable cases (e.g., small AI tool returns)
            if npv_at(low) * npv_at(high) > 0:
                return None

        for _ in range(max_iterations):
            mid = (low + high) / 2.0
            npv_mid = npv_at(mid)

            if abs(npv_mid) < tolerance:
                return mid

            if npv_at(low) * npv_mid < 0:
                high = mid
            else:
                low = mid

        return (low + high) / 2.0

    def analyze(self, case: DecisionCase) -> FinancialAnalysisResult:
        """Executes full quantitative assessment on a given DecisionCase."""

        # Annualized forward cash flow, consistent with the rest of the platform's convention
        annual_cf = case.expected_return / max(1, case.horizon_years)

        # 1. Build cash flow streams
        # Forward flows: year 0 is the fresh initial investment out
        forward_flows = [-case.investment] + [annual_cf] * case.horizon_years

        # Total flows: treats sunk costs as an instantaneous loss incurred at Year 0 alongside new investment
        total_investment = case.investment + case.sunk_costs
        total_flows = [-total_investment] + [annual_cf] * case.horizon_years

        # 2. Compute NPVs
        forward_npv = self._calculate_npv(case.discount_rate, forward_flows)
        total_project_npv = self._calculate_npv(case.discount_rate, total_flows)

        # 3. Compute IRR (Forward-looking)
        irr = self._calculate_irr(forward_flows)

        # 4. Compute ROI Metrics
        total_nominal_returns = annual_cf * case.horizon_years

        forward_roi = (
            (total_nominal_returns - case.investment) / case.investment
            if case.investment > 0 else 0.0
        )

        total_roi = (
            (total_nominal_returns - total_investment) / total_investment
            if total_investment > 0 else 0.0
        )

        # 5. Compute Payback Period (Simple / Non-discounted)
        payback = None
        if annual_cf > 0:
            payback = case.investment / annual_cf

        return FinancialAnalysisResult(
            case_id=case.case_id,
            forward_npv=round(forward_npv, 2),
            total_project_npv=round(total_project_npv, 2),
            irr=round(irr, 4) if irr is not None else None,
            forward_roi=round(forward_roi, 4),
            total_roi=round(total_roi, 4),
            payback_period_years=round(payback, 2) if payback is not None else None,
            forward_cash_flows=[round(cf, 2) for cf in forward_flows]
        )

    def analyze_alternative(self, case: DecisionCase) -> Optional[FinancialAnalysisResult]:
        """
        If the case defines a second financing structure for the same opportunity
        (e.g. lease vs. buy), analyzes it through the identical model as the primary
        path so the two are directly comparable rather than eyeballed.
        """
        if not case.alternative_path:
            return None

        alt = case.alternative_path
        shadow_case = SimpleNamespace(
            case_id=f"{case.case_id}-ALT",
            investment=alt["investment"],
            expected_return=alt.get("expected_return", case.expected_return),
            sunk_costs=0.0,
            horizon_years=alt.get("horizon_years", case.horizon_years),
            discount_rate=alt.get("discount_rate", case.discount_rate),
        )
        return self.analyze(shadow_case)
