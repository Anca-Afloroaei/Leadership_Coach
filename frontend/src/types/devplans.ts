export interface DevelopmentPlan {
  id: string;
  user_id: string;
  user_answers_record_id: string | null;
  goal: string;
  description: string | null;
  start_date: string;
  end_date: string;
  status: string;
  progress: number;
  resources: string | null;
  challenges: string | null;
  next_steps: string | null;
  action_items: string;
  target_date: string;
  created_at: string;
  updated_at: string;
  plan_markdown: string;
}

export interface GeneratePlanResponse {
  plan: DevelopmentPlan;
  plan_markdown: string;
}

export interface DevelopmentPlanSummary {
  plan_id: string;
  user_answers_record_id: string;
  questionnaire_id: string;
  questionnaire_title: string;
  created_at: string;
}
