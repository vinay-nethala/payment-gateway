# Step 1: Build the React App
FROM node:18-alpine

WORKDIR /app

# Install dependencies
COPY package*.json ./
RUN npm install

# Copy source code
COPY . .

# Build the project (creates the 'dist' folder)
RUN npm run build

# Install a simple static file server
RUN npm install -g serve

# Serve the 'dist' folder on port 3000
CMD ["serve", "-s", "dist", "-l", "3000"]