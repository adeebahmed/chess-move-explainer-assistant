#!/usr/bin/env python3
"""
Chess.com Board Recognition Module
Analyzes chess.com screenshots by checking each square individually
"""

import cv2
import numpy as np
import chess
import os

class ChessBoardRecognizer:
    def __init__(self):
        """Initialize the board recognizer."""
        self.square_size = None
        self.debug = True
        self.debug_dir = "debug_images"
        
        if self.debug and not os.path.exists(self.debug_dir):
            os.makedirs(self.debug_dir)

    def analyze_screenshot(self, image_path: str) -> str:
        """
        Analyze a chess.com screenshot and return the FEN position.
        """
        try:
            # Read image
            img = cv2.imread(image_path)
            if img is None:
                raise ValueError(f"Could not read image: {image_path}")
            
            # Convert BGR to RGB
            img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            
            # Get image dimensions
            height, width = img.shape[:2]
            
            # For chess.com screenshots, calculate square size
            self.square_size = min(width, height) // 8
            
            # Initialize empty board
            board = [['' for _ in range(8)] for _ in range(8)]
            
            # Process each square
            for rank in range(8):
                for file in range(8):
                    # Extract square region
                    x = file * self.square_size
                    y = rank * self.square_size
                    square = img[y:y+self.square_size, x:x+self.square_size]
                    
                    # Analyze square
                    piece = self.analyze_square(square, rank, file)
                    board[rank][file] = piece
                    
                    if self.debug:
                        # Save square image for debugging
                        debug_path = os.path.join(self.debug_dir, f'square_{rank}_{file}.png')
                        cv2.imwrite(debug_path, cv2.cvtColor(square, cv2.COLOR_RGB2BGR))
            
            # Convert board array to FEN
            fen = self.board_to_fen(board)
            
            return fen
            
        except Exception as e:
            raise ValueError(f"Error analyzing screenshot: {e}")

    def analyze_square(self, square_img: np.ndarray, rank: int, file: int) -> str:
        """
        Analyze a single square to determine piece type and color.
        Returns FEN symbol for the piece (empty string if no piece).
        """
        # Get bottom edge of square
        h, w = square_img.shape[:2]
        bottom_edge = square_img[-3:, w//4:3*w//4]  # Last 3 rows, middle half
        
        # Calculate average color
        avg_color = np.mean(bottom_edge, axis=(0,1))
        r, g, b = avg_color
        
        # Calculate color ratios
        rg_ratio = r / (g + 1)  # Add 1 to avoid division by zero
        rb_ratio = r / (b + 1)
        gb_ratio = g / (b + 1)
        
        # Calculate brightness
        brightness = np.mean([r, g, b])
        
        if self.debug:
            debug_path = os.path.join(self.debug_dir, f'piece_{rank}_{file}.txt')
            with open(debug_path, 'w') as f:
                f.write(f"Bottom color (RGB): {avg_color}\n")
                f.write(f"R/G ratio: {rg_ratio:.2f}\n")
                f.write(f"R/B ratio: {rb_ratio:.2f}\n")
                f.write(f"G/B ratio: {gb_ratio:.2f}\n")
                f.write(f"Brightness: {brightness:.1f}\n")
        
        # Empty squares have low brightness and balanced color ratios
        if brightness < 100 and 1.4 < rg_ratio < 1.6 and 2.4 < rb_ratio < 2.6:
            return ''
        
        # White pieces have high brightness and high red ratios
        is_white = brightness > 150 and rg_ratio > 1.3 and rb_ratio > 2.0
        
        # Get top region for piece type identification
        top_region = square_img[h//8:3*h//8, w//4:3*w//4]
        
        # Convert to grayscale and threshold
        gray = cv2.cvtColor(top_region, cv2.COLOR_RGB2GRAY)
        _, binary = cv2.threshold(gray, 128, 255, cv2.THRESH_BINARY)
        
        # Calculate width profile (percentage of piece pixels in each column)
        width_profile = np.sum(binary > 128, axis=0) / binary.shape[0]
        
        # Calculate shape features
        top_width = np.mean(width_profile)
        width_std = np.std(width_profile)
        
        if self.debug:
            with open(debug_path, 'a') as f:
                f.write(f"Top width: {top_width:.2f}\n")
                f.write(f"Width std: {width_std:.2f}\n")
        
        # Identify piece type based on shape
        if top_width > 0.7:  # Very wide top
            piece = 'K'  # King
        elif top_width > 0.5:  # Wide top
            piece = 'Q'  # Queen
        elif width_std > 0.3:  # Irregular top
            piece = 'N'  # Knight
        elif 0.3 < top_width < 0.5:  # Medium top
            piece = 'B'  # Bishop
        elif top_width < 0.3:  # Narrow top
            piece = 'R'  # Rook
        else:  # Default to pawn
            piece = 'P'  # Pawn
            
        return piece if is_white else piece.lower()

    def board_to_fen(self, board: list) -> str:
        """Convert board array to FEN notation."""
        fen_parts = []
        
        # Process each rank
        for rank in board:
            empty_count = 0
            rank_str = ''
            
            for square in rank:
                if square == '':
                    empty_count += 1
                else:
                    if empty_count > 0:
                        rank_str += str(empty_count)
                        empty_count = 0
                    rank_str += square
            
            if empty_count > 0:
                rank_str += str(empty_count)
            
            fen_parts.append(rank_str)
        
        # Join ranks with '/' and reverse (since we processed from top to bottom)
        fen = '/'.join(reversed(fen_parts))
        
        # Add other FEN components (assuming white to move, all castling available)
        fen += ' w KQkq - 0 1'
        
        return fen

def main():
    """Test the board recognition with a sample image."""
    recognizer = ChessBoardRecognizer()
    
    # Get image path from command line
    import sys
    if len(sys.argv) != 2:
        print("Usage: python board_recognition.py <image_path>")
        return
    
    image_path = sys.argv[1]
    
    try:
        fen = recognizer.analyze_screenshot(image_path)
        print(f"Detected FEN: {fen}")
        
        # Create a board from FEN to validate it
        board = chess.Board(fen)
        print("\nDetected position:")
        print(board)
        
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()