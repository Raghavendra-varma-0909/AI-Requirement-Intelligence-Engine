import React, { useState } from 'react';
import ScoreGauge from './ScoreGauge';
import DependencyGraph from './DependencyGraph';

const Section = ({ title, count, children, defaultOpen = false }) => {
  const [open, setOpen] = useState(defaultOpen);
  return (
    <div className="section-card">
      <div className="section-header" onClick={() => setOpen(o => !o)}>
        <h4>{title}</h4>
        <span>{count !== undefined ? `${count} found` : ''} {open ? '▲' : '▼'}</span>
      </div>
      {open && <div className="section-body">{children}</div>}
    </div>
  );
};

const ResultsPanel = ({ data, isDeep, loading }) => {
  if (loading) {
    return (
      <div className="results-container glass-panel loading-state">
        <div className="spinner" />
        <p>Running deep analysis pipeline...</p>
      </div>
    );
  }

  if (!data) {
    return (
      <div className="results-container glass-panel empty-state">
        <p style={{ fontSize: '2rem', marginBottom: 8 }}>⚙️</p>
        <p>Start typing to activate the engine.</p>
        <p style={{ fontSize: '0.82rem', color: 'var(--text-muted)' }}>Click <strong>Deep Analyze</strong> for full pipeline output.</p>
      </div>
    );
  }

  const { issues, ambiguities, missing_requirements, dependencies,
          strong_features, improved_requirements, final_clean_version,
          confidence_score, score_breakdown } = data;

  const nfrMissing = (missing_requirements || []).filter(m => m.domain === 'Non-Functional Requirements');
  const flowMissing = (missing_requirements || []).filter(m => m.domain !== 'Non-Functional Requirements');

  return (
    <div className="results-container glass-panel">
      {/* Score */}
      <div className="score-section">
        <div className="score-widget">
          <div className="gauge-container">
            <ScoreGauge score={confidence_score} />
            <div className="score-label">Quality Score</div>
          </div>
          <div className="breakdown">
            <h5>Score Breakdown</h5>
            <div className="breakdown-item">Base Score <span>100</span></div>
            {score_breakdown?.ambiguity_penalty !== 0 &&
              <div className="breakdown-item penalty">Ambiguities <span>{score_breakdown?.ambiguity_penalty}</span></div>}
            {score_breakdown?.missing_flow_penalty !== 0 &&
              <div className="breakdown-item penalty">Missing Flows <span>{score_breakdown?.missing_flow_penalty}</span></div>}
            {score_breakdown?.missing_nfr_penalty !== 0 &&
              <div className="breakdown-item penalty">Missing NFRs <span>{score_breakdown?.missing_nfr_penalty}</span></div>}
            {score_breakdown?.completeness_penalty !== 0 &&
              <div className="breakdown-item penalty">Completeness <span>{score_breakdown?.completeness_penalty}</span></div>}
            {score_breakdown?.strength_bonus > 0 &&
              <div className="breakdown-item bonus">Strength Bonus <span>+{score_breakdown?.strength_bonus}</span></div>}
            {score_breakdown?.dependency_bonus > 0 &&
              <div className="breakdown-item bonus">Dep. Bonus <span>+{score_breakdown?.dependency_bonus}</span></div>}
          </div>
        </div>
      </div>

      <div className="analysis-sections">
        {/* Strength Features */}
        {strong_features?.length > 0 && (
          <Section title="✅ Detected Strengths" count={strong_features.length} defaultOpen={true}>
            <div className="strength-grid">
              {strong_features.map((f, i) => (
                <span key={i} className="strength-badge">✅ {f.label} <em>+{f.bonus}</em></span>
              ))}
            </div>
          </Section>
        )}

        {/* Issues & Ambiguities */}
        {issues?.length > 0 && (
          <Section title="⚠️ Issues & Ambiguities" count={issues.length}>
            <ul className="issue-list">
              {issues.map((iss, i) => (
                <li key={i} className={`issue-item severity-${iss.severity}`}>
                  <strong>[{iss.severity?.toUpperCase()}]</strong> {iss.description}
                  <div className="impact">↳ {iss.impact}</div>
                </li>
              ))}
            </ul>
          </Section>
        )}

        {/* Missing Functional Flows */}
        {flowMissing?.length > 0 && (
          <Section title="🔍 Missing Functional Flows" count={flowMissing.length}>
            <ul className="missing-list">
              {flowMissing.map((m, i) => (
                <li key={i}>
                  <span className="badge">{m.domain}</span>
                  <span className="badge" style={{ background: 'rgba(59,130,246,0.1)', color: '#93c5fd', borderColor: 'rgba(59,130,246,0.2)' }}>{m.category}</span>
                  {m.suggestion}
                </li>
              ))}
            </ul>
          </Section>
        )}

        {/* NFR Suggestions — consultant-grade */}
        {nfrMissing?.length > 0 && (
          <Section title="📐 NFR Recommendations" count={nfrMissing.length}>
            <ul className="missing-list">
              {nfrMissing.map((m, i) => (
                <li key={i}>
                  <span className="badge" style={{ background: 'rgba(251,146,60,0.1)', color: '#fdba74', borderColor: 'rgba(251,146,60,0.2)' }}>{m.category}</span>
                  {m.suggestion}
                </li>
              ))}
            </ul>
          </Section>
        )}

        {/* Dependency Graph */}
        {dependencies?.length > 0 && (
          <Section title="🔗 Dependency Graph" count={dependencies.length}>
            <DependencyGraph dependencies={dependencies} />
          </Section>
        )}

        {/* Side-by-side Improved View */}
        {isDeep && (improved_requirements?.length > 0 || final_clean_version) && (
          <Section title="✏️ Original vs Improved" defaultOpen={true}>
            <div className="side-by-side">
              <div className="side-original">
                <div className="side-label">📄 Original</div>
                <div className="side-content original-text">{data.text || 'Your input above'}</div>
              </div>
              <div className="side-divider">→</div>
              <div className="side-improved">
                <div className="side-label">⚡ Improved</div>
                {improved_requirements?.length > 0 ? (
                  <ul className="improved-list">
                    {improved_requirements.map((req, i) => (
                      <li key={i}>{req}</li>
                    ))}
                  </ul>
                ) : null}
                {final_clean_version && (
                  <div className="code-block" style={{ marginTop: 10 }}>{final_clean_version}</div>
                )}
              </div>
            </div>
          </Section>
        )}
      </div>
    </div>
  );
};

export default ResultsPanel;
