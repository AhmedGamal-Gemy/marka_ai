import { Router } from 'express'
import { authMiddleware } from '../../middleware/auth'
import { callAI } from '../../services/aiService'

const router = Router()

/**
 * Wired hello world.
 * Validates JWT, calls FastAPI (which validates service key + JWT independently),
 * and returns the AI layer response.
 * @route GET /api/v1/hello
 * @returns AI layer greeting confirming full chain
 * @throws {401} Missing or invalid JWT
 * @throws {503} FastAPI unreachable
 */
router.get('/', authMiddleware, async (req, res) => {
  try {
    const result = await callAI('/ai/hello', 'GET', req.headers.authorization!)
    res.json(result)
  } catch (err) {
    res.status(503).json({
      success: false,
      error: 'AI layer unavailable — is FastAPI running?',
    })
  }
})

export default router