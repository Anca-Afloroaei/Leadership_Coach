'use client';

import React, { createContext, useContext, useState, useCallback, ReactNode } from 'react';
import { Questionnaire, Question, Answer, UserResponse } from '@/types/questionnaire';
import { updateUserAnswers } from '@/lib/api/user_answers';

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
  userAnswersId: string | null;

  // Navigation
  goToNext: () => void;
  goToPrevious: () => void;
  goToIndex: (index: number) => void;

  // Response management
  recordResponse: (questionId: string, answerId: string, scoreValue: number) => void;
  getResponseForQuestion: (questionId: string) => UserResponse | undefined;
  saveAnswer: (questionId: string, answerId: string, options?: { flush?: boolean }) => void;
  hydrateAnswers: (answers: Record<string, string>) => void;

  // State setters
  setQuestionnaire: (questionnaire: Questionnaire) => void;
  setQuestions: (questions: QuestionWithAnswers[]) => void;
  setIsLoading: (loading: boolean) => void;
  setError: (error: string | null) => void;
  setUserAnswersId: (id: string | null) => void;
}

const QuestionnaireContext = createContext<QuestionnaireContextType | undefined>(undefined);

export function QuestionnaireProvider({ children }: { children: ReactNode }) {
  const [questionnaire, setQuestionnaire] = useState<Questionnaire | null>(null);
  const [questions, setQuestions] = useState<QuestionWithAnswers[]>([]);
  const [currentIndex, setCurrentIndex] = useState(0);
  const [userResponses, setUserResponses] = useState<UserResponse[]>([]);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [userAnswersId, setUserAnswersId] = useState<string | null>(null);
  // Debounce timers per question to avoid duplicate PATCH calls
  const debounceTimersRef = React.useRef<Record<string, ReturnType<typeof setTimeout> | undefined>>({});

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
    // Keep recordResponse as a direct call or migrate to saveAnswer if needed
    if (userAnswersId) {
      updateUserAnswers({ id: userAnswersId, answers: { [questionId]: answerId } }).catch(() => {
        // Handle error silently or add error handling logic here if needed
      });
    }
  }, [userAnswersId]);

  const getResponseForQuestion = useCallback((questionId: string) => {
    return userResponses.find((r) => r.question_id === questionId);
  }, [userResponses]);

  // Save answer with score_value defaulting to 0, and update user answers if userAnswersId is set
  const saveAnswer = useCallback(async (questionId: string, answerId: string, options?: { flush?: boolean }) => {
    // Update local state only if changed to avoid unnecessary re-renders
    setUserResponses((prev) => {
      const existingIndex = prev.findIndex((r) => r.question_id === questionId);
      const existing = existingIndex >= 0 ? prev[existingIndex] : undefined;
      if (existing && existing.answer_id === answerId) {
        return prev; // no change
      }
      const newResponse: UserResponse = { question_id: questionId, answer_id: answerId, score_value: 0 };
      if (existingIndex >= 0) {
        const updated = [...prev];
        updated[existingIndex] = newResponse;
        return updated;
      }
      return [...prev, newResponse];
    });

    if (!userAnswersId) return;

    // Debounced server update to prevent duplicates
    const timers = debounceTimersRef.current;
    if (timers[questionId]) {
      clearTimeout(timers[questionId]);
    }

    const send = () => {
      updateUserAnswers({ id: userAnswersId, answers: { [questionId]: answerId } })
        .catch(() => {
          // Handle error silently or add error handling logic here if needed
        });
    };

    if (options?.flush) {
      send();
      delete timers[questionId];
    } else {
      timers[questionId] = setTimeout(() => {
        send();
        delete timers[questionId];
      }, 300);
    }
  }, [userAnswersId]);

  // Hydrate existing answers from a map without triggering network calls
  const hydrateAnswers = useCallback((answers: Record<string, string>) => {
    const entries = Object.entries(answers) as Array<[string, string]>;
    setUserResponses((prev) => {
      // Merge with any existing but prefer incoming
      const map = new Map<string, UserResponse>(prev.map(r => [r.question_id, r]));
      for (const [qid, aid] of entries) {
        map.set(qid, { question_id: qid, answer_id: aid, score_value: 0 });
      }
      return Array.from(map.values());
    });
  }, []);

  const value: QuestionnaireContextType = {
    questionnaire,
    questions,
    currentIndex,
    userResponses,
    isLoading,
    error,
    userAnswersId,
    goToNext,
    goToPrevious,
    goToIndex,
    recordResponse,
    getResponseForQuestion,
    saveAnswer,
    hydrateAnswers,
    setQuestionnaire,
    setQuestions,
    setIsLoading,
    setError,
    setUserAnswersId,
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