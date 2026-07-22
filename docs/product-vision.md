# Product Vision: Executive Decision Intelligence (EDI)

## 1. Core Intent
The Executive Decision Intelligence system is designed to remove cognitive bias, untangle conflicting constraints, and provide a clear line of sight from strategic **Vision** to execution **Intent**. By formalizing decision cases, the system acts as an automated governance and recommendation layer for high-stakes executive decisions.

## 2. Target Decision Frameworks
The initial implementation focuses on three primary decision scenarios, modeled in the static data layer:
*   **Capital Expenditure (CapEx) Cases:** Evaluating long-term resource allocations against projected returns.
*   **Sunk Cost Dilemmas:** Striking an objective, un-emotional balance when deciding whether to pivot, persist, or terminate legacy projects.
*   **AI Implementation / ROI Analysis:** Rigorously calculating the direct return on investment for automation and multi-agent system orchestration.

## 3. Core Engine Architecture
The system processes data through five distinct analytical lenses:
*   **Financial Engine:** Quantitative ROI modeling and capital constraint checking.
*   **Recommendation Engine:** Synthesis of quantitative and qualitative data to present trade-offs.
*   **Governance Engine:** Compliance matching, policy guardrails, and risk threshold analysis.
*   **Hypothesis Engine:** "What-if" simulations to stress-test decisions against changing market parameters.
*   **Provenance Engine:** The immutable record keeper. It tracks the lineage of data sources, assumptions, and LLM prompts used to reach a recommendation, ensuring complete auditability.

## 4. Technical Foundations
*   **LLM Integration:** Local Ollama inference via a configurable host (`OLLAMA_HOST`), with a deterministic offline fallback so the app degrades gracefully rather than failing when the model is unreachable. A pluggable provider abstraction (OpenAI, Hugging Face, LM Studio) is a plausible future extension, not a current capability — the shipped implementation is intentionally a single, well-tested path.
*   **Modular Architecture:** Strict separation between analytical pipelines (Engines), the shared pipeline/rendering layer (`ui/executive_brief.py`), and presentation entry points (the case selector, the Ask EDI intake form, and the roadmap page).