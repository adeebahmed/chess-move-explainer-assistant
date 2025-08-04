#!/usr/bin/env python3
"""
Chess Move Explainer Assistant (Stockfish-only version)
Analyzes chess moves using the Stockfish engine.
"""

import os
import chess
import chess.engine
from typing import Tuple, List
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def get_stockfish_path() -> str:
    """Get Stockfish path from environment or use default."""
    stockfish_path = os.getenv('STOCKFISH_PATH', '/opt/homebrew/bin/stockfish')
    if not os.path.exists(stockfish_path):
        raise FileNotFoundError(f"Stockfish not found at {stockfish_path}. Please install Stockfish and update STOCKFISH_PATH in .env")
    return stockfish_path

def evaluate_move(fen: str, move: str) -> Tuple[float, List[str], str]:
    """
    Evaluate a move using Stockfish engine.
    
    Args:
        fen: FEN string representing the board position
        move: Move in algebraic notation (e.g., 'e4', 'Nf3')
    
    Returns:
        Tuple of (evaluation_score, principal_variation, move_san)
    """
    try:
        # Create board from FEN
        board = chess.Board(fen)
        
        # Store original move in SAN format
        move_obj = board.parse_san(move)
        move_san = board.san(move_obj)
        
        # Apply the move to get the resulting position
        board.push(move_obj)
        
        # Initialize Stockfish engine
        stockfish_path = get_stockfish_path()
        with chess.engine.SimpleEngine.popen_uci(stockfish_path) as engine:
            # Analyze the resulting position
            info = engine.analyse(board, chess.engine.Limit(time=2.0), multipv=3)
            
            # Get evaluation score (convert to centipawns)
            score = info[0]["score"].white().score(mate_score=10000)
            if score is None:
                score = 0.0
            
            # Convert to float (positive is good for white, negative for black)
            evaluation = score / 100.0
            
            # Get principal variations (top 3 lines)
            variations = []
            for pv_info in info:
                pv = pv_info.get("pv", [])
                # Convert PV moves to SAN notation
                temp_board = board.copy()
                pv_san = []
                for pv_move in pv[:4]:  # Show first 4 moves of each line
                    if pv_move in temp_board.legal_moves:
                        pv_san.append(temp_board.san(pv_move))
                        temp_board.push(pv_move)
                    else:
                        break
                variations.append(" ".join(pv_san))
            
            return evaluation, variations, move_san
            
    except Exception as e:
        raise ValueError(f"Error evaluating move: {e}")

def classify_move(evaluation: float, side_to_move: str) -> str:
    """Classify the move based on its evaluation."""
    abs_eval = abs(evaluation)
    is_white = side_to_move == 'w'
    eval_sign = evaluation > 0 if is_white else evaluation < 0
    
    if abs_eval < 0.3:
        return "Equal position"
    elif abs_eval < 0.7:
        return "Slight advantage" if eval_sign else "Slight disadvantage"
    elif abs_eval < 1.5:
        return "Clear advantage" if eval_sign else "Clear disadvantage"
    elif abs_eval < 3:
        return "Winning position" if eval_sign else "Lost position"
    else:
        return "Decisive advantage" if eval_sign else "Decisive disadvantage"

def main():
    """Main function to demonstrate the chess move analyzer."""
    
    # Example FEN and move from the prompt
    fen = "r1bqkbnr/pppppppp/n7/8/2B5/5N2/PPPPPPPP/RNBQK2R b KQkq - 0 2"
    move = "e6"
    
    print("♔ Chess Move Analyzer (Stockfish) ♔")
    print("=" * 40)
    
    # Get the side to move from FEN
    board = chess.Board(fen)
    side_to_move = 'w' if board.turn else 'b'
    
    try:
        # Evaluate the move
        print(f"Position: {fen}")
        print(f"Move: {move}")
        print("\n🔍 Analyzing move with Stockfish...")
        evaluation, variations, move_san = evaluate_move(fen, move)
        
        # Print analysis
        print(f"\n📊 Evaluation: {evaluation:+.2f}")
        print(f"💭 Assessment: {classify_move(evaluation, side_to_move)}")
        
        print("\n🎯 Top lines:")
        for i, variation in enumerate(variations, 1):
            print(f"{i}. {variation}")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        print("\n💡 Troubleshooting:")
        print("1. Make sure Stockfish is installed and STOCKFISH_PATH is correct in .env")
        print("2. Check that the FEN string and move are valid")

if __name__ == "__main__":
    main()