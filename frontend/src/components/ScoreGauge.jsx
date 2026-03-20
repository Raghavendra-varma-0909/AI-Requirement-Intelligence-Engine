import React from 'react';

const ScoreGauge = ({ score, breakdown }) => {
  // Determine color based on score
  let color = 'var(--error-red)';
  if (score >= 80) color = 'var(--success-green)';
  else if (score >= 50) color = 'var(--warn-orange)';

  return (
    <div className="score-widget">
      <div className="gauge-container">
        <svg viewBox="0 0 36 36" className="circular-chart">
          <path className="circle-bg"
            d="M18 2.0845
              a 15.9155 15.9155 0 0 1 0 31.831
              a 15.9155 15.9155 0 0 1 0 -31.831"
          />
          <path className="circle"
            strokeDasharray={`${score}, 100`}
            stroke={color}
            d="M18 2.0845
              a 15.9155 15.9155 0 0 1 0 31.831
              a 15.9155 15.9155 0 0 1 0 -31.831"
          />
          <text x="18" y="20.35" className="percentage" fill="var(--text-primary)">{score}</text>
        </svg>
        <div className="score-label">Quality Score</div>
      </div>
      
      {breakdown && (
        <div className="breakdown">
          <h5>Score Breakdown</h5>
          <div className="breakdown-item">
            <span>Base Score</span>
            <span>100</span>
          </div>
          {breakdown.ambiguity_penalty < 0 && (
            <div className="breakdown-item penalty">
              <span>Ambiguities</span>
              <span>{breakdown.ambiguity_penalty}</span>
            </div>
          )}
          {breakdown.missing_flow_penalty < 0 && (
            <div className="breakdown-item penalty">
              <span>Missing Flows</span>
              <span>{breakdown.missing_flow_penalty}</span>
            </div>
          )}
           {breakdown.missing_nfr_penalty < 0 && (
            <div className="breakdown-item penalty">
              <span>Missing NFRs</span>
              <span>{breakdown.missing_nfr_penalty}</span>
            </div>
          )}
        </div>
      )}
    </div>
  );
};

export default ScoreGauge;
