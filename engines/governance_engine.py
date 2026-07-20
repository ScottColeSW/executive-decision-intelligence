from typing import List
from data.cases import DecisionCase

class GovernanceEngine:
    """
    Ensures SME projects respect strategic business policies, budget constraints, 
    and classic risk-mitigation criteria.
    """
    
    def review(self, case: DecisionCase) -> List[str]:
        checks = []
        
        # Policy Rule 1: Investment Limits
        if case.investment > 100000.0:
            checks.append("⚠️ Budget Cap Flag: Capital allocation exceeds standard discretionary thresholds ($100k). Requires multi-partner signature.")
        else:
            checks.append("✅ Budget Check: Investment capital falls within standard SME working limits.")
            
        # Policy Rule 2: Decoupled Sunk Costs
        if case.sunk_costs > 0:
            checks.append(f"✅ Governance Standard: Emotional sunk costs (${case.sunk_costs:,.2f}) successfully flagged and decoupled from future planning math.")
            
        # Policy Rule 3: Time Horizon Check
        if case.horizon_years > 5:
            checks.append("⚠️ Horizon Risk: Projections past 5 years introduce high estimation risk. Requesting annual reviews.")
        else:
            checks.append("✅ Lifecycle Alignment: Horizon parameters sit inside reliable, near-term modeling buffers.")
            
        return checks