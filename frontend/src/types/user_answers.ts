    

export interface UserAnswers {
    id: string;
    user_id: string;
    questionnaire_id: string;
    answers: Record<string, string>; // Dict of answers provided by the user
    created_at: string;
    updated_at: string;
    completed_at: string | null;
}


export interface UserAnswersSubmission {
    user_id: string;
    questionnaire_id: string;
    answers: Record<string, string>;
}


export interface UserAnswersUpdate{
    id: string;
    answers?: Record<string, string>;
    completed_at?: string; // optional
}

