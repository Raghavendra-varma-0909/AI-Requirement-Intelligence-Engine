def calculate_score(issues, ambiguities, missing_requirements, dependencies):
    """
    Advanced Quality Score (0-100).

    Penalties:
    - Ambiguity (per unique word): High = -8, Medium = -4, Low = -2
    - Missing requirement flows: -3 each (capped at -30)
    - Missing NFRs (flat): -15
    - Critically Incomplete (< 10 words): -40
    - Insufficient Detail (< 20 words): -20
    - No Engineering Keywords: -20
    - Missing Actor: -10
    - Generic Placeholder terms: -15 each (capped at -25)

    Bonus:
    - Dependencies mapped: +5
    """
    score = 100
    breakdown = {
        "base": 100,
        "ambiguity_penalty": 0,
        "missing_flow_penalty": 0,
        "missing_nfr_penalty": 0,
        "completeness_penalty": 0,
        "dependency_bonus": 0
    }

    # Severity-based ambiguity penalty
    for amb in ambiguities:
        sev = amb.get("severity", "low")
        penalty = {"high": 8, "medium": 4, "low": 2}.get(sev, 2)
        breakdown["ambiguity_penalty"] -= penalty
        score -= penalty

    # Missing flows (capped at -30)
    missing_penalty = min(len(missing_requirements) * 3, 30)
    breakdown["missing_flow_penalty"] = -missing_penalty
    score -= missing_penalty

    # NFR absence
    has_nfr_issue = any(iss.get("type") == "Missing NFRs" for iss in issues)
    if has_nfr_issue:
        breakdown["missing_nfr_penalty"] = -15
        score -= 15

    # Specificity + completeness penalties
    completeness_penalty = 0
    for iss in issues:
        t = iss.get("type", "")
        if t == "Critically Incomplete":
            completeness_penalty -= 40
        elif t == "Insufficient Detail":
            completeness_penalty -= 20
        elif t == "No Engineering Keywords":
            completeness_penalty -= 20
        elif t == "Missing Actor":
            completeness_penalty -= 10

    # Generic placeholder penalty (capped at -25)
    placeholder_count = sum(1 for iss in issues if iss.get("type") == "Generic Placeholder Term")
    placeholder_penalty = -min(placeholder_count * 15, 25)
    completeness_penalty += placeholder_penalty

    breakdown["completeness_penalty"] = completeness_penalty
    score += completeness_penalty

    # Dependency richness bonus
    if dependencies:
        breakdown["dependency_bonus"] = 5
        score += 5

    return max(0, min(100, score)), breakdown
