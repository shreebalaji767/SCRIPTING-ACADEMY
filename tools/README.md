# Scripting Academy — REAL LAB V8

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

It listens on:

`http://127.0.0.1:8765`

The Android app's **REAL LAB V8 → Connect Windows Lab Agent** panel can test the connection.

### Supported real toolchains

- C → GCC
- C++ → G++
- Python → Python
- JavaScript → Node.js

The agent captures:

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
