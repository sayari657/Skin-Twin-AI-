// Fichier d'export principal pour faciliter les imports

export { default as QuickInfo } from './components/QuickInfo';
export { default as DiagnosticSection } from './components/DiagnosticSection';
export { default as AdviceSection } from './components/AdviceSection';
export { default as RecommendationsSection } from './components/RecommendationsSection';
export { default as DiagnosisResults } from './components/DiagnosisResults';

export { useDiagnosis } from './hooks/useDiagnosis';

export * from './types/diagnostic.types';
export * from './services/diagnosticApi';

