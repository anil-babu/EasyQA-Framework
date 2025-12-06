#!/bin/bash
# Quick script to build and run Docker containers

set -e

echo "🐳 EasyQA Framework Docker Build & Run"
echo "======================================="
echo ""

# Parse arguments
MODE=${1:-lightweight}

if [ "$MODE" = "full" ]; then
    echo "📦 Building FULL Docker image..."
    docker build -t easyqa-framework:latest .

    echo ""
    echo "🚀 Running tests in Docker..."
    docker run --rm \
        -v $(pwd)/test-output:/app/test-output \
        -v $(pwd)/screenshots:/app/screenshots \
        -v $(pwd)/logs:/app/logs \
        easyqa-framework:latest

elif [ "$MODE" = "lightweight" ]; then
    echo "📦 Building LIGHTWEIGHT Docker image..."
    docker build -f Dockerfile.lightweight -t easyqa-framework:light .

    echo ""
    echo "🚀 Running tests in Docker..."
    docker run --rm \
        -v $(pwd)/test-output:/app/test-output \
        -v $(pwd)/screenshots:/app/screenshots \
        -v $(pwd)/logs:/app/logs \
        easyqa-framework:light

elif [ "$MODE" = "compose" ]; then
    echo "📦 Starting with docker-compose..."
    docker-compose up --build

elif [ "$MODE" = "compose-light" ]; then
    echo "📦 Starting with docker-compose (lightweight)..."
    docker-compose -f docker-compose.lightweight.yml up --build

else
    echo "❌ Unknown mode: $MODE"
    echo ""
    echo "Usage: $0 [full|lightweight|compose|compose-light]"
    echo ""
    echo "  full           - Full Docker image with all features"
    echo "  lightweight    - Lightweight image (faster, minimal deps)"
    echo "  compose        - Full docker-compose stack with Selenium Grid"
    echo "  compose-light  - Lightweight docker-compose"
    echo ""
    echo "Default: lightweight"
    exit 1
fi

echo ""
echo "✅ Done! Check test-output/ for reports"
