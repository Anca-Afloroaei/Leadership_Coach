'use client';

import { useEffect, useMemo, useState } from 'react';
import { useParams, useSearchParams } from 'next/navigation';
import Link from 'next/link';
import { AuthGuard } from '@/components/AuthGuard';
import { fetchResults } from '@/lib/api/results';
import type { UserResults } from '@/types/results';
import { Button } from '@/components/ui/button';

export default function FocusAreasPage() {
  const params = useParams<{ answers_id: string }>();
  const answersId = params?.answers_id as string;
  const search = useSearchParams();

  const [data, setData] = useState<UserResults | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [selected, setSelected] = useState<string[]>([]);

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

  const focusOptions = useMemo(() => {
    if (!data) return [] as Array<[string, number]>;
    return Object.entries(data.results)
      .filter(([_, pct]) => (pct ?? 0) < 80)
      .sort((a, b) => (a[1] ?? 0) - (b[1] ?? 0));
  }, [data]);

  const toggle = (key: string) => {
    setSelected((prev) => {
      if (prev.includes(key)) {
        return prev.filter((k) => k !== key);
      }
      if (prev.length >= 3) return prev; // enforce limit
      return [...prev, key];
    });
  };

  const isDisabled = (key: string) => selected.length >= 3 && !selected.includes(key);
  const confirmHref = useMemo(() => {
    if (!answersId || selected.length < 1) return '#';
    const qs = new URLSearchParams();
    selected.forEach((c) => qs.append('c', c));
    return `/results/${encodeURIComponent(answersId)}/focus/confirm?${qs.toString()}`;
  }, [answersId, selected]);

  // Hydrate selection from query params when returning from confirm page
  useEffect(() => {
    if (!data) return;
    const fromQuery = search.getAll('c');
    if (fromQuery.length) {
      // De-duplicate and enforce max 3
      const unique = Array.from(new Set(fromQuery)).slice(0, 3);
      setSelected(unique);
    }
  }, [data, search]);

  return (
    <AuthGuard>
      <div className="flex flex-col items-center min-h-screen p-6">
        <div className="w-full max-w-2xl space-y-6">
          <div className="flex items-center justify-between">
            <h1 className="text-2xl font-bold">Choose Your Focus Areas</h1>
            <Link href={`/results/${encodeURIComponent(answersId)}`}>
              <Button variant="outline" size="sm">Back to Results</Button>
            </Link>
          </div>

          {loading && (<div className="text-muted-foreground">Loading...</div>)}
          {error && (<div className="p-4 bg-destructive/10 text-destructive rounded">{error}</div>)}

          {!loading && !error && (
            <>
              <div className="p-4 rounded border bg-muted/30">
                <h2 className="font-semibold mb-2">Guidelines</h2>
                <ul className="text-sm text-muted-foreground list-disc pl-5 space-y-1">
                  <li>Select up to 3 competencies to focus on.</li>
                  <li>Choices are based on areas scoring below 80%.</li>
                  <li>A personalized development plan will be generated from your selection.</li>
                </ul>
              </div>

              {focusOptions.length === 0 ? (
                <div className="text-muted-foreground">Great work — all competencies are at or above 80%.</div>
              ) : (
                <div className="space-y-3">
                  <div className="text-sm text-muted-foreground">Selected: {selected.length} / 3</div>
                  {focusOptions.map(([comp, pct]) => {
                    const percent = Math.max(0, Math.min(100, Math.round(pct)));
                    const checked = selected.includes(comp);
                    const disabled = isDisabled(comp);
                    return (
                      <label key={comp} className={`flex items-center justify-between border rounded p-3 ${disabled ? 'opacity-60' : ''}`}>
                        <div className="flex items-center gap-3">
                          <input
                            type="checkbox"
                            className="h-4 w-4"
                            checked={checked}
                            onChange={() => toggle(comp)}
                            disabled={disabled}
                          />
                          <span className="font-medium">{comp}</span>
                        </div>
                        <span className="text-sm text-muted-foreground">{percent}%</span>
                      </label>
                    );
                  })}
                  <div className="pt-2 flex justify-end">
                    {/* Confirm button only enabled if at least 1 selected */}
                    {answersId && (
                      <Link href={confirmHref} prefetch>
                        <Button disabled={selected.length < 1}>Confirm Selection</Button>
                      </Link>
                    )}
                  </div>
                </div>
              )}
            </>
          )}
        </div>
      </div>
    </AuthGuard>
  );
}
