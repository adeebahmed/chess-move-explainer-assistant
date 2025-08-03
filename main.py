#!/usr/bin/env python3
"""
Chess Move Explainer Assistant
Combines Stockfish engine analysis with GPT explanations for chess moves.
"""

import os
import chess
import chess.engine
from typing import Tuple, List, Optional
import openai
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def get_stockfish_path() -> str:
    """Get Stockfish path from environment or use default."""
    stockfish_path = os.getenv('STOCKFISH_PATH', '/usr/local/bin/stockfish')
    if not os.path.exists(stockfish_path):
        raise FileNotFoundError(f"Stockfish not found at {stockfish_path}. Please install Stockfish and update STOCKFISH_PATH in .env")
    return stockfish_path

def get_openai_api_key() -> str:
    """Get OpenAI API key from environment."""
    api_key = os.getenv('OPENAI_API_KEY')
    if not api_key or api_key == 'your_openai_api_key_here':
        raise ValueError("Please set your OpenAI API key in the .env file")
    return api_key

def evaluate_move(fen: str, move: str) -> Tuple[float, List[chess.Move], str]:
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
        
        # Parse the move
        move_obj = board.parse_san(move)
        
        # Apply the move to get the resulting position
        board.push(move_obj)
        resulting_fen = board.fen()
        
        # Initialize Stockfish engine
        stockfish_path = get_stockfish_path()
        with chess.engine.SimpleEngine.popen_uci(stockfish_path) as engine:
            # Analyze the resulting position
            result = engine.analyse(board, chess.engine.Limit(time=2.0), multipv=1)
            
            # Get evaluation score (convert to centipawns)
            score = result[0]["score"].white().score(mate_score=10000)
            if score is None:
                score = 0.0
            
            # Convert to float (positive is good for white, negative for black)
            evaluation = score / 100.0
            
            # Get principal variation
            pv = result[0].get("pv", [])
            
            # Convert PV moves to SAN notation for readability
            pv_san = []
            temp_board = board.copy()
            for pv_move in pv:
                if pv_move in temp_board.legal_moves:
                    pv_san.append(temp_board.san(pv_move))
                    temp_board.push(pv_move)
                else:
                    break
            
            return evaluation, pv_san, move
            
    except Exception as e:
        raise ValueError(f"Error evaluating move: {e}")

def get_explanation(fen: str, move: str, evaluation: float, pv: List[str], side_to_move: str) -> str:
    """
    Get a natural language explanation of the move using GPT.
    
    Args:
        fen: Original FEN string
        move: Move played
        evaluation: Stockfish evaluation score
        pv: Principal variation from Stockfish
        side_to_move: 'w' for white, 'b' for black
    
    Returns:
        Natural language explanation of the move
    """
    try:
        # Initialize OpenAI client
        openai.api_key = get_openai_api_key()
        
        # Determine if the move is good or bad
        if side_to_move == 'w':
            # For white, positive evaluation is good
            move_quality = "good" if evaluation > 0.1 else "bad" if evaluation < -0.1 else "neutral"
        else:
            # For black, negative evaluation is good (from white's perspective)
            move_quality = "good" if evaluation < -0.1 else "bad" if evaluation > 0.1 else "neutral"
        
        # Classify the move based on evaluation
        if abs(evaluation) < 0.1:
            classification = "equal"
        elif abs(evaluation) < 0.5:
            classification = "inaccuracy"
        elif abs(evaluation) < 1.0:
            classification = "mistake"
        else:
            classification = "blunder"
        
        # Create the prompt for GPT
        prompt = f"""You are a chess expert analyzing a move. Here's the situation:

Position (FEN): {fen}
Move played: {move}
Side to move: {'White' if side_to_move == 'w' else 'Black'}
Stockfish evaluation: {evaluation:.2f} (positive favors White, negative favors Black)
Best continuation: {' '.join(pv[:3]) if pv else 'No continuation available'}

Please provide a brief, clear explanation of this move in 2-3 sentences. Focus on:
1. Whether the move is good, bad, or neutral
2. Why it's good/bad (tactical, positional, development, etc.)
3. What the player should have done instead (if it's a mistake)

Keep it conversational and educational for a chess player."""
        
        # Call GPT
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful chess expert who explains moves clearly and concisely."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=200,
            temperature=0.7
        )
        
        return response.choices[0].message.content.strip()
        
    except Exception as e:
        return f"Error getting explanation: {e}"

def main():
    """Main function to demonstrate the chess move explainer."""
    
    # Example FEN and move from the prompt
    fen = "r1bqkbnr/pppppppp/n7/8/2B5/5N2/PPPPPPPP/RNBQK2R b KQkq - 0 2"
    move = "e6"
    
    print("♔ Chess Move Explainer Assistant ♔")
    print("=" * 40)
    print(f"Position: {fen}")
    print(f"Move: {move}")
    print()
    
    try:
        # Get the side to move from FEN
        board = chess.Board(fen)
        side_to_move = 'w' if board.turn else 'b'
        
        # Evaluate the move
        print("🔍 Analyzing move with Stockfish...")
        evaluation, pv, move_san = evaluate_move(fen, move)
        
        print(f"📊 Evaluation: {evaluation:+.2f}")
        if pv:
            print(f"🎯 Best continuation: {' '.join(pv[:3])}")
        print()
        
        # Get explanation from GPT
        print("🤖 Getting explanation from GPT...")
        explanation = get_explanation(fen, move, evaluation, pv, side_to_move)
        
        print("💡 Explanation:")
        print(explanation)
        
    except Exception as e:
        print(f"❌ Error: {e}")
        print("\n💡 Troubleshooting:")
        print("1. Make sure Stockfish is installed and STOCKFISH_PATH is correct in .env")
        print("2. Set your OpenAI API key in the .env file")
        print("3. Check that the FEN string and move are valid")

if __name__ == "__main__":
    main() 