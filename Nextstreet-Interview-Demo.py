"""
Executive Decision Intelligence (EDI)

Confident decisions for uncertain times.

Version: 0.1 Demo
"""

import streamlit as st
import requests

from data.cases import CASES
from ollama_client import OLLAMA_HOST
from ui.executive_brief import run_analysis, render_analysis, render_footer

# ---------------------------------------------------------
# Helpers
# ---------------------------------------------------------

def ollama_status():
    """Check whether the configured Ollama server is running."""
    try:
        response = requests.get(
            f"{OLLAMA_HOST}/api/tags",
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

    st.caption(f"Host: {OLLAMA_HOST}")

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

    st.metric(
        "Discount Rate Assumed",
        f"{case.discount_rate * 100:.1f}%"
    )

st.caption(f"📊 **Rate assumption:** {case.discount_rate_basis}")

# ---------------------------------------------------------
# Current State vs. Proposed AI-Supported Workflow
# ---------------------------------------------------------

if case.current_state or case.ai_workflow:

    st.divider()

    cs_col, fs_col = st.columns(2)

    with cs_col:
        st.subheader("📍 Current State")
        st.caption("How this decision gets made today, without EDI.")
        st.markdown(case.current_state)

    with fs_col:
        st.subheader("🤖 Proposed AI-Supported Workflow")
        st.caption("Where AI enters the process — and what stays human-led.")
        st.markdown(case.ai_workflow)

# ---------------------------------------------------------
# Analyze Button
# ---------------------------------------------------------

st.divider()

if st.button("Analyze Decision", type="primary"):

    with st.spinner("EDI is analyzing the decision..."):
        st.session_state["analysis"] = run_analysis(case)

analysis = st.session_state.get("analysis")

if analysis and analysis["case"].case_id == case.case_id:
    render_analysis(analysis)

render_footer()
