# ==========================================
# Stage 1: Development
# ==========================================
FROM node:22-alpine AS development

WORKDIR /app

# Install dependencies
COPY backend/package*.json ./
RUN npm install --omit=dev

# Copy source code
COPY backend/ .

# Expose port
EXPOSE 3000

# Start development server
CMD ["npm", "run", "dev"]

# ==========================================
# Stage 2: Production Build
# ==========================================
FROM node:22-alpine AS production-build

WORKDIR /app

# Install dependencies including TypeScript
COPY backend/package*.json ./
RUN npm install

# Copy source code
COPY backend/ .

# Build TypeScript using tsc from node_modules
RUN ./node_modules/.bin/tsc

# ==========================================
# Stage 3: Production Image
# ==========================================
FROM node:22-alpine AS production

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
  CMD node -e "const http=require('http');http.get('http://localhost:3000/health',(r)=>process.exit(r.statusCode===200?0:1))"

# Start production server
CMD ["node", "dist/index.js"]
