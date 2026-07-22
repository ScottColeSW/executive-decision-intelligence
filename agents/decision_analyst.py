from typing import Any, Dict, Optional
from data.cases import DecisionCase

class DecisionAnalyst:
    """
    Generates critical alternative perspectives to challenge cognitive bias and sunk-cost fallacies.
    Grounded in the same Monte Carlo simulation shown in the Risk & Uncertainty tab, so the
    challenge cites real simulated numbers rather than a restated abstract volatility score.
    """

    def analyze(
        self,
        case: DecisionCase,
        recommendation_result: Dict[str, Any],
        uncertainty_result: Dict[str, Any],
        monte_carlo: Optional[Dict[str, Any]] = None,
    ) -> str:
        decision = recommendation_result.get("decision", "DEFER")
        confidence = recommendation_result.get("confidence", 70)
        volatility = uncertainty_result.get("volatility_index", 0.3)

        if monte_carlo:
            downside_line = (
                f"In the worst **10%** of {monte_carlo['trials']:,} simulated outcomes, NPV falls to "
                f"**${monte_carlo['p10']:,.0f}**, and only **{monte_carlo['probability_profitable'] * 100:.0f}%** "
                f"of simulated scenarios stay profitable at all. See the Risk & Uncertainty tab for the full distribution."
            )
        else:
            downside_line = (
                f"Volatility is indexed at **{volatility * 100:.0f}%**. If project delivery slips by even 30 days, "
                "simple interest loops on physical overhead will challenge cash preservation."
            )

        analysis_text = f"""### 🛡️ Red-Team Challenge Report: '{case.title}'

The quantitative recommendation advises to **{decision}** with a confidence score of **{confidence}%**.

#### **Alternative Perspective & Dialectical Challenge:**
1. **The Core Fragility:** {downside_line}
2. **Behavioral Exposure:** {"Severe sunk-cost exposure identified. The temptation to throw good money after bad is high here." if case.sunk_costs > 0 else "Low legacy friction. Proceed based on clean metrics."}
3. **Rate Sensitivity:** This recommendation assumes a **{case.discount_rate * 100:.1f}%** hurdle rate ({case.discount_rate_basis}). A materially higher cost of capital would erode the case faster than any operational risk on this list.
4. **Actionable Directive:** Do not write a blank check. Establish hard monthly milestones. If key indicators slip below 80% targets within the first 60 days, trigger a pivot loop immediately."""

        return analysis_text
