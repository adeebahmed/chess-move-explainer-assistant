#!/usr/bin/env python3
"""
Chess.com Board Recognition Module
Detects chess positions from chess.com screenshots
"""

import cv2
import numpy as np
from PIL import Image
import chess
from pathlib import Path
from typing import Tuple, Optional

class ChessBoardRecognizer:
    def __init__(self):
        """Initialize the board recognizer with piece templates."""
        self.piece_templates = {}
        self.square_size = None
        self.board_corners = None
        
        # Chess.com piece colors
        self.white_color = np.array([235, 235, 235])  # RGB
        self.black_color = np.array([85, 85, 85])     # RGB
        
    def load_piece_templates(self, template_dir: str):
        """Load piece template images from directory."""
        template_path = Path(template_dir)
        for piece_file in template_path.glob("*.png"):
            piece_name = piece_file.stem  # e.g., 'white_king', 'black_pawn'
            template = cv2.imread(str(piece_file), cv2.IMREAD_GRAYSCALE)
            self.piece_templates[piece_name] = template
    
    def detect_board(self, image_path: str) -> Tuple[np.ndarray, Tuple[int, int, int, int]]:
        """
        Detect the chess board in the image and return the cropped board and corners.
        """
        # Read image
        img = cv2.imread(image_path)
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        
        # Apply adaptive thresholding
        thresh = cv2.adaptiveThreshold(
            gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2
        )
        
        # Find contours
        contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        
        # Find the largest square contour (the board)
        max_area = 0
        board_contour = None
        
        for contour in contours:
            area = cv2.contourArea(contour)
            if area > max_area:
                # Check if it's approximately square
                peri = cv2.arcLength(contour, True)
                approx = cv2.approxPolyDP(contour, 0.02 * peri, True)
                
                if len(approx) == 4:  # It's a rectangle
                    (x, y, w, h) = cv2.boundingRect(approx)
                    aspect_ratio = w / float(h)
                    
                    # Check if it's approximately square (aspect ratio close to 1)
                    if 0.9 <= aspect_ratio <= 1.1:
                        max_area = area
                        board_contour = approx
        
        if board_contour is None:
            raise ValueError("Could not detect chess board in image")
        
        # Get corner points
        rect = cv2.minAreaRect(board_contour)
        box = cv2.boxPoints(rect)
        box = np.int0(box)
        
        # Sort corners
        box = self._sort_corners(box)
        
        # Get transformation matrix
        width = height = int(max(
            np.linalg.norm(box[0] - box[1]),
            np.linalg.norm(box[2] - box[3])
        ))
        
        dst_points = np.array([
            [0, 0],
            [width - 1, 0],
            [width - 1, height - 1],
            [0, height - 1]
        ], dtype="float32")
        
        transform_matrix = cv2.getPerspectiveTransform(box.astype("float32"), dst_points)
        board_img = cv2.warpPerspective(img, transform_matrix, (width, height))
        
        self.square_size = width // 8
        self.board_corners = box
        
        return board_img
    
    def _sort_corners(self, corners: np.ndarray) -> np.ndarray:
        """Sort corners in order: top-left, top-right, bottom-right, bottom-left."""
        rect = np.zeros((4, 2), dtype="float32")
        
        # Top-left will have the smallest sum
        # Bottom-right will have the largest sum
        s = corners.sum(axis=1)
        rect[0] = corners[np.argmin(s)]
        rect[2] = corners[np.argmax(s)]
        
        # Top-right will have the smallest difference
        # Bottom-left will have the largest difference
        diff = np.diff(corners, axis=1)
        rect[1] = corners[np.argmin(diff)]
        rect[3] = corners[np.argmax(diff)]
        
        return rect
    
    def get_square_color(self, square_img: np.ndarray) -> str:
        """
        Determine if a square contains a white piece, black piece, or is empty.
        """
        # Convert to RGB for color comparison
        rgb_img = cv2.cvtColor(square_img, cv2.COLOR_BGR2RGB)
        
        # Get the center region of the square
        h, w = square_img.shape[:2]
        center_region = rgb_img[h//4:3*h//4, w//4:3*w//4]
        
        # Calculate average color
        avg_color = np.mean(center_region, axis=(0, 1))
        
        # Compare with piece colors
        white_dist = np.linalg.norm(avg_color - self.white_color)
        black_dist = np.linalg.norm(avg_color - self.black_color)
        
        # Thresholds for piece detection
        if white_dist < 50:  # Adjust threshold as needed
            return 'white'
        elif black_dist < 50:  # Adjust threshold as needed
            return 'black'
        else:
            return 'empty'
    
    def board_to_fen(self, board_img: np.ndarray) -> str:
        """
        Convert the board image to FEN notation.
        """
        # Initialize empty board
        board = [['' for _ in range(8)] for _ in range(8)]
        
        # Process each square
        for rank in range(8):
            for file in range(8):
                # Extract square image
                x = file * self.square_size
                y = rank * self.square_size
                square_img = board_img[y:y+self.square_size, x:x+self.square_size]
                
                # Determine piece color
                color = self.get_square_color(square_img)
                
                if color == 'white':
                    # For now, assume all white pieces are pawns (P)
                    # You'll need to implement piece type recognition
                    board[rank][file] = 'P'
                elif color == 'black':
                    # For now, assume all black pieces are pawns (p)
                    board[rank][file] = 'p'
                else:
                    board[rank][file] = ''
        
        # Convert board array to FEN
        fen_parts = []
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
        
        # Join ranks with '/'
        fen = '/'.join(fen_parts)
        
        # Add other FEN components (assuming white to move, all castling available)
        fen += ' w KQkq - 0 1'
        
        return fen
    
    def analyze_screenshot(self, image_path: str) -> str:
        """
        Analyze a chess.com screenshot and return the FEN position.
        """
        try:
            # Detect and extract the board
            board_img = self.detect_board(image_path)
            
            # Convert to FEN
            fen = self.board_to_fen(board_img)
            
            return fen
            
        except Exception as e:
            raise ValueError(f"Error analyzing screenshot: {e}")

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