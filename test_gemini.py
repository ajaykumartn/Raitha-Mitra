#!/usr/bin/env python3
"""
Test script to verify Gemini API functionality
"""

import os
import google.generativeai as genai
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def test_gemini_api():
    """Test Gemini API connection and response"""
    try:
        # Configure Gemini API
        api_key = os.getenv('GEMINI_API_KEY', 'AIzaSyDfvYhsvYOSCBE8r9GL72KXSJ6n9GMX8XA')
        
        if not api_key or api_key == "YOUR_GEMINI_API_KEY":
            print("❌ No valid Gemini API key found")
            return False
            
        print(f"🔑 Using API key: {api_key[:10]}...")
        
        genai.configure(api_key=api_key)
        
        # Create model
        model = genai.GenerativeModel('gemini-2.5-flash')
        print("✅ Gemini model created successfully")
        
        # Test simple prompt
        test_message = "Hello, can you help me with tomato farming?"
        print(f"📝 Testing with message: {test_message}")
        
        prompt = f"""You are an expert agricultural AI assistant for Indian farmers. You help with:
- Crop diseases and pest management
- Farming techniques and best practices
- Weather and seasonal advice
- Market information and crop planning
- Organic and sustainable farming methods
- Government schemes and subsidies
- Equipment and technology recommendations

Please provide helpful, practical advice in a friendly and conversational tone. Keep responses concise but informative.

User question: {test_message}

Please respond in a helpful and encouraging manner, focusing on practical solutions that Indian farmers can implement."""

        print("🤖 Calling Gemini API...")
        response = model.generate_content(prompt)
        
        if response and response.text:
            print("✅ Gemini API response received!")
            print(f"📄 Response: {response.text[:200]}...")
            return True
        else:
            print("❌ Empty response from Gemini API")
            return False
            
    except Exception as e:
        print(f"❌ Error testing Gemini API: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    print("🧪 Testing Gemini API...")
    success = test_gemini_api()
    
    if success:
        print("\n✅ Gemini API test passed! Chat should work properly.")
    else:
        print("\n❌ Gemini API test failed! Check your API key and internet connection.")