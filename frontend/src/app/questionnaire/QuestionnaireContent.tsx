'use client';

import { useEffect } from 'react';
import { useQuestionnaire } from '@/contexts/QuestionnaireContext';
import { fetchQuestionnaireWithDetails } from '@/lib/api/questionnaire';
import { fetchRecentUserAnswers } from '@/lib/api/user_answers';
import { InstructionCard } from '@/components/questionnaire/InstructionCard';
import { QuestionCard } from '@/components/questionnaire/QuestionCard';
import { SubmissionCard } from '@/components/questionnaire/SubmissionCard';
import { Progress } from '@/components/ui/progress';
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
    userAnswersId,
    setUserAnswersId,
  hydrateAnswers,
  goToIndex,
  } = useQuestionnaire();

  useEffect(() => {
    const loadQuestionnaire = async () => {
      setIsLoading(true);
      setError(null);
      
      try {
        const data = await fetchQuestionnaireWithDetails(questionnaireId);
        setQuestionnaire(data.questionnaire);
        setQuestions(data.questions);
        // Try to resume: fetch recent in-progress user_answers (within 7 days)
        const recent = await fetchRecentUserAnswers({ questionnaire_id: questionnaireId, days: 7 });
        if (recent && recent.id && !recent.completed_at) {
          // Set the existing userAnswersId
          setUserAnswersId(recent.id);
          // Load existing answers into local state
          if (recent.answers && typeof recent.answers === 'object') {
      hydrateAnswers(recent.answers);
          }
          // Jump to first unanswered question (skip Instruction)
          try {
            const answeredSet = new Set(Object.keys(recent.answers || {}));
            const firstUnansweredIdx = data.questions.findIndex(q => !answeredSet.has(q.id));
            const desiredIndex = (firstUnansweredIdx === -1)
              ? (data.questions.length + 1) // submission card if all answered
              : (firstUnansweredIdx + 1);    // +1 to account for Instruction card at 0
            // Defer until questions state is applied inside context
            setTimeout(() => goToIndex(desiredIndex), 0);
          } catch {}
        } else {
          // No recent in-progress record; leave userAnswersId null so InstructionCard creates new when starting.
        }

      } catch (err) {
        setError(err instanceof Error ? err.message : 'Failed to load questionnaire');
      } finally {
        setIsLoading(false);
      }
    };

    loadQuestionnaire();
  }, [questionnaireId, setQuestionnaire, setQuestions, setIsLoading, setError, userAnswersId, setUserAnswersId]);

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
        <p className="text-muted-foreground">Loading questionnaire data...</p>
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
      <div className="w-full max-w-2xl">
        {/* Progress indicator - same max width as cards */}
        <div className="mb-8">
          <Progress 
            value={(currentIndex / (questions.length + 1)) * 100} 
            className="h-2"
          />
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