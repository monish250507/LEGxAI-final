// LexAI Frontend Types - Complete Interface Definitions

export interface Clause {
  clause_id: string;
  text: string;
  type: string;
  priority_score: number;
  color: string;
  rank: number;
  explanation?: string;
  offensive_analysis?: string;
  defensive_analysis?: string;
  constitution_reference?: string;
  risk_level: 'high' | 'medium' | 'low' | 'unknown';
}

export interface Document {
  id: string;
  filename: string;
  upload_time: string;
  status: 'processing' | 'completed' | 'error';
  clauses?: Clause[];
  constitution?: string;
}

export interface AnalysisResult {
  status: string;
  filename: string;
  clauses: Clause[];
  document_text?: string;
  extracted_clauses?: any[];
  classified_clauses?: any[];
  standardized_clauses?: Clause[];
}

export interface ChatMessage {
  role: 'user' | 'assistant';
  content: string;
  timestamp: string;
  metadata?: any;
}

export interface ChatSession {
  session_id: string;
  document_text: string;
  constitution: string;
  clauses: Clause[];
  created_at: string;
  last_updated: string;
}

export interface ChatbotResponse {
  clause_text: string;
  question: string;
  analysis: string;
  clause_type: string;
  risk_level: string;
  constitution_reference: string;
  context: {
    session_id: string;
    conversation_turn: number;
  };
}

export interface UploadResponse {
  status: string;
  filename: string;
  document_id: string;
  clauses?: Clause[];
  message?: string;
}

export interface Constitution {
  code: string;
  name: string;
  flag: string;
}

export interface User {
  email: string;
  name?: string;
}

export interface AuthState {
  user: User | null;
  isAuthenticated: boolean;
  loading: boolean;
}

export type RiskLevel = 'high' | 'medium' | 'low' | 'unknown';

export type ClauseType = 
  | 'confidentiality'
  | 'liability'
  | 'termination'
  | 'payment'
  | 'intellectual_property'
  | 'dispute_resolution'
  | 'governing_law'
  | 'force_majeure'
  | 'assignment'
  | 'amendment'
  | 'notices'
  | 'miscellaneous'
  | 'general'
  | 'unknown';

export type ConstitutionType = 'India' | 'China' | 'Japan' | 'Russia';

export interface ClauseHighlight {
  id: string;
  text: string;
  color: string;
  position: {
    start: number;
    end: number;
  };
}

export interface AnalysisStats {
  total_clauses: number;
  high_risk_clauses: number;
  medium_risk_clauses: number;
  low_risk_clauses: number;
  most_common_type: string;
  risk_distribution: {
    high: number;
    medium: number;
    low: number;
  };
}
