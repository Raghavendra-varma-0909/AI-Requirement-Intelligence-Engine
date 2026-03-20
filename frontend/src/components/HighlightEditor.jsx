import React from 'react';

const HighlightEditor = ({ text, onChange, liveData }) => {

  const getHighlights = () => {
    let highlights = [];

    // 🔴 RED — Ambiguous terms
    if (liveData?.ambiguities) {
      liveData.ambiguities.forEach(amb => {
        const regex = new RegExp(`\\b${amb.word.replace(/[-\/]/g, '[\\-\\/]')}\\b`, 'gi');
        let match;
        while ((match = regex.exec(text)) !== null) {
          highlights.push({
            start: match.index,
            end: match.index + match[0].length,
            type: 'ambiguity',
            className: 'highlight-red',
            tooltip: `⚠️ Ambiguous: ${amb.reason}\n💡 Suggest: ${amb.suggestion}`,
          });
        }
      });
    }

    // 🟢 GREEN — Strength signals (detected engineering features)
    if (liveData?.strong_features) {
      liveData.strong_features.forEach(feat => {
        const regex = new RegExp(`\\b${feat.term.replace(/[-\/]/g, '[\\-\\/]')}\\b`, 'gi');
        let match;
        while ((match = regex.exec(text)) !== null) {
          // Don't overlap with red highlights
          highlights.push({
            start: match.index,
            end: match.index + match[0].length,
            type: 'strength',
            className: 'highlight-green',
            tooltip: `✅ Strong Feature: ${feat.label} (+${feat.bonus} pts)`,
          });
        }
      });
    }

    // Sort and de-overlap: red takes priority over green
    highlights.sort((a, b) => a.start - b.start || (a.type === 'ambiguity' ? -1 : 1));

    // Remove overlaps
    const deduped = [];
    let lastEnd = 0;
    for (const hl of highlights) {
      if (hl.start >= lastEnd) {
        deduped.push(hl);
        lastEnd = hl.end;
      }
    }
    return deduped;
  };

  const renderHighlightedText = () => {
    const highlights = getHighlights();
    if (highlights.length === 0) return text;

    let elements = [];
    let lastIndex = 0;

    highlights.forEach((hl, i) => {
      if (hl.start < lastIndex) return;
      if (hl.start > lastIndex) {
        elements.push(<span key={`text-${i}`}>{text.substring(lastIndex, hl.start)}</span>);
      }
      elements.push(
        <span key={`hl-${i}`} className={`highlight ${hl.className}`} title={hl.tooltip}>
          {text.substring(hl.start, hl.end)}
        </span>
      );
      lastIndex = hl.end;
    });

    if (lastIndex < text.length) {
      elements.push(<span key="tail">{text.substring(lastIndex)}</span>);
    }
    return elements;
  };

  const ambigCount = liveData?.ambiguities?.length || 0;
  const strengthCount = liveData?.strong_features?.length || 0;

  return (
    <div className="editor-container glass-panel">
      <div className="editor-header">
        <h3>📝 Requirement Input</h3>
        <span className="live-status">
          {liveData ? '🟢 Live Analysis Active' : '⚪ Waiting for input...'}
        </span>
      </div>
      <div className="editor-wrapper">
        <div className="highlight-layer" aria-hidden="true">
          {renderHighlightedText()}
        </div>
        <textarea
          className="text-input"
          value={text}
          onChange={(e) => onChange(e.target.value)}
          spellCheck="false"
          placeholder="Type your software requirements here..."
        />
      </div>
      <div className="editor-footer">
        <span className="hint">
          🔴 Ambiguous terms ({ambigCount}) &nbsp;·&nbsp; 🟢 Strength signals ({strengthCount}) &nbsp;·&nbsp; Hover any highlighted word
        </span>
      </div>
    </div>
  );
};

export default HighlightEditor;
