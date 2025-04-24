import base64
import io
import json
import requests
from PIL import Image

def transcribe_image(file):
    try:
        with Image.open(file) as img:
            # Resize image
            max_size = (800, 800)
            img.thumbnail(max_size, Image.LANCZOS)

            if img.mode != 'RGB':
                img = img.convert('RGB')

            buffer = io.BytesIO()
            img.save(buffer, format='JPEG', quality=70)
            buffer.seek(0)

            image_b64 = base64.b64encode(buffer.read()).decode()
    except Exception as e:
        return f"Failed to process image: {e}"

    assert len(image_b64) < 180_000, "Image too large after resize."

    invoke_url = "https://integrate.api.nvidia.com/v1/chat/completions"
    headers = {
        "Authorization": "Bearer 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",
        "Accept": "application/json"
    }

    payload = {
        "model": 'meta/llama-4-scout-17b-16e-instruct',
        "messages": [
            {
                "role": "user",
                "content": f'Transcribe the handwritten text in this image exactly as written. Only output the text content and nothing else. <img src="data:image/jpeg;base64,{image_b64}" />'
            }
        ],
        "max_tokens": 512,
        "temperature": 0.2,
        "top_p": 1.00,
        "stream": False
    }

    response = requests.post(invoke_url, headers=headers, json=payload)

    result = response.json()
    if "choices" in result and len(result["choices"]) > 0:
        return result["choices"][0]["message"]["content"]
    else:
        return "No transcription result."  