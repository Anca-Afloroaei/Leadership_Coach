'use client';

import { useRouter } from "next/navigation";

import { Button } from "@/components/ui/button"
import {
  Card,
  CardAction,
  CardContent,
  CardDescription,
  CardFooter,
  CardHeader,
  CardTitle,
} from "@/components/ui/card"
import { Input } from "@/components/ui/input"
import { Label } from "@/components/ui/label"
import { RadioGroup, RadioGroupItem } from "@/components/ui/radio-group"


export default function QuestionnairePage() {
  const router = useRouter();

//   const handleSubmit = (event: React.FormEvent) => {
//     event.preventDefault();
//     // Handle form submission logic here
//     // For example, you might want to send the data to an API
//     console.log("Form submitted");
//     router.push('/thank-you'); // Redirect after submission
//   };

  return (
    <div className="flex flex-col items-center justify-center min-h-screen">
      <h1 className="text-4xl font-bold mb-4">Questionnaire Page</h1>
      <p className="text-lg mb-8">Please fill out the questionnaire below.</p>
      <Card className="w-full max-w-md">
        <CardHeader>
          <CardTitle>Questionnaire</CardTitle>
          <CardDescription>Answer the following questions</CardDescription>
        </CardHeader>
        <CardContent>
          {/* <form onSubmit={handleSubmit}> */}
            <div className="grid gap-6">
              <div className="grid gap-2">
                <Label htmlFor="question1">What is your favorite color?</Label>
                <RadioGroup defaultValue="red" id="question1">
                  <div className="flex items-center space-x-4">
                    <RadioGroupItem value="red" id="red" />
                    <Label htmlFor="red">Red</Label>
                    <RadioGroupItem value="blue" id="blue" />
                    <Label htmlFor="blue">Blue</Label>
                    <RadioGroupItem value="green" id="green" />
                    <Label htmlFor="green">Green</Label>
                  </div>
                </RadioGroup>
              </div>
              {/* Add more questions as needed */}
            </div>
            <CardFooter className="mt-4">
              <Button type="submit">Submit</Button>
            </CardFooter>
          {/* </form> */}
        </CardContent>
      </Card>
    </div>
  );
}

