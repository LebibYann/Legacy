# ---- Dev stage ----
FROM node:20-alpine

# Set working directory
WORKDIR /app

# Copy package.json and package-lock.json
COPY package*.json ./

# Install dependencies
RUN npm install

# Copy the rest of the code
COPY . .

# Expose Vite dev server port
EXPOSE 5174

# Start the dev server
CMD ["npm", "run", "dev", "--", "--host", "0.0.0.0"]
