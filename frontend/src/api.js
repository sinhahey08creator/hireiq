// Change this if your backend runs on a different host/port
const API_BASE = "http://localhost:8000";

export async function analyzeCandidate(jobDescription, githubUsername, resumeFile) {
  const formData = new FormData();
  formData.append("job_description", jobDescription);
  formData.append("github_username", githubUsername);
  formData.append("resume", resumeFile);

  const response = await fetch(`${API_BASE}/analyze`, {
    method: "POST",
    body: formData,
  });

  if (!response.ok) {
    const text = await response.text();
    throw new Error(`Analysis failed: ${text}`);
  }

  return response.json();
}
