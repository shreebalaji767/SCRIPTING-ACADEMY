#!/usr/bin/env python3
"""Scripting Academy REAL Windows Lab Agent V20.

This agent never simulates compiler/interpreter results. It executes only
toolchains actually installed on the Windows PC and reports NOT AVAILABLE
when a toolchain is missing.

Default:
  python windows-lab-agent.py

LAN:
  python windows-lab-agent.py --host 0.0.0.0 --port 8765

Use only on a trusted machine/network. Submitted code is executed locally.
"""
import argparse, json, os, secrets, shutil, subprocess, tempfile, time
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

VERSION = "20.0"
MAX_SOURCE = 200_000
MAX_TESTS = 8
MAX_INPUT = 8_000
TIMEOUT = 8

def tool(*names):
    for name in names:
        p = shutil.which(name)
        if p:
            return p
    return ""

def run_process(cmd, cwd, stdin_text=""):
    started = time.time()
    try:
        p = subprocess.run(cmd, cwd=cwd, input=stdin_text, text=True,
                           capture_output=True, timeout=TIMEOUT,
                           creationflags=getattr(subprocess, "CREATE_NO_WINDOW", 0))
        return {"stdout": (p.stdout or "")[-20000:], "stderr": (p.stderr or "")[-20000:],
                "exit_code": p.returncode,
                "duration_ms": round((time.time()-started)*1000)}
    except subprocess.TimeoutExpired as e:
        return {"stdout": (e.stdout or "")[-20000:] if isinstance(e.stdout, str) else "",
                "stderr": "TIMEOUT: process exceeded 8 seconds.", "exit_code": 124,
                "duration_ms": round((time.time()-started)*1000)}
    except Exception as e:
        return {"stdout":"", "stderr":str(e), "exit_code":-1,
                "duration_ms": round((time.time()-started)*1000)}

# Each entry is a REAL Windows executable/toolchain. Availability is detected
# with PATH lookup at request time. No fake result is ever returned.
LANGUAGES = {
    "c": {"name":"C", "tool":("gcc",), "kind":"compile", "ext":".c"},
    "cpp": {"name":"C++", "tool":("g++",), "kind":"compile", "ext":".cpp"},
    "objective-c": {"name":"Objective-C", "tool":("gcc",), "kind":"compile", "ext":".m"},
    "fortran": {"name":"Fortran", "tool":("gfortran",), "kind":"compile", "ext":".f90"},
    "pascal": {"name":"Pascal", "tool":("fpc",), "kind":"compile", "ext":".pas"},
    "cobol": {"name":"COBOL", "tool":("cobc",), "kind":"compile", "ext":".cob"},
    "ada": {"name":"Ada", "tool":("gnatmake", "gnat"), "kind":"ada", "ext":".adb"},
    "d": {"name":"D", "tool":("dmd","gdc","ldc2"), "kind":"compile", "ext":".d"},
    "rust": {"name":"Rust", "tool":("rustc",), "kind":"compile", "ext":".rs"},
    "go": {"name":"Go", "tool":("go",), "kind":"go", "ext":".go"},
    "java": {"name":"Java", "tool":("javac",), "kind":"java", "ext":".java"},
    "csharp": {"name":"C#", "tool":("csc","dotnet"), "kind":"csharp", "ext":".cs"},
    "kotlin": {"name":"Kotlin", "tool":("kotlinc",), "kind":"kotlin", "ext":".kt"},
    "swift": {"name":"Swift", "tool":("swiftc",), "kind":"compile", "ext":".swift"},
    "basic": {"name":"FreeBASIC", "tool":("fbc",), "kind":"compile", "ext":".bas"},
    "assembly-nasm": {"name":"Assembly (NASM)", "tool":("nasm",), "kind":"nasm", "ext":".asm"},
    "assembly-masm": {"name":"Assembly (MASM)", "tool":("ml64","ml"), "kind":"masm", "ext":".asm"},
    "python": {"name":"Python", "tool":("python","py"), "kind":"script", "ext":".py"},
    "javascript": {"name":"JavaScript / Node.js", "tool":("node",), "kind":"script", "ext":".js"},
    "typescript": {"name":"TypeScript", "tool":("tsx","ts-node","node"), "kind":"typescript", "ext":".ts"},
    "perl": {"name":"Perl", "tool":("perl",), "kind":"script", "ext":".pl"},
    "ruby": {"name":"Ruby", "tool":("ruby",), "kind":"script", "ext":".rb"},
    "php": {"name":"PHP", "tool":("php",), "kind":"script", "ext":".php"},
    "tcl": {"name":"Tcl", "tool":("tclsh",), "kind":"script", "ext":".tcl"},
    "lua": {"name":"Lua", "tool":("lua",), "kind":"script", "ext":".lua"},
    "r": {"name":"R", "tool":("Rscript",), "kind":"script", "ext":".r"},
    "haskell": {"name":"Haskell", "tool":("ghc",), "kind":"haskell", "ext":".hs"},
    "ocaml": {"name":"OCaml", "tool":("ocamlc",), "kind":"ocaml", "ext":".ml"},
    "lisp": {"name":"Common Lisp (SBCL)", "tool":("sbcl",), "kind":"lisp", "ext":".lisp"},
    "scheme": {"name":"Scheme (Guile)", "tool":("guile",), "kind":"scheme", "ext":".scm"},
    "erlang": {"name":"Erlang", "tool":("erl",), "kind":"erlang", "ext":".erl"},
    "elixir": {"name":"Elixir", "tool":("elixir",), "kind":"script", "ext":".exs"},
    "prolog": {"name":"Prolog", "tool":("swipl",), "kind":"prolog", "ext":".pl"},
    "bash": {"name":"Bash", "tool":("bash",), "kind":"shell", "ext":".sh"},
    "powershell": {"name":"PowerShell", "tool":("pwsh","powershell"), "kind":"powershell", "ext":".ps1"},
    "batch": {"name":"Windows Batch", "tool":("cmd.exe",), "kind":"batch", "ext":".bat"},
    "vbscript": {"name":"VBScript", "tool":("cscript.exe",), "kind":"vbscript", "ext":".vbs"},
    "jscript": {"name":"Windows JScript", "tool":("cscript.exe",), "kind":"jscript", "ext":".js"},
}

def available_languages():
    out = {}
    for key, spec in LANGUAGES.items():
        p = tool(*spec["tool"])
        out[key] = {"name":spec["name"], "available":bool(p), "executable":p}
    return out

def execute(language, source, tests):
    spec = LANGUAGES.get(language)
    if not spec:
        return {"ok":False, "executed":False, "error":"Unsupported language ID."}
    executable = tool(*spec["tool"])
    if not executable:
        return {"ok":False, "executed":False,
                "error":spec["name"]+" toolchain is NOT AVAILABLE on this Windows PC.",
                "language":language}
    ext = spec["ext"]
    with tempfile.TemporaryDirectory(prefix="scripting_academy_") as d:
        src = os.path.join(d, "main" + ext)
        with open(src, "w", encoding="utf-8") as f: f.write(source)
        exe = os.path.join(d, "academy.exe")

        kind = spec["kind"]
        if kind == "compile":
            extra = []
            if language == "cpp": extra = ["-std=c++17"]
            build = run_process([executable, src, "-O0", "-Wall", "-Wextra", *extra, "-o", exe], d)
            if build["exit_code"] != 0:
                return {"ok":True,"executed":True,"compile":build,"run":None,"tests":[]}
            command=[exe]
        elif kind == "script":
            command=[executable, src]
        elif kind == "ada":
            build=run_process([executable, src], d)
            if build["exit_code"]!=0: return {"ok":True,"executed":True,"compile":build,"run":None,"tests":[]}
            command=[os.path.join(d,"main.exe")]
        elif kind == "go":
            build=run_process([executable,"build","-o",exe,src], d)
            if build["exit_code"]!=0: return {"ok":True,"executed":True,"compile":build,"run":None,"tests":[]}
            command=[exe]
        elif kind == "java":
            build=run_process([executable,src],d)
            if build["exit_code"]!=0: return {"ok":True,"executed":True,"compile":build,"run":None,"tests":[]}
            java=tool("java")
            if not java: return {"ok":False,"executed":False,"error":"javac exists but java runtime was not found."}
            command=[java,"-cp",d,"Main"]
        elif kind == "csharp":
            if os.path.basename(executable).lower() == "dotnet":
                project=os.path.join(d,"Academy.csproj")
                open(project,"w",encoding="utf-8").write('<Project Sdk="Microsoft.NET.Sdk"><PropertyGroup><OutputType>Exe</OutputType><TargetFramework>net8.0</TargetFramework><ImplicitUsings>enable</ImplicitUsings></PropertyGroup></Project>')
                os.rename(src,os.path.join(d,"Program.cs"))
                build=run_process([executable,"build","-nologo","-v","q"],d)
                if build["exit_code"]!=0: return {"ok":True,"executed":True,"compile":build,"run":None,"tests":[]}
                command=[executable,"run","--no-build","-nologo"]
            else:
                build=run_process([executable,src,"/nologo","/out:"+exe],d)
                if build["exit_code"]!=0: return {"ok":True,"executed":True,"compile":build,"run":None,"tests":[]}
                command=[exe]
        elif kind == "kotlin":
            build=run_process([executable,src,"-include-runtime","-d",exe],d)
            if build["exit_code"]!=0: return {"ok":True,"executed":True,"compile":build,"run":None,"tests":[]}
            command=["java","-jar",exe]
        elif kind == "nasm":
            obj=os.path.join(d,"main.obj")
            build=run_process([executable,"-f","win64",src,"-o",obj],d)
            if build["exit_code"]!=0: return {"ok":True,"executed":True,"compile":build,"run":None,"tests":[]}
            return {"ok":True,"executed":True,"compile":build,"run":None,"tests":[],"note":"Assembly assembled successfully; linking/execution depends on the selected object format and linker."}
        elif kind == "masm":
            build=run_process([executable,src,"/nologo","/c","/Fo"+os.path.join(d,"main.obj")],d)
            return {"ok":build["exit_code"]==0,"executed":True,"compile":build,"run":None,"tests":[]}
        elif kind == "haskell":
            build=run_process([executable,src,"-o",exe],d)
            if build["exit_code"]!=0: return {"ok":True,"executed":True,"compile":build,"run":None,"tests":[]}
            command=[exe]
        elif kind == "ocaml":
            build=run_process([executable,"-o",exe,src],d)
            if build["exit_code"]!=0: return {"ok":True,"executed":True,"compile":build,"run":None,"tests":[]}
            command=[exe]
        elif kind == "lisp":
            command=[executable,"--script",src]
        elif kind == "scheme":
            command=[executable,"-s",src]
        elif kind == "erlang":
            command=[executable,"-noshell","-s","main","start","-s","init","stop"]
        elif kind == "prolog":
            command=[executable,"-q","-s",src,"-g","halt"]
        elif kind == "powershell":
            command=[executable,"-NoProfile","-NonInteractive","-ExecutionPolicy","Bypass","-File",src]
        elif kind == "shell":
            command=[executable,src]
        elif kind == "batch":
            command=[executable,"/d","/c",src]
        elif kind in ("vbscript","jscript"):
            command=[executable,"//nologo",src]
        elif kind == "typescript":
            if os.path.basename(executable).lower() == "node":
                return {"ok":False,"executed":False,"error":"TypeScript compiler/runtime not installed. Node.js alone is not a TypeScript compiler."}
            command=[executable,src]
        else:
            return {"ok":False,"executed":False,"error":"No real executor configured for "+spec["name"]}

        if tests:
            results=[]
            for i,t in enumerate(tests):
                inp=str(t.get("input",""))
                if len(inp)>MAX_INPUT: return {"ok":False,"executed":False,"error":"Test input too large."}
                r=run_process(command,d,inp); r["name"]=str(t.get("name","test-"+str(i+1))); results.append(r)
            return {"ok":True,"executed":True,"compile":None,"run":None,"tests":results}
        return {"ok":True,"executed":True,"compile":None,"run":run_process(command,d),"tests":[]}

class Handler(BaseHTTPRequestHandler):
    server_version="ScriptingAcademyAgent/"+VERSION
    token=""
    def send_json(self,status,data):
        body=json.dumps(data).encode()
        self.send_response(status)
        self.send_header("Content-Type","application/json")
        self.send_header("Access-Control-Allow-Origin","*")
        self.send_header("Access-Control-Allow-Headers","Content-Type, X-Academy-Token")
        self.send_header("Access-Control-Allow-Methods","GET, POST, OPTIONS")
        self.send_header("Content-Length",str(len(body))); self.end_headers(); self.wfile.write(body)
    def do_OPTIONS(self): self.send_json(204,{})
    def authorized(self): return secrets.compare_digest(self.headers.get("X-Academy-Token",""),self.token)
    def do_GET(self):
        if self.path not in ("/health","/toolchains"): return self.send_json(404,{"ok":False,"error":"Not found"})
        if not self.authorized(): return self.send_json(401,{"ok":False,"error":"Invalid Lab Token"})
        if self.path=="/health":
            return self.send_json(200,{"ok":True,"version":VERSION,"platform":"Windows","real":True,"fakeExecution":False,"tools":available_languages(),"limits":{"source":MAX_SOURCE,"tests":MAX_TESTS,"input":MAX_INPUT,"timeout_seconds":TIMEOUT}})
        self.send_json(200,{"ok":True,"version":VERSION,"toolchains":available_languages()})
    def do_POST(self):
        if not self.authorized(): return self.send_json(401,{"ok":False,"error":"Invalid Lab Token"})
        try:
            length=int(self.headers.get("Content-Length","0"))
            if length>MAX_SOURCE+20000: return self.send_json(413,{"ok":False,"error":"Request too large"})
            payload=json.loads(self.rfile.read(length).decode())
            if self.path=="/run":
                language=payload.get("language",""); source=payload.get("source",""); tests=payload.get("tests") or []
                if len(source)>MAX_SOURCE: return self.send_json(413,{"ok":False,"error":"Source too large"})
                if not isinstance(tests,list) or len(tests)>MAX_TESTS: return self.send_json(400,{"ok":False,"error":"Too many test cases"})
                result=execute(language,source,tests)
                return self.send_json(200 if result.get("ok") else 400,result)
            if self.path=="/terminal":
                command=str(payload.get("command","")).strip()
                allow=["dir","cd","echo","ver","whoami","ipconfig","ping","nslookup","tasklist","where",
                       "python --version","py --version","node --version","gcc --version","g++ --version",
                       "gfortran --version","fpc -iV","cobc --version","gnatmake --version","rustc --version",
                       "go version","javac -version","java -version","php --version","ruby --version",
                       "perl --version","tclsh --version","lua -v","pwsh --version","powershell -version",
                       "cscript //nologo","nasm -v","ml64 /?"]
                low=command.lower()
                if not command or not any(low==x.lower() or low.startswith(x.lower()+" ") for x in allow):
                    return self.send_json(400,{"ok":False,"error":"Command not allowed by the real learning terminal allowlist."})
                r=run_process(["cmd.exe","/d","/c",command],os.getcwd())
                return self.send_json(200,{"ok":True,"executed":True,"command":command,"result":r})
            return self.send_json(404,{"ok":False,"error":"Not found"})
        except Exception as e:
            return self.send_json(500,{"ok":False,"error":"Agent error: "+str(e)})
    def log_message(self,fmt,*args): print("[agent]",fmt%args)

def main():
    ap=argparse.ArgumentParser(); ap.add_argument("--host",default="127.0.0.1"); ap.add_argument("--port",type=int,default=8765); a=ap.parse_args()
    Handler.token=secrets.token_urlsafe(24)
    print("SCRIPTING ACADEMY REAL WINDOWS LAB AGENT V"+VERSION)
    print("Listening on http://%s:%d"%(a.host,a.port))
    print("LAB TOKEN:",Handler.token)
    print("WARNING: submitted source is executed by REAL local toolchains on this Windows PC.")
    print("Available toolchains are detected automatically; missing toolchains are reported as NOT AVAILABLE.")
    ThreadingHTTPServer((a.host,a.port),Handler).serve_forever()
if __name__=="__main__": main()
