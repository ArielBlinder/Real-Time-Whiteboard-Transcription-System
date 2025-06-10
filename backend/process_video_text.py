import os
import time
from typing import List, Tuple
from google import genai
from google.genai import types

# IMPORTANT: Replace with your API key, Get it from https://aistudio.google.com/apikey
GEMINI_API_KEY = "ADD_KEY_HERE"

def process_frames_with_gemini(frame_data: List[Tuple[str, str]]) -> str:
    # Process a list of OCR texts with timestamps from video frames using Gemini API
    
    # Args: "frame_data": List of (OCR_text, timestamp_str) tuples from individual frames that are ordered chronologically
        
    # Returns: Processed and cleaned transcription from Gemini giving the final result with timestamps
    
    if not GEMINI_API_KEY:
        raise ValueError("GEMINI_API_KEY environment variable is not set")
    
    if not frame_data:
        return "No frame data provided for processing"
    
    # Combine all frame texts with timestamps and frame markers for context
    combined_text = ""
    for i, (text, timestamp) in enumerate(frame_data, 1):
        if text.strip():  # Only include non-empty texts
            combined_text += f"Frame {i} [Timestamp: {timestamp}]:\n{text}\n\n==================================================\n\n"
    
    if not combined_text.strip():
        return "No valid text content found in frames"
    
    # Define the AI prompt for processing the OCR results with timestamp preservation
    ai_prompt = (
        """**Role:** You are an expert AI assistant specializing in processing and refining OCR output from whiteboard lectures. 
        These lectures are captured frame by frame, and the content is mathematical, including formulas, definitions, and explanations.

**Context:** The provided input is a collation of OCR text from sequential frames of a whiteboard with exact timestamps. This means:
* Content is generally added incrementally.
* Later frames often repeat content from earlier frames, along with new additions.
* Sometimes, a concept or formula might be written partially in one frame and completed or elaborated upon in a subsequent frame.
* The input text includes frame markers, timestamps (e.g., `[Timestamp: 0:01:30]`), and separators (`==================================================`) which are part of the OCR capture process, not the lecture content itself.

**Primary Goal:** Your task is to meticulously transform this raw, sequential OCR data into a single, clean, logically and chronologically ordered, and accurate transcription of the entire lecture, as if it were a well-edited set of lecture notes. 
**CRITICALLY IMPORTANT**: You must include the exact timestamp [h:mm:ss] for each distinct piece of content to show when it appeared in the video.

**Detailed Instructions:**

1. **Analyze Full Context:** Process the entire provided OCR text, considering all frames and their sequence.

2. **Identify and Eliminate Redundancy:**
   * Identify all instances of duplicated or overlapping content across frames.
   * Ensure each piece of information appears only once in the final output.

3. **Retain Completeness and Accuracy:**
   * For each unique segment, keep the most complete and correct version.
   * If information evolves across frames, use the final complete version.
   * Correct obvious OCR errors (e.g., "5" as "S", "0" as "O").

4. **Timestamp Integration:**
   * Include timestamp [h:mm:ss] when content first became complete/readable.
   * Use timestamp of the frame where content reached its most complete form.
   * Present timestamps at the beginning of each logical section, only once.

5. **Mathematical Accuracy:**
   * Preserve proper mathematical notation and structure.
   * Ensure formulas are syntactically correct and complete.
   * Use consistent notation throughout.

6. **Sequential Reconstruction:**
   * Arrange content in logical and chronological order of appearance.
   * Maintain pedagogical flow between related concepts.

7. **Structure and Formatting:**
   * Format timestamps as [h:mm:ss] at the beginning of each concept, then new line.
   * Use clear paragraphing for readability.
   * Preserve mathematical structure (fractions, exponents, subscripts).

**Output Constraints:**
* Include only cleaned transcription with relevant timestamps.
* Exclude frame markers, frame numbers, and separators.
* No additional commentary or explanations about your process.
* Each concept must be self-contained and mathematically accurate.
* full transcript of the lecture.

**Example Output Format:**
[0:00:30]
First concept or formula introduced
Content describing the first concept...

[0:01:00]
Second concept or additional information
Content describing the second concept...

**Input Text:**
""" + combined_text
    )

    try:
        # Make the API request with exponential backoff retry logic
        # Google AI Studio API can sometimes be unstable so we need to retry
        result = make_api_request_with_retry(ai_prompt)
        return result
        
    except Exception as e:
        return f"An unexpected error occurred: {str(e)}"

def make_api_request_with_retry(prompt: str, max_retries: int = 3, initial_delay: float = 1.0) -> str:
    
    # Make an API request with exponential backoff retry logic for rate limiting. 
    # Google AI Studio API can sometimes be unstable so we need to retry
    
    # Args:
    #     prompt: The text prompt to send to Gemini
    #     max_retries: Maximum number of retry attempts
    #     initial_delay: Initial delay in seconds before first retry
        
    # Returns: str: The API response content

    delay = initial_delay
    
    for attempt in range(max_retries):
        try:
            # Create the Gemini client
            client = genai.Client(
                api_key=GEMINI_API_KEY,
            )

            model = "gemini-2.0-flash"
            contents = [
                types.Content(
                    role="user",
                    parts=[
                        types.Part.from_text(text=prompt),
                    ],
                ),
            ]
            generate_content_config = types.GenerateContentConfig(
                response_mime_type="text/plain",
            )

            # Collect the streaming response
            result = ""
            for chunk in client.models.generate_content_stream(
                model=model,
                contents=contents,
                config=generate_content_config,
            ):
                if chunk.text:
                    result += chunk.text
            
            # Return the complete result
            return result
            
        except Exception as e:
            if attempt == max_retries - 1:  # Last attempt
                raise e
            time.sleep(delay)
            delay *= 2  # Exponential backoff
            
    raise Exception("Max retries exceeded")
