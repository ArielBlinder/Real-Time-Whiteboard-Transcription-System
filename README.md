# Real-Time Whiteboard Transcription System (BoardCast) 🎯

## Overview

**BoardCast** is a real-time whiteboard transcription system that captures handwritten notes, mathematical formulas, and diagrams from images or videos of whiteboards, and transcribes them into organized, editable digital text. The system is designed for students, educators, and professionals to effortlessly document lectures, meetings, and brainstorming sessions.

- **Input:** Upload images or videos, or use a live video feed.
- **Output:** Download transcriptions as `.docx`, `.pdf`, or `.txt` files.
- **Core:** Advanced OCR, handwriting, and math recognition using AI/LLM models (Llama 4, Gemini, Nvidia NIM).
- **Interface:** Modern, user-friendly React web app with editing and export features.

---

## Features

- **Real-Time Transcription:** Processes live video feeds or uploaded images/videos with minimal latency.
- **Mathematical Formula Recognition:** Accurately transcribes mathematical symbols and equations.
- **Handwriting Recognition:** Converts various handwriting styles into clear, readable digital text.
- **Content Filtering:** Automatically excludes erased or irrelevant whiteboard content.
- **Export Options:** Download transcriptions as `.docx`, `.pdf`, or `.txt`.
- **User-Friendly Interface:** Responsive UI for easy interaction and review.
- **Editing and Collaboration:** Edit transcriptions and add comments before export.

---

## System Architecture

- **Frontend:** React.js, Material-UI
- **Backend:** Python (Flask), Llama 4 Scout LLM, Gemini 2.0 flash
- **Video Processing:** FFMPEG (frame extraction, enhancement)
- **APIs:** Nvidia NIM for Llama 4 Scout , OpenRouter for Gemini 2.0 flash

### Project Structure

```
/Backend        # Python Flask server, OCR, AI/LLM integration
/Frontend       # React.js web application
/Docs           # Additional documentation and design docs
/requirements.txt # Python dependencies for backend
/launcher.py    # Windows launcher for both frontend and backend
/start_app.bat  # Batch file to launch the app on Windows
/LICENSE        # MIT License
```

---

## Installation & Setup

### 1. Clone the Repository

```bash
git clone https://github.com/ArielBlinder/Real-Time-Whiteboard-Transcription-System.git
cd Real-Time-Whiteboard-Transcription-System
```

### 2. Backend Setup (Python)

- **Requirements:** Python 3.8+
- **Install dependencies:**

```bash
pip install -r requirements.txt
```

- **API Keys:**
  - Set your Nvidia NIM API key in `Backend/process_frames.py` (`API_KEY`)
  - Set your OpenRouter (Gemini) API key in `Backend/process_video_text.py` (`OPENROUTER_API_KEY`)
  - _For production, use environment variables or a `.env` file for security._

### 3. Frontend Setup (React)

- **Requirements:** Node.js (v18+), npm or yarn
- **Install dependencies:**

```bash
cd Frontend
npm install
# or
yarn install
```

### 4. FFMPEG

- **Required for video processing.**
- [Download FFMPEG](https://ffmpeg.org/download.html) and ensure `ffmpeg` and `ffprobe` are in your system PATH.

### 5. Quick Start (Windows)

- Double-click `start_app.bat` to launch both frontend and backend, and open the app in your browser.

### 6. Manual Start (All Platforms)

- **Backend:**
  ```bash
  cd Backend
  python app.py
  ```
- **Frontend:**
  ```bash
  cd Frontend
  npm run dev
  # or
  yarn dev
  ```
- Open [http://localhost:5173](http://localhost:5173) in your browser.

---

## Usage

1. **Upload** an image or video of a whiteboard, or select a video.
2. **Transcription** is performed automatically.
3. **Review & Edit** the generated text. Make corrections or add comments as needed.
4. **Export** the final transcription as `.docx`, `.pdf`, or `.txt`.

---

## Example

- Upload a `.jpg` or `.mp4` file.
- Wait for processing (OCR + AI processing).
- Edit the result if needed.
- Download as your preferred format.

---

## Requirements

- Python 3.8+
- Node.js 18+
- FFMPEG (in PATH)
- Nvidia NIM API key
- OpenRouter API key

### Python Dependencies (from `requirements.txt`)

- Flask, flask-cors, python-docx, pypdf, Pillow, requests, opencv-python, numpy, python-dotenv, pyinstaller, psutil, pywin32

### Frontend Dependencies (from `package.json`)

- React, react-dom, react-icons, docx, file-saver, jspdf, @fortawesome/free-solid-svg-icons, react-router-dom, etc.

---

## Testing & Development

- **Integration Test:**
  - Run `Backend/test_integration.py` to verify API and AI integration.
  - Ensure API keys are set before running tests.
- **Frontend:**
  - Use `npm run dev` for hot-reload development.
- **Backend:**
  - Use `python app.py` for local development (auto-reloads with `debug=True`).

---

## Contribution Guidelines

1. Fork the repository and create a new branch for your feature or bugfix.
2. Write clear, well-documented code and update/add tests as needed.
3. Ensure your code passes all tests and does not break existing functionality.
4. Submit a pull request with a clear description of your changes.

---

## License

This project is licensed under the MIT License. See [LICENSE](./LICENSE) for details.

---

## Authors & Credits

- **Ariel Blinder**
- **Saar Attarchi**

---

## Troubleshooting & FAQ

- **FFMPEG not found:** Ensure `ffmpeg` and `ffprobe` are installed and in your system PATH.
- **API errors:** Double-check your API keys and network connection.
- **Windows users:** Use `start_app.bat` for easiest startup.
- **Other issues:** Please open an issue or check the [Docs](./Docs) folder for more details.

---

## Related & Further Reading

- See `/Docs` for detailed design, requirements, and competitor analysis.
- For FFMPEG help: [FFMPEG Documentation](https://ffmpeg.org/documentation.html)
- For Nvidia NIM and OpenRouter API docs, see their respective official sites.
