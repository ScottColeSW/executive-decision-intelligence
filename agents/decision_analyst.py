from typing import Dict, Any
from data.cases import DecisionCase

class DecisionAnalyst:
    """
    Generates critical alternative perspectives to challenge cognitive bias and sunk-cost fallacies.
    """
    
    def analyze(self, case: DecisionCase, recommendation_result: Dict[str, Any], uncertainty_result: Dict[str, Any]) -> str:
        decision = recommendation_result.get("decision", "DEFER")
        confidence = recommendation_result.get("confidence", 70)
        volatility = uncertainty_result.get("volatility_index", 0.3)
        
        analysis_text = f"""### 🛡️ Red-Team Challenge Report: '{case.title}'

The quantitative recommendation advises to **{decision}** with a confidence score of **{confidence}%**. 

#### **Alternative Perspective & Dialectical Challenge:**
1. **The Core Fragility:** Volatility is indexed at **{volatility * 100:.0f}%**. If project delivery slips by even 30 days, simple interest loops on physical overhead will challenge cash preservation.
2. **Behavioral Exposure:** {"Severe sunk-cost exposure identified. The temptation to throw good money after bad is high here." if case.sunk_costs > 0 else "Low legacy friction. Proceed based on clean metrics."}
3. **Actionable Directive:** Do not write a blank check. Establish hard monthly milestones. If key indicators slip below 80% targets within the first 60 days, trigger a pivot loop immediately."""
        
        return analysis_text