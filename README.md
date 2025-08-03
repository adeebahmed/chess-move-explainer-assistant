# ♔ Chess Move Explainer Assistant

A Python application that combines Stockfish chess engine analysis with GPT explanations to provide natural language insights about chess moves.

## 🚀 Features

- **Stockfish Integration**: Uses the powerful Stockfish engine for accurate move evaluation
- **GPT Explanations**: Provides human-readable explanations of move quality using OpenAI's GPT
- **Move Classification**: Automatically categorizes moves as inaccuracies, mistakes, or blunders
- **Principal Variation**: Shows the best continuation after the analyzed move
- **Easy Setup**: Simple configuration via environment variables

## 📋 Prerequisites

1. **Python 3.7+**
2. **Stockfish Engine**: Download and install from [Stockfish website](https://stockfishchess.org/download/)
3. **OpenAI API Key**: Get one from [OpenAI Platform](https://platform.openai.com/api-keys)

## 🛠️ Installation

1. **Clone or download this project**
2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure environment variables**:
   - Copy the `.env` file and update it with your settings:
   ```bash
   # Stockfish engine path - update this to your local Stockfish installation
   STOCKFISH_PATH=/usr/local/bin/stockfish
   
   # OpenAI API key - get yours from https://platform.openai.com/api-keys
   OPENAI_API_KEY=your_actual_api_key_here
   ```

## 🎯 Usage

Run the application with the default example:

```bash
python main.py
```

### Example Output

```
♔ Chess Move Explainer Assistant ♔
========================================
Position: r1bqkbnr/pppppppp/n7/8/2B5/5N2/PPPPPPPP/RNBQK2R b KQkq - 0 2
Move: e6

🔍 Analyzing move with Stockfish...
📊 Evaluation: +0.25
🎯 Best continuation: e6 Nc3 d5

🤖 Getting explanation from GPT...
💡 Explanation:
e6 is a solid but passive move. It delays kingside development and doesn't 
contest the center directly. A more active approach would be to develop the 
knight to f6 or play d5 to challenge White's center control.
```

## 🔧 Customization

### Using Different Positions and Moves

To analyze different positions, modify the `fen` and `move` variables in the `main()` function:

```python
fen = "your_fen_string_here"
move = "your_move_here"
```

### FEN String Format

FEN (Forsyth-Edwards Notation) represents chess positions. Example:
- Starting position: `rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1`
- Your example: `r1bqkbnr/pppppppp/n7/8/2B5/5N2/PPPPPPPP/RNBQK2R b KQkq - 0 2`

### Move Notation

Use standard algebraic notation:
- `e4`, `d5`, `Nf3`, `Bxc6`, `O-O` (castling), etc.

## 🐛 Troubleshooting

### Common Issues

1. **Stockfish not found**:
   ```
   FileNotFoundError: Stockfish not found at /usr/local/bin/stockfish
   ```
   **Solution**: Update `STOCKFISH_PATH` in `.env` to point to your Stockfish installation

2. **OpenAI API key error**:
   ```
   ValueError: Please set your OpenAI API key in the .env file
   ```
   **Solution**: Add your OpenAI API key to the `.env` file

3. **Invalid FEN or move**:
   ```
   ValueError: Error evaluating move: ...
   ```
   **Solution**: Check that your FEN string and move are valid chess notation

### Finding Stockfish Path

**macOS** (if installed via Homebrew):
```bash
which stockfish
# Usually: /usr/local/bin/stockfish
```

**Linux**:
```bash
which stockfish
# Usually: /usr/bin/stockfish or /usr/local/bin/stockfish
```

**Windows**:
- Stockfish is typically in the same directory as the executable
- Update path to: `C:\path\to\stockfish.exe`

## 📚 Dependencies

- `python-chess`: Chess library for Python
- `openai`: OpenAI API client
- `python-dotenv`: Environment variable management

## 🎯 Future Enhancements

- [ ] Add mistake classification: inaccuracy, mistake, blunder (based on centipawn loss)
- [ ] Add CLI arguments for FEN + move input
- [ ] Cache Stockfish evaluations to avoid duplicate analysis
- [ ] Wrap as a local API endpoint using Flask/FastAPI
- [ ] Add support for analyzing entire games
- [ ] Include move alternatives and their evaluations

## 📄 License

This project is open source and available under the MIT License.

## 🤝 Contributing

Feel free to submit issues and enhancement requests! 