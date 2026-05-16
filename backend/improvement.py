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
        
    if not improved:
        improved.append("The provided requirement expresses raw functionality but strictly requires measurement targets.")
        improved.append(f"Original Context: '{text.strip()}'")
        
    return improved
