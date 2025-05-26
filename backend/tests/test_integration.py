#!/usr/bin/env python3
"""
Test script to verify the integration between NVIDIA OCR and Gemini processing.
"""

import os
from process_video_text import process_frames_with_gemini, OPENROUTER_API_KEY

def test_gemini_integration():
    """Test the Gemini integration with sample OCR data"""
    
    # Check if API key is available (either hardcoded or from environment)
    if not OPENROUTER_API_KEY:
        print("❌ OPENROUTER_API_KEY is not set!")
        print("Please check your API key in process_video_text.py")
        return False
    
    # Sample OCR texts from multiple frames (simulating video transcription)
    sample_frame_texts = [
        "Mathematical Analysis\nChapter 3: Derivatives",
        "Mathematical Analysis\nChapter 3: Derivatives\n\nDefinition: The derivative of f(x) at point a",
        "Mathematical Analysis\nChapter 3: Derivatives\n\nDefinition: The derivative of f(x) at point a\nf'(a) = lim(h→0) [f(a+h) - f(a)]/h",
        "Mathematical Analysis\nChapter 3: Derivatives\n\nDefinition: The derivative of f(x) at point a\nf'(a) = lim(h→0) [f(a+h) - f(a)]/h\n\nExample: f(x) = x²\nf'(x) = 2x"
    ]
    
    print("🧪 Testing Gemini integration with sample OCR data...")
    print(f"📊 Processing {len(sample_frame_texts)} sample frames...")
    print(f"🔑 Using API key: {OPENROUTER_API_KEY[:20]}..." if OPENROUTER_API_KEY else "🔑 No API key found")
    
    try:
        result = process_frames_with_gemini(sample_frame_texts)
        
        print("✅ Integration test successful!")
        print("📄 Processed result:")
        print("-" * 50)
        print(result)
        print("-" * 50)
        
        return True
        
    except Exception as e:
        print(f"❌ Integration test failed: {str(e)}")
        return False

def test_empty_input():
    """Test handling of empty input"""
    print("\n🧪 Testing empty input handling...")
    
    try:
        result = process_frames_with_gemini([])
        print(f"✅ Empty input handled correctly: {result}")
        return True
    except Exception as e:
        print(f"❌ Empty input test failed: {str(e)}")
        return False

def test_invalid_input():
    """Test handling of invalid input"""
    print("\n🧪 Testing invalid input handling...")
    
    try:
        result = process_frames_with_gemini(["", "   ", "\n\n"])
        print(f"✅ Invalid input handled correctly: {result}")
        return True
    except Exception as e:
        print(f"❌ Invalid input test failed: {str(e)}")
        return False

if __name__ == "__main__":
    print("🚀 Starting integration tests for Video Transcription System")
    print("=" * 60)
    
    tests_passed = 0
    total_tests = 3
    
    if test_gemini_integration():
        tests_passed += 1
    
    if test_empty_input():
        tests_passed += 1
    
    if test_invalid_input():
        tests_passed += 1
    
    print("\n" + "=" * 60)
    print(f"📊 Test Results: {tests_passed}/{total_tests} tests passed")
    
    if tests_passed == total_tests:
        print("🎉 All tests passed! The integration is working correctly.")
    else:
        print("⚠️  Some tests failed. Please check the configuration.")
    
    print("\n💡 Tips:")
    print("   - API key is configured in process_video_text.py")
    print("   - Test with a real video file using the Flask app")
    print("   - Check that all dependencies are installed") 