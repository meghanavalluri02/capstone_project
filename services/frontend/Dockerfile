# Use the official Node.js image
FROM node:18

# Set working directory inside container
WORKDIR /app

# Only copy the package.json and package-lock.json first
COPY package.json package-lock.json ./

# Install dependencies
RUN npm install

# Now copy the rest of the app source code
COPY . .

# Set environment variable to avoid warnings (optional)
ENV CI=true

# Expose the port your app runs on
EXPOSE 3000

# Start the application
CMD ["npm", "start"]
