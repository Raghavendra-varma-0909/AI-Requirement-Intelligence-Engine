# 🧠 AI Requirement Intelligence Engine (AIRE)

**Hybrid Rule-Based + AI Analysis Pipeline**

🌐 **Live Demo:** [ai-requirement-intelligence-engine.vercel.app](https://ai-requirement-intelligence-engine.vercel.app)

This document provides a comprehensive overview of the technology stack, application workflow, and the deterministic core logic powering the engine.

---

## 🛠️ 1. Technology Stack

### Frontend (User Interface)
*   **Framework**: React (managed via Vite for rapid HMR and optimized builds).
*   **Styling**: Custom Vanilla CSS3. Uses the "Aurora" theme—a premium glassmorphism aesthetic with deep purple/violet gradients, glowing transitions, and highly responsive layouts.
*   **State Management**: React Hooks (`useState`, `useEffect`, `useRef`) for handling debounced live inputs, UI transitions, and parallel data streams without external bloat like Redux.
*   **Deployment**: Edge-deployed automatically via **Vercel** (`vercel.json` configured).

### Backend (The Engine Layer)
*   **Framework**: Python 3.11 with **FastAPI**. Chosen for its asynchronous speed, which is critical when acting as an intermediary for both deterministic rules logic and AI LLM calls.
*   **Server**: Uvicorn (ASGI web server).
*   **Data Validation**: Pydantic models ensure strict typing for all incoming request payloads.
*   **AI Integration**: Google GenAI SDK (`google-generativeai`) connecting to the Gemini 2.5 Flash model for deep semantic reasoning.
*   **Deployment**: Hosted continually on **Render.com** (via `render.yaml`).

---

## 🔄 2. Application Workflow (Data Architecture)

The system operates on a **two-tier architecture**, prioritizing immediate user feedback via a high-speed local engine, followed by deep semantic analysis via AI.

### Phase A: Live Typing (Deterministic & Stateless)
1. **Input**: User types in the UI editor. React applies a 500ms debounce curve to prevent network flooding.
2. **Analysis (`POST /api/analyze/live`)**: The payload hits the FastAPI endpoint.
3. **Rule Processing**: The string is processed purely through Python native structures (RegEx, hash maps, conditional trees) inside `rules_engine.py`. This step takes `< 10ms`.
4. **Instant UI Updates**: The frontend instantly renders dual-color highlights (Red for ambiguities, Green for engineering strength signals) and a live Quality Score constraint without making any costly LLM calls.

### Phase B: Deep Analysis (Hybrid AI Pipeline)
1. **Trigger**: User clicks "⚡ Deep Analyze".
2. **Gathering Hard Data (`POST /api/analyze/deep`)**: The backend runs the deterministic rules engine *first* to gather hard structural data (exact penalty counts, missing domains, missing roles).
3. **LLM Synthesis**: The original raw text, along with the Engine's hard findings, is packaged into a structured prompt and sent to the Gemini AI model.
4. **Architectural Reasoning**: The AI acts as a Senior Systems Architect. It maps out hidden dependencies, generates consultant-grade NFR (Non-Functional Requirement) suggestions, and structurally rewrites the requirement.
5. **Final Scoring & Payload**: The final response merges the AI insights with the hard math of the Rules Engine to generate the ultimate Score Breakdown, the Dependency Graph, and the Side-by-Side Original vs. Improved view.

---

## 🧠 3. The Core Logic (The Intelligence Engine)

The magic of the application lies inside `rules_engine.py` and `scoring.py`. The engine consists of 8 interconnected gatekeeper modules.

### Module 1: Specificity & Completeness Checker
*   **Logic**: Tokenizes the input to count words and checks against dictionaries of known actors (e.g., "user", "admin", "client") and engineering domain keywords.
*   **Purpose**: Prevents the "Build a website" problem. Grossly incomplete or vague inputs under 10 words, or inputs completely lacking an actor, are slammed with -40 to -60 base penalties.

### Module 2: Generic Placeholder Detector
*   **Logic**: Scans for meaningless business consultant jargon ("solution", "platform", "system", "tool", "website") that are not backed up by concrete technical boundaries.
*   **Purpose**: Forces the user to define exactly *what* is being built rather than relying on abstract nouns. Penalizes -15 points per infraction.

### Module 3: Ambiguity Scanner
*   **Logic**: Compares the input text against a weighted severity dictionary of subjective adjectives (e.g., "fast", "scalable", "user-friendly").
*   **Purpose**: "Fast" cannot be QA tested. The engine demands measurable metrics (e.g., "< 200ms latency at p95"). Ambiguities are highlighted in Red.

### Module 4: Context-Aware Pattern Matcher
*   **Logic**: Detects functional operational domains. (e.g., If the string contains "login" or "authenticate").
*   **Purpose**: If "login" is detected, the engine inherently knows this is an Auth domain. It immediately scans for secondary necessary features like "Password Reset", "MFA/2FA", and "Session Lockout". If they are missing, it throws a "Missing Functional Flow" penalty.

### Module 5: Strength Signals Detector (Bonus System)
*   **Logic**: A positive-reinforcement scanner looking for explicit, high-quality engineering architecture decisions (e.g., "JWT", "Stripe integration", "OAuth 2.0", "transaction logs", "OWASP compliance").
*   **Purpose**: Rewards highly descriptive inputs with bonus points (up to +20) and highlights them in Green in the UI editor.

### Module 6: NFR Coverage Checker
*   **Logic**: Ensures Non-Functional Requirements are established.
*   **Purpose**: If no performance matrices are detected, it supplies consultant-grade targets (e.g., "Target 99.9% uptime SLA" or "Define RPO/RTO parameters").

### Module 7: Dependency Chain Resolver
*   **Logic**: Maps how frontend features rely on backend infrastructure (e.g., "Payment feature strictly requires Transaction Logs and an Order Management layer").
*   **Purpose**: This data powers the visual arrow-based Dependency Graph in the React UI.

### Module 8: The Scoring Algorithm (`scoring.py`)
*   **Logic**: A strict mathematical deduction model. Starts at a Base Score of 100. It deducts weighted penalties for missing actors, missing NFRs, and ambiguous terms, while adding capped bonuses for strength signals and resolved dependencies. Outputs the final Quality Score (0-100).

---

## 🌍 4. Deployment Architecture

The AI Requirement Intelligence Engine is strictly designed for production deployment rather than local testing.

*   **Frontend (Vercel.com)**
    *   The React suite is edge-deployed via Vercel. 
    *   It is natively configured with a `vercel.json` routing matrix and relies on a secure `VITE_API_URL` environment variable injected during the Vercel build phase to prevent hardcoded API routes.
*   **Backend (Render.com)**
    *   The FastAPI Python engine is deployed as a continuous Web Service on Render.
    *   Deployment is fully automated via the `render.yaml` Infrastructure-as-Code file, directing Render to install requirements and boot `uvicorn main:app --host 0.0.0.0 --port 10000`.
