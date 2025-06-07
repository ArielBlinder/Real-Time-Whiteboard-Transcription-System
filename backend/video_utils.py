import os
import subprocess
import tempfile
from pathlib import Path
from PIL import Image
import io
from typing import List, Tuple

FFMPEG  = "ffmpeg" 
FFPROBE = "ffprobe"
EXTRACT_EVERY_SEC = 30     # Frame interval (seconds)
FRAME_SIZE = 800    # Output image size is 800x800 

class DependencyError(RuntimeError):
    pass

# Check if the command is available
def _cmd_ok(cmd):
    try:
        # Run the command and check if it returns a successful exit code
        subprocess.run([cmd, "-version"], capture_output=True, check=True)
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        return False

# Check if the dependencies are installed
def check_dependencies():
    # Check if the commands are available
    missing = [c for c in (FFMPEG, FFPROBE) if not _cmd_ok(c)]
    if missing:
        raise DependencyError(f"Missing system packages: {', '.join(missing)}")

def format_timestamp(seconds: float) -> str:
    
    # Convert seconds to h:mm:ss format
    
    # Args: seconds: Time in seconds
    
    # Returns: Formatted timestamp string
    
    hours = int(seconds // 3600)
    minutes = int((seconds % 3600) // 60)
    seconds_remainder = int(seconds % 60)
    return f"{hours}:{minutes:02d}:{seconds_remainder:02d}"

def extract_frames_to_memory(video_path: Path) -> List[Tuple[int, Image.Image, str]]:
    
    # Extract frames from video directly to memory for immediate processing with timestamps. 
    # Args: video_path: Path to the video file
    # Returns: List of tuples containing (frame_number, Image, timestamp_str) ordered chronologically
    
    check_dependencies()
    
    # Create a temporary directory for frame extraction
    with tempfile.TemporaryDirectory(prefix="frames_") as temp_dir:
        temp_path = Path(temp_dir)
        # Create a pattern for the frame files
        frame_pattern = temp_path / "frame_%05d.jpg"
        # Extract frames to temporary files first (more reliable than parsing pipe)
        cmd = [
            FFMPEG,
            "-hide_banner",
            "-loglevel", "error",
            "-i", str(video_path),
            "-vf", (
                # One frame per every 30 seconds
                f"fps=1/{EXTRACT_EVERY_SEC},"
                # Scale the frame to 800x800
                f"scale={FRAME_SIZE}:{FRAME_SIZE}:force_original_aspect_ratio=decrease,"
                # Pad the frame to 800x800
                f"pad={FRAME_SIZE}:{FRAME_SIZE}:(ow-iw)/2:(oh-ih)/2"
            ),
            # Quality is 2
            "-q:v", "2",
            # Output the frame files
            str(frame_pattern)
        ]
        
        try:
            # Run the command and check if it returns a successful exit code
            subprocess.run(cmd, check=True, capture_output=True)
            
            # Load all frame files into memory
            frames = []
            frame_files = sorted(temp_path.glob("frame_*.jpg"))
            
            for frame_number, frame_file in enumerate(frame_files):
                try:
                    # Load image directly into PIL
                    image = Image.open(frame_file)
                    # Convert to RGB to ensure consistent format
                    if image.mode != 'RGB':
                        image = image.convert('RGB')
                    # Create a copy in memory so we can close the file
                    image_copy = image.copy()
                    image.close()
                    
                    # Calculate timestamp based on frame number and extraction interval
                    timestamp_seconds = frame_number * EXTRACT_EVERY_SEC
                    timestamp_str = format_timestamp(timestamp_seconds)
                    
                    frames.append((frame_number, image_copy, timestamp_str))
                except Exception as e:
                    print(f"Warning: Could not load frame {frame_number}: {e}")
                    
            return frames
            
        except subprocess.CalledProcessError as e:
            raise RuntimeError(f"FFmpeg failed: {e}")

def tmp_dir() -> tempfile.TemporaryDirectory:
    return tempfile.TemporaryDirectory(prefix="video_proc_")

# Legacy function for backward compatibility.
"""
def extract_frames(video_path: Path, dst_folder: Path) -> list[Path]:
    
    # Legacy function for backward compatibility.
    # Extract frames to files 
    
    check_dependencies()
    
    # Create the destination folder
    dst_folder.mkdir(parents=True, exist_ok=True)
    
    # Create a pattern for the frame files
    frame_pattern = dst_folder / "frame_%05d.jpg"
    
    # Run the command and check if it returns a successful exit code
    subprocess.run(
        [
            FFMPEG,
            "-hide_banner",
            "-loglevel", "error",
            "-i", str(video_path),
            "-vf", (
                f"fps=1/{EXTRACT_EVERY_SEC},"
                f"scale={FRAME_SIZE}:{FRAME_SIZE}:force_original_aspect_ratio=decrease,"
                f"pad={FRAME_SIZE}:{FRAME_SIZE}:(ow-iw)/2:(oh-ih)/2"
            ),
            "-q:v", "2",
            str(frame_pattern)
        ],
        check=True
    )
    return sorted(dst_folder.glob("frame_*.jpg"))
"""