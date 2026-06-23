// Change this if your backend runs on a different host/port
const API_BASE = "https://hireiq-production-d0b1.up.railway.app";

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
