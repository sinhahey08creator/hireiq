import { useState } from 'react'
import UploadForm from './components/UploadForm'
import ResultsDashboard from './components/ResultsDashboard'
import { analyzeCandidate } from './api'

export default function App() {
  const [result, setResult] = useState(null)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState(null)

  const handleAnalyze = async (jobDescription, githubUsername, resumeFile) => {
    setLoading(true)
    setError(null)
    setResult(null)
    try {
      const data = await analyzeCandidate(jobDescription, githubUsername, resumeFile)
      setResult(data)
    } catch (err) {
      setError(err.message)
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="app">
      <header className="dossier-header">
        <p className="case-label">Case File · Automated Hiring Panel</p>
        <h1>HireIQ</h1>
        <p className="subtitle">Planner → Researcher → Critic → Tester</p>
      </header>

      <UploadForm onAnalyze={handleAnalyze} loading={loading} />

      {loading && (
        <p className="loading">
          Panel is reviewing the file — Planner, Researcher, Critic and Tester
          are working in sequence. Usually takes 10-20 seconds.
        </p>
      )}

      {error && <p className="error">⚠ {error}</p>}

      <ResultsDashboard data={result} />
    </div>
  )
}
