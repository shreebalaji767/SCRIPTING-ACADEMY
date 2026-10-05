#!/usr/bin/env python3
"""
Scripting Academy Windows Lab Agent V17
REAL local toolchain bridge for the Android app.

Run:
  python windows-lab-agent.py
  python windows-lab-agent.py --host 0.0.0.0 --port 8765

The token is printed at startup. Keep the token private and use this only on a trusted LAN.
"""
import argparse, json, os, secrets, shutil, subprocess, tempfile, time
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

VERSION = "17.0"
MAX_SOURCE = 200_000
MAX_TESTS = 8
MAX_INPUT = 8_000
TIMEOUT = 8

def tool(name):
    return shutil.which(name) or ""

def run_process(cmd, cwd, stdin_text=""):
    started = time.time()
    try:
        p = subprocess.run(
            cmd, cwd=cwd, input=stdin_text, text=True,
            capture_output=True, timeout=TIMEOUT,
            creationflags=getattr(subprocess, "CREATE_NO_WINDOW", 0)
        )
        return {
            "stdout": p.stdout[-20000:],
            "stderr": p.stderr[-20000:],
            "exit_code": p.returncode,
            "duration_ms": round((time.time()-started)*1000)
        }
    except subprocess.TimeoutExpired as e:
        return {
            "stdout": (e.stdout or "")[-20000:] if isinstance(e.stdout, str) else "",
            "stderr": "TIMEOUT: process exceeded 8 seconds.",
            "exit_code": 124,
            "duration_ms": round((time.time()-started)*1000)
        }

def execute(language, source, tests):
    ext = {"c": ".c", "cpp": ".cpp", "python": ".py", "javascript": ".js"}.get(language)
    if not ext:
        return {"ok": False, "error": "Unsupported language."}
    with tempfile.TemporaryDirectory(prefix="scripting_academy_") as d:
        src = os.path.join(d, "main" + ext)
        with open(src, "w", encoding="utf-8") as f:
            f.write(source)

        if language == "c":
            compiler = tool("gcc")
            if not compiler: return {"ok": False, "error": "GCC not found in PATH."}
            exe = os.path.join(d, "academy.exe")
            build = run_process([compiler, src, "-O0", "-Wall", "-Wextra", "-o", exe], d)
            if build["exit_code"] != 0: return {"ok": True, "compile": build, "run": None, "tests": []}
            command = [exe]
        elif language == "cpp":
            compiler = tool("g++")
            if not compiler: return {"ok": False, "error": "G++ not found in PATH."}
            exe = os.path.join(d, "academy.exe")
            build = run_process([compiler, src, "-O0", "-Wall", "-Wextra", "-std=c++17", "-o", exe], d)
            if build["exit_code"] != 0: return {"ok": True, "compile": build, "run": None, "tests": []}
            command = [exe]
        elif language == "python":
            py = tool("python") or tool("py")
            if not py: return {"ok": False, "error": "Python not found in PATH."}
            command = [py, src]
        else:
            node = tool("node")
            if not node: return {"ok": False, "error": "Node.js not found in PATH."}
            command = [node, src]

        if tests:
            results = []
            for i, t in enumerate(tests):
                inp = str(t.get("input", ""))
                if len(inp) > MAX_INPUT: return {"ok": False, "error": "Test input too large."}
                r = run_process(command, d, inp)
                r["name"] = str(t.get("name", "test-" + str(i+1)))
                results.append(r)
            return {"ok": True, "compile": None, "run": None, "tests": results}

        return {"ok": True, "compile": None, "run": run_process(command, d), "tests": []}

class Handler(BaseHTTPRequestHandler):
    server_version = "ScriptingAcademyAgent/" + VERSION
    token = ""

    def send_json(self, status, data):
        body = json.dumps(data).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Headers", "Content-Type, X-Academy-Token")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def do_OPTIONS(self):
        self.send_json(204, {})

    def authorized(self):
        return secrets.compare_digest(self.headers.get("X-Academy-Token", ""), self.token)

    def do_GET(self):
        if self.path != "/health":
            return self.send_json(404, {"ok": False, "error": "Not found"})
        if not self.authorized():
            return self.send_json(401, {"ok": False, "error": "Invalid Lab Token"})
        self.send_json(200, {
            "ok": True, "version": VERSION,
            "platform": "Windows",
            "real": True,
            "tools": {
                "gcc": bool(tool("gcc")), "g++": bool(tool("g++")),
                "python": bool(tool("python") or tool("py")),
                "node": bool(tool("node"))
            },
            "limits": {"source": MAX_SOURCE, "tests": MAX_TESTS, "input": MAX_INPUT, "timeout_seconds": TIMEOUT}
        })

    def do_POST(self):
        if self.path == "/terminal":
            if not self.authorized(): return self.send_json(401, {"ok": False, "error": "Invalid Lab Token"})
            try:
                length = int(self.headers.get("Content-Length", "0"))
                payload = json.loads(self.rfile.read(length).decode("utf-8"))
                command = str(payload.get("command", "")).strip()
                allow = ["dir", "cd", "echo", "ver", "whoami", "ipconfig", "ping", "nslookup", "tasklist", "where", "python --version", "py --version", "node --version", "gcc --version", "g++ --version"]
                base = command.lower().split()[0] if command else ""
                if not command or not any(command.lower() == x or command.lower().startswith(x + " ") for x in allow):
                    return self.send_json(400, {"ok": False, "error": "Command not allowed by the learning terminal allowlist."})
                r = run_process(["cmd.exe", "/d", "/c", command], os.getcwd())
                return self.send_json(200, {"ok": True, "command": command, "result": r})
            except Exception as e:
                return self.send_json(500, {"ok": False, "error": "Terminal error: " + str(e)})
        if self.path != "/run":
            return self.send_json(404, {"ok": False, "error": "Not found"})
        if not self.authorized():
            return self.send_json(401, {"ok": False, "error": "Invalid Lab Token"})
        try:
            length = int(self.headers.get("Content-Length", "0"))
            if length > MAX_SOURCE + 20000:
                return self.send_json(413, {"ok": False, "error": "Request too large"})
            payload = json.loads(self.rfile.read(length).decode("utf-8"))
            language = payload.get("language", "")
            source = payload.get("source", "")
            tests = payload.get("tests") or []
            if len(source) > MAX_SOURCE: return self.send_json(413, {"ok": False, "error": "Source too large"})
            if not isinstance(tests, list) or len(tests) > MAX_TESTS:
                return self.send_json(400, {"ok": False, "error": "Too many test cases"})
            result = execute(language, source, tests)
            self.send_json(200 if result.get("ok") else 400, result)
        except Exception as e:
            self.send_json(500, {"ok": False, "error": "Agent error: " + str(e)})

    def log_message(self, fmt, *args):
        print("[agent]", fmt % args)

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--host", default="127.0.0.1")
    ap.add_argument("--port", type=int, default=8765)
    args = ap.parse_args()
    Handler.token = secrets.token_urlsafe(24)
    print("SCRIPTING ACADEMY REAL WINDOWS LAB AGENT V" + VERSION)
    print("Listening on http://%s:%d" % (args.host, args.port))
    print("LAB TOKEN:", Handler.token)
    print("WARNING: this agent executes submitted code on this Windows PC.")
    ThreadingHTTPServer((args.host, args.port), Handler).serve_forever()

if __name__ == "__main__":
    main()
