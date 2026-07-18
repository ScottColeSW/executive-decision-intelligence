"""
Executive Decision Intelligence (EDI)

Confident decisions for uncertain times.

Version: 0.1 Demo
"""

import streamlit as st
import requests

from data.cases import CASES
from engines.recommendation_engine import RecommendationEngine
from engines.governance_engine import GovernanceEngine
from provenance.tracker import ProvenanceTracker
from agents.decision_analyst import DecisionAnalyst
from engines.uncertainty_engine import UncertaintyEngine
from ollama_client import ask_ollama

recommendation_engine = RecommendationEngine()
governance_engine = GovernanceEngine()
provenance_tracker = ProvenanceTracker()
decision_analyst = DecisionAnalyst()
uncertainty_engine = UncertaintyEngine()

# ---------------------------------------------------------
# Helpers
# ---------------------------------------------------------

def ollama_status():
    """Check whether the local Ollama server is running."""
    try:
        response = requests.get(
            "http://localhost:11434/api/tags",
            timeout=2
        )

        if response.status_code == 200:
            return True

    except Exception:
        pass

    return False


# ---------------------------------------------------------
# Page Setup
# ---------------------------------------------------------

st.set_page_config(
    page_title="Executive Decision Intelligence",
    page_icon="📈",
    layout="wide"
)

# ---------------------------------------------------------
# Header
# ---------------------------------------------------------

st.title("Executive Decision Intelligence")
st.subheader("Confident decisions for uncertain times.")

st.divider()

# ---------------------------------------------------------
# Sidebar
# ---------------------------------------------------------

with st.sidebar:

    st.header("Decision Cases")

    selected_case = st.selectbox(
        "Choose a Scenario",
        list(CASES.keys())
    )

    st.divider()

    st.header("AI Status")

    if ollama_status():
        st.success("🟢 Ollama Connected")
        st.caption("Model: llama3.1:8b")
    else:
        st.error("🔴 Ollama Offline")

# ---------------------------------------------------------
# Load Selected Case
# ---------------------------------------------------------

case = CASES[selected_case]

left, right = st.columns([2, 1])

# ---------------------------------------------------------
# Executive Brief
# ---------------------------------------------------------

with left:

    st.header(case.title)

    st.subheader("Business Question")

    st.info(case.question)

    st.subheader("Business Context")

    st.write(case.company)

# ---------------------------------------------------------
# Metrics
# ---------------------------------------------------------

with right:

    st.metric(
        "Investment",
        f"${case.investment:,.0f}"
    )

    st.metric(
        "Expected Return",
        f"${case.expected_return:,.0f}"
    )

# ---------------------------------------------------------
# Analyze Button
# ---------------------------------------------------------

st.divider()

if st.button("Analyze Decision", type="primary"):

    with st.spinner("EDI is analyzing the decision..."):
    
        result = recommendation_engine.evaluate(case)
        
        uncertainty = uncertainty_engine.analyze(
            case,
            result
        )

        ai_analysis = decision_analyst.analyze(
            case,
            result,
            uncertainty
        )

        governance = governance_engine.review(case)

        prompt = f"""
You are EDI Analyst.

Provide an executive recommendation.

Business Question:
{case.question}

Recommendation:
{result['decision']}

Confidence:
{result['confidence']}

Reasons:
{result['reasons']}

Risks:
{result['risks']}

Write a concise executive summary suitable for a CEO.
Maximum 200 words.
"""

        ai_summary = ask_ollama(prompt)

        provenance = provenance_tracker.create(
            engine="RecommendationEngine",
            function="evaluate_case"
        )

    st.divider()

    st.header("Executive Recommendation")

    decision = result["decision"]

    if decision == "INVEST":
        st.success(f"# {decision}")
    elif decision == "DEFER":
        st.warning(f"# {decision}")
    else:
        st.error(f"# {decision}")

    st.metric(
        "Confidence",
        f"{result['confidence']}%"
    )

    tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs(
        [
            "Summary",
            "AI Challenge",
            "Risks",
            "Governance",
            "Provenance",
            "Executive Brief"
        ]
    )

    # ---------------------------------------------------------
    # Summary
    # ---------------------------------------------------------

    with tab1:

        st.subheader("EDI Analyst Summary")

        st.write(ai_summary)

        st.subheader("Primary Reasons")

        for reason in result["reasons"]:
            st.write(f"✅ {reason}")


    # ---------------------------------------------------------
    # AI Challenge
    # ---------------------------------------------------------

    with tab2:

        st.subheader("AI Decision Challenge")

        st.write(
            ai_analysis
        )

    # ---------------------------------------------------------
    # Risks
    # ---------------------------------------------------------

    with tab3:

        st.subheader("Key Risks")

        for risk in result["risks"]:
            st.warning(risk)

    # ---------------------------------------------------------
    # Governance
    # ---------------------------------------------------------

    with tab4:

        st.subheader("Governance Review")

        for item in governance:
            st.write(f"• {item}")

    # ---------------------------------------------------------
    # Provenance
    # ---------------------------------------------------------

    with tab5:

        st.subheader("Decision Provenance")

        st.success("Decision analysis trace recorded")

        st.write("**Engine**")
        st.write(provenance["engine"])

        st.write("**Function**")
        st.write(provenance["function"])
    
        st.write("**Version**")
        st.write(provenance["version"])

        st.write("**Timestamp**")
        st.write(provenance["timestamp"])
        
    # ---------------------------------------------------------
    # Executive Brief
    # ---------------------------------------------------------

    with tab6:

        st.subheader("Executive Brief")

        st.write(ai_summary)

        st.subheader("Primary Reasons")

        for reason in result["reasons"]:
            st.write(f"✅ {reason}")        
        

st.divider()

st.caption("EDI v0.1 • Governance-first AI for Executive Decision Intelligence")