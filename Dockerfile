# ----------------------
# Builder Stage
# ----------------------
    FROM node:18-alpine AS builder

    WORKDIR /app
    
    # Copy package.json and package-lock.json
    COPY package*.json ./
    
    # Install dependencies
    RUN npm install
    
    # Copy all source code
    COPY . .
    
    # Build the application
    RUN npm run build
    
    # ----------------------
    # Production Stage
    # ----------------------
    FROM node:18-alpine AS runner
    
    WORKDIR /app
    
    # Copy package.json and package-lock.json
    COPY --from=builder /app/package*.json ./
    
    # Copy node_modules
    COPY --from=builder /app/node_modules ./node_modules
    
    # Copy built Next.js files
    COPY --from=builder /app/.next ./.next
    COPY --from=builder /app/public ./public
    
    # Copy next.config.mjs
    COPY --from=builder /app/next.config.mjs ./
    
    ENV NODE_ENV production
    
    EXPOSE 8080
    
    CMD ["npm", "run", "start"]
    