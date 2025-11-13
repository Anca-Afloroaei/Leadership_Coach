import type { GeneratePlanResponse, DevelopmentPlanSummary } from '@/types/devplans';

const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

export interface GeneratePlanPayload {
  user_id: string;
  user_answers_record_id: string;
  focus_areas: string[];
  duration_days: number;
  role: string;
  industry: string;
  years_experience: number;
}

export async function generateDevelopmentPlan(payload: GeneratePlanPayload): Promise<GeneratePlanResponse> {
  const res = await fetch(`${API_BASE_URL}/devplans/generate`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    credentials: 'include',
    body: JSON.stringify(payload),
  });
  if (!res.ok) {
    let msg = res.statusText;
    try { const data = await res.json(); msg = data?.detail || msg; } catch {}
    throw new Error(`Failed to generate plan: ${msg}`);
  }
  return res.json();
}

export async function fetchDevelopmentPlanByUserAnswers(userAnswersRecordId: string): Promise<GeneratePlanResponse> {
  const res = await fetch(`${API_BASE_URL}/devplans/user_answers/${encodeURIComponent(userAnswersRecordId)}`, {
    method: 'GET',
    credentials: 'include',
  });
  if (!res.ok) {
    let msg = res.statusText;
    try { const data = await res.json(); msg = data?.detail || msg; } catch {}
    throw new Error(`Failed to fetch development plan: ${msg}`);
  }
  return res.json();
}

export async function fetchDevelopmentPlanSummaries(): Promise<DevelopmentPlanSummary[]> {
  const res = await fetch(`${API_BASE_URL}/devplans/`, {
    method: 'GET',
    credentials: 'include',
  });
  if (!res.ok) {
    if (res.status === 404) return [];
    let msg = res.statusText;
    try { const data = await res.json(); msg = data?.detail || msg; } catch {}
    throw new Error(`Failed to fetch development plans: ${msg}`);
  }
  return res.json();
}

export async function downloadDevelopmentPlanPdf(
  userAnswersRecordId: string,
): Promise<Blob> {
  const res = await fetch(
    `${API_BASE_URL}/devplans/user_answers/${encodeURIComponent(userAnswersRecordId)}/pdf`,
    {
      method: 'GET',
      credentials: 'include',
    },
  );
  if (!res.ok) {
    let msg = res.statusText;
    try {
      const data = await res.json();
      msg = data?.detail || msg;
    } catch {}
    throw new Error(`Failed to download development plan: ${msg}`);
  }
  return res.blob();
}
