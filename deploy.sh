#!/bin/bash
# Naviko LAB v1.4.0 Deployment Script

set -e

echo "=========================================="
echo "🚀 Naviko LAB v1.4.0 Deployment"
echo "=========================================="
echo ""

# 1. Environment Check
echo "📋 Checking environment..."
python --version
pip --version
echo ""

# 2. Install Dependencies
echo "📦 Installing dependencies..."
pip install -r requirements.txt
echo ""

# 3. Environment Variables
echo "🔑 Checking environment variables..."
if [ -z "\" ]; then
    echo "⚠️  Warning: GROQ_API_KEY not set"
    echo "   Will use local LLM (Ollama) or template mode"
else
    echo "✅ GROQ_API_KEY: Configured"
fi
echo ""

# 4. Run Tests (Optional)
if [ "\" = "true" ]; then
    echo "🧪 Running tests..."
    pytest tests/ -v
    echo ""
fi

# 5. Setup
echo "⚙️  Running setup..."
python setup.py install
echo ""

echo "=========================================="
echo "✅ Naviko LAB v1.4.0 Deployment Complete"
echo "=========================================="
echo ""
echo "📚 Next Steps:"
echo "  • Documentation: README.md, USER_GUIDE.md"
echo "  • Run tests: pytest tests/"
echo "  • Start using: python -c 'from navikoLAB import *'"
echo ""
