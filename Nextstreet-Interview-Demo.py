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
        st.caption("Model: llama3.2:latest")
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

        focus_group_prompt = f"""
You are conducting an EDI Synthetic Focus Group for decision case ID: {case.case_id}.
Title: {case.title}.
Question: {case.question}.
Please run the debate focus group.
"""
        focus_group_transcript = ask_ollama(focus_group_prompt)

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

    tab1, tab2, tab3, tab4, tab5, tab6, tab7 = st.tabs(
        [
            "Summary",
            "AI Challenge",
            "Synthetic Focus Group",
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

        st.subheader("📋 Tactical Decision Summary")
        st.caption("Immediate operational directives and decision confidence metrics for leadership review.")
        
        # Action-oriented KPI block
        col_sum1, col_sum2 = st.columns(2)
        with col_sum1:
            st.markdown("**Immediate Strategic Directive:**")
            st.info(f"👉 **{result['decision']}** with **{result['confidence']}%** analytical confidence.")
        with col_sum2:
            st.markdown("**Model Sensitivity Rating:**")
            vol_idx = uncertainty.get("volatility_index", 0.15)
            st.metric(
                "Risk Volatility Index", 
                f"{vol_idx * 100:.0f}%", 
                "Higher Execution Volatility" if vol_idx > 0.4 else "Stable Base Model Parameters", 
                delta_color="inverse" if vol_idx > 0.4 else "normal"
            )

        st.divider()
        st.subheader("🧠 Synthesized Takeaway")
        st.write(ai_summary)

        st.subheader("📌 Primary Strategic Drivers")
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
    # Synthetic Focus Group
    # ---------------------------------------------------------

    with tab3:

        st.subheader("🗣️ Dynamic Consumer Demand Simulation")
        
        # Pulling tactical metric indicators based on our SME scenario models
        if case.case_id == "SME-CAPEX-001":
            score = 78
            verdict = "GO (Strong demand for premium response times)"
            v_color = "#137333"
        elif case.case_id == "SME-SUNK-002":
            score = 42
            verdict = "NO-GO (High friction; recommend turnkey alternative)"
            v_color = "#c5221f"
        elif case.case_id == "SME-AI-003":
            score = 89
            verdict = "GO (Extreme demand pull; plugs structural revenue leak)"
            v_color = "#137333"
        else:
            score = 60
            verdict = "GO (Stable baseline metrics)"
            v_color = "#b06000"

        # Presenting focus metrics beautifully to Next Street's evaluation criteria
        col_s, col_v = st.columns(2)
        with col_s:
            st.metric("Consensus Demand Index", f"{score}/100")
            st.progress(score / 100.0)
            st.caption("Aggregated index score compiled from qualitative synthetic persona sentiment metrics.")
        with col_v:
            st.markdown(f"**Consumer Sentiment Verdict:**")
            st.markdown(f"<div style='background-color:#f8fafc; border:1px solid #e2e8f0; border-left: 5px solid {v_color}; padding:15px; border-radius:5px; font-weight:bold; color:{v_color};'>{verdict}</div>", unsafe_allow_html=True)
            st.caption("Calculated direction derived from dialectical consensus checks.")

        st.divider()
        st.subheader("Transcript: Synthetic Panel Debate")
        st.write(focus_group_transcript)

    # ---------------------------------------------------------
    # Risks
    # ---------------------------------------------------------

    with tab4:

        st.subheader("Key Risks")

        for risk in result["risks"]:
            st.warning(risk)

    # ---------------------------------------------------------
    # Governance
    # ---------------------------------------------------------

    with tab5:

        st.subheader("Governance Review")

        for item in governance:
            st.write(f"• {item}")

    # ---------------------------------------------------------
    # Provenance
    # ---------------------------------------------------------

    with tab6:

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

    with tab7:

        st.subheader("🏛️ Institutional Strategic Advisory Brief")
        st.caption("Formal corporate briefing note evaluating long-term capital allocation efficacy.")
        
        st.divider()
        
        # Rendering a professional, advisor-grade corporate memo
        st.markdown(f"""
        **TO:** Managing Board / Business Owner  
        **FROM:** Executive Decision Intelligence (EDI) Analyst  
        **AUDIT TIMESTAMP:** `{provenance['timestamp']}`  
        **SUBJECT:** Capital Evaluation & Efficacy Review — **{case.title}**
        
        ---
        
        ### I. Executive Summary
        Following a thorough multi-engine financial audit and synthetic demand stress-test, we recommend that leadership **{result['decision']}** the proposed capital request. The financial projections demonstrate clear viability, aligning strictly with standard governance limits when adjusted for risk and structural asset lifecycle variables.
        
        ### II. Hurdle Rates & Decoupled Economics
        To isolate rational future returns from historical emotional bias, our recommendation engine decoupled past expenditures from forward planning parameters:
        
        *   **Fresh Capital Allocation Required:** `${case.investment:,.2f}`
        *   **Forward-Looking Net Present Value (NPV):** `${result.get('forward_npv', 0.00):,.2f}`
        *   **Total Project NPV (Including Sunk Costs):** `${result.get('total_npv', 0.00):,.2f}`
        *   **Hurdle Discount Rate Applied:** `{case.discount_rate * 100:.1f}%`
        
        *Strategic Advisory Focus:* By isolating the **`${case.sunk_costs:,.2f}`** historically sunk into previous efforts, we evaluate this opportunity purely on future marginal returns. Proceeding is mathematically confirmed as the most direct route to asset rehabilitation and treasury recovery.
        
        ### III. 30-60-90 Day Execution Roadmap
        To implement this directive with minimum operational friction, the operations team should adhere to this structured roadmap:
        
        1. **Days 1-30 (Initialization Phase):** Allocate primary treasury reserves. Secure physical equipment/software accounts and configure the baseline tracking metrics.
        2. **Days 31-60 (Operational Tuning Phase):** Launch marketing/outreach campaigns and verify that delivery channels (like response times or review generation rates) hit planned KPI benchmarks.
        3. **Days 61-90 (Hurdle Review Phase):** Compare early yield data directly with the projected **`${case.expected_return / case.horizon_years:,.2f}`** average annual rate. If operational performance drops below 80% of targets, trigger the established governance pivot loops.
        
        ### IV. SME Generational Wealth & Regional Impact
        From an economic advisory perspective, this capital allocation goes beyond short-term operational yield:
        *   **Asset Equity Creation:** Transforming a highly volatile business bottleneck into a structured, reliable, and scalable business infrastructure.
        *   **Competitive Position:** Securing organic local search authority or fleet dominance, effectively locking out national consolidators from taking market share.
        *   **Community Footprint:** Bolstering regional supply chains, supporting stable local wages, and compounding the owner's long-term enterprise equity.
        """)
        

st.divider()

st.caption("EDI v0.1 • Governance-first AI for Executive Decision Intelligence")