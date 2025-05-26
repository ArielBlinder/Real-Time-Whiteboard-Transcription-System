# Real-Time Whiteboard Transcription System 🎯

## Overview 📋

The Real-Time Whiteboard Transcription System is an innovative solution designed to effortlessly capture and transcribe whiteboard content. Whether it's handwritten notes, mathematical formulas, or diagrams, this system converts visual data into organized, editable digital formats (.docx, .pdf, .txt).

This project addresses the common challenge faced by students, educators, and professionals in documenting lectures, meetings, and brainstorming sessions. By leveraging advanced Optical Character Recognition (OCR), AI/ML models (specifically Llama 4 LLM), and sophisticated image processing techniques, the system aims for high accuracy and efficiency.

## Features ✨

- **Real-Time Transcription:** Processes live video feeds or uploaded images/videos with minimal latency.
- **Mathematical Formula Recognition:** Accurately transcribes mathematical symbols and equations.
- **Handwriting Recognition:** Converts various handwriting styles into clear, readable digital text.
- **Content Filtering:** Automatically excludes erased or irrelevant whiteboard content.
- **Export Options:** Seamlessly exports transcriptions to `.docx`, `.pdf`, or `.txt`.
- **User-Friendly Interface:** Intuitive and responsive UI designed for easy interaction across various devices.
- **Editing and Collaboration:** Allows manual text corrections and adding user comments for enhanced collaboration.

## System Architecture 🏗️

The system employs a robust Model-View-Controller (MVC) architecture:

- **Model:**

  - OCR and handwriting recognition powered by Llama 4 LLM.
  - Advanced image processing for content enhancement and noise reduction.
  - Filtering algorithms to exclude erased or irrelevant whiteboard content.

- **View:**

  - Intuitive and responsive web interface built with React.js and Material-UI.
  - Allows users to upload media, monitor transcription progress, review and edit results, and configure export settings.

- **Controller:**
  - Manages user interactions, orchestrates OCR processing, and updates views.

## Tech Stack 🛠️

- **Frontend:** React.js, Material-UI
- **Backend:** Python,Flask, Llama 4 LLM
- **Video Processing:** FFMPEG
- **APIs:** Nvidia NIM and OpenRouter.

## Project Structure 📂

The project is organized into the following main directories:

- **`/Frontend`**: Contains the React.js application for the user interface.
- **`/Backend`**: Houses the Python server with Flask and core transcription logic, including Llama 4 LLM integration.
- **`/video process`**: Includes scripts and tools related to video capture and pre-processing using FFMPEG.
- **`/Docs`**: Contains additional documentation, design documents, or user guides.
- **`/requirements.txt`**: Lists the Python dependencies for the backend.
- **`README.md`**: This file, providing an overview of the project.
- **`LICENSE`**: Contains the project's license information.

## Requirements Installation 📦

To set up the development environment and install the required packages:

1.  **Clone the repository:**

    ```bash
    git clone https://github.com/ArielBlinder/Real-Time-Whiteboard-Transcription-System.git
    cd Real-Time-Whiteboard-Transcription-System
    ```

2.  **Backend (Python):**
    Ensure you have Python 3.8+ installed.
    Navigate to the `Backend` directory (if applicable, otherwise run from root) and install dependencies:

    ```bash
    # Assuming requirements.txt is in the root or Backend
    pip install -r requirements.txt
    ```

    _(Note: If `requirements.txt` is specific to the Backend, adjust the path accordingly. Consider having separate requirements for `video process` if needed.)_

3.  **Frontend (React.js):**
    Ensure you have Node.js and npm/yarn installed.
    Navigate to the `Frontend` directory:

    ```bash
    cd Frontend
    npm install
    # or
    # yarn install
    ```

4.  **FFMPEG:**
    FFMPEG must be installed and accessible in your system's PATH. Installation instructions vary by operating system. Refer to the [official FFMPEG website](https://ffmpeg.org/download.html) for details.

## How It Works 🚀

1.  **Input:** Users can upload video files (e.g., `.mp4`, `.avi`), images (e.g., `.jpg`, `.png`), or connect a live video feed.
2.  **Preprocessing:** The `video process` module (utilizing FFMPEG) handles video stream decoding, frame extraction, and initial image enhancements.
3.  **Core Processing (Backend):**
    - Selected frames or images are sent to the backend.
    - The Llama 4 LLM performs OCR, handwriting recognition, and mathematical symbol detection.
    - Content filtering algorithms remove noise and irrelevant information.
4.  **Review & Edit (Frontend):** The transcribed content is displayed on the user-friendly interface. Users can review, make corrections, and add comments.
5.  **Export:** Users can download the final transcription in their preferred format (`.docx`, `.pdf`, `.txt`).

## Usage (Running the Project) 🏃‍♂️

(Detailed instructions on how to start the backend server and the frontend development server will be added here. This typically involves commands like `python app.py` or `flask run` for the backend, and `npm start` or `yarn start` for the frontend.)

## Stakeholders 👥

- **Students and Educators:** Primary users capturing and utilizing lecture content efficiently.
- **Educational Institutions:** Enhancing accessibility and documentation of educational materials.
- **Software Developers:** Building, maintaining, and enhancing the system's capabilities.

## Expected Challenges ⚠️

- Handling diverse handwriting styles and low-quality images/video frames.
- Ensuring real-time performance with complex mathematical symbol recognition.
- Scalability of the system to handle multiple users and large files.

## Metrics for Success 📈

- **Transcription Accuracy Rate:** Quantitative evaluation of transcription accuracy (e.g., Word Error Rate, Character Error Rate) across diverse inputs (handwriting, print, mathematical formulas).
- **Processing Speed:** Time taken from input to final transcription output.
- **User Satisfaction:** Feedback collected through surveys and usability testing on the interface, features, and overall experience.
- **Exported Content Quality:** Assessment of the accuracy, formatting, and completeness of the exported `.docx`, `.pdf`, and `.txt` files.
- **System Robustness:** Performance evaluation under various conditions, including low-quality inputs and concurrent user access.

## Competitor Comparison 🆚

- **Google Lens:** Limited handwriting support; lacks real-time video capabilities.
- **Microsoft OCR (Azure):** Costly and requires extensive customization.
- **OpenCV:** Requires high technical expertise for custom solutions.

**Our Innovation:** Combines real-time processing capabilities with robust multilingual and mathematical transcription, an intuitive user interface, efficient content filtering, and flexible export options, setting it apart from existing solutions.

## Authors ✏️

- **Ariel Blinder**
- **Saar Attarchi**
