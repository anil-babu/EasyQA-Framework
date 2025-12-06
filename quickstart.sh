#!/bin/bash
# EasyQA Framework Quick Start Script

set -e

echo "🚀 EasyQA AI Testing Framework - Quick Start"
echo "=============================================="

# Check prerequisites
check_prerequisites() {
    echo ""
    echo "📋 Checking prerequisites..."

    if ! command -v java &> /dev/null; then
        echo "❌ Java not found. Please install JDK 11+"
        exit 1
    fi
    echo "✅ Java found: $(java -version 2>&1 | head -n 1)"

    if ! command -v mvn &> /dev/null; then
        echo "❌ Maven not found. Please install Maven 3.6+"
        exit 1
    fi
    echo "✅ Maven found: $(mvn -version | head -n 1)"

    if ! command -v python3 &> /dev/null; then
        echo "❌ Python not found. Please install Python 3.9+"
        exit 1
    fi
    echo "✅ Python found: $(python3 --version)"

    if ! command -v pip3 &> /dev/null; then
        echo "❌ pip not found. Please install pip"
        exit 1
    fi
    echo "✅ pip found"
}

# Install dependencies
install_dependencies() {
    echo ""
    echo "📦 Installing dependencies..."

    echo "Installing Java dependencies..."
    mvn clean install -DskipTests

    echo "Installing Python dependencies..."
    pip3 install -r requirements.txt

    echo "Installing Playwright browsers..."
    playwright install
    playwright install-deps
}

# Create directories
create_directories() {
    echo ""
    echo "📁 Creating necessary directories..."

    mkdir -p screenshots
    mkdir -p videos
    mkdir -p logs
    mkdir -p visual_baselines
    mkdir -p visual_results
    mkdir -p data
    mkdir -p test_data
    mkdir -p models
    mkdir -p test-output/reports

    echo "✅ Directories created"
}

# Run demo tests
run_demo() {
    echo ""
    echo "🧪 Running demo tests..."

    echo ""
    echo "1️⃣ Running Java tests..."
    mvn test -Dtest=LoginTests || true

    echo ""
    echo "2️⃣ Running Python AI tests..."
    pytest python/easyqa/tests/examples/test_ecommerce_demo.py::test_ml_predictions -v -s || true

    echo ""
    echo "✅ Demo tests completed!"
}

# Show next steps
show_next_steps() {
    echo ""
    echo "=============================================="
    echo "🎉 Setup Complete!"
    echo "=============================================="
    echo ""
    echo "📚 Next Steps:"
    echo ""
    echo "1. Run Java tests:"
    echo "   mvn test"
    echo ""
    echo "2. Run Python tests:"
    echo "   pytest python/easyqa/tests/ -v"
    echo ""
    echo "3. Run example e-commerce tests:"
    echo "   pytest python/easyqa/tests/examples/test_ecommerce_demo.py -v -s"
    echo ""
    echo "4. Generate test data:"
    echo "   python python/easyqa/cli.py generate users --count 10"
    echo ""
    echo "5. View analytics:"
    echo "   python python/easyqa/cli.py analytics insights"
    echo ""
    echo "6. Generate reports:"
    echo "   mvn allure:serve  (Java tests)"
    echo "   pytest --html=report.html  (Python tests)"
    echo ""
    echo "7. Run with Docker:"
    echo "   docker-compose up"
    echo ""
    echo "📖 Documentation:"
    echo "   - README.md - Project overview"
    echo "   - README_AI.md - Complete AI features guide"
    echo ""
    echo "=============================================="
}

# Main execution
main() {
    check_prerequisites
    install_dependencies
    create_directories

    echo ""
    read -p "🤔 Do you want to run demo tests? (y/n): " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        run_demo
    fi

    show_next_steps
}

# Run main
main
