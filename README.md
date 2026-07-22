🧠 Executive Decision Intelligence (EDI)

Democratizing Institutional-Grade Capital Governance & Synthetic Market Validation for SMEs

1. The Strategic Vision: Solving the SME Decision "Blind Spot"

SMEs are the foundational engine of economic mobility and community wealth-building, yet they face a stark capital allocation challenge. While corporate-grade enterprises have access to dedicated CFO teams, quantitative risk models, and independent boards to stress-test major purchases, the average small business owner must rely heavily on intuition. This leaves them highly vulnerable to structural cognitive blind spots:

The Sunk-Cost Trap: Emotional over-commitment to legacy assets or poorly performing vendors out of frustration over historical cash spent.

CapEx Capacity Friction: Underestimating the forward-looking hurdle rate required to support equipment, fleet, or software expansion.

The Vendor Echo-Chamber: Relying on sales-incentivized consultants who rubber-stamp expansions without presenting objective, adversarial challenges.

EDI (Executive Decision Intelligence) levels the playing field. It packages sophisticated, institutional-grade capital budgeting, dialectical reasoning, and local, data-secure edge AI into a high-utility advisor dashboard.

2. Core High-Impact Features

🧩 A. Sunk-Cost Decoupling (The Emotional Shield)

The quantitative modeling engine dynamically splits the math of an active proposal into two distinct calculations:

Forward-Looking Net Present Value ($NPV_{\text{forward}}$): Evaluates whether allocating fresh cash is mathematically rational, completely ignoring historical outlays.

Total Project Net Present Value ($NPV_{\text{total}}$): Includes past expenditures (sunk costs) to evaluate total lifecycle asset efficacy.

The system calculates these values using the following Discounted Cash Flow (DCF) models:

$$NPV_{\text{forward}} = \sum_{t=1}^{N} \frac{CF_t}{(1 + r)^t} - I_{\text{fresh}}$$

$$NPV_{\text{total}} = \sum_{t=1}^{N} \frac{CF_t}{(1 + r)^t} - (I_{\text{fresh}} + I_{\text{sunk}})$$

Where:

$CF_t$ is the projected annualized operational cash flow yield in year $t$.

$r$ is the owner's risk-adjusted hurdle rate / discount rate.

$I_{\text{fresh}}$ is the fresh capital required to execute or complete the project.

$I_{\text{sunk}}$ represents historical sunk costs that cannot be recovered.

$N$ is the strategic planning horizon in years.

This mathematical split-view gives the business owner a clinical exit ramp, allowing them to confidently halt project spending or proceed based on future marginal yield without emotional baggage.

🗣️ B. Synthetic Market Focus Group Simulator

To bypass static business assumptions, EDI leverages a multi-agent dialectical panel running locally via Ollama. It simulates real-world customer segments debating the proposed investment:

The Cost-Conscious Skeptic: Focuses on price barriers, overhead, and budget alternatives.

The Convenience-Driven Advocate: Evaluates responsiveness, speed, and premium service delivery.

The Pragmatic Local Tech-Adopter: Evaluates booking friction, digital reputation, and seamless checkouts.

The output aggregates qualitative sentiment indicators to produce an actionable Consensus Demand Index (0-100) and a clear consumer sentiment verdict.

🛡️ C. Dialectical "Red Team" Adversarial Challenge

Rather than acting as a passive chatbot, the built-in Decision Analyst agent acts as an independent risk officer. It actively challenges the qualitative confidence parameters of the scenario, highlighting execution bottlenecks, timeline delays, and capital-depletion risks.

📑 D. Institutional CDFI Provenance Ledger

To bridge the credit gap between local businesses and Community Development Financial Institutions (CDFIs) or commercial lenders, EDI implements an Immutable Provenance Trace.

Every run generates a secure, pseudo-cryptographic transaction record showing exact execution timestamps, version identifiers, mathematical input snapshots, and microsecond telemetry steps. SME owners can print this ledger directly for underwriters to demonstrate institutional-grade capital governance.

🗺️ E. The 30-60-90 Day Execution Roadmap

EDI bridges the gap between complex financial modeling and physical business execution. Each positive recommendation compiles an operational milestone playbook:

Days 1-30 (Initialization Phase): Physical setup, reserve allocations, and initial configuration.

Days 31-60 (Operational Tuning Phase): Market launch, channel setup, and verification of key feedback benchmarks.

Days 61-90 (Hurdle Review Phase): Direct yield audit comparing cash flows to targeted annual hurdle rates to trigger defensive pivot loops.

3. Repository Architecture

The project is structured according to strict modular domain-driven design principles, decoupling computation, prompt configurations, data stores, and UI renderers:

executive-decision-intelligence/
│
├── Nextstreet-Interview-Demo.py   # Primary Streamlit Dashboard & Control UI
├── ollama_client.py               # Local Ollama LLM Connection Client
├── update_repo.bat                # Windows automation identity & git sync script
│
├── data/
│   ├── cases.py                   # Standardized SME Scenario Datastore
│   └── prompts_config.json        # Decoupled prompts & offline fallback transcripts
│
├── engines/
│   ├── recommendation_engine.py   # Financial Split NPV, IRR & Confidence Engine
│   ├── uncertainty_engine.py      # Volatility Multiplier & Margin Sensitivity Engine
│   └── governance_engine.py       # Strategic SME Capital Limits & Policy Check Engine
│
├── agents/
│   └── decision_analyst.py        # Red Team Dialectical Challenger Logic
│
├── provenance/
│   └── tracker.py                 # Pseudo-Cryptographic Audit Trace Generator
│
└── docs/
    └── strategic_reframing_analysis.md # Core business problems & social impact thesis


4. Local Installation & Setup

Because data privacy and zero marginal execution costs are critical for small business operators, EDI runs entirely on your local machine using open-source models. No API keys are required. Two ways to run it:

Option A: Docker (recommended)

Requires Docker Desktop and a locally-running Ollama instance (see Step 2 below).

docker compose up --build

Then open http://localhost:8501. The container reaches your host's Ollama via `host.docker.internal` by default (configurable through the `OLLAMA_HOST` env var in `docker-compose.yml`). If Ollama isn't reachable, EDI falls back to a deterministic offline response rather than failing.

Option B: Bare Metal

Step 1: Install Dependencies

Ensure you have Python 3.10+ installed. In your repository directory:

pip install -r requirements.txt

Step 2: Set Up Ollama (Edge AI Engine)

Download and run Ollama, then pull the default model:

ollama pull llama3.2

Keep the Ollama application running locally in the background. To use a different host or model, set the `OLLAMA_HOST` / `OLLAMA_MODEL` environment variables before launching.

Step 3: Run the Dashboard

streamlit run Nextstreet-Interview-Demo.py


5. Quick Test Scenarios

Once the interface launches, use the sidebar to cycle through three realistic SME strategic challenges:

Hydro-Jetter Service Van Expansion: A classic CapEx capacity scenario requiring high-margin commercial backlog validation.

Legacy E-Commerce Platform Overhaul: A classic sunk-cost trap evaluating whether to pay an agency more milestone fees or cut historical losses.

Automated Review Booster: An AI automation ROI scenario highlighting immediate process value, local search visibility, and lead rescue rates.

6. Social Impact Alignment: Next Street & CDFI Integration

By packaging institutional-grade quantitative budgeting, behavioral risk offsets, and transparent compliance tracking into an intuitive desktop app, this project directly advances Next Street’s core mission:

Equity & Democratization: It makes high-end fractional CFO risk advisory services accessible to micro-businesses, historically underserved founders, and localized entrepreneurs.

Institutional Credit Readiness: The printable cryptographic Provenance Ledger structures small business metrics in a format that accelerates loan decisions for CDFI partners, making risk evaluation fast and reliable.

Community Wealth Retention: By guiding owners away from wasteful vendor spending and helping them identify optimal capacity expansions, the tool compounds long-term business equity, supports stable local wages, and preserves regional community footprint.
