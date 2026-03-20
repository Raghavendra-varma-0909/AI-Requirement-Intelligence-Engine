import React from 'react';

const STATUS_CONFIG = {
  triggered: { icon: '🔥', color: '#f97316', label: 'Triggered' },
  flagged:   { icon: '🚩', color: '#ef4444', label: 'Flagged'   },
  clear:     { icon: '✅', color: '#10b981', label: 'Clear'     },
};

const EnginePipeline = ({ modules, classification }) => {
  if (!modules || modules.length === 0) return null;

  const classColors = {
    'Functional':     { bg: 'rgba(59,130,246,0.15)', border: 'rgba(59,130,246,0.4)', text: '#93c5fd' },
    'Non-Functional': { bg: 'rgba(168,85,247,0.15)', border: 'rgba(168,85,247,0.4)', text: '#d8b4fe' },
    'Constraint':     { bg: 'rgba(251,146,60,0.15)', border: 'rgba(251,146,60,0.4)', text: '#fdba74' },
  };
  const cls = classColors[classification] || classColors['Functional'];

  return (
    <div className="engine-pipeline">
      <div className="pipeline-header">
        <span className="pipeline-title">⚙️ Engine Pipeline</span>
        {classification && (
          <span className="req-classification" style={{ background: cls.bg, border: `1px solid ${cls.border}`, color: cls.text }}>
            {classification} Requirement
          </span>
        )}
      </div>
      <div className="pipeline-modules">
        {modules.map((mod, i) => {
          const cfg = STATUS_CONFIG[mod.status] || STATUS_CONFIG['clear'];
          return (
            <div key={i} className="pipeline-module" style={{ borderColor: `${cfg.color}33` }}>
              <span className="module-icon">{cfg.icon}</span>
              <div className="module-info">
                <span className="module-name">{mod.module}</span>
                <span className="module-status" style={{ color: cfg.color }}>{cfg.label}</span>
              </div>
              <span className="module-count" style={{ color: cfg.color }}>
                {mod.findings > 0 ? `${mod.findings} found` : (mod.classification || '—')}
              </span>
            </div>
          );
        })}
      </div>
    </div>
  );
};

export default EnginePipeline;
