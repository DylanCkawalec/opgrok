#!/usr/bin/env python3
"""
Test script for Grok Chat API
Tests all major capabilities:
- Text chat
- File attachments (text)
- Image attachments (multimodal)
- Web search
- Deep research mode
- Cost estimation
- Image generation
"""

import json
import base64
import sys

try:
    import httpx
except ImportError:
    print("❌ httpx not installed. Run: pip install httpx")
    sys.exit(1)

BASE_URL = "http://127.0.0.1:8000"


def test_basic_chat():
    """Test basic text chat."""
    print("\n🧪 Test 1: Basic Chat")
    print("=" * 60)
    
    payload = {
        "message": "What is 2+2? Answer in one sentence.",
        "model": "grok-4-0709",
        "max_tokens": 100,
        "temperature": 0.7,
        "expected_output_tokens": 50,
    }
    
    response = httpx.post(f"{BASE_URL}/api/chat", json=payload, timeout=60)
    
    if response.status_code == 200:
        data = response.json()
        print(f"✅ Success!")
        print(f"Response: {data['assistant'][:200]}")
        print(f"Session ID: {data['session_id']}")
        print(f"Cost: ${data['estimate']['cost']['total_usd']}")
        return data['session_id']
    else:
        print(f"❌ Failed: {response.status_code}")
        print(response.text)
        return None


def test_chat_with_file(session_id):
    """Test chat with text file attachment."""
    print("\n🧪 Test 2: Chat with Text File")
    print("=" * 60)
    
    # Create a sample text file content
    file_content = """
# Sample Document
This is a test document about the number 42.
The number 42 is significant in many contexts.
"""
    
    payload = {
        "session_id": session_id,
        "message": "What number is mentioned in the attached file?",
        "model": "grok-4-0709",
        "max_tokens": 100,
        "expected_output_tokens": 50,
        "files": [
            {"name": "test.txt", "content": file_content}
        ]
    }
    
    response = httpx.post(f"{BASE_URL}/api/chat", json=payload, timeout=60)
    
    if response.status_code == 200:
        data = response.json()
        print(f"✅ Success!")
        print(f"Response: {data['assistant'][:200]}")
        print(f"Cost: ${data['estimate']['cost']['total_usd']}")
    else:
        print(f"❌ Failed: {response.status_code}")
        print(response.text)


def test_chat_with_image():
    """Test chat with image (multimodal)."""
    print("\n🧪 Test 3: Chat with Image (Multimodal)")
    print("=" * 60)
    
    # Create a tiny 1x1 red PNG image (base64)
    # This is a valid PNG file header + IHDR + IDAT + IEND
    tiny_png_b64 = "iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mP8z8DwHwAFBQIAX8jx0gAAAABJRU5ErkJggg=="
    image_data_url = f"data:image/png;base64,{tiny_png_b64}"
    
    payload = {
        "message": "Describe this image.",
        "model": "grok-4-0709",
        "max_tokens": 200,
        "expected_output_tokens": 100,
        "files": [
            {"name": "test.png", "content": image_data_url}
        ]
    }
    
    response = httpx.post(f"{BASE_URL}/api/chat", json=payload, timeout=60)
    
    if response.status_code == 200:
        data = response.json()
        print(f"✅ Success!")
        print(f"Response: {data['assistant'][:200]}")
        print(f"Cost: ${data['estimate']['cost']['total_usd']}")
    else:
        print(f"❌ Failed: {response.status_code}")
        print(response.text)


def test_web_search():
    """Test web search augmentation."""
    print("\n🧪 Test 4: Web Search Augmentation")
    print("=" * 60)
    
    payload = {
        "message": "What is the capital of France?",
        "model": "grok-4-0709",
        "max_tokens": 100,
        "expected_output_tokens": 50,
        "web_search": True,
    }
    
    response = httpx.post(f"{BASE_URL}/api/chat", json=payload, timeout=60)
    
    if response.status_code == 200:
        data = response.json()
        print(f"✅ Success!")
        print(f"Response: {data['assistant'][:200]}")
        print(f"Cost: ${data['estimate']['cost']['total_usd']}")
    else:
        print(f"❌ Failed: {response.status_code}")
        print(response.text)


def test_deep_research():
    """Test deep research mode."""
    print("\n🧪 Test 5: Deep Research Mode")
    print("=" * 60)
    
    payload = {
        "message": "Explain quantum entanglement.",
        "model": "grok-4-0709",
        "max_tokens": 500,
        "expected_output_tokens": 400,
        "mode": "deep_research",
        "context_window": 10,
    }
    
    response = httpx.post(f"{BASE_URL}/api/chat", json=payload, timeout=60)
    
    if response.status_code == 200:
        data = response.json()
        print(f"✅ Success!")
        print(f"Response: {data['assistant'][:200]}...")
        print(f"Mode: {data['mode']}")
        print(f"Cost: ${data['estimate']['cost']['total_usd']}")
    else:
        print(f"❌ Failed: {response.status_code}")
        print(response.text)


def test_cost_estimate():
    """Test cost estimation endpoint."""
    print("\n🧪 Test 6: Cost Estimation (No Inference)")
    print("=" * 60)
    
    payload = {
        "message": "This is a test message for cost estimation only.",
        "model": "grok-4-0709",
        "max_tokens": 2048,
        "expected_output_tokens": 512,
    }
    
    response = httpx.post(f"{BASE_URL}/api/estimate", json=payload, timeout=10)
    
    if response.status_code == 200:
        data = response.json()
        print(f"✅ Success!")
        print(f"Prompt tokens: {data['prompt_tokens']}")
        print(f"Completion tokens: {data['completion_tokens']}")
        print(f"Total tokens: {data['total_tokens']}")
        print(f"Estimated cost: ${data['cost']['total_usd']}")
    else:
        print(f"❌ Failed: {response.status_code}")
        print(response.text)


def test_image_generation():
    """Test image generation."""
    print("\n🧪 Test 7: Image Generation")
    print("=" * 60)
    
    payload = {
        "prompt": "A red circle on white background",
        "size": "256x256",
        "n": 1,
    }
    
    response = httpx.post(f"{BASE_URL}/api/image", json=payload, timeout=60)
    
    if response.status_code == 200:
        data = response.json()
        print(f"✅ Success!")
        print(f"Generated {data['count']} image(s)")
        print(f"Size: {data['size']}")
        print(f"Prompt: {data['prompt']}")
        if data['images']:
            img_preview = data['images'][0][:100]
            print(f"Image data: {img_preview}...")
    else:
        print(f"❌ Failed: {response.status_code}")
        print(response.text)


def test_list_models():
    """Test models listing endpoint."""
    print("\n🧪 Test 8: List Models")
    print("=" * 60)
    
    response = httpx.get(f"{BASE_URL}/api/models", timeout=10)
    
    if response.status_code == 200:
        data = response.json()
        print(f"✅ Success!")
        print(f"Available models: {data['count']}")
        for model in data['models']:
            print(f"  - {model['name']}: ${model['pricing']['input']}/MTok in, ${model['pricing']['output']}/MTok out")
    else:
        print(f"❌ Failed: {response.status_code}")
        print(response.text)


def main():
    """Run all tests."""
    print("🚀 Grok Chat API Test Suite")
    print("=" * 60)
    
    try:
        # Test basic functionality
        session_id = test_basic_chat()
        
        if session_id:
            test_chat_with_file(session_id)
        
        # Test advanced features
        test_chat_with_image()
        test_web_search()
        test_deep_research()
        test_cost_estimate()
        test_image_generation()
        test_list_models()
        
        print("\n" + "=" * 60)
        print("✅ All tests completed!")
        print("=" * 60)
        
    except Exception as e:
        print(f"\n❌ Test suite failed with error: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
