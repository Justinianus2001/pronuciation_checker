#!/bin/bash

###############################################################################
# Docker Deployment Script for Pronunciation Checker
# This script builds and deploys the application using Docker
###############################################################################

set -e

echo "=========================================="
echo "Docker Deployment for Pronunciation Checker"
echo "=========================================="

# Check if Docker is installed
if ! command -v docker &> /dev/null; then
    echo "Error: Docker is not installed. Please install Docker first."
    echo "Visit: https://docs.docker.com/get-docker/"
    exit 1
fi

# Check if Docker Compose is installed
if ! command -v docker-compose &> /dev/null && ! docker compose version &> /dev/null; then
    echo "Error: Docker Compose is not installed. Please install Docker Compose first."
    exit 1
fi

# Check if .env file exists
if [ ! -f ".env" ]; then
    echo "Creating .env file from example..."
    cp .env.example .env
    echo "⚠️  IMPORTANT: Edit .env file and add your Google API key!"
    echo "   Run: nano .env"
    read -p "Press Enter to continue after updating .env file..."
fi

# Create necessary directories
echo "Creating necessary directories..."
mkdir -p uploads logs

# Build Docker image
echo "Building Docker image..."
docker build -t pronunciation-checker:latest .

# Stop existing containers
echo "Stopping existing containers..."
docker-compose down || true

# Start containers
echo "Starting containers..."
docker-compose up -d

# Wait for application to be ready
echo "Waiting for application to start..."
sleep 10

# Check if application is running
echo "Checking application health..."
if curl -f http://localhost:5000/api/v1/health-check &> /dev/null; then
    echo "✓ Application is running successfully!"
else
    echo "⚠️  Warning: Application may not be running correctly."
    echo "Check logs with: docker-compose logs -f"
fi

echo ""
echo "=========================================="
echo "Deployment Complete!"
echo "=========================================="
echo "Application URL: http://localhost:5000"
echo "Health Check: http://localhost:5000/api/v1/health-check"
echo "Storage Stats: http://localhost:5000/api/v1/storage-stats"
echo ""
echo "Useful commands:"
echo "  View logs:        docker-compose logs -f"
echo "  Stop containers:  docker-compose down"
echo "  Restart:          docker-compose restart"
echo "  Rebuild:          docker-compose up -d --build"
echo "=========================================="
