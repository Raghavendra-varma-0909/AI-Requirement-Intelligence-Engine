import React from 'react';

const HighlightEditor = ({ text, onChange, liveData }) => {

  const getHighlights = () => {
    if (!liveData || !liveData.ambiguities) return [];
    let highlights = [];

    liveData.ambiguities.forEach(amb => {
      const regex = new RegExp(`\\b${amb.word}\\b`, 'gi');
      let match;
      while ((match = regex.exec(text)) !== null) {
        highlights.push({
          start: match.index,
          end: match.index + match[0].length,
          type: 'ambiguity',
          tooltip: `⚠️ Ambiguous: ${amb.reason} → ${amb.suggestion}`,
          word: amb.word
        });
      }
    });

    highlights.sort((a, b) => a.start - b.start);
    return highlights;
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
        <span key={`hl-${i}`} className="highlight highlight-red" title={hl.tooltip}>
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
        <span className="hint">🔴 Red underlines = ambiguous terms · Hover for suggestions</span>
      </div>
    </div>
  );
};

export default HighlightEditor;
