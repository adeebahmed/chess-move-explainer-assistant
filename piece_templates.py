#!/usr/bin/env python3
"""
Chess piece template definitions for template matching
"""

import cv2
import numpy as np

def create_piece_templates(size=32):
    """Create basic piece templates for matching."""
    templates = {}
    
    # King template (cross on top)
    king = np.zeros((size, size), dtype=np.uint8)
    cv2.rectangle(king, (size//4, size//4), (3*size//4, 7*size//8), 255, -1)
    cv2.rectangle(king, (3*size//8, size//8), (5*size//8, 3*size//8), 255, -1)
    cv2.line(king, (size//2, size//8), (size//2, 3*size//8), 255, 2)
    templates['king'] = king
    
    # Queen template (crown with points)
    queen = np.zeros((size, size), dtype=np.uint8)
    cv2.rectangle(queen, (size//4, size//4), (3*size//4, 7*size//8), 255, -1)
    points = np.array([
        [size//4, size//4],
        [3*size//8, size//8],
        [size//2, size//4],
        [5*size//8, size//8],
        [3*size//4, size//4]
    ], dtype=np.int32)
    cv2.fillPoly(queen, [points], 255)
    templates['queen'] = queen
    
    # Rook template (castle top)
    rook = np.zeros((size, size), dtype=np.uint8)
    cv2.rectangle(rook, (size//4, size//4), (3*size//4, 7*size//8), 255, -1)
    cv2.rectangle(rook, (size//4, size//8), (3*size//4, size//4), 255, -1)
    templates['rook'] = rook
    
    # Bishop template (diagonal cut)
    bishop = np.zeros((size, size), dtype=np.uint8)
    cv2.rectangle(bishop, (size//4, size//4), (3*size//4, 7*size//8), 255, -1)
    points = np.array([
        [size//4, size//4],
        [size//2, size//8],
        [3*size//4, size//4]
    ], dtype=np.int32)
    cv2.fillPoly(bishop, [points], 255)
    templates['bishop'] = bishop
    
    # Knight template (horse head)
    knight = np.zeros((size, size), dtype=np.uint8)
    cv2.rectangle(knight, (size//4, size//4), (3*size//4, 7*size//8), 255, -1)
    points = np.array([
        [size//4, size//4],
        [5*size//8, size//8],
        [3*size//4, size//4],
        [5*size//8, 3*size//8]
    ], dtype=np.int32)
    cv2.fillPoly(knight, [points], 255)
    templates['knight'] = knight
    
    # Pawn template (simple round top)
    pawn = np.zeros((size, size), dtype=np.uint8)
    cv2.rectangle(pawn, (3*size//8, size//3), (5*size//8, 7*size//8), 255, -1)
    cv2.circle(pawn, (size//2, size//3), size//8, 255, -1)
    templates['pawn'] = pawn
    
    return templates