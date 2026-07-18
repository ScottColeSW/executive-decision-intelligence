class DecisionBriefEngine:

    def generate(self, case, recommendation, ai_analysis):

        return {

            "decision":
                case.question,

            "recommendation":
                recommendation["decision"],

            "confidence":
                recommendation["confidence"],

            "key_dependencies":
                case.assumptions,

            "ai_challenge":
                ai_analysis["challenge"],

            "executive_questions":
                [
                    ai_analysis["executive_question"]
                ]

        }