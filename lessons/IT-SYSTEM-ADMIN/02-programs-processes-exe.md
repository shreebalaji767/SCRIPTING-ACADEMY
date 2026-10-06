# IT / SYSTEM ADMIN — LESSON 2

## 🤡 WHAT HAPPENS WHEN YOU DOUBLE-CLICK AN `.exe`?

> We are going to follow the computer circus one step at a time.

## 1. An `.exe` is an executable program

Examples:

```text
notepad.exe
calc.exe
chrome.exe
```

An executable contains machine-readable instructions and supporting data that Windows can use to start a program.

Think:

> `.exe` = a box containing instructions for the computer.

## 2. The program is stored on storage

For example, Windows may have a program at a path such as:

```text
C:\\Windows\\System32\\notepad.exe
```

The executable is stored on persistent storage such as an SSD.

Remember:

> SSD = warehouse.

## 3. Windows loads what the program needs

When you start a program, Windows loads the required program code and data into memory and prepares the process to run.

Simplified picture:

```text
SSD / storage
     |
     | load
     v
RAM / memory
```

## 4. Program vs process

This is one of the most important beginner distinctions.

### Program

A **program** is the stored instructions and files that make up an application.

Example:

```text
notepad.exe
```

### Process

A **process** is a running instance managed by the operating system.

Simplified:

```text
notepad.exe
    |
    | start
    v
Notepad process
```

### Stupidly memorable analogy

A recipe sitting in a cupboard = **program**.

A cook actually using that recipe = **process**.

The recipe is not cooking anything by itself.

## 5. The CPU executes instructions

The CPU executes instructions belonging to running processes.

Think:

```text
PROCESS
   |
   v
instructions
   |
   v
CPU executes them
```

The CPU does this incredibly quickly.

## 6. Windows is the manager

Windows coordinates resources and provides the environment in which applications run.

Simplified:

```text
                 WINDOWS
                   |
        +----------+----------+
        |          |          |
       CPU        RAM       STORAGE
        ^
        |
      PROCESS
        |
     Notepad
```

Windows also manages many other things, including users, permissions, devices, networking and services.

## 7. Real Windows lab

### Lab A — Start Notepad

Press:

```text
Win + R
```

Type:

```text
notepad
```

Press Enter.

### Lab B — Find the process

Press:

```text
Ctrl + Shift + Esc
```

Look under **Processes** for Notepad.

You are now looking at a running process.

### Lab C — End the process

Select Notepad in Task Manager and choose **End task**.

Notepad should close.

You have just performed a tiny piece of system administration: you instructed Windows to terminate a running process.

## 8. Why this matters to an administrator

When a user says:

> “The application is frozen!”

An administrator starts asking questions:

- Is the process still running?
- Is CPU usage unusually high?
- Is memory exhausted?
- Is disk activity stuck?
- Is another process blocking it?
- Are there relevant Windows events or logs?

That is troubleshooting.

## Brain card

```text
.EXE
  |
  v
PROGRAM
  |
  | start
  v
PROCESS
  |
  v
CPU executes instructions

SSD = persistent storage
RAM = working memory
Windows = operating-system manager
```

## Check yourself

1. Is `notepad.exe` a stored program or a running process?
2. What is a process?
3. Where is a program stored permanently?
4. What does RAM provide?
5. Who executes instructions?
6. What does Windows manage?
7. What does Task Manager show?
8. What does **End task** do?
9. Which is the warehouse: SSD or RAM?
10. Which is the worker: CPU or SSD?

## Important note

This lesson intentionally uses a simplified model. Real Windows process startup involves executable formats, loaders, virtual memory, DLLs, handles, security tokens and many other mechanisms. Those details come later.
