"""
Governance Engine
"""


class GovernanceEngine:

    def review(self, case):

        return {

            "required_approvals": [

                "COO",

                "CFO",

                "Capital Investment Committee"

            ],

            "human_approval": True,

            "audit_required": True

        }