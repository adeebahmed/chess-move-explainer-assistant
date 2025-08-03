#!/usr/bin/env python3
"""
Chess Move Analyzer (Stockfish-only version)
Analyzes chess moves using the Stockfish engine.
"""

import os
import sys
import chess
import chess.engine
from typing import Tuple, List
from dotenv import load_dotenv
from board_recognition import ChessBoardRecognizer

# Load environment variables
load_dotenv()

def get_stockfish_path() -> str:
    """Get Stockfish path from environment or use default."""
    stockfish_path = os.getenv('STOCKFISH_PATH', '/opt/homebrew/bin/stockfish')
    if not os.path.exists(stockfish_path):
        raise FileNotFoundError(f"Stockfish not found at {stockfish_path}")
    return stockfish_path

def evaluate_position(board: chess.Board, move: str = None) -> Tuple[float, List[str]]:
    """Evaluate a position using Stockfish engine."""
    try:
        # Apply the move if provided
        if move:
            move_obj = board.parse_san(move)
            board.push(move_obj)
        
        # Initialize Stockfish engine
        with chess.engine.SimpleEngine.popen_uci(get_stockfish_path()) as engine:
            # Analyze the position
            info = engine.analyse(board, chess.engine.Limit(time=2.0), multipv=3)
            
            # Get evaluation score
            score = info[0]["score"].white().score(mate_score=10000)
            evaluation = (score or 0) / 100.0
            
            # Get principal variations
            variations = []
            for pv_info in info:
                pv = pv_info.get("pv", [])
                temp_board = board.copy()
                pv_san = []
                for pv_move in pv[:4]:
                    if pv_move in temp_board.legal_moves:
                        pv_san.append(temp_board.san(pv_move))
                        temp_board.push(pv_move)
                variations.append(" ".join(pv_san))
            
            return evaluation, variations
            
    except Exception as e:
        raise ValueError(f"Error evaluating position: {e}")

def print_board(board: chess.Board):
    """Print chess board in a nice format."""
    print("\n  Current Position:")
    print("  " + "─" * 33)
    ranks = "87654321"
    files = "abcdefgh"
    
    # Unicode chess pieces
    pieces = {
        'P': '♙', 'N': '♘', 'B': '♗', 'R': '♖', 'Q': '♕', 'K': '♔',
        'p': '♟', 'n': '♞', 'b': '♝', 'r': '♜', 'q': '♛', 'k': '♚',
        '.': '·'
    }
    
    for rank in ranks:
        print(f"{rank} │", end=" ")
        for file in files:
            square = chess.parse_square(file + rank)
            piece = board.piece_at(square)
            if piece:
                print(pieces[piece.symbol()], end=" ")
            else:
                print(pieces['.'], end=" ")
        print("│")
    
    print("  " + "─" * 33)
    print("    a b c d e f g h")
    print()

def print_help():
    """Print usage instructions."""
    print("""
Chess Move Analyzer - Usage Examples:

1. Analyze starting position:
   python analyze.py

2. Analyze after moves:
   python analyze.py e4 e5 Nf3

3. Analyze specific position (FEN):
   python analyze.py "rnbqkbnr/pppppppp/8/8/4P3/8/PPPP1PPP/RNBQKBNR b KQkq - 0 1"

4. Analyze position and move:
   python analyze.py "rnbqkbnr/pppppppp/8/8/4P3/8/PPPP1PPP/RNBQKBNR b KQkq - 0 1" e5

5. Analyze chess.com screenshot:
   python analyze.py --image board.png

6. Show this help:
   python analyze.py --help
""")

def is_valid_fen(fen: str) -> bool:
    """Check if a FEN string is valid."""
    try:
        chess.Board(fen)
        return True
    except ValueError:
        return False

def main():
    """Main function to analyze chess positions."""
    
    if len(sys.argv) == 1:
        # No arguments - use starting position
        board = chess.Board()
        fen = board.fen()
        move = None
    elif len(sys.argv) == 2 and sys.argv[1] in ['--help', '-h', 'help']:
        print_help()
        return
    elif len(sys.argv) == 3 and sys.argv[1] == '--image':
        # Analyze screenshot
        try:
            recognizer = ChessBoardRecognizer()
            fen = recognizer.analyze_screenshot(sys.argv[2])
            board = chess.Board(fen)
            move = None
        except Exception as e:
            print(f"❌ Error analyzing screenshot: {e}")
            return
    elif is_valid_fen(sys.argv[1]):
        # FEN string provided
        fen = sys.argv[1]
        board = chess.Board(fen)
        move = sys.argv[2] if len(sys.argv) > 2 else None
    else:
        # Sequence of moves from starting position
        board = chess.Board()
        for move in sys.argv[1:]:
            try:
                board.push_san(move)
            except ValueError:
                print(f"❌ Invalid move: {move}")
                return
        fen = board.fen()
        move = None
    
    print("♔ Chess Position Analyzer ♔")
    print("=" * 40)
    
    try:
        # Print current position
        print_board(board)
        
        # Show FEN for reference
        print(f"FEN: {fen}")
        if move:
            print(f"Analyzing move: {move}")
        
        print("\n🔍 Analyzing with Stockfish...")
        evaluation, variations = evaluate_position(board, move)
        
        # Print analysis
        print(f"\n📊 Evaluation: {evaluation:+.2f}")
        side_to_move = "Black" if board.turn else "White"
        print(f"   ({side_to_move} to move)")
        
        print("\n🎯 Top lines:")
        for i, variation in enumerate(variations, 1):
            print(f"{i}. {variation}")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        print("\n💡 Troubleshooting:")
        print("1. Make sure Stockfish is installed")
        print("2. Check that your moves or FEN are valid")

if __name__ == "__main__":
    main()