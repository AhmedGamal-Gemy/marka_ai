# ==========================================
# Stage 1: Development (used in CI)
# ==========================================
FROM node:20-alpine AS development

WORKDIR /app

# Install dependencies
COPY backend/package*.json ./
RUN npm ci

# Copy source code
COPY backend/ .

# Expose port
EXPOSE 3000

# Start development server
CMD ["npm", "run", "dev"]

# ==========================================
# Stage 2: Production Build
# ==========================================
FROM node:20-alpine AS production-build

WORKDIR /app

# Install dependencies only
COPY backend/package*.json ./
RUN npm ci --only=production

# Copy source code
COPY backend/ .

# Build TypeScript
RUN npm run build

# ==========================================
# Stage 3: Production Image
# ==========================================
FROM node:20-alpine AS production

WORKDIR /app

# Copy production build from stage 2
COPY --from=production-build /app/dist ./dist
COPY --from=production-build /app/node_modules ./node_modules
COPY --from=production-build /app/package.json ./

# Create non-root user for security
RUN addgroup -g 1001 -S nodejs && \
    adduser -S nodejs -u 1001 && \
    chown -R nodejs:nodejs /app

USER nodejs

# Expose port
EXPOSE 3000

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=40s --retries=3 \
  CMD node -e "require('http').get('http://localhost:3000/health', (r) => {process.exit(r.statusCode === 200 ? 0 : 1)})"

# Start production server
CMD ["node", "dist/index.js"]
