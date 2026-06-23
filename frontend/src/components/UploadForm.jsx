import { useState } from 'react'

export default function UploadForm({ onAnalyze, loading }) {
  const [jobDescription, setJobDescription] = useState("")
  const [githubUsername, setGithubUsername] = useState("")
  const [resumeFile, setResumeFile] = useState(null)

  const handleSubmit = (e) => {
    e.preventDefault()
    if (!jobDescription.trim() || !resumeFile) {
      alert("Please provide a job description and upload a resume PDF.")
      return
    }
    onAnalyze(jobDescription, githubUsername, resumeFile)
  }

  return (
    <form className="card upload-form" onSubmit={handleSubmit}>
      <h2><span className="tab-number">IN</span> Case Intake</h2>

      <label className="field-label" htmlFor="jd">Job Description</label>
      <textarea
        id="jd"
        rows={6}
        placeholder="Paste the role's requirements here..."
        value={jobDescription}
        onChange={(e) => setJobDescription(e.target.value)}
      />

      <label className="field-label" htmlFor="resume">Candidate Resume (PDF)</label>
      <input
        id="resume"
        type="file"
        accept="application/pdf"
        onChange={(e) => setResumeFile(e.target.files[0])}
      />

      <label className="field-label" htmlFor="github">GitHub Handle (optional)</label>
      <input
        id="github"
        type="text"
        placeholder="e.g. octocat"
        value={githubUsername}
        onChange={(e) => setGithubUsername(e.target.value)}
      />

      <button type="submit" disabled={loading}>
        {loading ? "Reviewing..." : "Begin Review"}
      </button>
    </form>
  )
}
