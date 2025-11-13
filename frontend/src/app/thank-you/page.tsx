"use client";

import Link from 'next/link';
import { Button } from '@/components/ui/button';
import { CheckCircle } from 'lucide-react';
import { useSearchParams } from 'next/navigation';
import { useMemo } from 'react';

export default function ThankYouPage() {
  const searchParams = useSearchParams();
  const answersId = useMemo(() => searchParams.get('answers_id') || '', [searchParams]);

  return (
    <div className="flex flex-col items-center justify-center min-h-screen p-4">
      <div className="max-w-md text-center space-y-6">
        <div className="flex justify-center">
          <div className="h-20 w-20 rounded-full bg-green-100 flex items-center justify-center">
            <CheckCircle className="h-12 w-12 text-green-600" />
          </div>
        </div>
        
        <h1 className="text-3xl font-bold">Thank You!</h1>
        
        <p className="text-muted-foreground">
          Your leadership assessment has been successfully submitted. 
          We're analyzing your responses to create a personalized development plan.
        </p>
        
        <div className="space-y-4">
          <p className="text-sm text-muted-foreground">
            You can now view your results and recommended leadership modules.
          </p>
          {answersId && (
            <div className="pt-2">
              <Link href={`/results/${encodeURIComponent(answersId)}`}>
                <Button variant="default" size="lg">
                  View Your Results
                </Button>
              </Link>
            </div>
          )}
        </div>
        
        <div className="pt-4">
          <Link href="/">
            <Button size="lg">
              Return to Home
            </Button>
          </Link>
        </div>
      </div>
    </div>
  );
}
