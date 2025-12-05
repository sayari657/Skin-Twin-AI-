// Service API pour communiquer avec le backend Django

import { AnalysisResponse, DiagnosisResult } from '../types/diagnostic.types';

const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000';

/**
 * Analyse une image de peau et retourne les résultats complets
 */
export const analyzeSkinImage = async (
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
): Promise<AnalysisResponse> => {
  const formData = new FormData();
  formData.append('file', imageFile);
  formData.append('age', userInfo.age.toString());
  formData.append('gender', userInfo.gender);
  formData.append('sleep_hours', userInfo.sleep_hours.toString());
  formData.append('stress_level', userInfo.stress_level.toString());
  formData.append('diet_quality', userInfo.diet_quality);
  formData.append('smoker', userInfo.smoker);
  formData.append('alcohol_consumption', userInfo.alcohol_consumption);
  
  if (userInfo.name) formData.append('name', userInfo.name);
  if (userInfo.email) formData.append('email', userInfo.email);
  formData.append('save_to_db', 'true');

  const headers: HeadersInit = {};
  if (token) {
    headers['Authorization'] = `Bearer ${token}`;
  }

  const response = await fetch(`${API_BASE_URL}/api/analyze/`, {
    method: 'POST',
    body: formData,
    headers,
  });

  if (!response.ok) {
    const error = await response.json().catch(() => ({ detail: 'Erreur lors de l\'analyse' }));
    throw new Error(error.detail || 'Erreur lors de l\'analyse');
  }

  return await response.json();
};

/**
 * Récupère un diagnostic spécifique par son ID
 */
export const getDiagnosisById = async (
  diagnosisId: number,
  token?: string
): Promise<DiagnosisResult> => {
  const headers: HeadersInit = {
    'Content-Type': 'application/json',
  };
  
  if (token) {
    headers['Authorization'] = `Bearer ${token}`;
  }

  const response = await fetch(`${API_BASE_URL}/api/diagnoses/${diagnosisId}/`, {
    method: 'GET',
    headers,
  });

  if (!response.ok) {
    throw new Error('Diagnostic non trouvé');
  }

  const data = await response.json();
  return transformToDiagnosisResult(data);
};

/**
 * Transforme la réponse API en format DiagnosisResult
 */
export const transformToDiagnosisResult = (data: AnalysisResponse): DiagnosisResult => {
  // Convertir les troubles détectés en format DetectedTrouble
  const detectedTroubles = data.detected_troubles.map((trouble, index) => {
    const detection = data.detections?.find(d => d.label === trouble);
    return {
      name: trouble,
      confidence: detection?.confidence || 0.5,
      severity: getSeverity(detection?.confidence || 0.5),
    };
  });

  return {
    quickInfo: {
      skinType: {
        type: data.skin_type as 'Dry' | 'Normal' | 'Oily',
        confidence: data.confidence,
      },
      confidence: data.confidence,
      detectedTroubles,
    },
    diagnostic: {
      diagnostic: data.diagnostic,
      skinType: data.skin_type,
      problems: data.detected_troubles,
    },
    conseils_pratiques: data.conseils_pratiques,
    recommendations: data.recommendations || [],
    annotated_image: data.annotated_image,
    diagnosis_id: data.diagnosis_id,
  };
};

/**
 * Détermine la sévérité basée sur la confiance
 */
const getSeverity = (confidence: number): 'LOW' | 'MODERATE' | 'HIGH' => {
  if (confidence >= 0.7) return 'HIGH';
  if (confidence >= 0.4) return 'MODERATE';
  return 'LOW';
};

