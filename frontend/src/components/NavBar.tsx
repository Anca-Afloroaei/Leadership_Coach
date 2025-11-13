// frontend/src/components/NavBar.tsx
'use client'

import Link from 'next/link'
import { ModeToggle } from '@/components/ui/mode-toggle'
import { useSession } from '@/contexts/SessionContext'
import { useEffect, useState, useMemo } from 'react'
import { fetchCompletedUserAnswers } from '@/lib/api/user_answers'
import type { CompletedAnswersSummary } from '@/types/user_answers'
import {
  DropdownMenu,
  DropdownMenuTrigger,
  DropdownMenuContent,
  DropdownMenuItem,
  DropdownMenuLabel,
  DropdownMenuSeparator,
} from '@/components/ui/dropdown-menu'

export function NavBar() {

    const { state, logout } = useSession()
    const handleLogout = async () => { await logout() }

    const [completed, setCompleted] = useState<CompletedAnswersSummary[] | null>(null)

    useEffect(() => {
        let active = true
        const run = async () => {
            if (!state.isAuthenticated || !state.user) {
                setCompleted(null)
                return
            }
            try {
                const list = await fetchCompletedUserAnswers()
                if (!active) return
                setCompleted(Array.isArray(list) ? list : [])
            } catch {
                if (active) setCompleted([])
            }
        }
        run()
        return () => { active = false }
    }, [state.isAuthenticated, state.user])

    const hasResults = useMemo(() => (completed && completed.length > 0) || false, [completed])
    const singleResult = useMemo(() => (completed && completed.length === 1 ? completed[0] : null), [completed])
    const planButtonLabel = useMemo(() => {
        if (completed && completed.length > 1) return 'My Leadership Plans'
        if (completed && completed.length === 1) return 'Leadership Plan'
        return 'Leadership Plan'
    }, [completed])

    const formatCompletedLabel = (rec: CompletedAnswersSummary) => {
        const date = new Date(rec.completed_at)
        const dateLabel = isNaN(date.getTime()) ? '' : date.toLocaleDateString()
        return dateLabel ? `${rec.questionnaire_title} — ${dateLabel}` : rec.questionnaire_title
    }

    return (
        <header
            className="
        sticky top-0 z-50
        bg-background/80 backdrop-blur-sm
        border-b border-border
        p-4 flex justify-between items-center
      "
        >
            <nav className="flex space-x-4">
                <Link href="/questionnaire">Questionnaire</Link>
                {singleResult ? (
                  <>
                    <Link href={`/results/${encodeURIComponent(singleResult.id)}`}>My Results</Link>
                    <Link href={`/devplans/${encodeURIComponent(singleResult.id)}`}>
                      {planButtonLabel}
                    </Link>
                  </>
                ) : hasResults ? (
                  <>
                    <DropdownMenu>
                      <DropdownMenuTrigger className="text-left">My Results</DropdownMenuTrigger>
                      <DropdownMenuContent align="start">
                        <DropdownMenuLabel>Completed Assessments</DropdownMenuLabel>
                        <DropdownMenuSeparator />
                        {completed?.map((rec) => (
                          <Link key={rec.id} href={`/results/${encodeURIComponent(rec.id)}`}>
                            <DropdownMenuItem>{formatCompletedLabel(rec)}</DropdownMenuItem>
                          </Link>
                        ))}
                      </DropdownMenuContent>
                    </DropdownMenu>
                    <DropdownMenu>
                      <DropdownMenuTrigger className="text-left">{planButtonLabel}</DropdownMenuTrigger>
                      <DropdownMenuContent align="start">
                        <DropdownMenuLabel>Select a Leadership Plan</DropdownMenuLabel>
                        <DropdownMenuSeparator />
                        {completed?.map((rec) => (
                          <Link key={`${rec.id}-plan`} href={`/devplans/${encodeURIComponent(rec.id)}`}>
                            <DropdownMenuItem>{formatCompletedLabel(rec)}</DropdownMenuItem>
                          </Link>
                        ))}
                      </DropdownMenuContent>
                    </DropdownMenu>
                  </>
                ) : null}
                <Link href="/about">About</Link>
                <Link href="/support">Support</Link>
            </nav>

            <div className="flex items-center space-x-4">
                {state.isAuthenticated && state.user ? ( 
                    <>
                    <Link
                    href="/profile"
                    className="text-sm text-muted-foreground hover:text-foreground transition:colors">
                        {state.user.first_name} {state.user.last_name} 
                    </Link>
                    <button
                        onClick={logout}
                        className="text-sm text-destructive"
                    >
                        Logout
                    </button>
                    </>
                ) : (
                    <>
                        <Link href="/login" className="text-sm">
                            Log In
                        </Link>
                        <Link href="/signup" className="text-sm">
                            Sign Up
                        </Link>
                    </>
                )} 
                <ModeToggle />
            </div>
        </header>
    )
}
