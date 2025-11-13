'use client';

import { useMemo, useState } from 'react';
import { useParams, useSearchParams } from 'next/navigation';
import Link from 'next/link';
import { AuthGuard } from '@/components/AuthGuard';
import { Button } from '@/components/ui/button';
import { RadioGroup, RadioGroupItem } from '@/components/ui/radio-group';
import { Label } from '@/components/ui/label';

export default function ConfirmFocusSelectionPage() {
  const params = useParams<{ answers_id: string }>();
  const answersId = params?.answers_id as string;
  const search = useSearchParams();
  const selected = useMemo(() => search.getAll('c').filter(Boolean), [search]);

  // No pre-selected option; user must choose explicitly
  const [duration, setDuration] = useState<string>('');

  const durations = [
    { value: '30', label: '30 days (1 month)' },
    { value: '60', label: '60 days (2 months)' },
    { value: '90', label: '90 days (3 months)' },
    { value: '180', label: '180 days (6 months)' },
  ];

  return (
    <AuthGuard>
      <div className="flex flex-col items-center min-h-screen p-6">
        <div className="w-full max-w-2xl space-y-6">
          <div className="flex items-center justify-between">
            <h1 className="text-2xl font-bold">Confirm Your Focus Areas</h1>
            <Link href={`/results/${encodeURIComponent(answersId)}/focus?${search.toString()}`}>
              <Button variant="outline" size="sm">Back</Button>
            </Link>
          </div>

          <div className="space-y-2">
            <h2 className="font-semibold">Your choices</h2>
            {selected.length === 0 ? (
              <div className="text-muted-foreground">No focus areas selected.</div>
            ) : (
              <ul className="list-disc pl-5 space-y-1">
                {selected.map((c) => (
                  <li key={c}>{c}</li>
                ))}
              </ul>
            )}
          </div>

          <div className="p-4 rounded border bg-muted/30 space-y-3">
            <h2 className="font-semibold">Select Plan Duration</h2>
            <p className="text-sm text-muted-foreground">Choose a timeframe for your Leadership Development Plan.</p>
            <RadioGroup value={duration} onValueChange={setDuration}>
              {durations.map((d) => (
                <label key={d.value} className="flex items-center gap-3">
                  <RadioGroupItem value={d.value} />
                  <span>{d.label}</span>
                </label>
              ))}
            </RadioGroup>
          </div>

          <div className="flex justify-center">
            <Link
              href={useMemo(() => {
                if (!answersId || !duration || selected.length === 0) return '#';
                const qs = new URLSearchParams();
                qs.set('duration', duration);
                selected.forEach((c) => qs.append('c', c));
                return `/results/${encodeURIComponent(answersId)}/plan?${qs.toString()}`;
              }, [answersId, duration, selected])}
            >
              <Button size="lg" className="px-8 py-6 text-base" disabled={!duration || selected.length === 0}>
                Generate My Leadership Development Plan
              </Button>
            </Link>
          </div>

          <div className="text-sm text-muted-foreground">
            Suggested durations: 30, 60, 90, or 180 days — these align with common 1–3 month goals and a longer 6‑month plan for broader development.
          </div>
        </div>
      </div>
    </AuthGuard>
  );
}
