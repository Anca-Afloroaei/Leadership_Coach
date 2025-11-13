import type { UserAnswersSubmission, UserAnswersUpdate, CompletedAnswersSummary } from '@/types/user_answers';

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

// Fetch a user_answers record by its ID
export async function fetchUserAnswersById(id: string) {
  const res = await fetch(`${API_BASE_URL}/user_answers/${encodeURIComponent(id)}`, {
    method: 'GET',
    credentials: 'include'
  });
  if (!res.ok) {
    let msg = res.statusText;
    try { const data = await res.json(); msg = data?.detail || msg; } catch {}
    throw new Error(`Failed to fetch user answers: ${msg}`);
  }
  return res.json();
}

// Fetch the latest completed user_answers for a questionnaire (completed_at != null)
export async function fetchLatestCompletedUserAnswers(params: { questionnaire_id: string }) {
  const res = await fetch(`${API_BASE_URL}/user_answers/latest_completed/${encodeURIComponent(params.questionnaire_id)}` , {
    method: 'GET',
    credentials: 'include'
  });
  if (!res.ok) {
    // Return null gracefully on 404 or other non-OK
    return null;
  }
  return res.json();
}

// List completed user_answers for the authenticated user (optionally filter by questionnaire)
export async function fetchCompletedUserAnswers(params?: { questionnaire_id?: string; limit?: number; offset?: number }): Promise<CompletedAnswersSummary[] | null> {
  const qs = new URLSearchParams();
  if (params?.questionnaire_id) qs.set('questionnaire_id', params.questionnaire_id);
  if (typeof params?.limit === 'number') qs.set('limit', String(params.limit));
  if (typeof params?.offset === 'number') qs.set('offset', String(params.offset));
  const url = `${API_BASE_URL}/user_answers/completed${qs.toString() ? `?${qs.toString()}` : ''}`;
  const res = await fetch(url, { method: 'GET', credentials: 'include' });
  if (!res.ok) {
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
