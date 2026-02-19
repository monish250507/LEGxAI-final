// LexAI API Integration - Complete Backend Communication

const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

export interface UploadResponse {
  status: string;
  filename: string;
  document_id: string;
  clauses?: any[];
  message?: string;
}

export interface ChatSessionRequest {
  document_text: string;
  constitution: string;
  clauses: any[];
}

export interface ChatMessageRequest {
  session_id: string;
  message: string;
}

export interface ClauseAnalysisRequest {
  session_id: string;
  clause_text: string;
  question: string;
}

export interface ChatSessionResponse {
  session_id: string;
  message: string;
}

export interface ChatMessageResponse {
  response: string;
  session_id: string;
  timestamp: string;
}

export interface ClauseAnalysisResponse {
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

class ApiError extends Error {
  public status?: number;
  public statusText?: string;

  constructor(
    message: string,
    status?: number,
    statusText?: string
  ) {
    super(message);
    this.name = 'ApiError';
    if (status) this.status = status;
    if (statusText) this.statusText = statusText;
  }
}

async function apiRequest<T>(
  endpoint: string,
  options: RequestInit = {}
): Promise<T> {
  const url = `${API_BASE_URL}${endpoint}`;
  
  const config: RequestInit = {
    headers: {
      'Content-Type': 'application/json',
      ...options.headers,
    },
    ...options,
  };

  try {
    const response = await fetch(url, config);
    
    if (!response.ok) {
      const errorData = await response.json().catch(() => ({}));
      throw new ApiError(
        errorData.message || `HTTP error! status: ${response.status}`,
        response.status,
        response.statusText
      );
    }

    return await response.json();
  } catch (error) {
    if (error instanceof ApiError) {
      throw error;
    }
    throw new ApiError('Network error occurred');
  }
}

// Document Upload API
export async function uploadDocument(
  file: File,
  constitution: string
): Promise<UploadResponse> {
  const formData = new FormData();
  formData.append('file', file);
  formData.append('constitution', constitution);

  return apiRequest<UploadResponse>('/api/upload', {
    method: 'POST',
    body: formData,
    headers: {}, // Let browser set Content-Type for FormData
  });
}

// Analysis Fetch API
export async function fetchAnalysis(documentId: string): Promise<any> {
  return apiRequest<any>(`/api/analysis/${documentId}`);
}

// Chatbot API - Create Session
export async function createChatSession(
  documentText: string,
  constitution: string,
  clauses: any[]
): Promise<ChatSessionResponse> {
  return apiRequest<ChatSessionResponse>('/api/chatbot/session/create', {
    method: 'POST',
    body: JSON.stringify({
      document_text: documentText,
      constitution: constitution,
      clauses: clauses
    }),
  });
}

// Chatbot API - Send Message
export async function sendChatMessage(
  sessionId: string,
  message: string
): Promise<ChatMessageResponse> {
  return apiRequest<ChatMessageResponse>('/api/chatbot/message', {
    method: 'POST',
    body: JSON.stringify({
      session_id: sessionId,
      message: message
    }),
  });
}

// Chatbot API - Analyze Clause
export async function analyzeClauseInContext(
  sessionId: string,
  clauseText: string,
  question: string
): Promise<ClauseAnalysisResponse> {
  return apiRequest<ClauseAnalysisResponse>('/api/chatbot/analyze-clause', {
    method: 'POST',
    body: JSON.stringify({
      session_id: sessionId,
      clause_text: clauseText,
      question: question
    }),
  });
}

// Chatbot API - Get Document Summary
export async function getDocumentSummary(sessionId: string): Promise<any> {
  return apiRequest<any>(`/api/chatbot/session/${sessionId}/summary`);
}

// Chatbot API - Get Conversation History
export async function getConversationHistory(
  sessionId: string,
  limit: number = 10
): Promise<any> {
  return apiRequest<any>(`/api/chatbot/session/${sessionId}/history?limit=${limit}`);
}

// Chatbot API - Get Session Stats
export async function getSessionStats(sessionId: string): Promise<any> {
  return apiRequest<any>(`/api/chatbot/session/${sessionId}/stats`);
}

// Chatbot API - Clear Session
export async function clearChatSession(sessionId: string): Promise<any> {
  return apiRequest<any>(`/api/chatbot/session/${sessionId}`, {
    method: 'DELETE',
  });
}

// Health Check API
export async function healthCheck(): Promise<any> {
  return apiRequest<any>('/api/health');
}

// Download Annotated Document
export async function downloadAnnotatedDocument(documentId: string): Promise<Blob> {
  const url = `${API_BASE_URL}/api/download/${documentId}`;
  
  try {
    const response = await fetch(url);
    if (!response.ok) {
      throw new ApiError(`Download failed: ${response.status}`, response.status);
    }
    
    return await response.blob();
  } catch (error) {
    if (error instanceof ApiError) {
      throw error;
    }
    throw new ApiError('Download network error');
  }
}

export { ApiError };
