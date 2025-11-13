import { Card, CardContent, CardDescription, CardFooter, CardHeader, CardTitle } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { RadioGroup, RadioGroupItem } from "@/components/ui/radio-group";
import { Label } from "@/components/ui/label";
import { useQuestionnaire } from "@/contexts/QuestionnaireContext";
import { Question, Answer } from "@/types/questionnaire";
import { useState, useEffect } from "react";
import { set } from "react-hook-form";

interface QuestionCardProps {
  question: Question;
  answers: Answer[];
  questionNumber: number;
  totalQuestions: number;
}

export function QuestionCard({ question, answers, questionNumber, totalQuestions }: QuestionCardProps) {
  const { goToNext, goToPrevious, saveAnswer, getResponseForQuestion } = useQuestionnaire();
  const [selectedAnswer, setSelectedAnswer] = useState<string | null>(null);
  
  // Get existing response if user navigated back
  useEffect(() => {
    const existingResponse = getResponseForQuestion(question.id);
    if (existingResponse) {
      setSelectedAnswer(existingResponse.answer_id);
    }
  }, [question.id, getResponseForQuestion]);

  const handleAnswerSelect = (answerId: string | null) => {
    setSelectedAnswer(answerId);
    saveAnswer(question.id, answerId);
  };

  const handleNext = () => {
    // Always flush the current answer before moving to next
    saveAnswer(question.id, selectedAnswer, { flush: true });
    goToNext();
    setSelectedAnswer(null); // Reset selection for next question
  };

  return (
    <Card className="w-full max-w-2xl">
      <CardHeader>
        <div className="flex justify-between items-start mb-2">
          <CardDescription>Question {questionNumber} of {totalQuestions}</CardDescription>
          {question.competency && (
            <span className="text-sm font-medium text-muted-foreground">
              {question.competency}
            </span>
          )}
        </div>
        <CardTitle className="text-xl">{question.question_text}</CardTitle>
      </CardHeader>
      <CardContent>
        <RadioGroup value={selectedAnswer} onValueChange={handleAnswerSelect}>
          <div className="space-y-3">
            {answers.map((answer) => (
              <div key={answer.id} className="flex items-start space-x-3 p-3 rounded-lg hover:bg-muted/50 transition-colors">
                <RadioGroupItem value={answer.id} id={answer.id} className="mt-0.5" />
                <Label 
                  htmlFor={answer.id} 
                  className="flex-1 cursor-pointer font-normal"
                >
                  {answer.answer_text}
                </Label>
              </div>
            ))}
          </div>
        </RadioGroup>
      </CardContent>
      <CardFooter className="justify-between">
        <Button 
          variant="outline" 
          onClick={goToPrevious}
          disabled={questionNumber === 1}
        >
          Previous
        </Button>
        <span className="text-sm text-muted-foreground">
          {Math.round((questionNumber / totalQuestions) * 100)}% Complete
        </span>
        <Button 
          onClick={handleNext}
          // disabled={!selectedAnswer}
        >
          Next
        </Button>
      </CardFooter>
    </Card>
  );
}