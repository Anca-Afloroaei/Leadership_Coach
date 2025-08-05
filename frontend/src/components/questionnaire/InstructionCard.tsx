import { Card, CardContent, CardDescription, CardFooter, CardHeader, CardTitle } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { useQuestionnaire } from "@/contexts/QuestionnaireContext";

export function InstructionCard() {
  const { questionnaire, goToNext } = useQuestionnaire();

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
        <Button onClick={goToNext} size="lg">
          Begin Assessment
        </Button>
      </CardFooter>
    </Card>
  );
}