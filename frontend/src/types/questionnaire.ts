// TypeScript interfaces for Questionnaire API data models

export interface Questionnaire {
  id: string;
  title: string;
  description: string | null;
  questions: string[]; // Array of question IDs
  is_active: boolean;
  created_at: string;
  updated_at: string;
}

export interface Question {
  id: string;
  question_text: string;
  competency: string | null;
  explanation: string | null;
  is_active: boolean;
  created_at: string;
  updated_at: string;
}

export interface Answer {
  id: string;
  question_id: string;
  answer_text: string;
  score_value: number;
  created_at: string;
  updated_at: string;
}

export interface UserResponse {
  question_id: string;
  answer_id: string | null;
  score_value: number;
}

export interface QuestionnaireSubmission {
  questionnaire_id: string;
  responses: UserResponse[];
  total_score: number;
  submitted_at: string;
}