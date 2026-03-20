import re

# ============================================================
# AMBIGUITY DICTIONARY — 20 vague terms with severity + fixes
# ============================================================
AMBIGUOUS_WORDS = {
    "fast":         {"severity": "high",   "reason": "Subjective speed; cannot be tested.",             "suggestion": "Specify: e.g., 'System must respond to 95% of requests within 200ms'"},
    "slow":         {"severity": "high",   "reason": "Subjective slowness; no baseline defined.",        "suggestion": "Define acceptable latency threshold (e.g., < 500ms)"},
    "scalable":     {"severity": "high",   "reason": "No target load or concurrency defined.",           "suggestion": "Specify: 'Must support N concurrent users / X requests/sec'"},
    "secure":       {"severity": "high",   "reason": "Vague security objective; no standard cited.",     "suggestion": "Reference a standard: OAuth 2.0, OWASP Top 10, AES-256, TLS 1.3"},
    "performant":   {"severity": "high",   "reason": "Unmeasurable performance claim.",                  "suggestion": "Define throughput, latency, and payload size constraints"},
    "user-friendly":{"severity": "medium", "reason": "Subjective UX goal with no measurable criteria.", "suggestion": "Reference WCAG 2.1 AA or define max clicks-to-action metric"},
    "efficient":    {"severity": "medium", "reason": "Ambiguous resource usage.",                        "suggestion": "Define: CPU%, RAM limit (e.g., < 512MB), or ops/sec"},
    "robust":       {"severity": "medium", "reason": "Vague reliability claim.",                         "suggestion": "Define SLA: e.g., '99.9% uptime', MTBF, or error rate threshold"},
    "reliable":     {"severity": "medium", "reason": "No reliability metric defined.",                   "suggestion": "Specify: MTTR, MTBF, uptime SLA, or max error rate"},
    "easy":         {"severity": "low",    "reason": "Subjective usability claim.",                      "suggestion": "Define training time, SUS score target, or learnability metric"},
    "simple":       {"severity": "low",    "reason": "Subjective complexity claim.",                     "suggestion": "Define: number of steps, UI complexity score, or cognitive load metric"},
    "seamless":     {"severity": "low",    "reason": "Marketing term with no engineering definition.",   "suggestion": "Define specific integration mechanics or transition behavior"},
    "intuitive":    {"severity": "low",    "reason": "Unmeasurable UX descriptor.",                      "suggestion": "Conduct usability testing; define task-success-rate target"},
    "quickly":      {"severity": "medium", "reason": "Temporally ambiguous modifier.",                   "suggestion": "Replace with exact time constraint (e.g., 'within 2 seconds')"},
    "modern":       {"severity": "low",    "reason": "Trends change; 'modern' is highly time-dependent.","suggestion": "List the specific frameworks, design system, or tech stack expected"},
    "large":        {"severity": "medium", "reason": "No quantitative threshold.",                       "suggestion": "Specify exact data size (e.g., 'files up to 50MB')"},
    "good":         {"severity": "low",    "reason": "Subjective quality term.",                         "suggestion": "Define the acceptance criterion with a specific measurable goal"},
    "high":         {"severity": "medium", "reason": "Relative term with no baseline.",                  "suggestion": "Supply the benchmark (e.g., 'high availability = 99.95% uptime')"},
    "optimized":    {"severity": "medium", "reason": "Optimization with no target metric.",              "suggestion": "State what is being optimized and by how much (e.g., 30% faster load)"},
    "real-time":    {"severity": "high",   "reason": "'Real-time' means different things to different systems.", "suggestion": "Define acceptable latency: e.g., 'updates within 100ms of event'"},
}

# ============================================================
# CONTEXT PATTERN LIBRARY — 15 system domains
# ============================================================
CONTEXT_PATTERNS = {
    "login": {
        "label": "Authentication",
        "missing": [
            {"category": "Auth",     "suggestion": "Implement password reset and recovery flow."},
            {"category": "Security", "suggestion": "Enforce account lockout after N failed login attempts."},
            {"category": "Security", "suggestion": "Support Multi-Factor Authentication (MFA/TOTP)."},
            {"category": "Session",  "suggestion": "Define session timeout and token expiry policy."},
        ],
        "dependencies": [
            {"feature": "Login", "depends_on": "Session Management", "reason": "Auth state must be tracked securely across requests."},
            {"feature": "Login", "depends_on": "User Database",      "reason": "Credentials must be stored and validated against a persistent store."},
        ]
    },
    "register": {
        "label": "User Registration",
        "missing": [
            {"category": "Validation", "suggestion": "Enforce email format and uniqueness validation at registration."},
            {"category": "Auth",       "suggestion": "Implement email verification before account activation."},
            {"category": "UX",         "suggestion": "Define password strength policy (min length, special chars, etc.)."},
        ],
        "dependencies": [
            {"feature": "Registration", "depends_on": "Email Service",   "reason": "Verification emails require SMTP/transactional email integration."},
            {"feature": "Registration", "depends_on": "User Database",   "reason": "User records must be persisted."},
        ]
    },
    "payment": {
        "label": "Payment Processing",
        "missing": [
            {"category": "Transactions", "suggestion": "Handle payment failure with retry logic and user notification."},
            {"category": "Transactions", "suggestion": "Implement refund and chargeback workflows."},
            {"category": "Compliance",   "suggestion": "Ensure PCI-DSS compliance for cardholder data."},
            {"category": "Audit",        "suggestion": "Implement immutable transaction audit log."},
        ],
        "dependencies": [
            {"feature": "Payment",  "depends_on": "Order Management",      "reason": "Payments must be tied to a specific validated order."},
            {"feature": "Payment",  "depends_on": "Security / Compliance", "reason": "PCI-DSS requires encrypted card data and secure endpoints."},
            {"feature": "Payment",  "depends_on": "Notification Service",  "reason": "Users must receive confirmation/failure emails after payment."},
        ]
    },
    "upload": {
        "label": "File Management",
        "missing": [
            {"category": "Validation", "suggestion": "Define and enforce allowed file types and maximum file size."},
            {"category": "Security",   "suggestion": "Scan uploaded files for malware before storage."},
            {"category": "Storage",    "suggestion": "Define file retention policy and deletion workflow."},
        ],
        "dependencies": [
            {"feature": "File Upload", "depends_on": "Object Storage (e.g., S3)", "reason": "Scalable file storage requires external infrastructure."},
            {"feature": "File Upload", "depends_on": "CDN / Delivery Layer",       "reason": "Efficient file serving needs a content delivery network."},
        ]
    },
    "search": {
        "label": "Search & Discovery",
        "missing": [
            {"category": "UX",         "suggestion": "Define behavior and messaging for 'zero results' state."},
            {"category": "UX",         "suggestion": "Implement filter, sort, and pagination for search results."},
            {"category": "Performance","suggestion": "Specify acceptable search latency under full dataset load."},
        ],
        "dependencies": [
            {"feature": "Search", "depends_on": "Indexing Service (e.g., Elasticsearch)", "reason": "Full-text and faceted search requires indexed data."},
        ]
    },
    "notification": {
        "label": "Notification System",
        "missing": [
            {"category": "Delivery",     "suggestion": "Define notification channels: email, SMS, in-app, push."},
            {"category": "UX",           "suggestion": "Allow users to configure notification preferences."},
            {"category": "Reliability",  "suggestion": "Implement retry logic for failed notification deliveries."},
        ],
        "dependencies": [
            {"feature": "Notifications", "depends_on": "Email / SMS Gateway", "reason": "External communication requires transactional messaging providers."},
            {"feature": "Notifications", "depends_on": "User Preferences",    "reason": "Users must opt-in/out per notification type."},
        ]
    },
    "admin": {
        "label": "Admin Panel",
        "missing": [
            {"category": "Access Control", "suggestion": "Define admin roles and permission levels (super-admin, moderator, etc.)."},
            {"category": "Audit",          "suggestion": "Log all admin actions with actor, timestamp, and change diff."},
            {"category": "Security",       "suggestion": "Restrict admin panel access by IP allowlist or VPN."},
        ],
        "dependencies": [
            {"feature": "Admin Panel", "depends_on": "Role-Based Access Control (RBAC)", "reason": "Admin features require granular permission enforcement."},
            {"feature": "Admin Panel", "depends_on": "Audit Log Service",                "reason": "Every admin action must be traceable for compliance."},
        ]
    },
    "report": {
        "label": "Reporting & Analytics",
        "missing": [
            {"category": "Data",     "suggestion": "Define report types, data sources, and refresh intervals."},
            {"category": "Export",   "suggestion": "Allow report export in CSV, PDF, or Excel formats."},
            {"category": "Access",   "suggestion": "Define who can view which reports (role-based access)."},
        ],
        "dependencies": [
            {"feature": "Reports", "depends_on": "Analytics / Data Warehouse", "reason": "Reports require aggregated, queryable data pipelines."},
        ]
    },
    "api": {
        "label": "API / Integration",
        "missing": [
            {"category": "Security",    "suggestion": "Define API authentication mechanism (API key, OAuth 2.0, JWT)."},
            {"category": "Reliability", "suggestion": "Implement rate limiting and throttling per client/IP."},
            {"category": "Versioning",  "suggestion": "Define API versioning strategy (e.g., /v1/, /v2/)."},
            {"category": "Docs",        "suggestion": "Provide auto-generated API documentation (OpenAPI/Swagger)."},
        ],
        "dependencies": [
            {"feature": "Public API", "depends_on": "API Gateway",     "reason": "External APIs require centralized routing and auth enforcement."},
            {"feature": "Public API", "depends_on": "Rate Limit Store", "reason": "Rate limiting requires a fast shared counter (e.g., Redis)."},
        ]
    },
    "dashboard": {
        "label": "User Dashboard",
        "missing": [
            {"category": "UX",         "suggestion": "Define which KPIs and metrics are surfaced on the dashboard."},
            {"category": "Performance","suggestion": "Set a data freshness SLA (e.g., data must be < 5 min old)."},
            {"category": "Access",     "suggestion": "Define if the dashboard is personalized per user or role."},
        ],
        "dependencies": [
            {"feature": "Dashboard", "depends_on": "Data Aggregation Layer", "reason": "Real-time metrics require aggregated, optimized data sources."},
        ]
    },
    "role": {
        "label": "Role & Permission Management",
        "missing": [
            {"category": "Access",  "suggestion": "Define all system roles and their explicit permission sets."},
            {"category": "Audit",   "suggestion": "Log permission changes with actor and timestamp."},
            {"category": "UX",      "suggestion": "Provide a UI for administrators to assign and revoke roles."},
        ],
        "dependencies": [
            {"feature": "Role Management", "depends_on": "User Database", "reason": "Roles must be persisted and enforced consistently."},
        ]
    },
    "email": {
        "label": "Email Communication",
        "missing": [
            {"category": "Reliability",  "suggestion": "Handle SMTP failures with retry queue and dead-letter logging."},
            {"category": "Compliance",   "suggestion": "Include unsubscribe option per CAN-SPAM / GDPR regulations."},
            {"category": "Templates",    "suggestion": "Define transactional email templates with fallback plain-text."},
        ],
        "dependencies": [
            {"feature": "Email", "depends_on": "Transactional Email Provider (e.g., SendGrid, SES)", "reason": "Reliable email delivery requires an external provider."},
        ]
    },
    "order": {
        "label": "Order Management",
        "missing": [
            {"category": "Lifecycle",  "suggestion": "Define all order states and valid state transitions."},
            {"category": "UX",         "suggestion": "Provide order tracking and status updates to users."},
            {"category": "Edge Cases", "suggestion": "Handle partial fulfillment, cancellation, and return flows."},
        ],
        "dependencies": [
            {"feature": "Orders", "depends_on": "Inventory System",     "reason": "Orders must decrement available stock atomically."},
            {"feature": "Orders", "depends_on": "Payment Gateway",      "reason": "Orders cannot be confirmed without successful payment."},
            {"feature": "Orders", "depends_on": "Notification Service", "reason": "Users must be notified on order status changes."},
        ]
    },
    "cache": {
        "label": "Caching Layer",
        "missing": [
            {"category": "Invalidation","suggestion": "Define cache invalidation strategy (TTL, event-based, or manual)."},
            {"category": "Consistency", "suggestion": "Specify acceptable cache staleness window."},
            {"category": "Failover",    "suggestion": "Define behavior when cache is unavailable (fallback to DB)."},
        ],
        "dependencies": [
            {"feature": "Cache", "depends_on": "In-Memory Store (e.g., Redis)", "reason": "High-speed caching requires a dedicated in-memory data store."},
        ]
    },
    "database": {
        "label": "Data Layer",
        "missing": [
            {"category": "Backup",       "suggestion": "Define automated backup frequency and recovery point objective (RPO)."},
            {"category": "Migration",    "suggestion": "Establish a schema migration strategy (e.g., Flyway, Alembic)."},
            {"category": "Performance",  "suggestion": "Define indexing strategy for high-query-volume tables."},
        ],
        "dependencies": [
            {"feature": "Database", "depends_on": "Backup / DR Infrastructure", "reason": "Production databases require automated backup and disaster recovery."},
        ]
    },
}

# ============================================================
# CLASSIFIER — maps requirement text to FR / NFR / Constraint
# ============================================================
FR_KEYWORDS  = ["login", "register", "upload", "download", "search", "filter", "payment", "buy",
                 "add", "remove", "create", "delete", "edit", "view", "display", "submit",
                 "send", "receive", "notify", "track", "order", "report", "export", "import"]
NFR_KEYWORDS = ["fast", "scalable", "secure", "reliable", "available", "performance", "latency",
                 "throughput", "uptime", "real-time", "responsive", "concurrent", "efficient",
                 "robust", "backup", "recovery", "compliance"]
CON_KEYWORDS = ["must", "shall", "only", "within", "budget", "deadline", "regulation",
                 "GDPR", "HIPAA", "PCI", "ISO", "constraint", "limit", "maximum", "minimum"]

def classify_requirement(text):
    tl = text.lower()
    score_fr  = sum(1 for kw in FR_KEYWORDS  if kw in tl)
    score_nfr = sum(1 for kw in NFR_KEYWORDS if kw in tl)
    score_con = sum(1 for kw in CON_KEYWORDS if kw in tl)
    if score_con >= score_fr and score_con >= score_nfr:
        return "Constraint"
    elif score_nfr >= score_fr:
        return "Non-Functional"
    else:
        return "Functional"


# ============================================================
# MAIN ANALYSIS FUNCTION
# ============================================================
def analyze(text: str):
    issues               = []
    ambiguities          = []
    missing_requirements = []
    dependencies         = []
    modules_fired        = []

    text_lower = text.lower()

    # --- MODULE 1: Ambiguity Scanner ---
    for word, data in AMBIGUOUS_WORDS.items():
        pattern = r'\b' + re.escape(word.replace("-", "[- ]")) + r'\b'
        matches = list(re.finditer(pattern, text_lower))
        if matches:
            ambiguities.append({
                "word":       word,
                "severity":   data["severity"],
                "reason":     data["reason"],
                "suggestion": data["suggestion"],
                "count":      len(matches)
            })
            issues.append({
                "type":        "Ambiguity",
                "severity":    data["severity"],
                "description": f"Ambiguous term '{word}' detected. {data['reason']}",
                "impact":      f"Requirements using '{word}' cannot be verified during QA or acceptance testing."
            })

    if ambiguities:
        modules_fired.append({"module": "Ambiguity Scanner",     "status": "triggered", "findings": len(ambiguities)})
    else:
        modules_fired.append({"module": "Ambiguity Scanner",     "status": "clear",     "findings": 0})

    # --- MODULE 2: Context-Aware Pattern Matcher ---
    pattern_hits = 0
    for keyword, data in CONTEXT_PATTERNS.items():
        if keyword in text_lower:
            pattern_hits += 1
            for req in data.get("missing", []):
                missing_requirements.append({
                    "domain":    data["label"],
                    "category":  req["category"],
                    "suggestion": req["suggestion"]
                })
            for dep in data.get("dependencies", []):
                if not any(d["feature"] == dep["feature"] and d["depends_on"] == dep["depends_on"] for d in dependencies):
                    dependencies.append(dep)

    if pattern_hits:
        modules_fired.append({"module": "Pattern Matcher",       "status": "triggered", "findings": pattern_hits})
    else:
        modules_fired.append({"module": "Pattern Matcher",       "status": "clear",     "findings": 0})

    # --- MODULE 3: NFR Coverage Checker ---
    nfr_keywords = ["scale", "concurrent", "load", "uptime", "availability", "latency",
                     "throughput", "response time", "performance", "reliability", "backup"]
    has_nfrs = any(kw in text_lower for kw in nfr_keywords)
    if not has_nfrs:
        issues.append({
            "type":        "Missing NFRs",
            "severity":    "high",
            "description": "No measurable Non-Functional Requirements detected in the specification.",
            "impact":      "System architecture cannot be sized, tested, or validated without performance/reliability targets."
        })
        modules_fired.append({"module": "NFR Coverage Checker",  "status": "flagged",   "findings": 1})
    else:
        modules_fired.append({"module": "NFR Coverage Checker",  "status": "clear",     "findings": 0})

    # --- MODULE 4: Dependency Resolver ---
    modules_fired.append({"module": "Dependency Resolver",       "status": "triggered" if dependencies else "clear", "findings": len(dependencies)})

    # --- MODULE 5: Requirement Classifier ---
    req_class = classify_requirement(text)
    modules_fired.append({"module": "Requirement Classifier",    "status": "triggered", "findings": 1, "classification": req_class})

    return issues, ambiguities, missing_requirements, dependencies, modules_fired, req_class
