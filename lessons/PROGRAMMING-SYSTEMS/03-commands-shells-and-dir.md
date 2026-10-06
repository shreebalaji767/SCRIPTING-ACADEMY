# LESSON 3 — COMMANDS, SHELLS & WHAT ACTUALLY HAPPENS WHEN YOU TYPE `DIR`

## 🤡 IDIOT MODE

A command is an instruction given to a command interpreter, commonly called a shell.

> **CMD is a program. CMD is NOT Windows.**

Windows is the operating system. CMD runs inside Windows.

## 1. What is a shell?

A shell gives you a way to communicate with the operating system.

Common examples: CMD, PowerShell, Bash, Zsh and Fish.

```text
YOU
 ↓
COMMAND
 ↓
SHELL
 ↓
OPERATING SYSTEM
 ↓
KERNEL
 ↓
HARDWARE
```

## 2. What happens when you type `dir`?

Simplified:

1. Keyboard input reaches CMD.
2. CMD interprets `dir`.
3. CMD/Windows obtain directory information.
4. The result is formatted.
5. Text appears on the screen.

The real implementation has more layers. This model is for learning the big picture.

## 3. Built-in vs external commands

CMD built-ins include:

```bat
cd
dir
echo
set
if
for
```

External programs include:

```text
notepad.exe
ping.exe
ipconfig.exe
```

Try:

```bat
where notepad
where ping
where dir
```

`dir` is a CMD built-in, so it does not behave like an external `.exe` command.

## 4. PATH

`PATH` is an environment variable containing directories Windows can search for executable programs.

```bat
echo %PATH%
```

## 5. Environment variables

```bat
echo %USERNAME%
echo %COMPUTERNAME%
echo %USERPROFILE%
set BANANA=yellow
echo %BANANA%
```

Congratulations. Windows now knows about a banana.

## 6. REAL LAB

```bat
mkdir lesson3
cd lesson3
echo Hello > hello.txt
echo Banana > banana.txt
echo Potato > potato.txt
echo Computer > computer.txt
dir
type hello.txt
type banana.txt
type computer.txt
```

Explore:

```bat
dir /?
dir /w
dir /p
dir /b
```

## Brain card

```text
CMD = shell/program
Windows = operating system
Kernel = privileged core of the OS
Command = instruction interpreted by a shell
EXE = executable program
PATH = executable search locations
Environment variable = named value
```

## Check yourself

1. Is CMD the operating system?
2. What is a shell?
3. Is `dir` necessarily an EXE file?
4. What does PATH do?
5. What is an environment variable?
6. Name two CMD built-ins.
7. Name two external Windows commands.

Next: **what the hell is code?**