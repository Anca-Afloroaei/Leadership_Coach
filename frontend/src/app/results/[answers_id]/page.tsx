'use client';

import { useEffect, useState } from 'react';
import { useParams } from 'next/navigation';
import { AuthGuard } from '@/components/AuthGuard';
import { fetchResults } from '@/lib/api/results';
import type { UserResults } from '@/types/results';
// Using a local progress bar to enable subtle per-competency color coding
import Link from 'next/link';
import { Button } from '@/components/ui/button';

export default function ResultsByIdPage() {
  const params = useParams<{ answers_id: string }>();
  const answersId = params?.answers_id as string;

  const [data, setData] = useState<UserResults | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    let active = true;
    const run = async () => {
      if (!answersId) {
        setError('Missing results identifier.');
        setLoading(false);
        return;
      }
      setLoading(true);
      setError(null);
      try {
        const res = await fetchResults(answersId);
        if (!active) return;
        setData(res);
      } catch (e) {
        if (!active) return;
        setError(e instanceof Error ? e.message : 'Failed to load results');
      } finally {
        if (active) setLoading(false);
      }
    };
    run();
    return () => { active = false; };
  }, [answersId]);

  return (
    <AuthGuard>
      <div className="flex flex-col items-center min-h-screen p-6">
        <div className="w-full max-w-2xl">
          <div className="flex items-center justify-between mb-6">
            <h1 className="text-2xl font-bold">Your Results</h1>
            {answersId && (
              <Link href={`/results/${encodeURIComponent(answersId)}/focus`}>
                <Button size="sm" variant="default">Choose Your Focus Areas</Button>
              </Link>
            )}
          </div>

          {loading && (
            <div className="text-muted-foreground">Loading results...</div>
          )}

          {error && (
            <div className="p-4 bg-destructive/10 text-destructive rounded mb-4">{error}</div>
          )}

          {!loading && !error && data && (
            <div className="space-y-5">
              {Object.keys(data.results).length === 0 && (
                <div className="text-muted-foreground">No results available yet.</div>
              )}
              {Object.entries(data.results)
                .sort((a, b) => (b[1] ?? 0) - (a[1] ?? 0))
                .map(([competency, value]) => {
                  const percent = Math.max(0, Math.min(100, Math.round(value)));
                  // Color thresholds: green > 80, amber 60–80, dark orange 35–60, red < 35
                  const barColor = percent > 80
                    ? 'bg-emerald-500'
                    : percent >= 60
                      ? 'bg-amber-500'
                      : percent >= 35
                        ? 'bg-orange-600'
                        : 'bg-rose-500';
                  return (
                    <div key={competency} className="space-y-2">
                      <div className="flex justify-between text-sm">
                        <span className="font-medium">{competency}</span>
                        <span className="text-muted-foreground">{percent}%</span>
                      </div>
                      <div className="h-2 w-full rounded-full bg-primary/20 overflow-hidden">
                        <div
                          className={`h-2 rounded-full ${barColor} opacity-80 transition-all`}
                          style={{ width: `${percent}%` }}
                        />
                      </div>
                    </div>
                  );
                })}
            </div>
          )}
        </div>
      </div>
    </AuthGuard>
  );
}
