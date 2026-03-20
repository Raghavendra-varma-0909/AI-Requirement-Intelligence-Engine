import { useState, useEffect, useRef } from 'react'
import './App.css'
import HighlightEditor from './components/HighlightEditor'
import ResultsPanel from './components/ResultsPanel'
import EnginePipeline from './components/EnginePipeline'

const API_BASE = import.meta.env.VITE_API_URL || 'http://localhost:8001'

function App() {
  const [text, setText] = useState("Build a fast and user-friendly e-commerce website where users can login and buy products.")
  const [liveData, setLiveData] = useState(null)
  const [deepData, setDeepData] = useState(null)
  const [isAnalyzing, setIsAnalyzing] = useState(false)
  const debounceRef = useRef(null)

  const handleTextChange = (newText) => {
    setText(newText)
    if (debounceRef.current) clearTimeout(debounceRef.current)
    debounceRef.current = setTimeout(() => fetchLiveCritique(newText), 500)
  }

  const fetchLiveCritique = async (currentText) => {
    if (!currentText.trim()) return
    try {
      const res = await fetch(`${API_BASE}/api/analyze/live`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ text: currentText, privacy_mode: false })
      })
      const data = await res.json()
      setLiveData(data)
    } catch (e) { console.error("Live analysis failed", e) }
  }

  const handleDeepAnalyze = async () => {
    if (!text.trim()) return
    setIsAnalyzing(true)
    setDeepData(null)
    try {
      const res = await fetch(`${API_BASE}/api/analyze/deep`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ text, privacy_mode: false })
      })
      const data = await res.json()
      setDeepData(data)
      setLiveData(data)
    } catch (e) { console.error("Deep analysis failed", e) }
    finally { setIsAnalyzing(false) }
  }

  useEffect(() => { fetchLiveCritique(text) }, [])

  const activeData = deepData || liveData

  return (
    <div className="app-container">
      <header className="app-header glass-panel">
        <div className="header-left">
          <div className="logo">
            <span className="logo-icon">⚙️</span>
            <span className="logo-text">AI Requirement Intelligence Engine</span>
          </div>
          <div className="header-tagline">Hybrid Rule-Based + AI Analysis Pipeline</div>
        </div>
        <div className="header-actions">
          {activeData && (
            <div className="score-pill" style={{ color: activeData.confidence_score >= 80 ? '#34d399' : activeData.confidence_score >= 50 ? '#fb923c' : '#f87171' }}>
              Quality Score: <strong>{activeData.confidence_score}/100</strong>
            </div>
          )}
          <button className="button-primary" onClick={handleDeepAnalyze} disabled={isAnalyzing}>
            {isAnalyzing ? <><span className="btn-spinner"></span> Analyzing...</> : '⚡ Deep Analyze'}
          </button>
        </div>
      </header>

      {activeData?.modules_fired && (
        <EnginePipeline
          modules={activeData.modules_fired}
          classification={activeData.requirement_classification}
        />
      )}

      <main className="dashboard">
        <div className="left-panel">
          <HighlightEditor text={text} onChange={handleTextChange} liveData={liveData} />
        </div>
        <div className="right-panel">
          <ResultsPanel data={activeData} isDeep={!!deepData} loading={isAnalyzing} />
        </div>
      </main>
    </div>
  )
}

export default App
