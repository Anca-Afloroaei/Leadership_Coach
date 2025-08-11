// frontend/src/components/NavBar.tsx
'use client'

import Link from 'next/link'
import { ModeToggle } from '@/components/ui/mode-toggle'
import { useSession } from '@/contexts/SessionContext'

export function NavBar() {

    const { state, logout } = useSession()
    const handleLogout = async () => { await logout() }

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