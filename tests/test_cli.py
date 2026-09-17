"""Unit tests for Command-Line Interface (CLI) entry point and subcommands."""

import os
import sys
from pathlib import Path
import pytest

from ufo_sacred_geometry.cli import main


def test_cli_help(capsys):
    """Verify CLI prints help when invoked without arguments."""
    exit_code = main([])
    assert exit_code == 0
    captured = capsys.readouterr()
    assert "ufo-sacred-geometry" in captured.out or "usage:" in captured.out


def test_cli_presets(capsys):
    """Verify 'presets' command lists registered catalog items."""
    exit_code = main(["presets"])
    assert exit_code == 0
    captured = capsys.readouterr()
    assert "Flower of Life" in captured.out or "flower_of_life" in captured.out


def test_cli_presets_json(capsys):
    """Verify 'presets --json' outputs valid parseable JSON."""
    exit_code = main(["presets", "--json"])
    assert exit_code == 0
    captured = capsys.readouterr()
    assert '"id":' in captured.out


def test_cli_generate_svg_file(tmp_path):
    """Verify 'generate' command outputs SVG file."""
    out_svg = tmp_path / "flower.svg"
    exit_code = main([
        "generate",
        "flower_of_life",
        "--radius", "80",
        "--iterations", "2",
        "--format", "svg",
        "--output", str(out_svg),
    ])
    assert exit_code == 0
    assert out_svg.exists()
    content = out_svg.read_text(encoding="utf-8")
    assert "<svg" in content
    assert "</svg>" in content


def test_cli_generate_dxf_file(tmp_path):
    """Verify 'generate' command outputs DXF file."""
    out_dxf = tmp_path / "metatron.dxf"
    exit_code = main([
        "generate",
        "metatrons_cube",
        "--radius", "100",
        "--format", "dxf",
        "--output", str(out_dxf),
    ])
    assert exit_code == 0
    assert out_dxf.exists()
    content = out_dxf.read_text(encoding="utf-8")
    assert "SECTION" in content
    assert "EOF" in content


def test_cli_generate_obj_file(tmp_path):
    """Verify 'generate' command outputs OBJ file."""
    out_obj = tmp_path / "merkaba.obj"
    exit_code = main([
        "generate",
        "merkaba_star",
        "--radius", "120",
        "--format", "obj",
        "--output", str(out_obj),
    ])
    assert exit_code == 0
    assert out_obj.exists()
    content = out_obj.read_text(encoding="utf-8")
    assert "v " in content


def test_cli_export_command(tmp_path):
    """Verify 'export' command."""
    out_sri = tmp_path / "sri_yantra.svg"
    exit_code = main([
        "export",
        "sri_yantra",
        "--radius", "140",
        "--theme", "gold",
        "--format", "svg",
        "--output", str(out_sri),
    ])
    assert exit_code == 0
    assert out_sri.exists()


def test_cli_diagnostics(capsys):
    """Verify 'diagnostics' command runs system benchmark."""
    exit_code = main(["diagnostics"])
    assert exit_code == 0
    captured = capsys.readouterr()
    assert "PASS" in captured.out or "Diagnostic" in captured.out
