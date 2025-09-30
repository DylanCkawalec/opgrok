#!/usr/bin/env python3
"""
Test script for xAI Grok API capabilities
Tests what xAI actually supports:
- Text chat
- File attachments (text)
- Image analysis (vision/multimodal)
- Web search augmentation
- Deep research mode
- Cost estimation
"""

import json
import sys

try:
    import httpx
except ImportError:
    print("❌ httpx not installed. Run: pip install httpx")
    sys.exit(1)

BASE_URL = "http://127.0.0.1:8000"


def test_basic_chat():
    """Test basic text chat."""
    print("\n🧪 Test 1: Basic Text Chat")
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
        print(f"Response: {data['assistant']}")
        print(f"Session ID: {data['session_id']}")
        print(f"Cost: ${data['estimate']['cost']['total_usd']}")
        return data['session_id']
    else:
        print(f"❌ Failed: {response.status_code}")
        print(response.text)
        return None


def test_chat_with_text_file(session_id):
    """Test chat with text file attachment."""
    print("\n🧪 Test 2: Chat with Text File")
    print("=" * 60)
    
    # Create a sample text file content
    file_content = """
# Sample Document
This is a test document about the number 42.
The number 42 is significant in many contexts, including:
- The Hitchhiker's Guide to the Galaxy (the answer to life, the universe, and everything)
- Mathematics and computer science
"""
    
    payload = {
        "session_id": session_id,
        "message": "What number is mentioned in the attached file? What is it known for?",
        "model": "grok-4-0709",
        "max_tokens": 200,
        "expected_output_tokens": 100,
        "files": [
            {"name": "test.txt", "content": file_content}
        ]
    }
    
    response = httpx.post(f"{BASE_URL}/api/chat", json=payload, timeout=60)
    
    if response.status_code == 200:
        data = response.json()
        print(f"✅ Success!")
        print(f"Response: {data['assistant']}")
        print(f"Cost: ${data['estimate']['cost']['total_usd']}")
    else:
        print(f"❌ Failed: {response.status_code}")
        print(response.text)


def test_vision_with_image():
    """Test vision/multimodal - analyzing an image."""
    print("\n🧪 Test 3: Vision - Image Analysis (Multimodal)")
    print("=" * 60)
    
    # Create a tiny 1x1 red PNG image (base64)
    # This is a valid minimal PNG file
    tiny_red_png_b64 = "iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mP8/5+hHgAHggJ/PchI7wAAAABJRU5ErkJggg=="
    image_data_url = f"data:image/png;base64,{tiny_red_png_b64}"
    
    payload = {
        "message": "What color is this image? Describe what you see.",
        "model": "grok-4-0709",
        "max_tokens": 200,
        "expected_output_tokens": 100,
        "files": [
            {"name": "test_image.png", "content": image_data_url}
        ]
    }
    
    response = httpx.post(f"{BASE_URL}/api/chat", json=payload, timeout=60)
    
    if response.status_code == 200:
        data = response.json()
        print(f"✅ Success!")
        print(f"Response: {data['assistant']}")
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
        print(f"Response: {data['assistant']}")
        print(f"Cost: ${data['estimate']['cost']['total_usd']}")
    else:
        print(f"❌ Failed: {response.status_code}")
        print(response.text)


def test_deep_research():
    """Test deep research mode."""
    print("\n🧪 Test 5: Deep Research Mode")
    print("=" * 60)
    
    payload = {
        "message": "Explain quantum entanglement in simple terms.",
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
        print(f"Response: {data['assistant'][:300]}...")
        print(f"Mode: {data['mode']}")
        print(f"Cost: ${data['estimate']['cost']['total_usd']}")
    else:
        print(f"❌ Failed: {response.status_code}")
        print(response.text)


def test_cost_estimate():
    """Test cost estimation endpoint (no actual inference)."""
    print("\n🧪 Test 6: Cost Estimation (No Inference)")
    print("=" * 60)
    
    payload = {
        "message": "This is a test message for cost estimation only. It should not be sent to the API.",
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


def test_list_models():
    """Test models listing endpoint."""
    print("\n🧪 Test 7: List Available Models")
    print("=" * 60)
    
    response = httpx.get(f"{BASE_URL}/api/models", timeout=10)
    
    if response.status_code == 200:
        data = response.json()
        print(f"✅ Success!")
        print(f"Available models: {data['count']}")
        for model in data['models']:
            print(f"  • {model['name']}")
            print(f"    Input: ${model['pricing']['input']}/MTok | Output: ${model['pricing']['output']}/MTok")
    else:
        print(f"❌ Failed: {response.status_code}")
        print(response.text)


def test_multimodal_combined():
    """Test combining text file + image + web search."""
    print("\n🧪 Test 8: Combined Features (Text + Image + Web Search)")
    print("=" * 60)
    
    # Text file
    text_content = "The sky is typically blue during the day."
    
    # Tiny blue PNG (1x1 pixel)
    tiny_blue_png_b64 = "iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mNkYPhfDwAChwGA60e6kgAAAABJRU5ErkJggg=="
    image_data_url = f"data:image/png;base64,{tiny_blue_png_b64}"
    
    payload = {
        "message": "Based on the text file and image, what color is the sky?",
        "model": "grok-4-0709",
        "max_tokens": 200,
        "expected_output_tokens": 100,
        "web_search": True,
        "files": [
            {"name": "sky_info.txt", "content": text_content},
            {"name": "sky_color.png", "content": image_data_url}
        ]
    }
    
    response = httpx.post(f"{BASE_URL}/api/chat", json=payload, timeout=60)
    
    if response.status_code == 200:
        data = response.json()
        print(f"✅ Success!")
        print(f"Response: {data['assistant']}")
        print(f"Cost: ${data['estimate']['cost']['total_usd']}")
    else:
        print(f"❌ Failed: {response.status_code}")
        print(response.text)


def main():
    """Run all tests."""
    print("🚀 xAI Grok API Test Suite")
    print("=" * 60)
    print("Testing actual xAI capabilities:")
    print("  ✓ Chat completions")
    print("  ✓ Vision (image analysis)")
    print("  ✓ File attachments")
    print("  ✓ Web search")
    print("  ✓ Deep research mode")
    print("  ✗ Image generation (NOT supported by xAI)")
    
    try:
        # Test basic functionality
        session_id = test_basic_chat()
        
        if session_id:
            test_chat_with_text_file(session_id)
        
        # Test advanced features
        test_vision_with_image()
        test_web_search()
        test_deep_research()
        test_cost_estimate()
        test_list_models()
        test_multimodal_combined()
        
        print("\n" + "=" * 60)
        print("✅ All tests completed!")
        print("=" * 60)
        print("\n💡 The web UI is running at: http://127.0.0.1:8000")
        print("   Try uploading an image and asking Grok to describe it!")
        
    except Exception as e:
        print(f"\n❌ Test suite failed with error: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
