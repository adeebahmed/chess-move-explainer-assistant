#!/usr/bin/env python3
"""
Generate a test chess board image that looks like chess.com
"""

import numpy as np
from PIL import Image, ImageDraw, ImageFont
import chess

# Chess.com-like colors
LIGHT_SQUARE = (238, 238, 210)  # Light squares
DARK_SQUARE = (118, 150, 86)    # Dark squares
WHITE_PIECE = (255, 255, 255)   # White pieces
BLACK_PIECE = (60, 60, 60)      # Black pieces
BACKGROUND = (49, 46, 43)       # Background

def create_piece_shape(draw, x, y, radius, color, is_pawn=True):
    """Draw a chess piece shape."""
    # Draw base circle
    draw.ellipse([x-radius-2, y-radius-2, x+radius+2, y+radius+2], fill=(30, 30, 30))
    draw.ellipse([x-radius, y-radius, x+radius, y+radius], fill=color)
    
    if not is_pawn:
        # Add a crown-like shape for non-pawns
        points = [
            (x-radius//2, y-radius//2),
            (x+radius//2, y-radius//2),
            (x, y+radius//2)
        ]
        draw.polygon(points, fill=(30, 30, 30) if color == WHITE_PIECE else (200, 200, 200))

def create_board_image(fen: str, size: int = 800):
    """Create a chess board image with pieces."""
    board = chess.Board(fen)
    square_size = size // 8
    border = square_size // 2
    
    # Create image with background
    img = Image.new('RGB', (size + 2*border, size + 2*border), BACKGROUND)
    draw = ImageDraw.Draw(img)
    
    # Draw squares
    for rank in range(8):
        for file in range(8):
            x1 = file * square_size + border
            y1 = rank * square_size + border
            x2 = x1 + square_size
            y2 = y1 + square_size
            
            # Alternate square colors
            color = LIGHT_SQUARE if (rank + file) % 2 == 0 else DARK_SQUARE
            draw.rectangle([x1, y1, x2, y2], fill=color)
    
    # Draw pieces
    for rank in range(8):
        for file in range(8):
            square = chess.square(file, 7-rank)
            piece = board.piece_at(square)
            
            if piece:
                x = file * square_size + border + square_size//2
                y = rank * square_size + border + square_size//2
                radius = square_size//3
                
                # Draw piece
                color = WHITE_PIECE if piece.color else BLACK_PIECE
                is_pawn = piece.piece_type == chess.PAWN
                create_piece_shape(draw, x, y, radius, color, is_pawn)
    
    return img

def main():
    # Create test position (Italian Game)
    fen = "r1bqkbnr/pppp1ppp/2n5/4p3/2B1P3/5N2/PPPP1PPP/RNBQK2R b KQkq - 3 3"
    
    # Generate image
    img = create_board_image(fen)
    
    # Save image
    img.save("test_board.png")
    print("Created test board image: test_board.png")

if __name__ == "__main__":
    main()