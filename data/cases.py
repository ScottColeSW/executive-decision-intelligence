"""
Executive Decision Intelligence
Demo Decision Cases

Creates DecisionCase domain objects.
"""

from models.decision_case import DecisionCase


CASES = {

    "Capital Investment": DecisionCase(

        id="EDI-001",

        title="Apex Manufacturing Automation Investment",

        company="Apex Manufacturing",

        question=
        "Should Apex invest $2.4M in robotic assembly automation?",

        investment=2_400_000,

        expected_return=3_180_000,

        assumptions=[

            "Labor savings are achievable",

            "Demand remains stable",

            "Implementation completes within 12 months"

        ],

        risks=[

            "Technology adoption delays",

            "Implementation cost overruns",

            "Lower than expected labor savings"

        ]

    ),


    "Sunk Cost Review": DecisionCase(

        id="EDI-002",

        title="Product Phoenix Strategic Exit",

        company="Apex Manufacturing",

        question=
        "Should Apex continue investing in Product Phoenix?",

        investment=8_000_000,

        expected_return=-1_200_000,

        assumptions=[

            "Past spending is unrecoverable",

            "Future value matters more than historical cost"

        ],

        risks=[

            "Executive attachment to prior investment",

            "Opportunity cost",

            "Market uncertainty"

        ]

    ),


    "AI Transformation": DecisionCase(

        id="EDI-003",

        title="Customer Support AI Initiative",

        company="Apex Manufacturing",

        question=
        "Should Apex invest $450K in AI-powered customer support?",

        investment=450_000,

        expected_return=300_000,

        assumptions=[

            "Employees adopt the platform",

            "Customer experience remains acceptable",

            "Governance controls are implemented"

        ],

        risks=[

            "Low adoption",

            "Customer satisfaction impact",

            "AI reliability concerns"

        ]

    )
}