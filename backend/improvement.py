def rewrite_and_finalize(text, issues, ambiguities, missing, dependencies):
    improved = []
    
    text_lower = text.lower()
    if "fast" in text_lower or "performant" in text_lower:
        improved.append("System must respond to 95% of user requests in under 200ms.")
    if "secure" in text_lower:
        improved.append("System must enforce OAuth 2.0 for API endpoints and encrypt data at rest (AES-256).")
    if "scalable" in text_lower:
        improved.append("Architecture must automatically scale to support up to 5,000 concurrent active users.")
    if "user-friendly" in text_lower:
        improved.append("User Interface must comply with WCAG 2.1 Level AA accessibility standards.")
        
    for dep in dependencies:
        improved.append(f"{dep['feature']} Module: Must integrate seamlessly with {dep['depends_on']}.")
        
    for m in missing:
        improved.append(f"[{m['category']}] {m['suggestion']}")
        
    if not improved:
        improved.append("The provided requirement expresses raw functionality but strictly requires measurement targets.")
        improved.append(f"Original Context: '{text.strip()}'")
        
    final_version = [
        "## Functional Requirements",
    ]
    for m in missing:
         final_version.append(f"- REQ-F: {m['suggestion']}")
         
    final_version.append("\n## Non-Functional Requirements")
    nfrs = [f"- REQ-NFR: {req}" for req in improved if "Must" in req or "Architecture" in req or "System" in req]
    if nfrs:
        final_version.extend(nfrs)
    else:
        final_version.append("- No explicit Non-Functional Overrides discovered.")
    
    if dependencies:
        final_version.append("\n## Architectural Dependencies")
        for dep in dependencies:
            final_version.append(f"- DEP: {dep['feature']} -> {dep['depends_on']} ({dep['reason']})")
        
    return improved, final_version
