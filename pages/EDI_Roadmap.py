import streamlit as st

from ui.executive_brief import render_footer

st.set_page_config(
    page_title="EDI Roadmap",
    page_icon="🧭"
)


st.title("🚀 Executive Decision Intelligence Roadmap")

st.caption(
    "From decision analysis prototype to enterprise decision operating system"
)


st.divider()


st.subheader("Vision")

st.write(
    """
Executive Decision Intelligence helps leaders make confident decisions
under uncertainty by combining financial analysis, AI reasoning,
scenario testing, and governance controls.
"""
)

st.subheader("Long-Term Goals")

st.info(
    """
EDI becomes the organization's trusted decision partner:

Not replacing executives.

Helping executives see what they cannot easily see.
"""
)

st.divider()


st.subheader("Product Evolution")


roadmap = [
    (
        "V0.1 — Decision Analysis Foundation",
        [
            "Financial evaluation engine",
            "ROI, NPV, payback analysis",
            "Recommendation generation",
            "Governance and provenance tracking"
        ]
    ),

    (
        "V0.2 — AI Decision Analyst",
        [
            "Challenge assumptions",
            "Identify hidden risks",
            "Generate executive questions",
            "Stress test recommendations"
        ]
    ),

    (
        "V0.3 — Decision Workspace",
        [
            "Create new decisions",
            "Editable business context",
            "Assumptions and constraints",
            "Scenario comparison"
        ]
    ),

    (
        "V0.4 — Enterprise Governance",
        [
            "Approval workflows",
            "Decision audit trails",
            "Policy enforcement",
            "Human-in-the-loop controls"
        ]
    ),

    (
        "V1.0 — Organizational Decision Intelligence",
        [
            "Decision memory",
            "Historical pattern recognition",
            "Cross-project learning",
            "Executive intelligence dashboard"
        ]
    )
]


for version, items in roadmap:

    with st.container():

        st.subheader(version)

        for item in items:
            st.write("✓ " + item)

        st.divider()

render_footer()
