# Product Roadmap & To-Do List

**Publisher:** ScottColeSW  
**Contact:** colepossible@berkeley.edu  
**Repository:** [executive-decision-intelligence](https://github.com/ScottColeSW/executive-decision-intelligence)

---

## 🗺️ Strategic Roadmap

### Phase 1: Foundation & Data Modeling — Done
*   Core decision case model (`data/cases.py`), including a stated, auditable `discount_rate_basis` on every case rather than a hidden constant.
*   Three worked SME scenarios (CapEx, sunk cost, AI ROI), each with current-state vs. AI-supported-workflow narrative.
*   Custom-decision intake (`pages/Ask_EDI.py`) so a user isn't limited to the three built-in cases — runs the identical pipeline on live input.

### Phase 2: Core Processing Engines — Done
*   **Financial Engine:** NPV, IRR, forward vs. total ROI, payback period.
*   **Uncertainty Engine:** Monte Carlo simulation (P10/P50/P90, probability of profit, tornado sensitivity ranking) sharing one formula with the summary-level volatility metric, so the two never drift apart.
*   **Governance Engine:** structured, multi-rule policy review (budget cap, approval routing, hurdle-rate compliance, assumption documentation, category-specific checks).
*   **Provenance:** transaction ID, input snapshot, and full processing trace, surfaced in the UI rather than computed and discarded.

### Phase 3: Orchestration & UI — Done
*   Streamlit presentation layer with a single shared pipeline (`ui/executive_brief.py`) used identically by the case selector, the Ask EDI form, and rendered consistently across all pages.
*   Local Ollama inference via `OLLAMA_HOST`, with a deterministic offline fallback (`ollama_client.py`) so the app degrades gracefully instead of failing.
*   Dockerized (`Dockerfile`, `docker-compose.yml`) — reaches a host-installed Ollama via `host.docker.internal`.

---

## 📝 Next Up

### 🧪 Testing & Validation
- [ ] Real unit tests (`pytest`) for `FinancialEngine`, `UncertaintyEngine`, and `GovernanceEngine` — none exist yet; the repo previously had empty stub files for this and they've been removed rather than left as unconvincing placeholders.
- [ ] Regression check that `RecommendationEngine` and `FinancialEngine` NPV outputs stay identical (they're computed independently today and only agreed by construction — see `engines/financial_engine.py` and `engines/recommendation_engine.py`).

### 🧠 Engine Enhancement
- [ ] Wire a real interest-rate source (e.g., a treasury/FRED API) behind `discount_rate_basis`, replacing the manually-stated rate with a fetched one while keeping the same "show your basis" UI pattern.
- [ ] Persist analyses (currently session-state only) so a decision case and its result survive a page reload.

### 🔌 Optional Future Extension
- [ ] Pluggable LLM providers beyond Ollama (OpenAI, Hugging Face, LM Studio) — deliberately not built yet; the shipped version is one well-tested path rather than an abstraction layer with three untested ones.

---

> **Note on Contribution:** For security or architectural adjustments, open an issue or submit a pull request directly to the `ScottColeSW` organization repository.
