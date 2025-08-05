'use client';

import { useEffect } from 'react';
import { useQuestionnaire } from '@/contexts/QuestionnaireContext';
import { fetchQuestionnaireWithDetails } from '@/lib/api/questionnaire';
import { InstructionCard } from '@/components/questionnaire/InstructionCard';
import { QuestionCard } from '@/components/questionnaire/QuestionCard';
import { SubmissionCard } from '@/components/questionnaire/SubmissionCard';
import { Loader2 } from 'lucide-react';

interface QuestionnaireContentProps {
  questionnaireId: string;
}

export function QuestionnaireContent({ questionnaireId }: QuestionnaireContentProps) {
  const {
    questionnaire,
    questions,
    currentIndex,
    isLoading,
    error,
    setQuestionnaire,
    setQuestions,
    setIsLoading,
    setError,
  } = useQuestionnaire();

  useEffect(() => {
    const loadQuestionnaire = async () => {
      setIsLoading(true);
      setError(null);
      
      try {
        const data = await fetchQuestionnaireWithDetails(questionnaireId);
        setQuestionnaire(data.questionnaire);
        setQuestions(data.questions);
      } catch (err) {
        setError(err instanceof Error ? err.message : 'Failed to load questionnaire');
      } finally {
        setIsLoading(false);
      }
    };

    loadQuestionnaire();
  }, [questionnaireId, setQuestionnaire, setQuestions, setIsLoading, setError]);

  if (isLoading) {
    return (
      <div className="flex flex-col items-center justify-center min-h-screen">
        <Loader2 className="h-8 w-8 animate-spin text-primary" />
        <p className="mt-4 text-muted-foreground">Loading questionnaire...</p>
      </div>
    );
  }

  if (error) {
    return (
      <div className="flex flex-col items-center justify-center min-h-screen">
        <div className="max-w-md text-center space-y-4">
          <h2 className="text-2xl font-semibold text-destructive">Error</h2>
          <p className="text-muted-foreground">{error}</p>
          <button 
            onClick={() => window.location.reload()} 
            className="text-primary hover:underline"
          >
            Try again
          </button>
        </div>
      </div>
    );
  }

  if (!questionnaire || questions.length === 0) {
    return (
      <div className="flex flex-col items-center justify-center min-h-screen">
        <p className="text-muted-foreground">No questionnaire data available</p>
      </div>
    );
  }

  // Render the appropriate card based on currentIndex
  const renderCard = () => {
    if (currentIndex === 0) {
      // Instruction card
      return <InstructionCard />;
    } else if (currentIndex === questions.length + 1) {
      // Submission card (last card)
      return <SubmissionCard />;
    } else {
      // Question cards
      const questionIndex = currentIndex - 1;
      const question = questions[questionIndex];
      return (
        <QuestionCard
          question={question}
          answers={question.answers}
          questionNumber={questionIndex + 1}
          totalQuestions={questions.length}
        />
      );
    }
  };

  return (
    <div className="flex flex-col items-center justify-center min-h-screen p-4">
      <div className="w-full max-w-4xl">
        {/* Progress indicator */}
        <div className="mb-8">
          <div className="h-2 bg-muted rounded-full overflow-hidden">
            <div
              className="h-full bg-primary transition-all duration-300"
              style={{
                width: `${(currentIndex / (questions.length + 1)) * 100}%`,
              }}
            />
          </div>
        </div>

        {/* Card container with animation */}
        <div className="flex justify-center">
          <div className="w-full transition-all duration-300">
            {renderCard()}
          </div>
        </div>
      </div>
    </div>
  );
}