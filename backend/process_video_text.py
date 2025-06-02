import requests
import json
import os
import time
from typing import List

# IMPORTANT: Replace with your API key, Get it from https://openrouter.ai/settings/keys
OPENROUTER_API_KEY = "ADD_KEY_HERE" 

def process_frames_with_gemini(frame_texts: List[str]) -> str:
    # Process a list of OCR texts from video frames using Gemini API
    
    # Args: "frame_texts": List of OCR text results from individual frames that are ordered chronologically
        
    # Returns: Processed and cleaned transcription from Gemini giving the final result
    
    if not OPENROUTER_API_KEY:
        raise ValueError("OPENROUTER_API_KEY environment variable is not set")
    
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
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type": "application/json",
    }
        
    data = {
        "model": "google/gemini-2.0-flash-exp:free", 
        "messages": [
            {
                "role": "user",
                "content": [{"type": "text", "text": ai_prompt}] 
            }
        ]
    }

    try:

        # Make the API request with exponential backoff retry logic
        # OpenRouter API endpoint is unstable sometimes so we need to retry
        response = make_api_request_with_retry(
            url="https://openrouter.ai/api/v1/chat/completions",
            headers=headers,
            data=data
        )

        # Get the response data
        response_data = response.json()
        
        # Check if the response contains a valid message
        if response_data.get("choices") and response_data["choices"][0].get("message"):
            result = response_data["choices"][0]["message"].get("content", "No content found in response.")
            return result
        else:
            return "No valid response from Gemini API"
        
    except requests.exceptions.RequestException as e:
        return f"API request failed: {str(e)}"
    except json.JSONDecodeError as e:
        return f"Could not decode JSON response: {str(e)}"
    except Exception as e:
        return f"An unexpected error occurred: {str(e)}"

def make_api_request_with_retry(url: str, headers: dict, data: dict, max_retries: int = 3, initial_delay: float = 1.0) -> requests.Response:
    
    # Make an API request with exponential backoff retry logic for rate limiting. 
    # OpenRouter API endpoint is unstable sometimes so we need to retry
    
    # Args:
    #     url: The API endpoint URL
    #     headers: Request headers
    #     data: Request data
    #     max_retries: Maximum number of retry attempts
    #     initial_delay: Initial delay in seconds before first retry
        
    # Returns: requests.Response: The API response

    delay = initial_delay
    
    for attempt in range(max_retries):
        try:
            # Send the request to the API
            response = requests.post(
                url=url,
                headers=headers,
                data=json.dumps(data),
                timeout=180
            )
            
            # If we get a 429, wait and retry
            if response.status_code == 429:
                if attempt < max_retries - 1:  # Don't sleep on the last attempt
                    time.sleep(delay)
                    delay *= 2  # Exponential backoff
                    continue
            # Raise an error if the response is not successful
            response.raise_for_status()
            
            # Return the response
            return response
            
        except requests.exceptions.RequestException as e:
            if attempt == max_retries - 1:  # Last attempt
                raise e
            time.sleep(delay)
            delay *= 2  # Exponential backoff
            
    raise requests.exceptions.RequestException("Max retries exceeded")
