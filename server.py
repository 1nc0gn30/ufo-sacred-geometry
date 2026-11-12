#!/usr/bin/env python3
"""
UFO Sacred Geometry Studio — Sovereign Server Launcher.
Parametric Sacred Geometry & Agro-Glyph CAD Studio on port 8083.
"""

from __future__ import annotations

import argparse
import os
import sys
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
SRC_DIR = BASE_DIR / "src"
if str(SRC_DIR) not in sys.path:
    sys.path.insert(0, str(SRC_DIR))

from ufo_sacred_geometry.ui_server import start_ui_server

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="UFO Sacred Geometry Studio Server")
    parser.add_argument("--host", default="127.0.0.1", help="Host interface (default: 127.0.0.1)")
    parser.add_argument("--port", "-p", type=int, default=8083, help="Port to listen on (default: 8083)")
    args = parser.parse_args()

    httpd = start_ui_server(host=args.host, port=args.port, open_browser=False)
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\nStopping Sacred Geometry Studio...")
        httpd.server_close()
