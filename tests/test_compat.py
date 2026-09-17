"""Unit tests for compat.py cross-platform utilities."""

import os
import sys
from pathlib import Path
import pytest

from ufo_sacred_geometry.compat import (
    is_windows,
    is_macos,
    is_linux,
    is_termux,
    get_platform_info,
    normalize_path,
    atomic_write_text,
    atomic_write_bytes,
    read_text_safe,
    read_json_safe,
    write_json_safe,
    safe_delete,
)


def test_platform_detection_booleans():
    """Verify platform detection functions return boolean types without error."""
    assert isinstance(is_windows(), bool)
    assert isinstance(is_macos(), bool)
    assert isinstance(is_linux(), bool)
    assert isinstance(is_termux(), bool)


def test_get_platform_info():
    """Verify get_platform_info returns dictionary with expected keys."""
    info = get_platform_info()
    assert isinstance(info, dict)
    assert "os_name" in info
    assert "platform" in info
    assert "python_version" in info
    assert "is_windows" in info
    assert "is_linux" in info
    assert "is_macos" in info
    assert "path_sep" in info


def test_normalize_path(tmp_path):
    """Verify path normalization expands and resolves paths correctly."""
    test_file = tmp_path / "test_subdir" / "sample.txt"
    resolved = normalize_path(test_file, create_parent=True)
    assert isinstance(resolved, Path)
    assert resolved.parent.exists()
    assert resolved.is_absolute()


def test_atomic_write_and_read_text(tmp_path):
    """Verify atomic write text and safe text reading."""
    test_file = tmp_path / "atomic_text.txt"
    sample_content = "✨ Sacred Geometry Core v1.0.0 ✨\nLine 2: Phi = 1.6180339887"

    written_path = atomic_write_text(test_file, sample_content)
    assert written_path.exists()

    read_back = read_text_safe(test_file)
    assert read_back == sample_content


def test_atomic_write_bytes(tmp_path):
    """Verify atomic write of binary payloads."""
    test_file = tmp_path / "binary_data.bin"
    payload = b"\x00\x01\x02\xFF\xFE\xFD"

    written_path = atomic_write_bytes(test_file, payload)
    assert written_path.exists()
    with open(written_path, "rb") as f:
        assert f.read() == payload


def test_read_text_safe_fallback_and_error(tmp_path):
    """Verify safe text reading with default fallback or error raising."""
    missing = tmp_path / "non_existent.txt"
    assert read_text_safe(missing, default="fallback") == "fallback"

    with pytest.raises(FileNotFoundError):
        read_text_safe(missing)


def test_json_safe_io(tmp_path):
    """Verify safe JSON serialization and deserialization."""
    test_file = tmp_path / "config.json"
    data = {
        "pattern": "flower_of_life",
        "radius": 150.0,
        "phi": 1.6180339887,
        "active": True,
        "nested": {"layers": [1, 2, 3]},
    }

    written = write_json_safe(test_file, data)
    assert written.exists()

    parsed = read_json_safe(test_file)
    assert parsed == data
    assert parsed["radius"] == 150.0

    # Missing file returns default
    missing_parsed = read_json_safe(tmp_path / "none.json", default={"default": 1})
    assert missing_parsed == {"default": 1}


def test_safe_delete(tmp_path):
    """Verify safe deletion handles existing and non-existing files safely."""
    f = tmp_path / "to_delete.txt"
    atomic_write_text(f, "Temporary")
    assert f.exists()
    assert safe_delete(f) is True
    assert not f.exists()

    # Deleting missing file returns False without raising
    assert safe_delete(f) is False
