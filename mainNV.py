from PIL import Image
import requests, base64
import tkinter as tk
from tkinter import filedialog
import io
import json

# Function to open a file dialog and let the user select a single image file
def select_single_image():
    root = tk.Tk()
    root.withdraw()  # Hide the main Tkinter window
    # test

    filetypes = [
        ("Image files", "*.png *.jpg *.jpeg *.bmp *.gif"),
        ("All files", "*.*")
    ]

    # Prompt the user to select an image file
    file_path = filedialog.askopenfilename(
        title="Select an Image",
        filetypes=filetypes
    )

    return file_path

img_path = select_single_image()

with Image.open(img_path) as img:
    # Resize the image to fit within 800x800 pixels, preserving aspect ratio
    max_size = (800, 800)
    img.thumbnail(max_size, Image.LANCZOS)

    # Ensure the image is in RGB mode for JPEG compatibility
    if img.mode != 'RGB':
        img = img.convert('RGB')

    # Save the resized image to an in-memory buffer as JPEG with reduced quality
    buffer = io.BytesIO()
    img.save(buffer, format='JPEG', quality=70)
    buffer.seek(0)

    # Encode the image buffer to a base64 string
    image_b64 = base64.b64encode(buffer.read()).decode()

# Ensure the base64-encoded image is below the API size limit
print(f"Base64 length: {len(image_b64)}")
assert len(image_b64) < 180_000, "Image is still too large. Try a smaller resize dimension."

# Set up the API endpoint and streaming option
invoke_url = "https://integrate.api.nvidia.com/v1/chat/completions"
stream = True

headers = {
    # Insert your API key here or use an environment variable
    # "Authorization
    "Authorization": "Bearer nvapi-----------------",
    "Accept": "text/event-stream" if stream else "application/json"
}

# Prepare the request payload with the image and transcription prompt
payload = {
    "model": 'meta/llama-4-scout-17b-16e-instruct',
    "messages": [
        {
            "role": "user",
            # Prompt: instructs the model to transcribe the handwritten text in the image
            "content": f'Transcribe the handwritten text in this image exactly as written. Only output the text content and nothing else. <img src="data:image/jpeg;base64,{image_b64}" />'
        }
    ],
    "max_tokens": 512,
    "temperature": 0.2,  # Lower temperature for more deterministic output
    "top_p": 1.00,
    "stream": stream
}

# Send the POST request to the API
response = requests.post(invoke_url, headers=headers, json=payload)

# Handle the streaming response from the API
if stream:
    full_text = ""
    print("Transcribed text:")
    print("-----------------")

    for line in response.iter_lines():
        if line:
            line_text = line.decode("utf-8")
            # Skip lines that are empty or indicate the end of the stream
            if line_text == "data: [DONE]" or not line_text.startswith("data: "):
                continue

            # Parse the JSON content from the stream
            try:
                json_str = line_text[6:]  # Remove "data: " prefix
                json_obj = json.loads(json_str)

                # Extract and print the transcribed content if available
                if "choices" in json_obj and len(json_obj["choices"]) > 0:
                    delta = json_obj["choices"][0].get("delta", {})
                    if "content" in delta and delta["content"]:
                        content = delta["content"]
                        full_text += content
                        print(content, end="")  # Print content without a newline
            except json.JSONDecodeError:
                continue

    print("\n-----------------")
    print("Complete transcription:", full_text)
else:
    # Handle non-streaming (standard) API responses
    result = response.json()
    if "choices" in result and len(result["choices"]) > 0:
        text = result["choices"][0]["message"]["content"]
        print("Transcribed text:")
        print("-----------------")
        print(text)
        print("-----------------")
