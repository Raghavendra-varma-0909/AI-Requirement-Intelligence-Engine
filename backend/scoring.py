def calculate_score(issues, ambiguities, missing_requirements, dependencies, strong_features=None):
    """
    Advanced Quality Score (0-100).

    Penalties:
    - Ambiguity (per unique word): High=-8, Medium=-4, Low=-2
    - Missing NFR flows: -3 each (capped -15 for NFR section only)
    - Missing NFRs (flat): -15
    - Critically Incomplete (<10 words): -40
    - Insufficient Detail (<20 words): -20
    - No Engineering Keywords: -20
    - Missing Actor: -10
    - Generic Placeholder: -15 each (capped -25)

    Bonuses (strength signals, capped at +20):
    - JWT, Stripe, failure handling, logs, etc: +3 to +6 each
    - Dependencies mapped: +5
    """
    score = 100
    breakdown = {
        "base": 100,
        "ambiguity_penalty": 0,
        "missing_flow_penalty": 0,
        "missing_nfr_penalty": 0,
        "completeness_penalty": 0,
        "strength_bonus": 0,
        "dependency_bonus": 0
    }

    # Ambiguity penalties
    for amb in ambiguities:
        penalty = {"high": 8, "medium": 4, "low": 2}.get(amb.get("severity", "low"), 2)
        breakdown["ambiguity_penalty"] -= penalty
        score -= penalty

    # Missing flows — count only non-NFR ones for the cap
    non_nfr_missing = [m for m in missing_requirements if m.get("domain") != "Non-Functional Requirements"]
    nfr_missing     = [m for m in missing_requirements if m.get("domain") == "Non-Functional Requirements"]

    flow_penalty = min(len(non_nfr_missing) * 3, 30)
    breakdown["missing_flow_penalty"] = -flow_penalty
    score -= flow_penalty

    # NFRs: flat -15 if flagged
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

    placeholder_count = sum(1 for iss in issues if iss.get("type") == "Generic Placeholder Term")
    completeness_penalty += -min(placeholder_count * 15, 25)

    breakdown["completeness_penalty"] = completeness_penalty
    score += completeness_penalty

    # Strength bonus (capped at +20)
    if strong_features:
        raw_bonus = sum(f.get("bonus", 3) for f in strong_features)
        bonus = min(raw_bonus, 20)
        breakdown["strength_bonus"] = bonus
        score += bonus

    # Dependency bonus
    if dependencies:
        breakdown["dependency_bonus"] = 5
        score += 5

    return max(0, min(100, score)), breakdown
