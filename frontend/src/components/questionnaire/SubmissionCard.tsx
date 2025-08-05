import { Card, CardContent, CardDescription, CardFooter, CardHeader, CardTitle } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { useQuestionnaire } from "@/contexts/QuestionnaireContext";
import { submitQuestionnaireResponses } from "@/lib/api/questionnaire";
import { useState } from "react";
import { useRouter } from "next/navigation";
import { CheckCircle } from "lucide-react";

export function SubmissionCard() {
  const { questionnaire, questions, userResponses, goToPrevious } = useQuestionnaire();
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const router = useRouter();

  const answeredQuestions = userResponses.length;
  const totalQuestions = questions.length;
  const isComplete = answeredQuestions === totalQuestions;
  const totalScore = userResponses.reduce((sum, response) => sum + response.score_value, 0);

  const handleSubmit = async () => {
    if (!isComplete || !questionnaire) return;

    setIsSubmitting(true);
    setError(null);

    try {
      await submitQuestionnaireResponses({
        questionnaire_id: questionnaire.id,
        responses: userResponses,
      });
      
      // Navigate to a success page or dashboard
      router.push('/thank-you');
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to submit questionnaire');
      setIsSubmitting(false);
    }
  };

  return (
    <Card className="w-full max-w-2xl">
      <CardHeader>
        <CardTitle className="text-2xl">Review & Submit</CardTitle>
        <CardDescription>
          Please review your responses before submitting the questionnaire
        </CardDescription>
      </CardHeader>
      <CardContent className="space-y-6">
        <div className="space-y-4">
          <div className="flex items-center justify-between p-4 bg-muted rounded-lg">
            <span className="font-medium">Questions Answered</span>
            <span className={`font-semibold ${isComplete ? 'text-green-600' : 'text-orange-600'}`}>
              {answeredQuestions} / {totalQuestions}
            </span>
          </div>
          
          {isComplete ? (
            <div className="flex items-center space-x-2 text-green-600">
              <CheckCircle className="h-5 w-5" />
              <span className="font-medium">All questions answered!</span>
            </div>
          ) : (
            <div className="text-orange-600">
              <p className="font-medium">Please answer all questions before submitting.</p>
              <p className="text-sm mt-1">You have {totalQuestions - answeredQuestions} questions remaining.</p>
            </div>
          )}
        </div>

        {error && (
          <div className="p-4 bg-destructive/10 text-destructive rounded-lg">
            <p className="text-sm">{error}</p>
          </div>
        )}

        <div className="bg-muted p-4 rounded-lg space-y-2">
          <h4 className="font-semibold">What happens next?</h4>
          <ul className="text-sm space-y-1 text-muted-foreground">
            <li>• Your responses will be analyzed to create a personalized leadership profile</li>
            <li>• You'll receive a detailed development plan based on your results</li>
            <li>• Recommended leadership modules will be suggested for your growth</li>
            <li>• You can track your progress over time with follow-up assessments</li>
          </ul>
        </div>
      </CardContent>
      <CardFooter className="justify-between">
        <Button 
          variant="outline" 
          onClick={goToPrevious}
          disabled={isSubmitting}
        >
          Previous
        </Button>
        <Button 
          onClick={handleSubmit}
          disabled={!isComplete || isSubmitting}
          size="lg"
        >
          {isSubmitting ? 'Submitting...' : 'Submit Assessment'}
        </Button>
      </CardFooter>
    </Card>
  );
}