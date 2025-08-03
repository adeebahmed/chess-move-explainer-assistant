#!/bin/bash

echo "♔ Chess Move Explainer Assistant - Setup Script ♔"
echo "=================================================="

# Check if Python 3 is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed. Please install Python 3.7+ first."
    exit 1
fi

echo "✅ Python 3 found: $(python3 --version)"

# Install dependencies
echo ""
echo "📦 Installing Python dependencies..."
pip3 install -r requirements.txt

if [ $? -eq 0 ]; then
    echo "✅ Dependencies installed successfully"
else
    echo "❌ Failed to install dependencies"
    exit 1
fi

# Check if Stockfish is installed
echo ""
echo "🔍 Checking for Stockfish..."
if command -v stockfish &> /dev/null; then
    STOCKFISH_PATH=$(which stockfish)
    echo "✅ Stockfish found at: $STOCKFISH_PATH"
    
    # Update .env file with correct Stockfish path
    sed -i.bak "s|STOCKFISH_PATH=.*|STOCKFISH_PATH=$STOCKFISH_PATH|" .env
    echo "✅ Updated .env with Stockfish path"
else
    echo "⚠️  Stockfish not found in PATH"
    echo "   Please install Stockfish:"
    echo "   - macOS: brew install stockfish"
    echo "   - Linux: sudo apt-get install stockfish"
    echo "   - Windows: Download from https://stockfishchess.org/download/"
    echo ""
    echo "   Then update STOCKFISH_PATH in .env file"
fi

echo ""
echo "🔧 Configuration:"
echo "1. Edit .env file and set your OpenAI API key:"
echo "   OPENAI_API_KEY=your_actual_api_key_here"
echo ""
echo "2. Test your setup:"
echo "   python3 test_setup.py"
echo ""
echo "3. Run the application:"
echo "   python3 main.py"
echo ""
echo "4. Or use CLI version:"
echo "   python3 cli.py \"<fen>\" \"<move>\""
echo ""
echo "🎉 Setup complete! Check the README.md for detailed instructions." 