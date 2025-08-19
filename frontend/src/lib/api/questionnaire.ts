// API client functions for questionnaire endpoints

import { Questionnaire, Question, Answer } from '@/types/questionnaire';

const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

// Fetch a questionnaire by ID
export async function fetchQuestionnaire(questionnaireId: string): Promise<Questionnaire> {
  const response = await fetch(`${API_BASE_URL}/questionnaires/${questionnaireId}`);
  if (!response.ok) {
    throw new Error(`Failed to fetch questionnaire: ${response.statusText}`);
  }
  return response.json();
}

// Fetch a question by ID
export async function fetchQuestion(questionId: string): Promise<Question> {
  const response = await fetch(`${API_BASE_URL}/questions/${questionId}`);
  if (!response.ok) {
    throw new Error(`Failed to fetch question: ${response.statusText}`);
  }
  return response.json();
}

// Fetch all answers for a specific question
export async function fetchAnswersByQuestion(questionId: string): Promise<Answer[]> {
  const response = await fetch(`${API_BASE_URL}/answers/list/${questionId}`);
  if (!response.ok) {
    throw new Error(`Failed to fetch answers: ${response.statusText}`);
  }
  return response.json();
}

// Fetch all questions for a questionnaire
export async function fetchQuestionnaireWithDetails(questionnaireId: string) {
  // First, fetch the questionnaire
  const questionnaire = await fetchQuestionnaire(questionnaireId);
  
  // Then, fetch all questions in parallel
  const questionsPromises = questionnaire.questions.map(questionId => 
    fetchQuestion(questionId)
  );
  const questions = await Promise.all(questionsPromises);
  
  // Finally, fetch all answers for each question in parallel
  const answersPromises = questions.map(question => 
    fetchAnswersByQuestion(question.id)
  );
  const answersArrays = await Promise.all(answersPromises);
  
  // Combine questions with their answers
  const questionsWithAnswers = questions.map((question, index) => ({
    ...question,
    answers: answersArrays[index]
  }));
  
  return {
    questionnaire,
    questions: questionsWithAnswers
  };
}
