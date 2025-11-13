

export interface UserResults {
  user_answers_record_id: string;
  user_id: string;
  questionnaire_id: string;
  // competency -> percentage (0-100)
  results: Record<string, number>;
  completed_at: string | null;
}
