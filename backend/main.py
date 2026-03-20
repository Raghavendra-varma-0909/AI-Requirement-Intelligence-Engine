from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import rules_engine
import scoring
import analyzer
import improvement
import uvicorn

app = FastAPI(title="AI Requirement Intelligence Engine API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class AnalyzeRequest(BaseModel):
    text: str
    privacy_mode: bool = False

@app.post("/api/analyze/live")
def analyze_live(req: AnalyzeRequest):
    issues, ambiguities, missing, dependencies, modules_fired, req_class, strong_features = rules_engine.analyze(req.text)
    score, breakdown = scoring.calculate_score(issues, ambiguities, missing, dependencies, strong_features)
    return {
        "issues": issues,
        "ambiguities": ambiguities,
        "missing_requirements": missing,
        "dependencies": dependencies,
        "modules_fired": modules_fired,
        "requirement_classification": req_class,
        "strong_features": strong_features,
        "confidence_score": score,
        "score_breakdown": breakdown,
        "explanations": ["Live analysis via Hybrid Intelligence Engine — deterministic modules only."]
    }

@app.post("/api/analyze/deep")
def analyze_deep(req: AnalyzeRequest):
    rules_issues, rules_ambig, rules_missing, rules_deps, modules_fired, req_class, strong_features = rules_engine.analyze(req.text)

    llm_result = analyzer.deep_analyze(req.text, rules_issues, rules_ambig, rules_missing, rules_deps)

    score, breakdown = scoring.calculate_score(
        llm_result["issues"], llm_result["ambiguities"],
        llm_result["missing_requirements"], llm_result["dependencies"],
        strong_features
    )

    improved, final = improvement.rewrite_and_finalize(
        req.text, llm_result["issues"],
        llm_result["ambiguities"], llm_result["missing_requirements"],
        llm_result["dependencies"]
    )

    return {
        "issues": llm_result["issues"],
        "ambiguities": llm_result["ambiguities"],
        "missing_requirements": llm_result["missing_requirements"],
        "dependencies": llm_result["dependencies"],
        "modules_fired": modules_fired,
        "requirement_classification": req_class,
        "strong_features": strong_features,
        "improved_requirements": improved,
        "final_clean_version": final,
        "confidence_score": score,
        "score_breakdown": breakdown,
        "explanations": llm_result["explanations"]
    }

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
