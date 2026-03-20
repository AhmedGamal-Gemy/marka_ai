const AI_BASE_URL = process.env.AI_BASE_URL || 'http://ai:8000'

/**
 * Call AI service with proper headers.
 * @param endpoint - The AI endpoint path (e.g., '/ai/hello')
 * @param method - HTTP method
 * @param authorization - JWT token from request
 * @returns Response from AI service
 */
export async function callAI(endpoint: string, method: string, authorization: string) {
  try {
    const response = await fetch(`${AI_BASE_URL}${endpoint}`, {
      method,
      headers: {
        'X-Service-Key': process.env.AI_SERVICE_KEY || '',
        'Authorization': authorization,
        'Content-Type': 'application/json',
      },
    })
    return await response.json()
  } catch (error) {
    throw new Error(`AI service error: ${error}`)
  }
}
