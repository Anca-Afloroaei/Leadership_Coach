'use client';

import { useEffect, useMemo, useState } from 'react';
import { useParams, useSearchParams } from 'next/navigation';
import Link from 'next/link';
import { AuthGuard } from '@/components/AuthGuard';
import { fetchResults } from '@/lib/api/results';
import type { UserResults } from '@/types/results';
import { Button } from '@/components/ui/button';
import { useSession } from '@/contexts/SessionContext';
import { generateDevelopmentPlan } from '@/lib/api/devplans';
import { PlanMarkdown } from '@/components/PlanMarkdown';

export default function DevelopmentPlanPage() {
  const params = useParams<{ answers_id: string }>();
  const answersId = params?.answers_id as string;
  const search = useSearchParams();

  const selected = useMemo(() => search.getAll('c').filter(Boolean), [search]);
  const duration = useMemo(() => search.get('duration') || '', [search]);

  const [data, setData] = useState<UserResults | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [planMd, setPlanMd] = useState<string>('');
  const [genError, setGenError] = useState<string | null>(null);
  const { state } = useSession();

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

  // Generate the plan when inputs are available
  useEffect(() => {
    const run = async () => {
      if (!answersId || !duration || selected.length === 0) return;
      if (!state.user) return;
      setGenError(null);
      try {
        const resp = await generateDevelopmentPlan({
          user_id: state.user.id,
          user_answers_record_id: answersId,
          focus_areas: selected,
          duration_days: parseInt(duration, 10),
          role: state.user.role,
          industry: state.user.industry,
          years_experience: state.user.years_experience,
        });
        setPlanMd(resp.plan_markdown || '');
      } catch (e) {
        setGenError(e instanceof Error ? e.message : 'Failed to generate plan');
      }
    };
    run();
  }, [answersId, duration, selected, state.user]);

  return (
    <AuthGuard>
      <div className="flex flex-col items-center min-h-screen p-6">
        <div className="w-full max-w-3xl space-y-6">
          <div className="flex items-center justify-between">
            <h1 className="text-2xl font-bold">Leadership Development Plan</h1>
            <Link href={`/results/${encodeURIComponent(answersId)}/focus/confirm?${search.toString()}`}>
              <Button variant="outline" size="sm">Back</Button>
            </Link>
          </div>

          {loading && (<div className="text-muted-foreground">Generating plan...</div>)}
          {error && (<div className="p-4 bg-destructive/10 text-destructive rounded">{error}</div>)}

          {!loading && !error && data && (
            <div className="space-y-6">
              <div className="p-4 rounded border bg-muted/30">
                <h2 className="font-semibold mb-2">Plan Inputs</h2>
                <ul className="text-sm text-muted-foreground list-disc pl-5 space-y-1">
                  <li>Assessment results (per-competency scores)</li>
                  <li>Focus areas: {selected.length ? selected.join(', ') : 'None'}</li>
                  <li>Duration: {duration ? `${duration} days` : 'Not selected'}</li>
                  <li>User attributes (role, industry, years experience)</li>
                </ul>
              </div>

              <div className="space-y-4">
                <h2 className="text-xl font-semibold">Your Plan</h2>
                {genError && (
                  <div className="p-4 bg-destructive/10 text-destructive rounded">{genError}</div>
                )}
                {!planMd && !genError && (
                  <div className="p-4 rounded border text-sm text-muted-foreground">Generating your plan...</div>
                )}
                {planMd && (
                  <div className="p-4 rounded border">
                    <PlanMarkdown content={planMd} />
                  </div>
                )}
              </div>


              <div className="space-y-2">
                <h3 className="font-semibold">Baseline (from assessment)</h3>
                <div className="grid grid-cols-1 md:grid-cols-2 gap-3">
                  {Object.entries(data.results)
                    .sort((a, b) => (a[0] > b[0] ? 1 : -1))
                    .map(([comp, pct]) => (
                      <div key={comp} className="flex items-center justify-between rounded border p-2">
                        <span className="text-sm font-medium">{comp}</span>
                        <span className="text-sm text-muted-foreground">{Math.round(pct)}%</span>
                      </div>
                  ))}
                </div>
              </div>
            </div>
          )}

        </div>
      </div>
    </AuthGuard>
  );
}
