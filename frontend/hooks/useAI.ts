import { useState, useCallback } from 'react'
import axios from 'axios'

export interface AIRequest {
  text: string
  purpose: string
  tone: string
}

export interface AIResponse {
  result: string
  success: boolean
  error?: string
}

export interface AITools {
  rewriteTitle: (text: string, tone?: string) => Promise<AIResponse>
  writeAdCopy: (text: string, tone?: string) => Promise<AIResponse>
  writeDescription: (text: string, tone?: string) => Promise<AIResponse>
  explainWhyWinning: (text: string) => Promise<AIResponse>
  analyzeTrends: (text: string) => Promise<AIResponse>
  generateKeywords: (text: string) => Promise<AIResponse>
}

export function useAI(): AITools & {
  loading: boolean
  error: string | null
  clearError: () => void
} {
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState<string | null>(null)

  const makeAIRequest = useCallback(async (endpoint: string, data: AIRequest): Promise<AIResponse> => {
    setLoading(true)
    setError(null)
    
    try {
      const response = await axios.post(`http://localhost:8000/api/ai/${endpoint}`, data)
      return {
        result: response.data.result || response.data,
        success: true
      }
    } catch (err: any) {
      const errorMessage = err.response?.data?.detail || err.message || 'AI request failed'
      setError(errorMessage)
      return {
        result: '',
        success: false,
        error: errorMessage
      }
    } finally {
      setLoading(false)
    }
  }, [])

  const rewriteTitle = useCallback(async (text: string, tone: string = 'professional'): Promise<AIResponse> => {
    return makeAIRequest('rewrite-title', { text, purpose: 'title', tone })
  }, [makeAIRequest])

  const writeAdCopy = useCallback(async (text: string, tone: string = 'persuasive'): Promise<AIResponse> => {
    return makeAIRequest('write-ad-copy', { text, purpose: 'ad_copy', tone })
  }, [makeAIRequest])

  const writeDescription = useCallback(async (text: string, tone: string = 'informative'): Promise<AIResponse> => {
    return makeAIRequest('write-description', { text, purpose: 'description', tone })
  }, [makeAIRequest])

  const explainWhyWinning = useCallback(async (text: string): Promise<AIResponse> => {
    return makeAIRequest('explain-why-winning', { text, purpose: 'analysis', tone: 'analytical' })
  }, [makeAIRequest])

  const analyzeTrends = useCallback(async (text: string): Promise<AIResponse> => {
    return makeAIRequest('analyze-trends', { text, purpose: 'trend_analysis', tone: 'analytical' })
  }, [makeAIRequest])

  const generateKeywords = useCallback(async (text: string): Promise<AIResponse> => {
    return makeAIRequest('generate-keywords', { text, purpose: 'keywords', tone: 'professional' })
  }, [makeAIRequest])

  const clearError = useCallback(() => {
    setError(null)
  }, [])

  return {
    rewriteTitle,
    writeAdCopy,
    writeDescription,
    explainWhyWinning,
    analyzeTrends,
    generateKeywords,
    loading,
    error,
    clearError
  }
} 