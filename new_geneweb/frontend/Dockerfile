FROM node:24-alpine

# Set working directory
WORKDIR /app

# Copy the code
COPY . .

# Install dependencies
RUN npm install

# Build the application
RUN npm run build

# Expose Vite dev server port
EXPOSE 5174

# Create .env file
RUN echo "PORT=5174" > .env

# Start the dev server
CMD ["node", "--env-file=.env", "build"]
