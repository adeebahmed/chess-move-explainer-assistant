#!/usr/bin/env python3
"""
CLI version of the Chess Move Explainer Assistant
Usage: python cli.py <fen> <move>
"""

import sys
import argparse
from main import evaluate_move, get_explanation

def main():
    parser = argparse.ArgumentParser(
        description="Chess Move Explainer Assistant - Analyze chess moves with Stockfish and GPT",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python cli.py "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1" "e4"
  python cli.py "r1bqkbnr/pppppppp/n7/8/2B5/5N2/PPPPPPPP/RNBQK2R b KQkq - 0 2" "e6"
        """
    )
    
    parser.add_argument(
        "fen", 
        help="FEN string representing the chess position"
    )
    
    parser.add_argument(
        "move", 
        help="Move in algebraic notation (e.g., e4, Nf3, O-O)"
    )
    
    parser.add_argument(
        "--verbose", "-v",
        action="store_true",
        help="Show detailed analysis information"
    )
    
    args = parser.parse_args()
    
    print("♔ Chess Move Explainer Assistant ♔")
    print("=" * 40)
    print(f"Position: {args.fen}")
    print(f"Move: {args.move}")
    print()
    
    try:
        import chess
        board = chess.Board(args.fen)
        side_to_move = 'w' if board.turn else 'b'
        
        # Evaluate the move
        print("🔍 Analyzing move with Stockfish...")
        evaluation, pv, move_san = evaluate_move(args.fen, args.move)
        
        print(f"📊 Evaluation: {evaluation:+.2f}")
        if pv:
            print(f"🎯 Best continuation: {' '.join(pv[:3])}")
        
        if args.verbose:
            print(f"📋 Full principal variation: {' '.join(pv)}")
            print(f"♟️  Side to move: {'White' if side_to_move == 'w' else 'Black'}")
        
        print()
        
        # Get explanation from GPT
        print("🤖 Getting explanation from GPT...")
        explanation = get_explanation(args.fen, args.move, evaluation, pv, side_to_move)
        
        print("💡 Explanation:")
        print(explanation)
        
    except Exception as e:
        print(f"❌ Error: {e}")
        print("\n💡 Troubleshooting:")
        print("1. Make sure Stockfish is installed and STOCKFISH_PATH is correct in .env")
        print("2. Set your OpenAI API key in the .env file")
        print("3. Check that the FEN string and move are valid")
        sys.exit(1)

if __name__ == "__main__":
    main() 