import React from 'react';

const DependencyGraph = ({ dependencies }) => {
  if (!dependencies || dependencies.length === 0) return null;

  // Group dependencies by feature chain
  const groups = {};
  dependencies.forEach(dep => {
    if (!groups[dep.feature]) groups[dep.feature] = [];
    groups[dep.feature].push(dep);
  });

  return (
    <div className="dep-graph">
      {Object.entries(groups).map(([feature, deps], gi) => (
        <div key={gi} className="dep-chain">
          <div className="dep-chain-row">
            <span className="dep-node dep-node-root">{feature}</span>
            {deps.map((dep, di) => (
              <React.Fragment key={di}>
                <span className="dep-arrow">→</span>
                <span className="dep-node dep-node-leaf" title={dep.reason}>
                  {dep.depends_on}
                </span>
              </React.Fragment>
            ))}
          </div>
          {deps.map((dep, di) => (
            <div key={di} className="dep-reason">
              <span className="dep-reason-arrow">↳</span>
              <em>{dep.depends_on}:</em> {dep.reason}
            </div>
          ))}
        </div>
      ))}
    </div>
  );
};

export default DependencyGraph;
