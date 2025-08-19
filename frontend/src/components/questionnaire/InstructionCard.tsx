import { Card, CardContent, CardDescription, CardFooter, CardHeader, CardTitle } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { useQuestionnaire } from "@/contexts/QuestionnaireContext";
import { createUserAnswers } from "@/lib/api/user_answers";
import { useSession } from "@/contexts/SessionContext";
import { useRef, useState } from "react";

export function InstructionCard() {
  const { userAnswersId, setUserAnswersId, questionnaire, goToNext } = useQuestionnaire();
  const { state } = useSession();
  const [isStarting, setIsStarting] = useState(false);
  const beginTimeoutRef = useRef<ReturnType<typeof setTimeout> | null>(null);

  const handleBeginAssessment = async () => {
    // Guard: prevent concurrent clicks
    if (isStarting) return;
    setIsStarting(true);

    try {
      if (!userAnswersId && questionnaire) {
        const user_id = state.user?.id;
        if (!user_id) {
          console.error("No authenticated user found in session context");
          return;
        }

        // Small debounce window to coalesce rapid clicks
        if (beginTimeoutRef.current) {
          clearTimeout(beginTimeoutRef.current);
        }

        await new Promise<void>((resolve) => {
          beginTimeoutRef.current = setTimeout(resolve, 250);
        });

        // Re-check after debounce window to avoid double-create
        if (!userAnswersId) {
          const newUserAnswers = await createUserAnswers({
            user_id,
            questionnaire_id: questionnaire.id,
            answers: {},
          });
          setUserAnswersId(newUserAnswers.id);
        }
      }
      goToNext();
    } finally {
      setIsStarting(false);
    }
  };

  return (
    <Card className="w-full max-w-2xl">
      <CardHeader>
        <CardTitle className="text-2xl">{questionnaire?.title || "Leadership Assessment"}</CardTitle>
        <CardDescription className="text-base mt-2">
          {questionnaire?.description || "Please read the instructions carefully before beginning."}
        </CardDescription>
      </CardHeader>
      <CardContent className="space-y-4">
        <div className="space-y-3">
          <h3 className="font-semibold">Instructions:</h3>
          <ul className="list-disc list-inside space-y-2 text-sm text-muted-foreground">
            <li>This questionnaire contains {questionnaire?.questions.length || 0} questions</li>
            <li>Each question has multiple choice answers</li>
            <li>Select the answer that best represents your current situation or opinion</li>
            <li>There are no right or wrong answers</li>
            <li>Your responses will be used to create a personalized leadership development plan</li>
            <li>The assessment should take approximately 10-15 minutes to complete</li>
          </ul>
        </div>
        <div className="bg-muted p-4 rounded-lg">
          <p className="text-sm">
            <strong>Note:</strong> You can navigate back and forth between questions using the navigation buttons.
            Your answers will be saved as you progress through the questionnaire.
          </p>
        </div>
      </CardContent>
      <CardFooter className="justify-end">
  <Button onClick={handleBeginAssessment} size="lg" disabled={isStarting}>
          Begin Assessment
        </Button>
      </CardFooter>
    </Card>
  );
}