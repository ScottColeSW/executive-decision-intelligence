from models.decision_case import DecisionCase


CAPEX = DecisionCase(

    id="001",

    title="Capital Investment",

    company="Apex Manufacturing",

    question="Should Apex invest $2.4M in robotic automation?",

    investment=2_400_000,

    expected_return=900_000,

    assumptions=[

        "Labor savings are achievable",

        "Demand remains stable",

        "Implementation completes within 12 months"

    ],

    risks=[

        "Technology adoption",

        "Schedule delays"

    ]

)


SUNK_COST = DecisionCase(

    id="002",

    title="Strategic Exit",

    company="Apex Manufacturing",

    question="Should Product Phoenix be cancelled?",

    investment=8_000_000,

    expected_return=-1_200_000,

    risks=[

        "Executive bias",

        "Customer perception"

    ]

)


AI = DecisionCase(

    id="003",

    title="AI Transformation",

    company="Apex Manufacturing",

    question="Should Apex invest $450K in AI customer support?",

    investment=450_000,

    expected_return=300_000,

    risks=[

        "Low adoption",

        "Operational readiness"

    ]

)


CASES = {

    CAPEX.title: CAPEX,

    SUNK_COST.title: SUNK_COST,

    AI.title: AI

}