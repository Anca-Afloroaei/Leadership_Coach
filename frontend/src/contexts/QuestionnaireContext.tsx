'use client';

import React, { createContext, useContext, useState, useCallback, ReactNode } from 'react';
import { Questionnaire, Question, Answer, UserResponse } from '@/types/questionnaire';

interface QuestionWithAnswers extends Question {
  answers: Answer[];
}

interface QuestionnaireContextType {
  questionnaire: Questionnaire | null;
  questions: QuestionWithAnswers[];
  currentIndex: number;
  userResponses: UserResponse[];
  isLoading: boolean;
  error: string | null;
  
  // Navigation
  goToNext: () => void;
  goToPrevious: () => void;
  goToIndex: (index: number) => void;
  
  // Response management
  recordResponse: (questionId: string, answerId: string, scoreValue: number) => void;
  getResponseForQuestion: (questionId: string) => UserResponse | undefined;
  
  // State setters
  setQuestionnaire: (questionnaire: Questionnaire) => void;
  setQuestions: (questions: QuestionWithAnswers[]) => void;
  setIsLoading: (loading: boolean) => void;
  setError: (error: string | null) => void;
}

const QuestionnaireContext = createContext<QuestionnaireContextType | undefined>(undefined);

export function QuestionnaireProvider({ children }: { children: ReactNode }) {
  const [questionnaire, setQuestionnaire] = useState<Questionnaire | null>(null);
  const [questions, setQuestions] = useState<QuestionWithAnswers[]>([]);
  const [currentIndex, setCurrentIndex] = useState(0);
  const [userResponses, setUserResponses] = useState<UserResponse[]>([]);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const goToNext = useCallback(() => {
    setCurrentIndex((prev) => {
      const totalCards = questions.length + 2; // +2 for instruction and submission cards
      return Math.min(prev + 1, totalCards - 1);
    });
  }, [questions.length]);

  const goToPrevious = useCallback(() => {
    setCurrentIndex((prev) => Math.max(prev - 1, 0));
  }, []);

  const goToIndex = useCallback((index: number) => {
    const totalCards = questions.length + 2;
    if (index >= 0 && index < totalCards) {
      setCurrentIndex(index);
    }
  }, [questions.length]);

  const recordResponse = useCallback((questionId: string, answerId: string, scoreValue: number) => {
    setUserResponses((prev) => {
      const existingIndex = prev.findIndex((r) => r.question_id === questionId);
      const newResponse: UserResponse = { question_id: questionId, answer_id: answerId, score_value: scoreValue };
      
      if (existingIndex >= 0) {
        // Update existing response
        const updated = [...prev];
        updated[existingIndex] = newResponse;
        return updated;
      } else {
        // Add new response
        return [...prev, newResponse];
      }
    });
  }, []);

  const getResponseForQuestion = useCallback((questionId: string) => {
    return userResponses.find((r) => r.question_id === questionId);
  }, [userResponses]);

  const value: QuestionnaireContextType = {
    questionnaire,
    questions,
    currentIndex,
    userResponses,
    isLoading,
    error,
    goToNext,
    goToPrevious,
    goToIndex,
    recordResponse,
    getResponseForQuestion,
    setQuestionnaire,
    setQuestions,
    setIsLoading,
    setError,
  };

  return (
    <QuestionnaireContext.Provider value={value}>
      {children}
    </QuestionnaireContext.Provider>
  );
}

export function useQuestionnaire() {
  const context = useContext(QuestionnaireContext);
  if (context === undefined) {
    throw new Error('useQuestionnaire must be used within a QuestionnaireProvider');
  }
  return context;
}