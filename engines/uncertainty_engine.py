from typing import Dict, Any
import numpy as np
from data.cases import DecisionCase

class UncertaintyEngine:
    """
    Stress-tests the cash flow assumptions to measure sensitivity to real-world deviations.

    Both analyze() and simulate() derive their uncertainty band from the same _spread()
    formula, so the "volatility index" shown in the Summary tab and the dispersion behind
    the Monte Carlo simulation in the Risk & Uncertainty tab are the same number, not two
    independently-tuned approximations of the same idea.
    """

    @staticmethod
    def _spread(case: DecisionCase) -> float:
        """Uncertainty band width, driven by how many unverified assumptions the case rests on."""
        num_assumptions = len(case.assumptions)
        return min(0.45, 0.15 + (num_assumptions * 0.08))

    def analyze(self, case: DecisionCase, recommendation_result: Dict[str, Any]) -> Dict[str, Any]:
        volatility_index = self._spread(case)

        if recommendation_result.get("decision") == "INVEST" and volatility_index > 0.35:
            sensitivity_summary = "High assumption dependency. Small changes in market demand will delay project breakeven."
        else:
            sensitivity_summary = "Stable forecast. Operational model holds up well against minor margin pressures."

        return {
            "volatility_index": round(volatility_index, 2),
            "sensitivity": sensitivity_summary,
            "risk_adjusted_discount": round(case.discount_rate + (volatility_index * 0.05), 3)
        }

    def simulate(self, case: DecisionCase, trials: int = 5000, seed: int = 42) -> Dict[str, Any]:
        """
        Runs a Monte Carlo simulation over investment cost, annual return, and discount rate
        uncertainty, producing a distribution of forward NPV outcomes rather than a single
        point estimate, plus a one-at-a-time sensitivity ranking (tornado analysis).
        """
        rng = np.random.default_rng(seed)

        spread = self._spread(case)
        base_annual_cf = case.expected_return / max(1, case.horizon_years)

        # Triangular distributions: capital costs skew upward (overruns are more common than
        # underruns), returns skew downward (optimism bias in owner-supplied forecasts).
        investment_draws = rng.triangular(
            case.investment * (1 - spread * 0.5),
            case.investment,
            case.investment * (1 + spread),
            trials
        )
        annual_cf_draws = rng.triangular(
            base_annual_cf * (1 - spread),
            base_annual_cf,
            base_annual_cf * (1 + spread * 0.5),
            trials
        )
        discount_draws = rng.triangular(
            max(0.01, case.discount_rate - 0.02),
            case.discount_rate,
            case.discount_rate + 0.05,
            trials
        )

        years = np.arange(1, case.horizon_years + 1)
        discount_factors = (1 + discount_draws[:, None]) ** years[None, :]
        pv_returns = (annual_cf_draws[:, None] / discount_factors).sum(axis=1)
        npv_draws = pv_returns - investment_draws

        p10, p50, p90 = np.percentile(npv_draws, [10, 50, 90])
        prob_profitable = float((npv_draws > 0).mean())

        hist_counts, hist_edges = np.histogram(npv_draws, bins=20)

        def npv_at(investment: float, annual_cf: float, rate: float) -> float:
            flows = [-investment] + [annual_cf] * case.horizon_years
            return sum(cf / ((1 + rate) ** t) for t, cf in enumerate(flows))

        base_npv = npv_at(case.investment, base_annual_cf, case.discount_rate)

        tornado_inputs = [
            (
                "Investment Cost (±20%)",
                npv_at(case.investment * 1.2, base_annual_cf, case.discount_rate),
                npv_at(case.investment * 0.8, base_annual_cf, case.discount_rate),
            ),
            (
                "Annual Return (±20%)",
                npv_at(case.investment, base_annual_cf * 0.8, case.discount_rate),
                npv_at(case.investment, base_annual_cf * 1.2, case.discount_rate),
            ),
            (
                "Discount Rate (±3pt)",
                npv_at(case.investment, base_annual_cf, case.discount_rate + 0.03),
                npv_at(case.investment, base_annual_cf, max(0.01, case.discount_rate - 0.03)),
            ),
        ]

        tornado = [
            {
                "variable": label,
                "downside_npv": round(downside, 2),
                "upside_npv": round(upside, 2),
                "swing": round(abs(upside - downside), 2),
            }
            for label, downside, upside in tornado_inputs
        ]
        tornado.sort(key=lambda row: row["swing"], reverse=True)

        return {
            "trials": trials,
            "spread": round(spread, 2),
            "base_npv": round(base_npv, 2),
            "p10": round(float(p10), 2),
            "p50": round(float(p50), 2),
            "p90": round(float(p90), 2),
            "probability_profitable": round(prob_profitable, 4),
            "hist_counts": hist_counts.tolist(),
            "hist_edges": [round(e, 2) for e in hist_edges.tolist()],
            "tornado": tornado,
        }
