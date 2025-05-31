import requests
import json
import os
import time
from typing import List

# IMPORTANT: Replace with your API key, Get it from https://openrouter.ai/
OPENROUTER_API_KEY = "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" 

def process_frames_with_gemini(frame_texts: List[str]) -> str:
    """
    Process a list of OCR texts from video frames using Gemini API.
    
    Args:
        frame_texts: List of OCR text results from individual frames (already ordered chronologically)
        
    Returns:
        str: Processed and cleaned transcription from Gemini
    """
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
        """**Role:** You are an expert AI assistant specializing in processing and refining OCR (Optical Character Recognition) output from whiteboard lectures. These lectures are captured frame by frame, and the content is mathematical, including formulas, definitions, explanations, and accompanying text.

**Context:** The provided input is a collation of OCR text from sequential frames of a whiteboard. This means:
* Content is incrementally added across frames.
* Later frames may repeat earlier content while introducing new additions.
* Concepts, formulas, or explanations may begin in one frame and be completed or refined in subsequent frames.
* The input contains frame markers (e.g., Frame Y:) and visual separators (==================================================), which are part of the OCR capture process and not part of the actual lecture content.

**Your task is to carefully transform this raw, sequential OCR output into a single, clean, logically ordered, and accurate transcription of the complete lecture—as if it were professionally edited lecture notes.

**Detailed Instructions:**

1.  **Analyze Full Context:** Carefully process the full set of frames, understanding the progression and cumulative nature of the lecture.
2.  **Identify and Eliminate Redundancy:**
    * Detect all repeated, overlapping, or duplicated content across frames.
    * Ensure that each piece of information—whether textual or mathematical—appears only once in the final transcript.
3.  **Retain Completeness and Accuracy (Handling Evolving Text):**
    * Preserve the most complete and accurate version of each segment (e.g., definitions, formulas, or explanations).
    * If a segment is introduced partially in one frame and completed or clarified later, include only the final, complete version.
    * Do not replace a complete version with a partial one from a later frame unless it clearly corrects or refines the content.
4.  **Sequential Reconstruction:**
    * Organize the cleaned segments in a logical and chronological order, reflecting how the lecture builds over time.
    * Ensure smooth progression of ideas, explanations, and formulas.
5.  **Preserve Mathematical Notation:**
    * Accurately preserve all mathematical expressions, symbols, and notation as captured.
    * Ensure that mathematical notation is correctly rendered and readable.
6.  **Structure and Formatting:**
    * Present the final transcription as a continuous, well-structured document.
    * Use appropriate paragraph breaks and spacing to enhance readability and comprehension.
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
        response = make_api_request_with_retry(
            url="https://openrouter.ai/api/v1/chat/completions",
            headers=headers,
            data=data
        )

        response_data = response.json()
        
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
    """
    Make an API request with exponential backoff retry logic for rate limiting.
    
    Args:
        url: The API endpoint URL
        headers: Request headers
        data: Request data
        max_retries: Maximum number of retry attempts
        initial_delay: Initial delay in seconds before first retry
        
    Returns:
        requests.Response: The API response
    """
    delay = initial_delay
    
    for attempt in range(max_retries):
        try:
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
                    
            response.raise_for_status()
            return response
            
        except requests.exceptions.RequestException as e:
            if attempt == max_retries - 1:  # Last attempt
                raise e
            time.sleep(delay)
            delay *= 2  # Exponential backoff
            
    raise requests.exceptions.RequestException("Max retries exceeded") 