def calculate_score(issues, ambiguities, missing_requirements, dependencies):
    """
    Advanced Quality Score (0-100):
    - Ambiguities: High = -8, Medium = -4, Low = -2 (per unique word, not per count)
    - Missing requirements: -3 per item (capped at -30)
    - Missing NFRs: -15 flat
    - Bonus: +5 if dependencies are clearly mapped
    """
    score = 100
    breakdown = {
        "base": 100,
        "ambiguity_penalty": 0,
        "missing_flow_penalty": 0,
        "missing_nfr_penalty": 0,
        "dependency_bonus": 0
    }

    # Ambiguity penalties (per unique ambiguous word found)
    for amb in ambiguities:
        sev = amb.get("severity", "low")
        penalty = {"high": 8, "medium": 4, "low": 2}.get(sev, 2)
        breakdown["ambiguity_penalty"] -= penalty
        score -= penalty

    # Missing flows (capped)
    missing_penalty = min(len(missing_requirements) * 3, 30)
    breakdown["missing_flow_penalty"] = -missing_penalty
    score -= missing_penalty

    # NFR absence
    has_nfr_issue = any(iss.get("type") == "Missing NFRs" for iss in issues)
    if has_nfr_issue:
        breakdown["missing_nfr_penalty"] = -15
        score -= 15

    # Dependency bonus: if the engine found and mapped dependencies, that's a sign of richness
    if dependencies:
        breakdown["dependency_bonus"] = 5
        score += 5

    return max(0, min(100, score)), breakdown
