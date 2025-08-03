# 🚀 Quick Start Guide

Get your Chess Move Explainer Assistant running in 3 minutes!

## ⚡ Super Quick Setup

1. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

2. **Install Stockfish** (if not already installed):
   ```bash
   # macOS
   brew install stockfish
   
   # Linux
   sudo apt-get install stockfish
   
   # Windows: Download from https://stockfishchess.org/download/
   ```

3. **Configure API key**:
   - Edit `.env` file
   - Replace `your_openai_api_key_here` with your actual OpenAI API key
   - Get your key from: https://platform.openai.com/api-keys

4. **Test everything**:
   ```bash
   python test_setup.py
   ```

5. **Run the app**:
   ```bash
   python main.py
   ```

## 🎯 Example Usage

### Basic Example
```bash
python main.py
```

### CLI with Custom Position
```bash
python cli.py "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1" "e4"
```

### CLI with Verbose Output
```bash
python cli.py "r1bqkbnr/pppppppp/n7/8/2B5/5N2/PPPPPPPP/RNBQK2R b KQkq - 0 2" "e6" --verbose
```

## 🔧 Troubleshooting

**"Stockfish not found"**
- Install Stockfish: `brew install stockfish` (macOS)
- Update path in `.env` file

**"OpenAI API key error"**
- Set your API key in `.env` file
- Get key from: https://platform.openai.com/api-keys

**"Import errors"**
- Run: `pip install -r requirements.txt`

## 📚 What You Get

- **Stockfish Analysis**: Professional chess engine evaluation
- **GPT Explanations**: Human-readable move explanations
- **Move Classification**: Automatic categorization of move quality
- **Best Continuations**: Shows what should be played next
- **CLI Interface**: Easy command-line usage

## 🎮 Try These Examples

1. **Starting position, e4**:
   ```bash
   python cli.py "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1" "e4"
   ```

2. **Your example position**:
   ```bash
   python cli.py "r1bqkbnr/pppppppp/n7/8/2B5/5N2/PPPPPPPP/RNBQK2R b KQkq - 0 2" "e6"
   ```

3. **Test a mistake**:
   ```bash
   python cli.py "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1" "f3"
   ```

That's it! You now have a working chess move explainer assistant. 🎉 