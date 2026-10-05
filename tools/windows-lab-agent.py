#!/usr/bin/env python3
"""
Scripting Academy REAL LAB V10 — Windows companion agent.

Run on the Windows PC:
    py tools/windows-lab-agent.py

It listens on localhost by default and can be bound to a LAN interface explicitly. It is intentionally small and transparent:
the Academy sends source code, this agent invokes the selected local toolchain,
captures stdout/stderr, and returns the real exit code.

Supported: C, C++, Python, JavaScript/Node.js.
PowerShell/CMD are intentionally not exposed as arbitrary HTTP execution.
"""

from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
import json
import os
import shutil
import subprocess
import tempfile
import time
import secrets
import argparse

HOST = "127.0.0.1"
PORT = 8765
TOKEN = secrets.token_urlsafe(18)
VERSION = "10.0"
MAX_SOURCE = 200_000
TIMEOUT = 8

TOOLS = {
    "c": ["gcc"],
    "cpp": ["g++"],
    "python": ["python"],
    "javascript": ["node"],
}

class Handler(BaseHTTPRequestHandler):
    def send_json(self, status, payload):
        data = json.dumps(payload, ensure_ascii=False).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(data)))
        self.send_header("Access-Control-Allow-Origin", "*")
        self.end_headers()
        self.wfile.write(data)

    def do_OPTIONS(self):
        self.send_response(204)
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Headers", "Content-Type, X-Academy-Token")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
        self.end_headers()

    def authorized(self):
        return self.headers.get("X-Academy-Token", "") == TOKEN

    def do_GET(self):
        if self.path == "/health":
            if not self.authorized():
                self.send_json(401, {"ok": False, "error": "invalid lab token"})
                return
            self.send_json(200, {
                "ok": True,
                "name": "Scripting Academy REAL LAB",
                "version": VERSION,
                "platform": "Windows",
                "host": HOST,
                "port": PORT,
                "tools": {k: {"command": v[0], "path": shutil.which(v[0]), "available": bool(shutil.which(v[0]))} for k, v in TOOLS.items()},
                "limits": {"max_source_bytes": MAX_SOURCE, "timeout_seconds": TIMEOUT},
            })
            return
        self.send_json(404, {"ok": False, "error": "Use /health or POST /run"})

    def do_POST(self):
        if not self.authorized():
            self.send_json(401, {"ok": False, "error": "invalid lab token"})
            return
        if self.path != "/run":
            self.send_json(404, {"ok": False, "error": "Unknown endpoint"})
            return

        try:
            length = int(self.headers.get("Content-Length", "0"))
            if length <= 0 or length > MAX_SOURCE:
                raise ValueError("source is empty or too large")
            body = json.loads(self.rfile.read(length).decode("utf-8"))
            language = str(body.get("language", "")).lower()
            source = str(body.get("source", ""))
            if language not in TOOLS:
                raise ValueError("unsupported language")
            if not source.strip():
                raise ValueError("source is empty")
        except Exception as exc:
            self.send_json(400, {"ok": False, "error": str(exc)})
            return

        compiler = shutil.which(TOOLS[language][0])
        if not compiler:
            self.send_json(503, {
                "ok": False,
                "error": f"{TOOLS[language][0]} was not found in PATH"
            })
            return

        with tempfile.TemporaryDirectory(prefix="scripting-academy-") as td:
            root = Path(td)
            if language == "c":
                src, exe = root / "main.c", root / "main.exe"
                src.write_text(source, encoding="utf-8")
                command = [compiler, str(src), "-O0", "-Wall", "-Wextra", "-o", str(exe)]
                result = self.run(command, root)
                if result["exit_code"] == 0:
                    result["compile"] = True
                    result["run"] = self.run([str(exe)], root)
            elif language == "cpp":
                src, exe = root / "main.cpp", root / "main.exe"
                src.write_text(source, encoding="utf-8")
                command = [compiler, str(src), "-std=c++17", "-O0", "-Wall", "-Wextra", "-o", str(exe)]
                result = self.run(command, root)
                if result["exit_code"] == 0:
                    result["compile"] = True
                    result["run"] = self.run([str(exe)], root)
            elif language == "python":
                src = root / "main.py"
                src.write_text(source, encoding="utf-8")
                result = self.run([compiler, str(src)], root)
            else:
                src = root / "main.js"
                src.write_text(source, encoding="utf-8")
                result = self.run([compiler, str(src)], root)

        self.send_json(200, {"ok": True, "language": language, "result": result})

    @staticmethod
    def run(command, cwd):
        started = time.time()
        try:
            p = subprocess.run(
                command, cwd=cwd, capture_output=True, text=True,
                timeout=TIMEOUT, shell=False
            )
            return {
                "command": command,
                "exit_code": p.returncode,
                "stdout": p.stdout[-12000:],
                "stderr": p.stderr[-12000:],
                "duration_ms": round((time.time() - started) * 1000),
            }
        except subprocess.TimeoutExpired as exc:
            return {
                "command": command,
                "exit_code": 124,
                "stdout": (exc.stdout or "")[-12000:] if isinstance(exc.stdout, str) else "",
                "stderr": "TIMEOUT: process exceeded 8 seconds",
                "duration_ms": round((time.time() - started) * 1000),
            }

if __name__ == "__main__":
    print(f"Scripting Academy REAL LAB V10 listening on http://{HOST}:{PORT}")
    print(f"LAB TOKEN: {TOKEN}")
    print("Use the LAN address only on a trusted network. Anyone with the token can submit code for execution.")
    print("Press Ctrl+C to stop.")
    server = ThreadingHTTPServer((HOST, PORT), Handler)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nStopping REAL LAB agent.")
    finally:
        server.server_close()
