# Product Roadmap & To-Do List

**Publisher:** ScottColeSW  
**Contact:** colepossible@berkeley.edu  
**Repository:** [executive-decision-intelligence](https://github.com/ScottColeSW/executive-decision-intelligence)

---

## 🗺️ Strategic Roadmap

### Phase 1: Foundation & Data Modeling (Current)
*   Finalize core data models (`decision_case.py`, `recommendation.py`).
*   Establish mock data sets for `capex_case.json`, `sunk_cost_case.json`, and `ai_case.json`.
*   Implement standard configuration management via `config.yaml`.

### Phase 2: Core Processing Engines
*   Build out the **Financial Engine** for core math and ROI modeling.
*   Develop the **Provenance Engine** to track data lineage and audit trails.
*   Implement baseline abstract interfaces for the `LLMProvider` layer.

### Phase 3: Orchestration & UI
*   Connect local providers (`OllamaProvider`, `LMStudioProvider`) and cloud alternatives.
*   Build out the Streamlit/Python command-line presentation layer (`executive_brief.py`).
*   Establish structural hypothesis testing loops.

---

## 📝 Immediate To-Do List

### 🏗️ Architecture & Core Setup
- [ ] Initialize Python environment and populate `requirements.txt` (Dependencies: `pyyaml`, `pydantic`, `ollama`, `openai`).
- [ ] Implement base configuration parser in `utils/config.py`.
- [ ] Create base abstract class inside `llm/provider.py`.

### 🧠 Engine Implementation
- [ ] **Financial:** Write functions to parse project costs, projected revenue, and calculate explicit net present value (NPV) or ROI.
- [ ] **Governance:** Build rule-matching logic to catch boundary violations (e.g., budget caps).
- [ ] **Provenance:** Code the tracking decorator to map exactly which model variables and prompt versions fed into a specific conclusion.

### 🧪 Testing & Validation
- [ ] Implement basic unit tests in `tests/test_financial.py` using `pytest`.
- [ ] Validate JSON schema compliance for `ai_case.json` against `decision_case.py` models.

---

> **Note on Contribution:** For security or architectural adjustments, open an issue or submit a pull request directly to the `ScottColeSW` organization repository.