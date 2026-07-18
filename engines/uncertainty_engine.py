"""
EDI Uncertainty Engine

Evaluates how sensitive a decision is to changing assumptions.
"""


from dataclasses import dataclass


@dataclass
class UncertaintyScenario:

    name: str

    adjustments: dict

    outcome: str

    recommendation: str



class UncertaintyEngine:


    def analyze(self, case, recommendation):

        scenarios = []


        # Downside scenario
        downside_return = case.expected_return * 0.7

        if downside_return < case.investment:
            downside_decision = "DEFER"
        else:
            downside_decision = "INVEST"


        scenarios.append(

            UncertaintyScenario(

                name="Downside Case",

                adjustments={
                    "expected_return": "-30%"
                },

                outcome=
                    f"Expected return: ${downside_return:,.0f}",

                recommendation=downside_decision

            )

        )


        # Base case

        scenarios.append(

            UncertaintyScenario(

                name="Base Case",

                adjustments={
                    "expected_return": "Current assumption"
                },

                outcome=
                    f"Expected return: ${case.expected_return:,.0f}",

                recommendation=
                    recommendation["decision"]

            )

        )


        return {

            "confidence":

                recommendation["confidence"],


            "decision_stability":

                "Stable"
                if all(
                    s.recommendation == recommendation["decision"]
                    for s in scenarios
                )
                else "Sensitive",


            "scenarios":

                scenarios,


            "breaking_points":

                [
                    "Expected benefits decrease materially",
                    "Implementation timeline extends"
                ]

        }