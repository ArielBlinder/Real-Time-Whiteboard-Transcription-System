import requests
import json
import os
from typing import List
from pathlib import Path

# --- Configuration ---
# Using NVIDIA API key from process_frames.py
API_KEY = "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"
API_URL = "https://integrate.api.nvidia.com/v1/chat/completions"

def process_frames_with_gemini(frame_texts: List[str]) -> str:
    """
    Process a list of OCR texts from video frames using NVIDIA's API with Gemini model.
    
    Args:
        frame_texts: List of OCR text results from individual frames
        
    Returns:
        str: Processed and cleaned transcription from NVIDIA API
    """
    if not API_KEY:
        raise ValueError("API_KEY is not set")
    
    if not frame_texts:
        return "No frame texts provided for processing"
    
    # Combine all frame texts with frame markers for context
    combined_text = ""
    for i, text in enumerate(frame_texts, 1):
        if text.strip():  # Only include non-empty texts
            combined_text += f"Frame {i}:\n{text}\n\n==================================================\n\n"
    
    if not combined_text.strip():
        return "No valid text content found in frames"
    
    # Define the AI prompt for processing the OCR results
    ai_prompt = (
        """**Role:** You are an expert AI assistant specializing in processing and refining OCR (Optical Character Recognition) output from whiteboard lectures. These lectures are captured frame by frame, and the content is mathematical, including formulas, definitions, and explanations.

**Context:** The provided input is a collation of OCR text from sequential frames of a whiteboard. This means:
* Content is generally added incrementally.
* Later frames often repeat content from earlier frames, along with new additions.
* Sometimes, a concept or formula might be written partially in one frame and completed or elaborated upon in a subsequent frame.
* The input text includes frame markers (e.g., `Frame Y:`) and separators (`==================================================`) which are part of the OCR capture process, not the lecture content itself.

**Primary Goal:** Your task is to meticulously transform this raw, sequential OCR data into a single, clean, logically ordered, and accurate transcription of the entire lecture, as if it were a well-edited set of lecture notes.

**Detailed Instructions:**

1.  **Analyze Full Context:** Process the entire provided OCR text, considering all frames and their sequence.
2.  **Identify and Eliminate Redundancy:**
    * Identify all instances of duplicated or overlapping content across the frames.
    * Your main goal is to ensure that each piece of information from the lecture appears only once in the final output.
3.  **Retain Completeness and Accuracy (Handling Evolving Text):**
    * For each unique segment of the lecture (e.g., a definition, a formula, an example), ensure you keep the most complete and correct version.
    * If a piece of information is introduced partially and then completed or refined in a later frame, the final transcript should reflect that completed/refined version.
    * Conversely, if a complete piece of information is already transcribed, do not replace it with a partial or summarized version from a later frame unless it's a clear correction.
4.  **Sequential Reconstruction:**
    * Reconstruct the lecture by arranging the unique, complete segments in their logical and chronological order of appearance.
5.  **Preserve Mathematical Notation:**
    * All mathematical notations must be accurately preserved.
    * Maintain LaTeX-style syntax if present in the input, ensuring consistency for mathematical expressions.
6.  **Structure and Formatting:**
    * Present the final transcription as a continuous text.
    * Use line breaks and paragraphing thoughtfully to enhance readability.
7.  **Output Constraints:**
    * The output must *only* be the final, cleaned transcription of the lecture content.
    * Do *not* include any frame markers, frame numbers, or separators from the input.
    * Provide no additional commentary, summaries, or explanations about your process.

**Input Text:**
""" + combined_text
    )

    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Accept": "application/json"
    }
        
    payload = {
        "model": "google/gemma-3-27b-it",
        "messages": [
            {
                "role": "user",
                "content": ai_prompt
            }
        ],
        "temperature": 0.2,
        "top_p": 0.7,
        "max_tokens": 1024,
        "stream": False
    }

    try:
        response = requests.post(
            url=API_URL,
            headers=headers,
            json=payload,
            timeout=180 
        )
        response.raise_for_status()

        response_data = response.json()
        
        if response_data.get("choices") and response_data["choices"][0].get("message"):
            return response_data["choices"][0]["message"].get("content", "No content found in response.")
        else:
            return "No valid response from NVIDIA API"
        
    except requests.exceptions.RequestException as e:
        return f"API request failed: {str(e)}"
    except json.JSONDecodeError as e:
        return f"Could not decode JSON response: {str(e)}"
    except Exception as e:
        return f"An unexpected error occurred: {str(e)}" 