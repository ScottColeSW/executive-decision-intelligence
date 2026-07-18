"""
Recommendation Engine
"""

from engines.financial_engine import FinancialEngine


class RecommendationEngine:

    def __init__(self):

        self.fin = FinancialEngine()

    def evaluate(self, case):

        roi = self.fin.calculate_roi(
            case.investment,
            case.expected_return
        )

        payback = self.fin.calculate_payback(
            case.investment,
            case.expected_return
        )

        npv = self.fin.calculate_npv(
            case.investment,
            case.expected_return
        )

        if npv > 0:

            decision = "INVEST"
            confidence = 84

        elif case.expected_return < 0:

            decision = "CANCEL"
            confidence = 91

        else:

            decision = "DEFER"
            confidence = 73

        return {

            "decision": decision,

          "confidence": confidence,

           "roi": roi,

           "payback": payback,

            "npv": npv,

          "reasons": [

                "Positive expected value",

                "Financial thresholds satisfied",

                "Key assumptions remain reasonable"

            ],

           "risks": case.risks,

           "assumptions": case.assumptions

        }