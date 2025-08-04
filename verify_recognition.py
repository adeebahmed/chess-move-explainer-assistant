#!/usr/bin/env python3

import sys
import cv2
import numpy as np
from PyQt6.QtWidgets import (QApplication, QMainWindow, QWidget, QGridLayout, 
                           QComboBox, QPushButton, QLabel, QVBoxLayout, QHBoxLayout)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QImage, QPixmap
import chess
from board_recognition import ChessBoardRecognizer

class ChessVerifier(QMainWindow):
    def __init__(self, image_path):
        super().__init__()
        self.image_path = image_path
        self.pieces = {
            'empty': ' ',
            'white_pawn': 'P', 'white_knight': 'N', 'white_bishop': 'B',
            'white_rook': 'R', 'white_queen': 'Q', 'white_king': 'K',
            'black_pawn': 'p', 'black_knight': 'n', 'black_bishop': 'b',
            'black_rook': 'r', 'black_queen': 'q', 'black_king': 'k'
        }
        self.board_state = [[' ' for _ in range(8)] for _ in range(8)]
        self.setup_ui()
        self.process_image()
        
    def setup_ui(self):
        self.setWindowTitle('Chess Position Verifier')
        self.setGeometry(100, 100, 800, 600)
        
        # Main widget and layout
        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        layout = QHBoxLayout(main_widget)
        
        # Left side - Image display
        self.image_label = QLabel()
        layout.addWidget(self.image_label)
        
        # Right side - Board controls
        board_widget = QWidget()
        board_layout = QGridLayout(board_widget)
        layout.addWidget(board_widget)
        
        # Create the 8x8 grid of piece selectors
        self.selectors = []
        for row in range(8):
            row_selectors = []
            for col in range(8):
                combo = QComboBox()
                combo.addItems(['empty'] + list(self.pieces.keys()))
                combo.currentTextChanged.connect(self.update_fen)
                board_layout.addWidget(combo, row, col)
                row_selectors.append(combo)
            self.selectors.append(row_selectors)
        
        # Add FEN display and controls at the bottom
        bottom_widget = QWidget()
        bottom_layout = QVBoxLayout(bottom_widget)
        
        self.fen_label = QLabel('FEN: ')
        bottom_layout.addWidget(self.fen_label)
        
        button_layout = QHBoxLayout()
        save_button = QPushButton('Save FEN')
        save_button.clicked.connect(self.save_fen)
        button_layout.addWidget(save_button)
        
        bottom_layout.addLayout(button_layout)
        layout.addWidget(bottom_widget)

    def process_image(self):
        # Load and display the image
        img = cv2.imread(self.image_path)
        if img is None:
            print(f"Error: Could not load image {self.image_path}")
            return
        
        # Convert BGR to RGB
        img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        
        # Initialize board recognizer
        recognizer = ChessBoardRecognizer()
        try:
            # Get initial FEN from the recognizer
            initial_fen = recognizer.analyze_screenshot(self.image_path)
            # Parse the FEN and update the selectors
            self.set_board_from_fen(initial_fen)
            
            # Display the processed image
            height, width = img.shape[:2]
            scale = min(600/height, 600/width)
            new_width = int(width * scale)
            new_height = int(height * scale)
            img_resized = cv2.resize(img_rgb, (new_width, new_height))
            
            # Convert to QImage and display
            h, w, ch = img_resized.shape
            q_img = QImage(img_resized.data, w, h, ch * w, QImage.Format.Format_RGB888)
            self.image_label.setPixmap(QPixmap.fromImage(q_img))
            
        except Exception as e:
            print(f"Error in initial recognition: {e}")
            # Continue with empty board if recognition fails
            self.update_fen()

    def set_board_from_fen(self, fen: str):
        """Update the UI selectors based on a FEN string"""
        try:
            # Split FEN to get just the board position
            board_fen = fen.split()[0]
            ranks = board_fen.split('/')
            
            # Reverse ranks since FEN starts from rank 8
            ranks = list(reversed(ranks))
            
            for rank_idx, rank in enumerate(ranks):
                file_idx = 0
                for char in rank:
                    if char.isdigit():
                        file_idx += int(char)
                    else:
                        # Find the corresponding piece name
                        piece_name = None
                        for name, symbol in self.pieces.items():
                            if symbol == char:
                                piece_name = name
                                break
                        if piece_name and file_idx < 8:
                            self.selectors[rank_idx][file_idx].setCurrentText(piece_name)
                        file_idx += 1
            
            self.update_fen()
            
        except Exception as e:
            print(f"Error setting board from FEN: {e}")

    def update_fen(self):
        # Update board state from selectors
        for row in range(8):
            for col in range(8):
                piece = self.selectors[row][col].currentText()
                self.board_state[row][col] = self.pieces[piece]
        
        # Convert board state to FEN
        fen = self.board_to_fen()
        self.fen_label.setText(f'FEN: {fen}')

    def board_to_fen(self):
        fen_parts = []
        for row in self.board_state:
            empty_count = 0
            row_str = ''
            for piece in row:
                if piece == ' ':
                    empty_count += 1
                else:
                    if empty_count > 0:
                        row_str += str(empty_count)
                        empty_count = 0
                    row_str += piece
            if empty_count > 0:
                row_str += str(empty_count)
            fen_parts.append(row_str)
        return '/'.join(reversed(fen_parts))  # Reverse because FEN starts from rank 8

    def save_fen(self):
        fen = self.board_to_fen()
        print(f"FEN: {fen}")
        # You can add additional save functionality here
        with open('verified_fen.txt', 'w') as f:
            f.write(fen)
        print("FEN saved to verified_fen.txt")

def main():
    if len(sys.argv) != 2:
        print("Usage: python verify_recognition.py <image_path>")
        sys.exit(1)
        
    app = QApplication(sys.argv)
    window = ChessVerifier(sys.argv[1])
    window.show()
    sys.exit(app.exec())

if __name__ == '__main__':
    main()