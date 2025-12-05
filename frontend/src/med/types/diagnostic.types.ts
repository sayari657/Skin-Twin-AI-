// Types TypeScript pour les données de diagnostic

export interface SkinType {
  type: 'Dry' | 'Normal' | 'Oily';
  confidence: number; // 0-1
}

export interface DetectedTrouble {
  name: string;
  confidence: number; // 0-1
  severity?: 'LOW' | 'MODERATE' | 'HIGH';
}

export interface QuickInfo {
  skinType: SkinType;
  confidence: number; // 0-1
  detectedTroubles: DetectedTrouble[];
}

export interface DiagnosticData {
  diagnostic: string;
  skinType: string;
  problems: string[];
}

export interface ProductLink {
  title: string;
  link: string;
  snippet: string;
}

export interface Product {
  nom: string;
  description_detaillee: string;
  links?: ProductLink[];
}

export interface RecommendationCategory {
  categorie: string;
  produits: Product[];
}

export interface DiagnosisResult {
  // Infos rapides
  quickInfo: QuickInfo;
  
  // Diagnostic
  diagnostic: DiagnosticData;
  
  // Conseils pratiques
  conseils_pratiques: string | string[];
  
  // Recommandations
  recommendations: RecommendationCategory[];
  
  // Image annotée (base64)
  annotated_image?: string;
  
  // Métadonnées
  created_at?: string;
  diagnosis_id?: number;
}

export interface AnalysisResponse {
  success: boolean;
  diagnosis_id?: number;
  skin_type: string;
  skin_type_probs: {
    Dry: number;
    Normal: number;
    Oily: number;
  };
  confidence: number;
  detected_troubles: string[];
  detections: Array<{
    label: string;
    confidence: number;
    box: number[];
  }>;
  diagnostic: string;
  conseils_pratiques: string | string[];
  recommendations: RecommendationCategory[];
  annotated_image: string;
}

