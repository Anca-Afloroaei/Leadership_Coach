'use client';

import { useEffect, useState } from 'react';
import { AuthGuard } from '@/components/AuthGuard';
import { fetchResults } from '@/lib/api/results';

// Hardcoded questionnaire ID for now
const QUESTIONNAIRE_ID = '0f9ca597d16a466ba0ce51941a87fe0e'; // Sample Questionnaire

export default function QuestionnairePage() {
    return (
        <AuthGuard>
            {/* Load the results from the API */}
            
            <div className="flex flex-col items-center justify-center min-h-screen bg-background"></div>
            <h1 className="text-2xl text-foreground font-bold mb-4">Questionnaire Results</h1>
            <p className="text-foreground mb-4">This page will display results for the questionnaire with ID: {QUESTIONNAIRE_ID}</p>
            {/* Placeholder for future components */}
            <div className="w-full max-w-2xl bg-white shadow-md rounded-lg p-6">
                <p className="text-foreground">Results will be displayed here.</p>
            </div>
            <p className="text-sm foreground mt-4">This is a placeholder page for the questionnaire results.</p>
            <p className="text-sm foreground">Currently, the questionnaire ID is hardcoded. This will be dynamic in the future.</p>
        </AuthGuard>
    );
}