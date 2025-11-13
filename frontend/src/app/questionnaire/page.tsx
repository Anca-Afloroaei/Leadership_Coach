'use client';

import { useEffect, useState } from 'react';
import { QuestionnaireProvider } from '@/contexts/QuestionnaireContext';
import { QuestionnaireContent } from './QuestionnaireContent';
import { AuthGuard } from '@/components/AuthGuard';
import { DEFAULT_QUESTIONNAIRE_ID } from '@/config/constants';


// Hardcoded questionnaire ID for now
// const QUESTIONNAIRE_ID = '0f9ca597d16a466ba0ce51941a87fe0e'; // Sample Questionnaire

// Use default questionnaire ID from config
const QUESTIONNAIRE_ID = DEFAULT_QUESTIONNAIRE_ID;

export default function QuestionnairePage() {
  return (
    <AuthGuard>
    <QuestionnaireProvider>
      <QuestionnaireContent questionnaireId={QUESTIONNAIRE_ID} />
    </QuestionnaireProvider>
    </AuthGuard>
  );
}
