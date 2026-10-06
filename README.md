# Scripting Academy

A free Android learning laboratory for programming, scripting, mathematics, systems, networking and administration.

## 📚 Learn IT / System Administration — IDIOT MODE

A beginner-first course is being built directly in this repository so anyone can learn from zero without assuming prior IT knowledge.

The teaching style is deliberately simple, practical and memorable:

> **No jargon without an explanation. No fake labs. One concept at a time. Real Windows practice where possible.**

### Start here

1. **[Lesson 1 — Computer Basics](lessons/IT-SYSTEM-ADMIN/01-computer-basics.md)**
2. **[Lesson 2 — What Happens When You Double-Click an `.exe`?](lessons/IT-SYSTEM-ADMIN/02-programs-processes-exe.md)**

### Course direction

The planned path goes from:

```text
ZERO KNOWLEDGE
      ↓
Computer Fundamentals
      ↓
Windows Fundamentals
      ↓
CMD / Batch
      ↓
PowerShell
      ↓
Troubleshooting
      ↓
Networking
      ↓
Windows Server
      ↓
DNS / DHCP
      ↓
Active Directory
      ↓
Group Policy
      ↓
Windows Security
      ↓
Automation
      ↓
Advanced Windows / Systems
```

Math is introduced **when the IT topic needs it**, rather than forcing beginners to study months of mathematics first.

## 📱 Scripting Academy V23 — GOOGLE PLAY BUILD

**V23 targets Android 16 / API 36 and builds both a debug APK and a Play release AAB.**

**[🔨 GitHub Actions](https://github.com/shreebalaji767/SCRIPTING-ACADEMY/actions)**

### Current build status
- Android App Bundle: built by GitHub Actions
- Target SDK: 36
- Minimum SDK: 24
- Version: 23.0
- Application ID: `com.shreebalaji.scriptingacademy`
- Optional Play signing: GitHub Actions secrets
- Privacy policy: https://shreebalaji767.github.io/SCRIPTING-ACADEMY/privacy.html
- Play Store package/checklist: [docs/PLAY-STORE.md](docs/PLAY-STORE.md)

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

The Windows lab detects the actual tools installed on that computer and can execute supported languages through their real compilers/interpreters. If a required runtime is missing, the app reports **NOT AVAILABLE** rather than inventing an execution result.

### Windows legacy learning path
- Batch / CMD
- VBScript / Windows Script Host
- Windows JScript
- WSF
- HTA
- WMI
- Registry automation
- Windows automation projects

### Truth rule

Scripting Academy does **not** turn an analysis into a fake execution result.

If something cannot execute, the app says:

`NOT EXECUTED`

and explains why.

## ⚠️ Windows agent security

The Lab Agent executes submitted source code on the Windows PC. Run it only on a trusted machine/LAN and never expose it directly to the public Internet. Keep the generated Lab Token private.

## Google Play publishing

The repository supports a private Play upload keystore through GitHub Actions secrets. The keystore itself is never committed to the repository.

Required repository secrets:

- `PLAY_STORE_KEYSTORE_BASE64`
- `PLAY_STORE_KEYSTORE_PASSWORD`
- `PLAY_STORE_KEY_ALIAS`
- `PLAY_STORE_KEY_PASSWORD`

The dedicated **Publish Signed Scripting Academy AAB** workflow refuses to publish when these secrets are missing and verifies the resulting AAB with `jarsigner`.

See **[Google Play Store Package](docs/PLAY-STORE.md)** for the store listing copy and release checklist.

## No Android Studio required

GitHub Actions builds the APK and AAB automatically.
