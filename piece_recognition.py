#!/usr/bin/env python3
"""
Chess Piece Recognition Module
Identifies chess pieces using advanced computer vision techniques
"""

import cv2
import numpy as np
from enum import Enum
from typing import Tuple, Optional
import math

class PieceType(Enum):
    KING = 'k'
    QUEEN = 'q'
    ROOK = 'r'
    BISHOP = 'b'
    KNIGHT = 'n'
    PAWN = 'p'

class PieceRecognizer:
    def __init__(self):
        # Debug mode
        self.debug = True
        
        # Feature thresholds
        self.thresholds = {
            'min_area': 25,  # Minimum contour area
            'tall_ratio': 1.6,  # Aspect ratio for tall pieces (King, Queen, Bishop)
            'medium_ratio': 1.2,  # Aspect ratio for medium height pieces (Rook, Knight)
            'high_convexity': 0.8,  # Threshold for very convex pieces (King, Queen)
            'high_symmetry': 0.7,  # Threshold for highly symmetric pieces (King, Rook)
            'low_symmetry': 0.5,  # Threshold for asymmetric pieces (Knight)
        }
        
        # Additional debug info
        self.debug_info = {}

    def identify_piece(self, piece_img: np.ndarray) -> Tuple[Optional[PieceType], Optional[bool]]:
        """
        Identify piece type and color from image.
        Returns (piece_type, is_white)
        """
        # Convert to HSV
        hsv = cv2.cvtColor(piece_img, cv2.COLOR_RGB2HSV)
        
        # Split channels
        h, s, v = cv2.split(hsv)
        
        # Use value channel for piece detection with more aggressive thresholding
        _, binary = cv2.threshold(v, 100, 255, cv2.THRESH_BINARY)
        
        # Find contours in binary image
        contours, _ = cv2.findContours(binary, cv2.RETR_EXTERNAL, 
                                     cv2.CHAIN_APPROX_SIMPLE)
        
        if not contours:
            return None, None
            
        # Get largest contour
        piece_contour = max(contours, key=cv2.contourArea)
        
        # Get contour area and bounding box
        area = cv2.contourArea(piece_contour)
        x, y, w, h = cv2.boundingRect(piece_contour)
        
        # If contour is too small, no piece
        if area < self.thresholds['min_area']:
            return None, None
            
        # Get color using average value in contour region
        mask = np.zeros_like(v)
        cv2.drawContours(mask, [piece_contour], -1, 255, -1)
        mean_v = cv2.mean(v, mask=mask)[0]
        is_white = mean_v > 128
        
        if self.debug:
            # Save debug images with unique names
            piece_id = len(self.debug_info) + 1
            cv2.imwrite(f'debug_piece_{piece_id}_binary.png', binary)
            cv2.imwrite(f'debug_piece_{piece_id}_mask.png', mask)
            cv2.imwrite(f'debug_piece_{piece_id}_original.png', 
                       cv2.cvtColor(piece_img, cv2.COLOR_RGB2BGR))
            
            # Draw contour on original image
            debug_img = cv2.cvtColor(piece_img.copy(), cv2.COLOR_RGB2BGR)
            cv2.drawContours(debug_img, [piece_contour], -1, (0,255,0), 2)
            cv2.imwrite(f'debug_piece_{piece_id}_contour.png', debug_img)
            
            # Store debug info
            self.debug_info[piece_id] = {
                'area': area,
                'dimensions': (w, h),
                'aspect_ratio': float(h) / w if w > 0 else 0,
                'mean_value': mean_v
            }
        
        # Extract features
        features = self.extract_features(piece_contour, mask, w, h)
        
        # Determine piece type based on features
        piece_type = self.classify_piece(features)
        
        if self.debug:
            # Add classification results to debug info
            self.debug_info[piece_id].update({
                'features': features,
                'piece_type': piece_type.value if piece_type else None,
                'is_white': is_white
            })
            
        return piece_type, is_white

    def extract_features(self, contour: np.ndarray, mask: np.ndarray, 
                        width: int, height: int) -> dict:
        """Extract features from piece contour and mask."""
        features = {}
        
        # Height/width ratio
        features['aspect_ratio'] = float(height) / width if width > 0 else 0
        
        # Convex hull features
        hull = cv2.convexHull(contour)
        hull_area = cv2.contourArea(hull)
        area = cv2.contourArea(contour)
        features['convexity'] = area / hull_area if hull_area > 0 else 0
        
        # Symmetry measure
        left_mask = mask[:, :width//2]
        right_mask = mask[:, width//2:]
        right_mask_flipped = cv2.flip(right_mask, 1)
        if left_mask.shape == right_mask_flipped.shape and left_mask.size > 0:
            features['symmetry'] = np.sum(left_mask == right_mask_flipped) / left_mask.size
        else:
            features['symmetry'] = 0
            
        return features

    def classify_piece(self, features: dict) -> Optional[PieceType]:
        """Classify piece type based on extracted features."""
        aspect_ratio = features['aspect_ratio']
        convexity = features['convexity']
        symmetry = features['symmetry']
        
        if aspect_ratio > self.thresholds['tall_ratio']:  # Tall pieces
            if convexity > self.thresholds['high_convexity']:
                # King and Queen are both tall and convex
                return (PieceType.KING if symmetry > self.thresholds['high_symmetry'] 
                       else PieceType.QUEEN)
            else:
                # Bishop is tall but less convex
                return PieceType.BISHOP
                
        elif aspect_ratio > self.thresholds['medium_ratio']:  # Medium height
            if symmetry < self.thresholds['low_symmetry']:
                # Knight is the least symmetric
                return PieceType.KNIGHT
            else:
                # Rook is more symmetric
                return PieceType.ROOK
                
        else:  # Short pieces
            return PieceType.PAWN

    def get_fen_symbol(self, piece_type: PieceType, is_white: bool) -> str:
        """Convert piece type and color to FEN symbol."""
        if piece_type is None:
            return ''
        symbol = piece_type.value
        return symbol.upper() if is_white else symbol.lower()

if __name__ == "__main__":
    # Test code
    import sys
    if len(sys.argv) > 1:
        img_path = sys.argv[1]
        img = cv2.imread(img_path)
        if img is not None:
            recognizer = PieceRecognizer()
            piece_type, is_white = recognizer.identify_piece(img)
            print(f"Piece: {piece_type}, {'White' if is_white else 'Black'}")
            print(f"FEN symbol: {recognizer.get_fen_symbol(piece_type, is_white)}")
        else:
            print(f"Could not read image: {img_path}")