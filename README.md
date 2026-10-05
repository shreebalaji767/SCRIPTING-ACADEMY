# Scripting Academy

A free Android learning laboratory for programming, scripting, mathematics, systems, networking and administration.

## 📱 Scripting Academy V18 — GOOGLE PLAY READY REAL LAB

**V18 is built as an Android App Bundle (AAB) for Google Play and also produces a debug APK.**

> The Play release is published automatically after the Play upload signing secrets are configured.

**[🔨 GitHub Actions](https://github.com/shreebalaji767/SCRIPTING-ACADEMY/actions)**

## What is actually real?

### Android
- JavaScript code executes in the Android WebView.
- Lessons, quizzes, notes, progress, projects and workspace data persist locally.
- The app does not claim that Android is Windows.

### Windows REAL LAB
Run `windows-lab-agent.py` on a Windows PC:

```text
python windows-lab-agent.py --host 0.0.0.0
```

The agent prints a private Lab Token. Put the Windows PC LAN IP and token into **REAL WORKBENCH**.

The app can then genuinely execute:

- C → GCC
- C++ → G++
- Python
- JavaScript → Node.js
- approved Windows learning-terminal commands

Compilation/runtime stdout, stderr, exit codes and timeouts come from the real Windows process.

### Truth rule

Scripting Academy V17 does **not** turn an analysis into a fake execution result.

If something cannot execute, the app says:

`NOT EXECUTED`

and explains why.

## ⚠️ Windows agent security

The Lab Agent executes submitted source code on the Windows PC. Run it only on a trusted machine/LAN and never expose it directly to the public Internet. Keep the generated Lab Token private.

## Google Play publishing

Google Play requires new apps to publish using an Android App Bundle. V18 targets Android 16 / API 36. The GitHub Actions pipeline supports a private Play upload keystore through GitHub Actions secrets; the keystore is never committed to the repository.

Required repository secrets:

- `PLAY_STORE_KEYSTORE_BASE64`
- `PLAY_STORE_KEYSTORE_PASSWORD`
- `PLAY_STORE_KEY_ALIAS`
- `PLAY_STORE_KEY_PASSWORD`

Privacy policy: https://shreebalaji767.github.io/SCRIPTING-ACADEMY/privacy.html

## No Android Studio required

GitHub Actions builds the APK automatically.
