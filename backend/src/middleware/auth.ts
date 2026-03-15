import { Request, Response, NextFunction } from 'express'
import jwt from 'jsonwebtoken'

export function authMiddleware(req: Request, res: Response, next: NextFunction) {
  const auth = req.headers.authorization

  if (!auth?.startsWith('Bearer ')) {
    return res.status(401).json({ success: false, error: 'Missing token' })
  }

  try {
    const payload = jwt.verify(auth.split(' ')[1], process.env.JWT_SECRET!) as any
    req.user = { id: payload.sub, email: payload.email, plan: payload.plan }
    next()
  } catch {
    res.status(401).json({ success: false, error: 'Invalid or expired token' })
  }
}