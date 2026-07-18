class DecisionAnalyst:

    def analyze(
        self,
        case,
        recommendation,
        uncertainty
        ):

        return {
            "challenge":
                "Labor savings assumption appears optimistic",

            "hypothesis_tests":
                [
                  "What if revenue declines 20%?",
                  "What if costs increase 15%?"
                ],

            "executive_question":
                "What evidence supports the adoption timeline?"
        }