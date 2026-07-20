from typing import Dict, Any, List
from data.cases import DecisionCase

class RecommendationEngine:
    """
    Evaluates SME decisions by running standard discounted cash flows 
    side-by-side with behavioral heuristics.
    """
    
    def evaluate(self, case: DecisionCase) -> Dict[str, Any]:
        forward_investment = case.investment
        total_investment = case.investment + case.sunk_costs
        expected_return = case.expected_return
        horizon = case.horizon_years
        rate = case.discount_rate

        # Simple annualized cash flow projection
        annual_cf = expected_return / max(1, horizon)
        
        # Calculate NPV (Forward-looking: ignores sunk costs)
        forward_npv = -forward_investment + sum(
            annual_cf / ((1 + rate) ** t) for t in range(1, horizon + 1)
        )
        
        # Calculate NPV (Total project: drags in sunk costs)
        total_npv = -total_investment + sum(
            annual_cf / ((1 + rate) ** t) for t in range(1, horizon + 1)
        )

        reasons: List[str] = []
        risks: List[str] = []
        
        if forward_npv > 0:
            decision = "INVEST"
            reasons.append(
                f"Highly viable forward-looking NPV of ${forward_npv:,.2f} over a {horizon}-year horizon."
            )
            reasons.append(
                f"Calculated forward-looking performance bypasses emotional sunk-cost baggage."
            )
        elif forward_npv == 0:
            decision = "DEFER"
            reasons.append(
                "Marginal forward NPV. Recommendation is to pause allocation until pricing variables stabilize."
            )
        else:
            decision = "AVOID"
            reasons.append(
                f"Capital destructive forward-looking NPV (${forward_npv:,.2f}). Reject proposal."
            )

        if case.sunk_costs > 0:
            risks.append(
                f"Sunk Cost Bias: ${case.sunk_costs:,.2f} already spent may lead to emotional over-commitment."
            )
        
        if len(case.assumptions) > 0:
            for assumption in case.assumptions:
                risks.append(f"Assumption Sensitivity: {assumption}")
        else:
            risks.append("No clear assumptions logged. This creates model blindspots.")

        # Estimate model confidence
        base_confidence = 90 - (len(case.assumptions) * 6)
        if case.sunk_costs > case.investment * 2:
            base_confidence -= 10 # High emotional penalty
            
        confidence = max(45, min(95, base_confidence))

        return {
            "decision": decision,
            "confidence": confidence,
            "reasons": reasons,
            "risks": risks,
            "forward_npv": round(forward_npv, 2),
            "total_npv": round(total_npv, 2)
        }