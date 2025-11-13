import type { UserResults } from '@/types/results';

const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

// Fetch all resutls for a user by their user_answers_record_id
// This is used to retrieve the results of a completed questionnaire
export async function fetchResults(userAnswersRecordId: string): Promise<UserResults> {
  const response = await fetch(`${API_BASE_URL}/results/${userAnswersRecordId}`, {
    method: 'GET',
    credentials: 'include'
  });
  if (!response.ok) {
    throw new Error(`Failed to fetch results: ${response.statusText}`);
  }
  return response.json();
}





