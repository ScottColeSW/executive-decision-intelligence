import streamlit as st

from data.cases import DecisionCase
from ui.executive_brief import run_analysis, render_analysis, render_footer

st.set_page_config(
    page_title="Ask EDI",
    page_icon="❓",
    layout="wide"
)

st.title("❓ Ask EDI a Question")
st.caption(
    "Bring your own decision. Fill in the numbers you already know — EDI runs the exact "
    "same financial, uncertainty, governance, and provenance pipeline it runs on the "
    "built-in cases, on your live inputs."
)

st.divider()

with st.form("custom_case_form"):

    title = st.text_input(
        "Decision Title",
        placeholder="e.g. Should we lease a second location?"
    )

    question = st.text_area(
        "Business Question",
        placeholder="State the decision as a single yes/no question."
    )

    company = st.text_area(
        "Business Context",
        placeholder="A sentence or two about the business and the situation driving this decision."
    )

    col1, col2, col3 = st.columns(3)

    with col1:
        investment = st.number_input(
            "Fresh Capital Required ($)", min_value=0.0, value=10000.0, step=500.0
        )
        sunk_costs = st.number_input(
            "Sunk Costs Already Spent ($)", min_value=0.0, value=0.0, step=500.0
        )

    with col2:
        expected_return = st.number_input(
            "Total Expected Return ($, over the full horizon)", min_value=0.0, value=20000.0, step=500.0
        )
        horizon_years = st.number_input(
            "Time Horizon (years)", min_value=1, max_value=20, value=3, step=1
        )

    with col3:
        discount_rate = st.number_input(
            "Discount / Hurdle Rate", min_value=0.0, max_value=1.0, value=0.08, step=0.01, format="%.2f"
        )
        discount_rate_basis = st.text_input(
            "Where does that rate come from?",
            placeholder="e.g. our bank's current small-business loan rate, or a guess if unsure",
            help="EDI treats the discount rate as a stated, auditable assumption — not a hidden constant. "
                 "If you're not sure, say so; that's more honest than silence."
        )

    assumptions_raw = st.text_area(
        "Key Assumptions (one per line)",
        placeholder="Demand remains steady through the year\nStaffing can be secured within 30 days"
    )

    submitted = st.form_submit_button("Run EDI Analysis", type="primary")

if submitted:
    if not title.strip() or not question.strip() or investment <= 0:
        st.error("A title, a business question, and a nonzero investment amount are required.")
    else:
        assumptions = [line.strip() for line in assumptions_raw.splitlines() if line.strip()]

        custom_case = DecisionCase(
            case_id=f"CUSTOM-{abs(hash(title)) % 10000:04d}",
            title=title.strip(),
            question=question.strip(),
            company=company.strip() or "A small or growth-stage business evaluating a discretionary capital decision.",
            investment=investment,
            expected_return=expected_return,
            sunk_costs=sunk_costs,
            horizon_years=int(horizon_years),
            discount_rate=discount_rate,
            discount_rate_basis=(
                discount_rate_basis.strip()
                or "Not specified by the user at intake — treat this rate as an unvalidated placeholder, not a sourced figure."
            ),
            assumptions=assumptions,
            current_state="Submitted live via the Ask EDI intake form — no pre-scripted narrative for this scenario.",
            ai_workflow=(
                "EDI ran its full standard pipeline (financial analysis, Monte Carlo simulation, "
                "red-team challenge, governance review, provenance trace) against these user-supplied numbers."
            )
        )

        with st.spinner("EDI is analyzing your decision..."):
            st.session_state["custom_analysis"] = run_analysis(custom_case)

analysis = st.session_state.get("custom_analysis")

if analysis:
    st.divider()
    st.subheader(f"Analysis: {analysis['case'].title}")
    st.info(analysis["case"].question)
    render_analysis(analysis)

render_footer()
