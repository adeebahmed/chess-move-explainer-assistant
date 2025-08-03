#!/usr/bin/env python3
"""
Test script to verify the chess move explainer setup
Run this before using the main application to check if everything is configured correctly.
"""

import sys
import os
from dotenv import load_dotenv

def test_imports():
    """Test if all required packages can be imported."""
    print("🔍 Testing imports...")
    
    try:
        import chess
        print("✅ python-chess imported successfully")
    except ImportError:
        print("❌ python-chess not found. Run: pip install python-chess")
        return False
    
    try:
        import openai
        print("✅ openai imported successfully")
    except ImportError:
        print("❌ openai not found. Run: pip install openai")
        return False
    
    try:
        from dotenv import load_dotenv
        print("✅ python-dotenv imported successfully")
    except ImportError:
        print("❌ python-dotenv not found. Run: pip install python-dotenv")
        return False
    
    return True

def test_environment():
    """Test environment variables."""
    print("\n🔍 Testing environment variables...")
    
    load_dotenv()
    
    # Test Stockfish path
    stockfish_path = os.getenv('STOCKFISH_PATH', '/usr/local/bin/stockfish')
    if os.path.exists(stockfish_path):
        print(f"✅ Stockfish found at: {stockfish_path}")
    else:
        print(f"❌ Stockfish not found at: {stockfish_path}")
        print("   Please install Stockfish and update STOCKFISH_PATH in .env")
        return False
    
    # Test OpenAI API key
    api_key = os.getenv('OPENAI_API_KEY')
    if api_key and api_key != 'your_openai_api_key_here':
        print("✅ OpenAI API key is set")
    else:
        print("❌ OpenAI API key not set or invalid")
        print("   Please set your OpenAI API key in the .env file")
        return False
    
    return True

def test_stockfish():
    """Test Stockfish engine."""
    print("\n🔍 Testing Stockfish engine...")
    
    try:
        import chess.engine
        stockfish_path = os.getenv('STOCKFISH_PATH', '/usr/local/bin/stockfish')
        
        with chess.engine.SimpleEngine.popen_uci(stockfish_path) as engine:
            # Test with starting position
            board = chess.Board()
            result = engine.analyse(board, chess.engine.Limit(time=1.0))
            print("✅ Stockfish engine working correctly")
            return True
            
    except Exception as e:
        print(f"❌ Stockfish test failed: {e}")
        return False

def test_openai():
    """Test OpenAI API connection."""
    print("\n🔍 Testing OpenAI API...")
    
    try:
        import openai
        from dotenv import load_dotenv
        
        load_dotenv()
        openai.api_key = os.getenv('OPENAI_API_KEY')
        
        # Simple test call
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": "Say 'Hello' if you can read this."}],
            max_tokens=10
        )
        
        if response.choices[0].message.content:
            print("✅ OpenAI API working correctly")
            return True
        else:
            print("❌ OpenAI API returned empty response")
            return False
            
    except Exception as e:
        print(f"❌ OpenAI API test failed: {e}")
        return False

def main():
    """Run all tests."""
    print("🧪 Chess Move Explainer - Setup Test")
    print("=" * 40)
    
    tests = [
        test_imports,
        test_environment,
        test_stockfish,
        test_openai
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        if test():
            passed += 1
        print()
    
    print("=" * 40)
    print(f"📊 Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! Your setup is ready to use.")
        print("   Run: python main.py")
    else:
        print("⚠️  Some tests failed. Please fix the issues above before using the application.")
        sys.exit(1)

if __name__ == "__main__":
    main() 