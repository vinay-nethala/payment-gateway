# Step 1: Build the React App
FROM node:18-alpine

WORKDIR /app

# Install dependencies
COPY package*.json ./
RUN npm install
# Install Lucide icons explicitly
RUN npm install lucide-react

# Copy source code
COPY . .

# Build the project (creates 'dist' folder)
RUN npm run build

# Install static file server
RUN npm install -g serve

# Serve the 'dist' folder on port 3001
CMD ["serve", "-s", "dist", "-l", "3001"]