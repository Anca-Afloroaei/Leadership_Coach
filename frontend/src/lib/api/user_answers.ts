import type { UserAnswersSubmission, UserAnswersUpdate } from '@/types/user_answers';

const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';


export async function createUserAnswers(submission: UserAnswersSubmission) {
  const res = await fetch(`${API_BASE_URL}/user_answers/`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json'
    },
    body: JSON.stringify(submission),
    credentials: 'include'
  });
  if (!res.ok) {
    let msg = res.statusText;
    try { const data = await res.json(); msg = data?.detail || msg; } catch {}
    throw new Error(`Failed to create user answers: ${msg}`);
  }
  return res.json();
}

export async function updateUserAnswers(update: UserAnswersUpdate) {
  const res = await fetch(`${API_BASE_URL}/user_answers/`, {
    method: 'PATCH',
    headers: {
      'Content-Type': 'application/json'
    },
    body: JSON.stringify(update),
    credentials: 'include'
  });
  if (!res.ok) {
    let msg = res.statusText;
    try { const data = await res.json(); msg = data?.detail || msg; } catch {}
    throw new Error(`Failed to update user answers: ${msg}`);
  }
  return res.json();
}

// Fetch the most recent user_answers for a questionnaire within a given window (days)
export async function fetchRecentUserAnswers(params: { questionnaire_id: string; days?: number }) {
  const days = params.days ?? 7;
  const res = await fetch(`${API_BASE_URL}/user_answers/recent/${encodeURIComponent(params.questionnaire_id)}?days=${encodeURIComponent(days)}`, {
    method: 'GET',
    credentials: 'include'
  });
  if (!res.ok) {
    // If endpoint not found, return null gracefully
    return null;
  }
  return res.json();
}

// export async function completeUserAnswers(id: string) {
//   const res = await fetch(`${API_BASE_URL}/complete`, {
//     method: 'PATCH',
//     headers: {
//       'Content-Type': 'application/json'
//     },
//     body: JSON.stringify({ id })
//   });
//   if (!res.ok) {
//     throw new Error(`Failed to complete user answers: ${res.statusText}`);
//   }
//   return res.json();
// }