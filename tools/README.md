# Scripting Academy — REAL LAB V12

Scripting Academy is an offline-first learning app. V8 changes the Code Lab philosophy:

> **Never claim that code executed when it was only simulated.**

## Android

Android WebView JavaScript is genuinely executed by the WebView engine.

C/C++ support through the Android NDK is a **native app build-time capability**. The NDK does not magically turn an Android WebView into a Windows GCC/CMD/PowerShell machine, so the app explicitly labels those environments as analysis-only unless a real external lab is connected.

## Windows REAL LAB

The repository now includes:

`tools/windows-lab-agent.py`

Run on a Windows PC with the required tools installed:

```powershell
py tools/windows-lab-agent.py
```

It listens on `127.0.0.1:8765` by default. For Android/LAN access, start it explicitly with `py tools\\windows-lab-agent.py --host 0.0.0.0`. The agent prints a random **Lab Token** at startup; enter that token in the app. Keep the token private.

The Android app's **REAL LAB V10 → Connect Windows Lab Agent** panel can test the connection.

### Supported real toolchains

- C → GCC
- C++ → G++
- Python → Python
- JavaScript → Node.js

The V10 workbench also records an on-device execution history and shows an **Execution Truth** badge (`REAL`, `CONNECTED`, `NOT EXECUTED`, etc.).\n\nThe agent captures:

- real compiler output
- real runtime output
- real stderr
- real exit codes
- execution time

It does **not** expose arbitrary CMD or PowerShell HTTP execution.

## Build APK without Android Studio

Use the existing GitHub Actions workflow:

**Actions → Build APK → Artifacts**

## Philosophy

```
TEACH
  ↓
WRITE
  ↓
RUN FOR REAL
  ↓
BREAK
  ↓
READ THE REAL ERROR
  ↓
FIX
  ↓
EXPLAIN
```

The Academy is allowed to say:

**NOT EXECUTED**

That is a feature, not a failure.


## V12 Project Workspace

V12 adds a local multi-file Project Workspace with file management, templates, local save/load and JSON export. The selected file can be sent through the existing authenticated Windows Lab Agent for real execution. Editing and saving are explicitly NOT EXECUTED.
