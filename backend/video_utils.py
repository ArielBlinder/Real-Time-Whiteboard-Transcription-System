import os
import subprocess
import tempfile
from pathlib import Path

FFMPEG  = "ffmpeg"
FFPROBE = "ffprobe"
EXTRACT_EVERY_SEC = 30     # Frame interval (seconds)
FRAME_SIZE = 800    # Output image size

class DependencyError(RuntimeError):
    pass

def _cmd_ok(cmd):
    try:
        subprocess.run([cmd, "-version"], capture_output=True, check=True)
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        return False

def check_dependencies():
    missing = [c for c in (FFMPEG, FFPROBE) if not _cmd_ok(c)]
    if missing:
        raise DependencyError(f"Missing system packages: {', '.join(missing)}")

def extract_frames(video_path: Path, dst_folder: Path) -> list[Path]:
    check_dependencies()
    dst_folder.mkdir(parents=True, exist_ok=True)
    frame_pattern = dst_folder / "frame_%05d.jpg"
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

def tmp_dir() -> tempfile.TemporaryDirectory:
    return tempfile.TemporaryDirectory(prefix="video_proc_")

