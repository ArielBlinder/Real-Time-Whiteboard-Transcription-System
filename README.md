# Real-Time Whiteboard Transcription System 🎯

## Overview 📋

The Real-Time Whiteboard Transcription System is an innovative solution designed to effortlessly capture and transcribe whiteboard content. Whether it’s handwritten notes, mathematical formulas, this system converts visual data into organized, editable digital formats (.docx, .pdf, .txt).

This project addresses the common challenge faced by students, educators, and professionals in documenting lectures, meetings, and brainstorming sessions. By leveraging advanced OCR (Optical Character Recognition), AI/ML models, and sophisticated image processing, the system ensures high accuracy and efficiency.

## Features ✨

- **Real-Time Transcription:** Processes live video feeds or uploaded images/videos with minimal latency.
- **Mathematical Formula Recognition:** Accurately transcribes mathematical symbols and equations.
- **Handwriting Recognition:** Converts handwritten notes into clear, readable digital text.
- **Content Filtering:** Automatically excludes erased or irrelevant whiteboard content.
- **Export Options:** Seamlessly exports transcriptions to `.docx`, `.pdf`, or `.txt`.
- **User-Friendly Interface:** Intuitive and responsive UI designed for easy interaction across various devices.
- **Editing and Collaboration:** Allows manual text corrections and adding user comments for enhanced collaboration.

## System Architecture 🏗️

The system employs a robust Model-View-Controller (MVC) architecture:

- **Model:**

  - OCR and handwriting recognition with Llama 4 LLM
  - Processes and filters content to maintain accuracy.

- **View:**

  - Responsive interface for uploads, reviewing transcriptions, and configuring export settings.

- **Controller:**
  - Manages user interactions, orchestrates OCR processing, and updates views.

## Tech Stack 🛠️

- **Frontend:** React.js, Material-UI
- **Backend:** Python (Flask/Django), and Llama 4 LLM
- **Data Formats:** `.docx`, `.pdf`, `.txt`
- **APIs:** FFMPEG (video processing), custom APIs for exporting and user preferences

## Requirements Installation 📦

To install the required packages, use the provided `requirements.txt` file:

```bash
pip install -r requirements.txt
```

Make sure your Python environment is properly configured.

## How It Works 🚀

1. **Upload:** Users upload videos, images, or access live video feeds.
2. **Processing:** The system applies OCR, handwriting recognition, and mathematical symbol detection.
3. **Review:** Transcribed content is displayed for review, editing, and adding comments.
4. **Export:** Users download transcriptions in their chosen format.

## Stakeholders 👥

- **Students and Educators:** Primary users capturing and utilizing lecture content efficiently.
- **Educational Institutions:** Enhancing accessibility and documentation of educational materials.
- **Software Developers:** Building, maintaining, and enhancing the system's capabilities.

## Expected Challenges ⚠️

- Handwriting recognition accuracy.
- Handling low-quality images and video frames.
- Mathematical symbol recognition complexity.

## Metrics for Success 📈

- **Accuracy Rate:** Evaluation of transcription accuracy across various inputs.
- **User Feedback:** Gathering feedback on usability and learning impact.
- **Exported Content Quality:** Meeting users’ expectations for format and organization.
- **Usability:** Performance evaluation under diverse classroom conditions.

## Competitor Comparison 🆚

- **Google Lens:** Limited handwriting support; lacks real-time video capabilities.
- **Microsoft OCR (Azure):** Costly and requires extensive customization.
- **OpenCV:** Requires high technical expertise for custom solutions.

**Our Innovation:** Real-time processing, multilingual and mathematical transcription, intuitive interface, efficient content filtering, and easy exporting capabilities.

## Authors ✏️

- **Ariel Blinder**
- **Saar Attarchi**
