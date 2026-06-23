function asciiBar(score) {
  const total = 20
  const filled = Math.round((score / 100) * total)
  return "█".repeat(filled) + "░".repeat(total - filled)
}

export default function ResultsDashboard({ data }) {
  if (!data) return null

  const { planner, researcher, critic, tester, final_score, recommendation } = data

  const tier =
    final_score >= 75 ? "strong" : final_score >= 50 ? "medium" : "weak"

  const stampLabel =
    tier === "strong" ? "APPROVED" : tier === "medium" ? "CONDITIONAL" : "REJECTED"

  return (
    <div className="results">
      {/* Planner */}
      <section className="card">
        <h2><span className="tab-number">01</span> Planner — Required Skills</h2>
        {planner?.skills?.length > 0 ? (
          <ul>
            {planner.skills.map((s, i) => (
              <li key={i}>
                {s.name} <span className="skill-weight">— weight {s.weight}%</span>
              </li>
            ))}
          </ul>
        ) : (
          <p className="muted">No skills extracted.</p>
        )}
      </section>

      {/* Researcher */}
      <section className="card">
        <h2><span className="tab-number">02</span> Researcher — Candidate Match</h2>
        <p className="big-stat">
          Match Score: <strong>{researcher?.score ?? "-"}%</strong>
        </p>
        <p className="ascii-bar">{asciiBar(researcher?.score ?? 0)}</p>
        <p style={{ marginTop: 12 }}>
          <span className="clean-item">✓ Matched:</span> {researcher?.matched?.join(", ") || "None"}
        </p>
        <p>
          <span className="red-flag-item" style={{ paddingLeft: 0 }}>✗ Missing:</span>{" "}
          {researcher?.missing?.join(", ") || "None"}
        </p>
      </section>

      {/* Critic */}
      <section className="card">
        <h2><span className="tab-number">03</span> Critic — Red Flags</h2>
        {critic?.red_flags?.length > 0 ? (
          <ul style={{ listStyle: "none", paddingLeft: 0 }}>
            {critic.red_flags.map((flag, i) => (
              <li key={i} className="red-flag-item">{flag}</li>
            ))}
          </ul>
        ) : (
          <p className="clean-item">No issues found — record is clean.</p>
        )}
      </section>

      {/* Tester */}
      <section className="card">
        <h2><span className="tab-number">04</span> Tester — Interview Questions</h2>
        {tester?.questions?.length > 0 ? (
          <ol>
            {tester.questions.map((q, i) => (
              <li key={i}>{q}</li>
            ))}
          </ol>
        ) : (
          <p className="muted">No questions generated.</p>
        )}
      </section>

      {/* Final verdict — rubber stamp */}
      <section className="card final">
        <div className={`stamp ${tier}`}>
          <span className="stamp-score">{final_score}/100</span>
          <span className="stamp-rec">{stampLabel} — {recommendation}</span>
        </div>
        <p className="case-footer">— END OF CASE FILE —</p>
      </section>
    </div>
  )
}
