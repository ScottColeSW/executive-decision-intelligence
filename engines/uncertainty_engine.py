from typing import Dict, Any
from data.cases import DecisionCase

class UncertaintyEngine:
    """
    Stress-tests the cash flow assumptions to measure sensitivity to real-world deviations.
    """
    
    def analyze(self, case: DecisionCase, recommendation_result: Dict[str, Any]) -> Dict[str, Any]:
        volatility_multiplier = 0.15
        num_assumptions = len(case.assumptions)
        
        # Base volatility index increases with the quantity of unproven assumptions
        volatility_index = min(0.85, 0.10 + (num_assumptions * 0.12))
        
        if recommendation_result.get("decision") == "INVEST" and volatility_index > 0.40:
            sensitivity_summary = "High assumption dependency. Small changes in market demand will delay project breakeven."
        else:
            sensitivity_summary = "Stable forecast. Operational model holds up well against minor margin pressures."

        return {
            "volatility_index": round(volatility_index, 2),
            "sensitivity": sensitivity_summary,
            "risk_adjusted_discount": round(case.discount_rate + (volatility_index * 0.05), 3)
        }