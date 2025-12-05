import axios from 'axios';

const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://127.0.0.1:8000';

export interface ChatMessage {
  id: number;
  role: 'user' | 'assistant' | 'system';
  content: string;
  timestamp: string;
  tokens_used: number;
}

export interface ChatSession {
  id: number;
  session_id: string;
  title: string;
  created_at: string;
  updated_at: string;
  is_active: boolean;
  messages: ChatMessage[];
}

export interface ChatRequest {
  message: string;
  session_id?: string;
  include_context?: boolean;
  system?: string;
  analysis_context?: string;
}

export interface ChatResponse {
  response: string;
  session_id: string;
  tokens_used: number;
  timestamp: string;
}

class ChatService {
  private baseURL = `${API_BASE_URL}/api/chat-ai`;

  private getAuthHeaders() {
    const token = localStorage.getItem('access_token');
    return {
      'Authorization': `Bearer ${token}`,
      'Content-Type': 'application/json',
    };
  }

  async chatWithAI(request: ChatRequest): Promise<ChatResponse> {
    try {
      const payload: any = {
        message: request.message,
        session_id: request.session_id,
        include_context: request.include_context,
      };
      
      // Ajouter le contexte système et d'analyse si fournis
      if (request.system) {
        payload.system = request.system;
      }
      if (request.analysis_context) {
        payload.analysis_context = request.analysis_context;
      }
      
      const response = await axios.post(
        `${this.baseURL}/chat/`,
        payload,
        { headers: this.getAuthHeaders() }
      );
      return response.data;
    } catch (error) {
      console.error('Erreur lors du chat avec l\'IA:', error);
      throw error;
    }
  }

  async getChatSessions(): Promise<ChatSession[]> {
    try {
      const response = await axios.get(
        `${this.baseURL}/sessions/`,
        { headers: this.getAuthHeaders() }
      );
      return response.data;
    } catch (error) {
      console.error('Erreur lors de la récupération des sessions:', error);
      throw error;
    }
  }

  async getChatSession(sessionId: string): Promise<ChatSession> {
    try {
      const response = await axios.get(
        `${this.baseURL}/sessions/${sessionId}/`,
        { headers: this.getAuthHeaders() }
      );
      return response.data;
    } catch (error) {
      console.error('Erreur lors de la récupération de la session:', error);
      throw error;
    }
  }

  async createNewSession(): Promise<ChatSession> {
    try {
      const response = await axios.post(
        `${this.baseURL}/sessions/new/`,
        {},
        { headers: this.getAuthHeaders() }
      );
      return response.data;
    } catch (error) {
      console.error('Erreur lors de la création de la session:', error);
      throw error;
    }
  }

  async deleteChatSession(sessionId: string): Promise<void> {
    try {
      await axios.delete(
        `${this.baseURL}/sessions/${sessionId}/delete/`,
        { headers: this.getAuthHeaders() }
      );
    } catch (error) {
      console.error('Erreur lors de la suppression de la session:', error);
      throw error;
    }
  }

  async getAISuggestions(): Promise<string[]> {
    try {
      const response = await axios.get(
        `${this.baseURL}/suggestions/`,
        { headers: this.getAuthHeaders() }
      );
      return response.data.suggestions;
    } catch (error) {
      console.error('Erreur lors de la récupération des suggestions:', error);
      throw error;
    }
  }
}

export const chatService = new ChatService();


