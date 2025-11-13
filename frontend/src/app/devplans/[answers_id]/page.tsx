'use client';

import { useEffect, useMemo, useState } from 'react';
import { useParams } from 'next/navigation';
import Link from 'next/link';
import { AuthGuard } from '@/components/AuthGuard';
import { Button } from '@/components/ui/button';
import { downloadDevelopmentPlanPdf, fetchDevelopmentPlanByUserAnswers } from '@/lib/api/devplans';
import type { GeneratePlanResponse } from '@/types/devplans';
import { PlanMarkdown } from '@/components/PlanMarkdown';

export default function DevelopmentPlanByAnswersPage() {
  const params = useParams<{ answers_id: string }>();
  const answersId = params?.answers_id as string;

  const [data, setData] = useState<GeneratePlanResponse | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [downloading, setDownloading] = useState(false);
  const [downloadError, setDownloadError] = useState<string | null>(null);

  useEffect(() => {
    let active = true;
    const run = async () => {
      if (!answersId) {
        setError('Missing plan identifier.');
        setLoading(false);
        return;
      }
      setLoading(true);
      setError(null);
      try {
        const resp = await fetchDevelopmentPlanByUserAnswers(answersId);
        if (!active) return;
        setData(resp);
      } catch (e) {
        if (!active) return;
        setError(e instanceof Error ? e.message : 'Failed to load development plan');
      } finally {
        if (active) setLoading(false);
      }
    };
    run();
    return () => {
      active = false;
    };
  }, [answersId]);

  const plan = data?.plan;

  const formatDate = (iso: string | null | undefined) => {
    if (!iso) return '—';
    const dt = new Date(iso);
    if (Number.isNaN(dt.getTime())) return '—';
    return dt.toLocaleDateString();
  };

  const splitLines = (value: string | null | undefined) => {
    if (!value) return [];
    return value
      .split(/\r?\n/)
      .map((line) => line.trim())
      .filter(Boolean)
      .map((line) => line.replace(/^([\-\*\u2022]\s*)+/, ''));
  };

  const renderList = (items: string[]) => {
    if (items.length === 0) return null;
    const markdown = items.map((item) => `- ${item}`).join('\n');
    return <PlanMarkdown content={markdown} className="!space-y-1" />;
  };

  const actionItems = useMemo(() => splitLines(plan?.action_items), [plan?.action_items]);
  const nextSteps = useMemo(() => splitLines(plan?.next_steps), [plan?.next_steps]);
  const challenges = useMemo(() => splitLines(plan?.challenges), [plan?.challenges]);
  const resources = useMemo(() => splitLines(plan?.resources), [plan?.resources]);

  const handleDownload = async () => {
    if (!answersId) return;
    setDownloadError(null);
    setDownloading(true);
    try {
      const blob = await downloadDevelopmentPlanPdf(answersId);
      const url = window.URL.createObjectURL(blob);
      const link = document.createElement('a');
      link.href = url;
      link.download = `leadership-plan-${answersId}.pdf`;
      document.body.appendChild(link);
      link.click();
      document.body.removeChild(link);
      window.URL.revokeObjectURL(url);
    } catch (err) {
      const message = err instanceof Error ? err.message : 'Failed to download development plan';
      setDownloadError(message);
    } finally {
      setDownloading(false);
    }
  };

  return (
    <AuthGuard>
      <div className="flex flex-col items-center min-h-screen p-6">
        <div className="w-full max-w-3xl space-y-6">
          <div className="flex flex-wrap items-center justify-between gap-3">
            <h1 className="text-2xl font-bold">My Leadership Plan</h1>
            <div className="flex flex-wrap gap-2">
              {answersId && (
                <Link href={`/results/${encodeURIComponent(answersId)}`}>
                  <Button variant="outline" size="sm">
                    Back to My Results
                  </Button>
                </Link>
              )}
              <Button size="sm" onClick={handleDownload} disabled={loading || !plan || downloading}>
                {downloading ? 'Preparing…' : 'Download Plan'}
              </Button>
            </div>
          </div>

          {downloadError && (
            <div className="text-sm text-destructive">{downloadError}</div>
          )}

          {loading && <div className="text-muted-foreground">Loading leadership plan…</div>}

          {error && (
            <div className="p-4 bg-destructive/10 text-destructive rounded">{error}</div>
          )}

          {!loading && !error && plan && (
            <div className="space-y-6">
              <section className="rounded border p-6 bg-muted/30 space-y-4">
                <div className="space-y-2">
                  <h2 className="text-lg font-semibold">Goal</h2>
                  <p className="text-base text-foreground leading-relaxed">{plan.goal || '—'}</p>
                  {plan.description && (
                    <p className="text-sm text-muted-foreground leading-relaxed">{plan.description}</p>
                  )}
                </div>
                <div className="grid grid-cols-1 sm:grid-cols-2 gap-4 text-sm">
                  <div className="space-y-1">
                    <span className="text-muted-foreground">Status</span>
                    <p className="font-medium">{plan.status}</p>
                  </div>
                  <div className="space-y-1">
                    <span className="text-muted-foreground">Target Date</span>
                    <p className="font-medium">{formatDate(plan.target_date)}</p>
                  </div>
                  <div className="space-y-1">
                    <span className="text-muted-foreground">Progress</span>
                    <p className="font-medium">{plan.progress}%</p>
                  </div>
                  <div className="space-y-1">
                    <span className="text-muted-foreground">Created</span>
                    <p className="font-medium">{formatDate(plan.created_at)}</p>
                  </div>
                </div>
              </section>

              <section className="rounded border p-6 space-y-4">
                <div className="space-y-2">
                  <h2 className="text-lg font-semibold">Detailed Plan</h2>
                  <PlanMarkdown content={data?.plan_markdown ?? plan.plan_markdown ?? ''} />
                </div>
              </section>

              <section className="rounded border p-6 space-y-5">
                <h2 className="text-lg font-semibold">Key Highlights</h2>
                <div className="space-y-4 text-sm">
                  {actionItems.length > 0 && (
                    <div className="space-y-2">
                      <h3 className="font-semibold">Action Items</h3>
                      {renderList(actionItems)}
                    </div>
                  )}
                  {nextSteps.length > 0 && (
                    <div className="space-y-2">
                      <h3 className="font-semibold">Next Steps</h3>
                      {renderList(nextSteps)}
                    </div>
                  )}
                  {challenges.length > 0 && (
                    <div className="space-y-2">
                      <h3 className="font-semibold">Challenges</h3>
                      {renderList(challenges)}
                    </div>
                  )}
                  {resources.length > 0 && (
                    <div className="space-y-2">
                      <h3 className="font-semibold">Resources</h3>
                      {renderList(resources)}
                    </div>
                  )}
                </div>
                {actionItems.length === 0 &&
                  nextSteps.length === 0 &&
                  challenges.length === 0 &&
                  resources.length === 0 && (
                    <p className="text-sm text-muted-foreground">
                      Additional details will appear here once they are available in your plan.
                    </p>
                  )}
              </section>
            </div>
          )}
        </div>
      </div>
    </AuthGuard>
  );
}
