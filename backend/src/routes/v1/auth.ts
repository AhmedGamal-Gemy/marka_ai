import { Router } from 'express'
import jwt from 'jsonwebtoken'

const router = Router()

// Mock user — replace with real DB lookup when auth is built
const MOCK_USER = { id: '1', email: 'demo@marka.ai', plan: 'starter' }

/**
 * Login and receive a JWT.
 * Hello world uses a mock user — no DB needed yet.
 * @route POST /api/v1/auth/login
 * @returns {{ token: string }} Signed JWT
 */
router.post('/login', (_req, res) => {
  const token = jwt.sign(
    { sub: MOCK_USER.id, email: MOCK_USER.email, plan: MOCK_USER.plan },
    process.env.JWT_SECRET!,
    { expiresIn: '24h' }
  )
  res.status(200).json({ success: true, data: { token } })
})

export default router