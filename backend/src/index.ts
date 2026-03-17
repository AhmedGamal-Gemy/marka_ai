import 'dotenv/config'
import express from 'express'
import cors from 'cors'
import authRoutes from './routes/v1/auth'
import helloRoutes from './routes/v1/hello'

const app = express()

app.use(cors())
app.use(express.json())

// Health check — no auth
app.get('/health', (_req, res) => {
  res.json({ status: 'ok', layer: 'express' })
})

// All routes under /api/v1/
app.use('/api/v1/auth', authRoutes)
app.use('/api/v1/hello', helloRoutes)

const PORT = process.env.PORT || 3000
app.listen(PORT, () => {
  console.log(`Express running on port :${PORT}`)
})