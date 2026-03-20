import React, { useState } from 'react';
import ScoreGauge from './ScoreGauge';

const ResultsPanel = ({ data, isDeep, loading }) => {
  if (loading) {
    return (
      <div className="results-container glass-panel loading-state">
        <div className="spinner"></div>
        <p>Analyzing requirements intelligently...</p>
      </div>
    );
  }

  if (!data) {
    return (
      <div className="results-container glass-panel empty-state">
        <h3>Intelligence Dashboard</h3>
        <p>Start typing or click Deep Analyze to view results.</p>
      </div>
    );
  }

  return (
    <div className="results-container glass-panel">
      <div className="score-section">
        <ScoreGauge score={data.confidence_score} breakdown={data.score_breakdown} />
      </div>

      <div className="analysis-sections">
        {isDeep && data.improved_requirements && (
          <CollapsibleSection title="🔵 Improved Version" defaultOpen={true}>
            <ul className="improved-list">
              {data.improved_requirements.map((req, i) => (
                <li key={i}>{req}</li>
              ))}
            </ul>
          </CollapsibleSection>
        )}

        <CollapsibleSection title={`🔴 Issues & Ambiguities (${data.issues?.length || 0})`} defaultOpen={true}>
          {data.issues?.length === 0 ? <p className="all-good">No major issues found.</p> : (
            <ul className="issue-list">
              {data.issues?.map((iss, i) => (
                <li key={i} className={`issue-item severity-${iss.severity}`}>
                  <strong>{iss.type}</strong>: {iss.description}
                  <div className="impact">Impact: {iss.impact}</div>
                </li>
              ))}
            </ul>
          )}
        </CollapsibleSection>

        <CollapsibleSection title={`🟠 Missing Logic & Flows (${data.missing_requirements?.length || 0})`} defaultOpen={true}>
           {data.missing_requirements?.length === 0 ? <p className="all-good">Flows look complete.</p> : (
            <ul className="missing-list">
              {data.missing_requirements?.map((req, i) => (
                <li key={i}>
                  <span className="badge">{req.category}</span> {req.suggestion}
                </li>
              ))}
            </ul>
          )}
        </CollapsibleSection>
        
        <CollapsibleSection title={`🌐 Architectural Dependencies (${data.dependencies?.length || 0})`} defaultOpen={false}>
           {data.dependencies?.length === 0 ? <p className="all-good">No external dependencies identified.</p> : (
            <ul className="dep-list">
              {data.dependencies?.map((dep, i) => (
                <li key={i}>
                  <strong>{dep.feature}</strong> depends on <strong>{dep.depends_on}</strong>
                  <div className="reason-text">{dep.reason}</div>
                </li>
              ))}
            </ul>
          )}
        </CollapsibleSection>

        {isDeep && data.final_clean_version && (
          <CollapsibleSection title="🟢 Final Clean Output (JSON / exportable)" defaultOpen={false}>
            <pre className="code-block">
              {data.final_clean_version.join('\n')}
            </pre>
          </CollapsibleSection>
        )}
        
      </div>
    </div>
  );
};

const CollapsibleSection = ({ title, children, defaultOpen }) => {
  const [open, setOpen] = useState(defaultOpen);
  return (
    <div className="section-card">
      <div className="section-header" onClick={() => setOpen(!open)}>
        <h4>{title}</h4>
        <span>{open ? '▼' : '▶'}</span>
      </div>
      {open && <div className="section-body">{children}</div>}
    </div>
  );
};

export default ResultsPanel;
