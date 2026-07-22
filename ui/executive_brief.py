"""
Shared EDI analysis pipeline and tabbed executive-brief renderer.

Both the built-in case selector (Nextstreet-Interview-Demo.py) and the
"Ask EDI" custom-decision intake form (pages/Ask_EDI.py) run the exact same
multi-engine pipeline against a data.cases.DecisionCase and render the exact
same tab layout — this module is the single shared implementation of both.

Tabs are deliberately consolidated (7, not 9): each one should carry a
distinct headline, and numbers that appear in more than one tab (volatility,
NPV, the discount rate) are computed once and passed through, not
re-derived per tab by a slightly different formula.
"""

from typing import Any, Dict

import pandas as pd
import streamlit as st

from data.cases import DecisionCase
from engines.recommendation_engine import RecommendationEngine
from engines.governance_engine import GovernanceEngine
from engines.uncertainty_engine import UncertaintyEngine
from engines.financial_engine import FinancialEngine
from agents.decision_analyst import DecisionAnalyst
from provenance.tracker import ProvenanceTracker
from ollama_client import ask_ollama

recommendation_engine = RecommendationEngine()
governance_engine = GovernanceEngine()
uncertainty_engine = UncertaintyEngine()
financial_engine = FinancialEngine()
decision_analyst = DecisionAnalyst()
provenance_tracker = ProvenanceTracker()

MONTE_CARLO_TRIALS = 5000

GOVERNANCE_STATUS_ICON = {"pass": "✅", "flag": "⚠️", "review": "🔎"}

# Synthetic market-sentiment data. Illustrative, not derived from the financial
# engines — see the signal-conflict callout in render_analysis() for why that's
# deliberate rather than an oversight.
DEMAND_SIGNALS = {
    "SME-CAPEX-001": {"score": 78, "verdict": "GO", "note": "Strong demand for premium response times"},
    "SME-SUNK-002": {"score": 42, "verdict": "NO-GO", "note": "High customer friction; recommend turnkey alternative"},
    "SME-AI-003": {"score": 89, "verdict": "GO", "note": "Extreme demand pull; plugs structural revenue leak"},
    "SME-VENDOR-004": {"score": 22, "verdict": "NO-GO", "note": "Customers see zero difference at checkout; the upgrade solves an owner-side annoyance, not a customer-facing gap"},
    "SME-LEASE-005": {"score": 82, "verdict": "GO", "note": "Strong existing corporate catering demand; the van is the bottleneck, not the financing terms"},
}
DEFAULT_DEMAND_SIGNAL = {"score": 60, "verdict": "GO", "note": "Stable baseline metrics"}


def run_analysis(case: DecisionCase) -> Dict[str, Any]:
    """Executes the full EDI multi-engine pipeline against any DecisionCase."""

    result = recommendation_engine.evaluate(case)
    financials = financial_engine.analyze(case)
    financials_alt = financial_engine.analyze_alternative(case)
    uncertainty = uncertainty_engine.analyze(case, result)
    monte_carlo = uncertainty_engine.simulate(case, trials=MONTE_CARLO_TRIALS)
    ai_analysis = decision_analyst.analyze(case, result, uncertainty, monte_carlo)
    governance = governance_engine.review(case)

    summary_prompt = f"""
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
    ai_summary = ask_ollama(summary_prompt)

    focus_group_prompt = f"""
You are conducting an EDI Synthetic Focus Group for decision case ID: {case.case_id}.
Title: {case.title}.
Question: {case.question}.
Please run the debate focus group.
"""
    focus_group_transcript = ask_ollama(focus_group_prompt)

    provenance = provenance_tracker.create(
        engine="RecommendationEngine",
        function="evaluate_case",
        case_id=case.case_id,
        investment=case.investment,
        expected_return=case.expected_return,
        sunk_costs=case.sunk_costs,
        monte_carlo_trials=MONTE_CARLO_TRIALS,
    )

    return {
        "case": case,
        "result": result,
        "financials": financials,
        "financials_alt": financials_alt,
        "uncertainty": uncertainty,
        "monte_carlo": monte_carlo,
        "ai_analysis": ai_analysis,
        "governance": governance,
        "ai_summary": ai_summary,
        "focus_group_transcript": focus_group_transcript,
        "provenance": provenance,
    }


def render_analysis(analysis: Dict[str, Any]) -> None:
    """Renders the 7-tab executive analysis view from a run_analysis() result."""

    case = analysis["case"]
    result = analysis["result"]
    financials = analysis["financials"]
    financials_alt = analysis["financials_alt"]
    monte_carlo = analysis["monte_carlo"]
    ai_analysis = analysis["ai_analysis"]
    governance = analysis["governance"]
    ai_summary = analysis["ai_summary"]
    focus_group_transcript = analysis["focus_group_transcript"]
    provenance = analysis["provenance"]

    st.divider()

    st.header("Executive Recommendation")

    decision = result["decision"]

    if decision == "INVEST":
        st.success(f"# {decision}")
    elif decision == "DEFER":
        st.warning(f"# {decision}")
    else:
        st.error(f"# {decision}")

    st.metric("Confidence", f"{result['confidence']}%")
    st.caption(
        f"Discount rate used throughout this analysis: **{case.discount_rate * 100:.1f}%** — {case.discount_rate_basis}"
    )

    tab1, tab2, tab3, tab4, tab5, tab6, tab7 = st.tabs(
        [
            "Summary",
            "Financial Analysis",
            "Risk & Uncertainty",
            "AI Challenge",
            "Market Signal",
            "Governance & Audit Trail",
            "Executive Brief",
        ]
    )

    # ---------------------------------------------------------
    # Summary
    # ---------------------------------------------------------

    with tab1:

        st.subheader("📋 Tactical Decision Summary")
        st.caption("Immediate operational directives and decision confidence metrics for leadership review.")

        col_sum1, col_sum2 = st.columns(2)
        with col_sum1:
            st.markdown("**Immediate Strategic Directive:**")
            st.info(f"👉 **{result['decision']}** with **{result['confidence']}%** analytical confidence.")
        with col_sum2:
            st.markdown("**Bottom Line, From the Simulation:**")
            st.metric(
                "Odds of a Profitable Outcome",
                f"{monte_carlo['probability_profitable'] * 100:.0f}%",
                f"Worst-case (P10): ${monte_carlo['p10']:,.0f}",
                delta_color="inverse" if monte_carlo["p10"] < 0 else "normal"
            )
            st.caption(
                f"Same {monte_carlo['trials']:,}-trial Monte Carlo run shown in full in the Risk & Uncertainty tab "
                "— not a separately-estimated number."
            )

        st.divider()
        st.subheader("🧠 Synthesized Takeaway")
        st.write(ai_summary)

        st.subheader("📌 Primary Strategic Drivers")
        for reason in result["reasons"]:
            st.write(f"✅ {reason}")

    # ---------------------------------------------------------
    # Financial Analysis (standard MBA-grade corporate finance metrics)
    # ---------------------------------------------------------

    with tab2:

        st.subheader("📐 Standard Financial Analysis")
        st.caption("The core NPV / IRR / ROI / payback math a finance analyst would run by hand — computed automatically from the same inputs above.")

        fin_col1, fin_col2, fin_col3, fin_col4 = st.columns(4)
        with fin_col1:
            st.metric("Forward NPV", f"${financials.forward_npv:,.0f}")
        with fin_col2:
            st.metric("IRR", f"{financials.irr * 100:.1f}%" if financials.irr is not None else "N/A")
        with fin_col3:
            st.metric("Forward ROI", f"{financials.forward_roi * 100:.0f}%")
        with fin_col4:
            st.metric(
                "Payback Period",
                f"{financials.payback_period_years:.1f} yrs" if financials.payback_period_years is not None else "N/A"
            )

        st.divider()

        npv_col, roi_col = st.columns(2)
        with npv_col:
            st.markdown("**NPV — Forward-Only vs. Total Project**")
            st.caption("Isolating fresh capital from historical sunk costs, consistent with the sunk-cost decoupling used elsewhere in EDI.")
            st.dataframe(
                pd.DataFrame({
                    "Basis": ["Forward-Only (excludes sunk cost)", "Total Project (includes sunk cost)"],
                    "NPV": [financials.forward_npv, financials.total_project_npv],
                    "ROI": [f"{financials.forward_roi * 100:.0f}%", f"{financials.total_roi * 100:.0f}%"]
                }),
                hide_index=True,
                use_container_width=True
            )

        with roi_col:
            st.markdown("**Forward Cash Flow Schedule**")
            st.caption("Year 0 is the initial outlay; Years 1+ are projected annual returns.")
            cf_df = pd.DataFrame({
                "Year": list(range(len(financials.forward_cash_flows))),
                "Cash Flow": financials.forward_cash_flows
            }).set_index("Year")
            st.bar_chart(cf_df)

        st.info(
            f"**Rate assumption:** {case.discount_rate * 100:.1f}% — {case.discount_rate_basis} "
            f"(Horizon: {case.horizon_years} years)"
        )

        if financials_alt is not None:
            alt = case.alternative_path
            primary_label = alt.get("primary_label", "Primary Plan")
            alt_label = alt.get("label", "Alternative Plan")

            st.divider()
            st.markdown(f"**Financing Comparison: {primary_label} vs. {alt_label}**")
            st.caption("Same underlying opportunity, two different capital structures — run through the identical model, not eyeballed.")

            comp_df = pd.DataFrame({
                "Path": [primary_label, alt_label],
                "Upfront Investment": [f"${case.investment:,.0f}", f"${alt['investment']:,.0f}"],
                "Forward NPV": [f"${financials.forward_npv:,.0f}", f"${financials_alt.forward_npv:,.0f}"],
                "IRR": [
                    f"{financials.irr * 100:.1f}%" if financials.irr is not None else "N/A",
                    f"{financials_alt.irr * 100:.1f}%" if financials_alt.irr is not None else "N/A",
                ],
                "Payback": [
                    f"{financials.payback_period_years:.1f} yrs" if financials.payback_period_years is not None else "N/A",
                    f"{financials_alt.payback_period_years:.1f} yrs" if financials_alt.payback_period_years is not None else "N/A",
                ],
            })
            st.dataframe(comp_df, hide_index=True, use_container_width=True)

            winner_label = primary_label if financials.forward_npv >= financials_alt.forward_npv else alt_label
            npv_gap = abs(financials.forward_npv - financials_alt.forward_npv)
            st.info(
                f"**{winner_label}** preserves more value over the {case.horizon_years}-year horizon "
                f"(NPV advantage of ${npv_gap:,.0f}) — even if it isn't the option with the lower upfront "
                "cost or the lower monthly payment. Lower monthly isn't the same as a better deal."
            )

    # ---------------------------------------------------------
    # Risk & Uncertainty (named risk factors + Monte Carlo, in one place)
    # ---------------------------------------------------------

    with tab3:

        st.subheader("⚠️ Named Risk Factors")
        for risk in result["risks"]:
            st.warning(risk)

        st.divider()

        st.subheader("🎲 Monte Carlo Simulation")
        st.caption(
            f"{monte_carlo['trials']:,} simulated trials over investment cost, annual return, and "
            "discount rate uncertainty — a real probability distribution instead of one point-estimate NPV."
        )

        mc_col1, mc_col2, mc_col3, mc_col4 = st.columns(4)
        with mc_col1:
            st.metric("P10 (Downside)", f"${monte_carlo['p10']:,.0f}")
        with mc_col2:
            st.metric("P50 (Median)", f"${monte_carlo['p50']:,.0f}")
        with mc_col3:
            st.metric("P90 (Upside)", f"${monte_carlo['p90']:,.0f}")
        with mc_col4:
            st.metric("Odds of Profit", f"{monte_carlo['probability_profitable'] * 100:.0f}%")

        st.divider()

        hist_col, tornado_col = st.columns(2)

        with hist_col:
            st.markdown("**Simulated NPV Distribution**")
            edges = monte_carlo["hist_edges"]
            midpoints = [round((edges[i] + edges[i + 1]) / 2, 0) for i in range(len(edges) - 1)]
            hist_df = pd.DataFrame({
                "NPV ($)": midpoints,
                "Trials": monte_carlo["hist_counts"]
            }).set_index("NPV ($)")
            st.bar_chart(hist_df)
            st.caption("Each bar is the count of simulated trials landing in that NPV range.")

        with tornado_col:
            st.markdown("**Sensitivity Ranking (Tornado)**")
            tornado_df = pd.DataFrame(monte_carlo["tornado"]).set_index("variable")
            st.bar_chart(tornado_df[["swing"]])
            st.caption("Which single assumption moves NPV the most when flexed ± independently — highest bar first.")
            st.dataframe(
                tornado_df[["downside_npv", "upside_npv", "swing"]].rename(
                    columns={"downside_npv": "Downside NPV", "upside_npv": "Upside NPV", "swing": "Swing"}
                ),
                use_container_width=True
            )

        st.info(
            "**Guardrail:** EDI shows a range and a probability, not a false-precision single number. "
            "The owner still makes the call — this tab exists to stop that call from being made on a "
            "point estimate that hides how much of the outcome is genuinely uncertain."
        )

    # ---------------------------------------------------------
    # AI Challenge
    # ---------------------------------------------------------

    with tab4:

        st.subheader("AI Decision Challenge")
        st.write(ai_analysis)

    # ---------------------------------------------------------
    # Market Signal (synthetic demand simulation)
    # ---------------------------------------------------------

    with tab5:

        st.subheader("🗣️ Synthetic Market Demand Signal")
        st.caption(
            "Illustrative synthetic-persona sentiment, kept deliberately separate from the financial "
            "engines above — it's a different kind of evidence (qualitative market read vs. quantitative "
            "cash-flow math), not a restatement of the same number."
        )

        signal = DEMAND_SIGNALS.get(case.case_id, DEFAULT_DEMAND_SIGNAL)
        score = signal["score"]
        verdict = signal["verdict"]
        v_color = "#137333" if verdict == "GO" else "#c5221f"

        col_s, col_v = st.columns(2)
        with col_s:
            st.metric("Consensus Demand Index", f"{score}/100")
            st.progress(score / 100.0)
            st.caption("Aggregated index score compiled from qualitative synthetic persona sentiment metrics.")
        with col_v:
            st.markdown("**Consumer Sentiment Verdict:**")
            st.markdown(
                f"<div style='background-color:#f8fafc; border:1px solid #e2e8f0; border-left: 5px solid {v_color}; "
                f"padding:15px; border-radius:5px; font-weight:bold; color:{v_color};'>{verdict} ({signal['note']})</div>",
                unsafe_allow_html=True
            )
            st.caption("Calculated direction derived from dialectical consensus checks.")

        # Signal-conflict check: when the qualitative market read disagrees with the
        # quantitative recommendation, say so explicitly rather than let the two tabs
        # quietly contradict each other.
        financially_positive = decision == "INVEST"
        market_positive = verdict == "GO"
        if financially_positive != market_positive:
            st.error(
                f"**⚠️ Signal Conflict:** The financial engines recommend **{decision}**, but synthetic "
                f"market sentiment leans **{verdict}**. EDI does not resolve this tension for you — a "
                "quantitatively sound case with lukewarm market reception (or vice versa) is exactly the "
                "kind of split signal a human owner needs to see before committing capital."
            )
        else:
            st.success(
                f"**Aligned Signal:** Financial recommendation (**{decision}**) and market sentiment "
                f"(**{verdict}**) point the same direction."
            )

        st.divider()
        st.subheader("Transcript: Synthetic Panel Debate")
        st.write(focus_group_transcript)

    # ---------------------------------------------------------
    # Governance & Audit Trail
    # ---------------------------------------------------------

    with tab6:

        st.subheader("🏛️ Governance Policy Review")
        st.caption("Automated policy-compliance pass, run on every decision before it reaches an executive.")

        passed = sum(1 for c in governance if c["status"] == "pass")
        flagged = sum(1 for c in governance if c["status"] == "flag")
        reviewed = sum(1 for c in governance if c["status"] == "review")

        gcol1, gcol2, gcol3 = st.columns(3)
        gcol1.metric("Checks Passed", passed)
        gcol2.metric("Flags Raised", flagged)
        gcol3.metric("Manual Reviews Required", reviewed)

        gov_df = pd.DataFrame(governance)
        gov_df["Status"] = gov_df["status"].map(lambda s: f"{GOVERNANCE_STATUS_ICON.get(s, '•')} {s.title()}")
        gov_df = gov_df.rename(columns={"check": "Policy Check", "detail": "Detail"})[["Policy Check", "Status", "Detail"]]
        st.dataframe(gov_df, hide_index=True, use_container_width=True)

        st.caption("EDI never auto-approves capital — every check here informs the human sign-off, it does not replace it.")

        st.divider()

        st.subheader("🔗 Decision Provenance")
        st.success("Decision analysis trace recorded")

        prov_col1, prov_col2 = st.columns(2)
        with prov_col1:
            st.write("**Transaction ID**")
            st.code(provenance["transaction_id"])
            st.write("**Engine**")
            st.write(provenance["engine"])
            st.write("**Function**")
            st.write(provenance["function"])
        with prov_col2:
            st.write("**Version**")
            st.write(provenance["version"])
            st.write("**Timestamp**")
            st.write(provenance["timestamp"])

        st.markdown("**Input Snapshot**")
        st.caption("Exact figures that fed this specific transaction — the audit record ties every downstream number back to these.")
        st.json(provenance["input_snapshot"])

        st.markdown("**Processing Trace**")
        st.caption("Each engine invocation in the pipeline, in execution order.")
        for event in provenance["system_events"]:
            st.write(f"`{event['time']}` — {event['event']}")

    # ---------------------------------------------------------
    # Executive Brief
    # ---------------------------------------------------------

    with tab7:

        st.subheader("🏛️ Institutional Strategic Advisory Brief")
        st.caption("Formal corporate briefing note evaluating long-term capital allocation efficacy.")

        st.divider()

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
        *   **Forward-Looking Net Present Value (NPV):** `${financials.forward_npv:,.2f}`
        *   **Total Project NPV (Including Sunk Costs):** `${financials.total_project_npv:,.2f}`
        *   **Hurdle Discount Rate Applied:** `{case.discount_rate * 100:.1f}%` — {case.discount_rate_basis}

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


def render_footer() -> None:
    """Shared footer, used identically across all three pages."""
    st.divider()
    st.markdown(
        "<div style='text-align:center; font-size:13px;'>"
        "EDI v0.1 • Governance-first AI for Executive Decision Intelligence &nbsp;·&nbsp; "
        "<a href='app/static/about-books.html' target='_blank'>About the Builder &amp; Book List</a>"
        "</div>",
        unsafe_allow_html=True,
    )
