import base64
import io
import json
import requests
from PIL import Image
from typing import Union
from pathlib import Path

# Constants
MAX_IMAGE_SIZE = (800, 800)
MAX_BASE64_SIZE = 180_000
API_URL = "https://integrate.api.nvidia.com/v1/chat/completions"
# IMPORTANT: Replace with your API key, Get it from https://build.nvidia.com/settings/api-keys
API_KEY = "ADD_KEY_HERE"
MODEL_NAME = 'meta/llama-4-scout-17b-16e-instruct'

def prepare_image(image_input) -> tuple[bool, Union[str, bytes]]:
    """
    Prepare and optimize the image for API transmission.
    
    Args:
        image_input: Either a PIL Image object, file object, or a path to the image file
        
    Returns:
        tuple: (success, result) where result is either error message or base64 encoded image
    """
    try:
        # Handle PIL Image objects directly
        if isinstance(image_input, Image.Image):
            img = image_input.copy()
        # Handle file paths
        elif isinstance(image_input, (str, Path)):
            img = Image.open(image_input)
        # Handle file objects
        else:
            img = Image.open(image_input)
            
        # Resize image while maintaining aspect ratio
        img.thumbnail(MAX_IMAGE_SIZE, Image.LANCZOS)
        
        # Convert to RGB if needed
        if img.mode != 'RGB':
            img = img.convert('RGB')
        
        # Optimize and encode
        buffer = io.BytesIO()
        img.save(buffer, format='JPEG', quality=70)
        buffer.seek(0)
        
        image_b64 = base64.b64encode(buffer.read()).decode()
        
        if len(image_b64) >= MAX_BASE64_SIZE:
            return False, "Image too large after processing"
            
        return True, image_b64
        
    except Exception as e:
        return False, f"Failed to process image: {str(e)}"

def transcribe_image(image_input) -> str:
    """
    Transcribe handwritten text from an image using NVIDIA's API.
    
    Args:
        image_input: PIL Image object, file object, or path to the image file
        
    Returns:
        str: Transcribed text or error message
    """
    # Prepare image
    success, result = prepare_image(image_input)
    if not success:
        return result
    
    # Prepare API request
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Accept": "application/json"
    }
    
    payload = {
        "model": MODEL_NAME,
        "messages": [
            {
                "role": "user",
                # This is the prompt for the API model
                "content": f'Transcribe the handwritten text in this image exactly as written. Only output the text content and nothing else. <img src="data:image/jpeg;base64,{result}" />'
            }
        ],
        "max_tokens": 512, # Adjust this value as needed for the model
        "temperature": 0.2, 
        "top_p": 1.00,
        "stream": False
    }
    
    try:
        response = requests.post(API_URL, headers=headers, json=payload)
        response.raise_for_status()
        
        result = response.json()
        if "choices" in result and len(result["choices"]) > 0:
            return result["choices"][0]["message"]["content"]
        return "No transcription result."
        
    except requests.exceptions.RequestException as e:
        return f"API request failed: {str(e)}"
    except json.JSONDecodeError:
        return "Invalid response from API"
    except Exception as e:
        return f"Unexpected error: {str(e)}"
