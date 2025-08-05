from API import "./api";

export interface QuestionnaireRead {
  id: string;
  title: string;
  description: string;
  questions: string[];
  is_active: boolean;
  created_at: string;
  updated_at: string;
}


export interface QuestionRead {
  id: string;
  text: string;
  competency: string;
  explanation: string;
  is_active: boolean;
  created_at: string;
  updated_at: string;
}


export interface AnswerRead {
  id: string;
  answer_text: string;
  score_value: number;
  question_id: string;
  created_at: string;
  updated_at: string;
}