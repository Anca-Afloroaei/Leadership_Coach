'use client';

import { useEffect, useState } from 'react';
import { QuestionnaireProvider } from '@/contexts/QuestionnaireContext';
import { QuestionnaireContent } from './QuestionnaireContent';
import { AuthGuard } from '@/components/AuthGuard';

// Hardcoded questionnaire ID for now
const QUESTIONNAIRE_ID = '0f9ca597d16a466ba0ce51941a87fe0e'; // Sample Questionnaire

export default function QuestionnairePage() {
  return (
    <AuthGuard>
    <QuestionnaireProvider>
      <QuestionnaireContent questionnaireId={QUESTIONNAIRE_ID} />
    </QuestionnaireProvider>
    </AuthGuard>
  );
}