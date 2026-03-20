# Walkthrough: AI Requirement Intelligence Engine

## 🎯 What was Built
A production-grade, highly-engineered hybrid intelligent system for analyzing and evaluating software requirements. The system acts as a strict "AI Product Manager," critically evaluating requirements in real-time.

## 🏢 Architecture & Intelligence
### 1. Hybrid Backend Engine (FastAPI)
The backend skips trivial GPT wrappers in favor of a layered intelligence architecture:
- **[rules_engine.py](file:///c:/Users/yarra/OneDrive/Desktop/babu/Projects/AI%20Requirement%20Intelligence%20Engine/backend/rules_engine.py)**: A robust, deterministic pattern-matching logic core. Capable of context-aware pattern detection (detecting missing operational flows implicitly linked to keywords like "login" or "payment"), severity-weighted ambiguity detection, and tracking architectural dependencies.
- **[scoring.py](file:///C:/Users/yarra/OneDrive/Desktop/babu/Projects/AI%20Requirement%20Intelligence%20Engine/backend/scoring.py)**: Computes an objective 0-100 Quality Score, penalizing unstructured statements based on their specific impact severity, and flagging total absences of measurable Non-Functional Requirements (NFRs).
- **REST Endpoints**:
  - `POST /api/analyze/live` -> Highly optimized route triggered in milliseconds for live editor semantic highlighting.
  - `POST /api/analyze/deep` -> The deep analysis route that constructs the fully structured, rewritten output parameters including architectural dependencies and exact re-wordings.

### 2. Premium Frontend Dashboard (React + Vite)
- We explicitly stayed away from Streamlit to build a true, bespoke SaaS application employing Vanilla CSS variables to achieve a modern, glassmorphic dark theme (inspired by top-tier modern apps like Linear).
- **Custom Intelligence Components**:
  - `HighlightEditor`: Creates an invisible background overlay to draw precise, color-coded underlines (Red=Ambiguity, Orange=Missing) behind specific problematic words natively in the text area.
  - [ScoreGauge](file:///c:/Users/yarra/OneDrive/Desktop/babu/Projects/AI%20Requirement%20Intelligence%20Engine/frontend/src/components/ScoreGauge.jsx#3-60): An elegant SVG visualizing the precise quality score penalty breakdowns dynamically.
  - [ResultsPanel](file:///c:/Users/yarra/OneDrive/Desktop/babu/Projects/AI%20Requirement%20Intelligence%20Engine/frontend/src/components/ResultsPanel.jsx#4-90): A dynamic side-by-side component mapping structured JSON output into expandable analysis sections cleanly showing explanations and impacts for every flagged rule.
  
## 🚀 How to Experience the Product
Both environments are available live or locally.

1. **Live Production App:** [ai-requirement-intelligence-engine.vercel.app](https://ai-requirement-intelligence-engine.vercel.app)
2. **Local Environment:** Open **[http://localhost:5174/](http://localhost:5174/)** in your browser. 
3. **Experience the Live Requirements Critique (WOW feature)**:
   Begin typing raw requirements (e.g. *"Build a fast and secure payment system"*). 
   Instantly, the system will highlight vague words like "fast", identify that "payment" is missing failure/rollback handling, calculate the architectural dependencies, map them, and dynamically drop your Quality Score in real-time.
4. Click **Deep Analyze** to synthesize the deterministic output into clean, structured software engineering objectives.

*(If you ever need to restart the servers manually: Run `npm run dev` in `frontend/` and `uvicorn main:app` in the `backend/` virtual environment).*
