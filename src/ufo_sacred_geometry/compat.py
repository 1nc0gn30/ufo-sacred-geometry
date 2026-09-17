"""Cross-platform compatibility utilities for ufo-sacred-geometry.

Provides platform-safe file I/O, atomic text/binary writing with sync,
path normalization (Linux, macOS, Windows, Android/Termux),
safe JSON parsing/serialization, and platform diagnostics.
100% Python Standard Library.
"""

from __future__ import annotations

import json
import os
import platform
import sys
import tempfile
from pathlib import Path
from typing import Any, Dict, Optional, Union


def is_termux() -> bool:
    """Check if running in Android Termux environment."""
    return "TERMUX_VERSION" in os.environ or "/data/data/com.termux" in os.environ.get("PREFIX", "")


def is_windows() -> bool:
    """Check if running on Windows."""
    return sys.platform.startswith("win") or os.name == "nt"


def is_macos() -> bool:
    """Check if running on macOS (Darwin)."""
    return sys.platform == "darwin"


def is_linux() -> bool:
    """Check if running on Linux (excluding Android/Termux when distinguished)."""
    return sys.platform.startswith("linux")


def get_platform_info() -> Dict[str, Any]:
    """Return diagnostic platform metadata dictionary."""
    return {
        "os_name": os.name,
        "platform": sys.platform,
        "system": platform.system(),
        "release": platform.release(),
        "machine": platform.machine(),
        "python_version": platform.python_version(),
        "is_windows": is_windows(),
        "is_macos": is_macos(),
        "is_linux": is_linux(),
        "is_termux": is_termux(),
        "path_sep": os.sep,
        "line_sep": os.linesep,
    }


def normalize_path(path: Union[str, Path], create_parent: bool = False) -> Path:
    """Normalize and resolve a path across Linux, macOS, Windows, and Termux.

    Args:
        path: File or directory path.
        create_parent: If True, recursively creates the parent directory if missing.

    Returns:
        Resolved Path object.
    """
    if isinstance(path, str):
        # Expand user home directory '~' and environment variables
        expanded = os.path.expanduser(os.path.expandvars(path))
        p = Path(expanded).resolve()
    else:
        p = path.expanduser().resolve()

    if create_parent and not p.parent.exists():
        p.parent.mkdir(parents=True, exist_ok=True)

    return p


def atomic_write_text(
    path: Union[str, Path],
    content: str,
    encoding: str = "utf-8",
    newline: Optional[str] = "\n",
) -> Path:
    """Atomically write text to disk using temporary file rename with fsync.

    Prevents partial/corrupted files during power loss or abrupt termination.
    Works reliably on POSIX, Windows, and Android Termux.

    Args:
        path: Destination file path.
        content: Text string content to write.
        encoding: Text encoding (default: 'utf-8').
        newline: Line ending to use (default: '\n').

    Returns:
        Path to written file.
    """
    target = normalize_path(path, create_parent=True)
    temp_dir = target.parent

    # Create temporary file in the same directory to ensure same filesystem for atomic rename
    fd, temp_file_path = tempfile.mkstemp(
        dir=str(temp_dir),
        prefix=f".tmp_{target.stem}_",
        suffix=target.suffix or ".tmp",
    )

    try:
        with open(fd, mode="w", encoding=encoding, newline=newline) as f:
            f.write(content)
            f.flush()
            os.fsync(f.fileno())

        # Atomically replace destination
        # On Windows, os.replace replaces existing files atomically in Python 3.3+
        os.replace(temp_file_path, str(target))
    except Exception:
        # Clean up temporary file on failure
        if os.path.exists(temp_file_path):
            try:
                os.remove(temp_file_path)
            except OSError:
                pass
        raise

    return target


def atomic_write_bytes(
    path: Union[str, Path],
    data: bytes,
) -> Path:
    """Atomically write raw binary data to disk with fsync.

    Args:
        path: Destination file path.
        data: Binary payload bytes.

    Returns:
        Path to written file.
    """
    target = normalize_path(path, create_parent=True)
    temp_dir = target.parent

    fd, temp_file_path = tempfile.mkstemp(
        dir=str(temp_dir),
        prefix=f".tmp_{target.stem}_",
        suffix=target.suffix or ".tmp",
    )

    try:
        with open(fd, mode="wb") as f:
            f.write(data)
            f.flush()
            os.fsync(f.fileno())

        os.replace(temp_file_path, str(target))
    except Exception:
        if os.path.exists(temp_file_path):
            try:
                os.remove(temp_file_path)
            except OSError:
                pass
        raise

    return target


def read_text_safe(
    path: Union[str, Path],
    default: Optional[str] = None,
    encodings: Optional[list[str]] = None,
) -> str:
    """Safely read text file content with fallback encodings.

    Tries utf-8, utf-8-sig (BOM handling), latin1, and cp1252.

    Args:
        path: Path to read from.
        default: Fallback string if file not found (if None, raises FileNotFoundError).
        encodings: List of encodings to try sequentially.

    Returns:
        File contents as string.
    """
    target = normalize_path(path)
    if not target.exists():
        if default is not None:
            return default
        raise FileNotFoundError(f"File not found: {target}")

    enc_list = encodings or ["utf-8", "utf-8-sig", "latin1", "cp1252"]
    last_err: Optional[Exception] = None

    for enc in enc_list:
        try:
            with open(target, "r", encoding=enc) as f:
                return f.read()
        except UnicodeDecodeError as err:
            last_err = err
            continue

    if last_err is not None:
        raise last_err
    return ""


def read_json_safe(
    path: Union[str, Path],
    default: Optional[Any] = None,
) -> Any:
    """Safely parse a JSON file with error tolerance.

    Args:
        path: File path to read.
        default: Default value returned if file is missing or invalid JSON.

    Returns:
        Parsed JSON object or default.
    """
    target = normalize_path(path)
    if not target.exists():
        return default

    try:
        text = read_text_safe(target)
        return json.loads(text)
    except (json.JSONDecodeError, OSError):
        return default


def write_json_safe(
    path: Union[str, Path],
    obj: Any,
    indent: int = 2,
    sort_keys: bool = False,
) -> Path:
    """Atomically serialize and write JSON to disk with clean formatting.

    Args:
        path: Target file path.
        obj: Serializable Python object.
        indent: JSON indentation spaces.
        sort_keys: Whether to sort dictionary keys.

    Returns:
        Resolved Path to written file.
    """
    payload = json.dumps(obj, indent=indent, sort_keys=sort_keys, ensure_ascii=False)
    return atomic_write_text(path, payload + "\n", encoding="utf-8")


def safe_delete(path: Union[str, Path]) -> bool:
    """Safely delete a file if it exists without raising errors.

    Returns:
        True if file was deleted, False if file did not exist or could not be deleted.
    """
    try:
        p = Path(path).resolve()
        if p.exists() and p.is_file():
            p.unlink()
            return True
    except OSError:
        return False
    return False
