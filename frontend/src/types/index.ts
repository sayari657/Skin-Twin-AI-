// Types pour l'application Skin Twin AI

export interface User {
  id: number;
  username: string;
  email: string;
  first_name: string;
  last_name: string;
  age?: number;
  gender?: 'M' | 'F' | 'O';
  location_country?: string;
  location_region?: string;
  skin_type?: 'DRY' | 'OILY' | 'COMBINATION' | 'NORMAL' | 'SENSITIVE';
  diabetes: boolean;
  hypertension: boolean;
  blood_disorders: boolean;
  autoimmune_diseases: boolean;
  pregnancy: boolean;
  sun_exposure?: 'LOW' | 'MODERATE' | 'HIGH';
  sunscreen_usage?: 'NEVER' | 'SOMETIMES' | 'DAILY';
  diet?: 'BALANCED' | 'HIGH_FAT_SUGAR' | 'VEGETARIAN';
  hydration?: 'LOW' | 'MODERATE' | 'HIGH';
  smoking: boolean;
  alcohol: boolean;
  sleep_hours?: 'LOW' | 'MODERATE' | 'HIGH';
  family_dermatological_history: boolean;
  current_skin_problems: string[];
  current_treatments: string;
  current_cosmetics: string;
  known_allergies: string;
  skin_goals: string[];
  profile_picture?: string;
  date_joined: string;
  last_login?: string;
}

export interface SkinAnalysis {
  id: number;
  image: string;
  skin_type_prediction?: string;
  skin_type_confidence?: number;
  acne_detected: boolean;
  acne_severity?: string;
  acne_confidence?: number;
  wrinkles_detected: boolean;
  wrinkles_severity?: string;
  wrinkles_confidence?: number;
  dark_spots_detected: boolean;
  dark_spots_severity?: string;
  dark_spots_confidence?: number;
  redness_detected: boolean;
  redness_severity?: string;
  redness_confidence?: number;
  analysis_date: string;
  processing_time?: number;
  raw_cnn_results: any;
  raw_yolo_results: any;
}

export interface Product {
  id: number;
  name: string;
  brand: string;
  category: 'CLEANSER' | 'MOISTURIZER' | 'SERUM' | 'SUNSCREEN' | 'TREATMENT' | 'MASK' | 'TONER' | 'EXFOLIANT';
  description: string;
  ingredients: string;
  price?: number;
  size?: string;
  target_skin_types: string[];
  target_issues: string[];
  image?: string;
  created_at: string;
  updated_at: string;
  is_active: boolean;
}

export interface Recommendation {
  id: number;
  product: Product;
  relevance_score: number;
  confidence_score: number;
  reasons: string[];
  created_at: string;
}

export interface GANSimulation {
  id: number;
  original_analysis: number;
  original_image: string;
  simulated_image: string;
  simulation_type: 'ACNE_TREATMENT' | 'WRINKLE_REDUCTION' | 'DARK_SPOT_REMOVAL' | 'SKIN_SMOOTHING' | 'COMPLETE_TREATMENT';
  improvement_score?: number;
  confidence_score?: number;
  created_at: string;
  processing_time?: number;
  raw_gan_results: any;
}

export interface AuthTokens {
  access: string;
  refresh: string;
}

export interface LoginRequest {
  email: string;
  password: string;
}

export interface RegisterRequest {
  email: string;
  password: string;
  password_confirm: string;
  first_name?: string;
  last_name?: string;
  age?: number;
  gender?: 'M' | 'F' | 'O';
  location_country?: string;
  location_region?: string;
  skin_type?: 'DRY' | 'OILY' | 'COMBINATION' | 'NORMAL' | 'SENSITIVE';
  diabetes?: boolean;
  hypertension?: boolean;
  blood_disorders?: boolean;
  autoimmune_diseases?: boolean;
  pregnancy?: boolean;
  sun_exposure?: 'LOW' | 'MODERATE' | 'HIGH';
  sunscreen_usage?: 'NEVER' | 'SOMETIMES' | 'DAILY';
  diet?: 'BALANCED' | 'HIGH_FAT_SUGAR' | 'VEGETARIAN';
  hydration?: 'LOW' | 'MODERATE' | 'HIGH';
  smoking?: boolean;
  alcohol?: boolean;
  sleep_hours?: 'LOW' | 'MODERATE' | 'HIGH';
  family_dermatological_history?: boolean;
  current_skin_problems?: string[];
  current_treatments?: string;
  current_cosmetics?: string;
  known_allergies?: string;
  skin_goals?: string[];
}

export interface ApiResponse<T> {
  data?: T;
  error?: string;
  message?: string;
}

export interface PaginatedResponse<T> {
  count: number;
  next?: string;
  previous?: string;
  results: T[];
}




