// Hook personnalisé pour gérer les diagnostics

import { useState, useCallback } from 'react';
import { DiagnosisResult, AnalysisResponse } from '../types/diagnostic.types';
import { analyzeSkinImage, transformToDiagnosisResult, getDiagnosisById } from '../services/diagnosticApi';

interface UseDiagnosisReturn {
  diagnosis: DiagnosisResult | null;
  loading: boolean;
  error: string | null;
  analyzeImage: (
    imageFile: File,
    userInfo: {
      age: number;
      gender: string;
      sleep_hours: number;
      stress_level: number;
      diet_quality: string;
      smoker: string;
      alcohol_consumption: string;
      name?: string;
      email?: string;
    },
    token?: string
  ) => Promise<void>;
  fetchDiagnosis: (diagnosisId: number, token?: string) => Promise<void>;
  reset: () => void;
}

export const useDiagnosis = (): UseDiagnosisReturn => {
  const [diagnosis, setDiagnosis] = useState<DiagnosisResult | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const analyzeImage = useCallback(async (
    imageFile: File,
    userInfo: {
      age: number;
      gender: string;
      sleep_hours: number;
      stress_level: number;
      diet_quality: string;
      smoker: string;
      alcohol_consumption: string;
      name?: string;
      email?: string;
    },
    token?: string
  ) => {
    setLoading(true);
    setError(null);
    
    try {
      const response: AnalysisResponse = await analyzeSkinImage(imageFile, userInfo, token);
      const diagnosisResult = transformToDiagnosisResult(response);
      setDiagnosis(diagnosisResult);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Erreur lors de l\'analyse');
      setDiagnosis(null);
    } finally {
      setLoading(false);
    }
  }, []);

  const fetchDiagnosis = useCallback(async (diagnosisId: number, token?: string) => {
    setLoading(true);
    setError(null);
    
    try {
      const diagnosisResult = await getDiagnosisById(diagnosisId, token);
      setDiagnosis(diagnosisResult);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Erreur lors de la récupération du diagnostic');
      setDiagnosis(null);
    } finally {
      setLoading(false);
    }
  }, []);

  const reset = useCallback(() => {
    setDiagnosis(null);
    setError(null);
    setLoading(false);
  }, []);

  return {
    diagnosis,
    loading,
    error,
    analyzeImage,
    fetchDiagnosis,
    reset,
  };
};

