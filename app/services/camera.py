import subprocess
import tempfile
from pathlib import Path

from fastapi import HTTPException


def capture_jpeg(width: int = None, height: int = None, timeout_ms: int = 2000) -> bytes:
    """Capture a JPEG image using rpicam-jpeg and return raw bytes."""
    with tempfile.TemporaryDirectory() as tmpdir:
        img_path = Path(tmpdir) / "capture.jpg"
        cmd = [
            "rpicam-jpeg",
            "-o",
            str(img_path),
            "-t",
            str(timeout_ms),
        ]
        if width:
            cmd.extend(["--width", str(width)])
        if height:
            cmd.extend(["--height", str(height)])
        result = subprocess.run(cmd, capture_output=True)
        if result.returncode != 0:
            stderr = result.stderr.decode("utf-8", errors="ignore")
            raise HTTPException(status_code=500, detail=f"Camera capture failed: {stderr}")

        try:
            return img_path.read_bytes()
        except FileNotFoundError as exc:
            raise HTTPException(status_code=500, detail="Camera output file not found") from exc
