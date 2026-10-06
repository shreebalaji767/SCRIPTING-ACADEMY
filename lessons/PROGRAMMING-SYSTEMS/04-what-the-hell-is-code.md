# LESSON 4 — WHAT THE HELL IS CODE?

## 🤡 IDIOT MODE

Humans write instructions. Computers execute instructions. Computers are terrible at vague instructions, so we use programming languages.

## 1. Source code

Source code is human-readable text written in a programming language.

```c
#include <stdio.h>

int main(void)
{
    printf("Hello, computer!\n");
    return 0;
}
```

That is C source code.

## 2. The CPU does not normally understand C

A CPU executes instructions defined by its instruction set architecture (ISA). Examples include x86-64, ARM64 and RISC-V.

```text
SOURCE CODE
     ↓
  COMPILER
     ↓
MACHINE CODE
     ↓
    CPU
```

A real toolchain may produce object files, libraries and intermediate artifacts too.

## 3. High-level vs low-level

```text
More human-friendly
       ↑
Python / JavaScript
       ↑
C
       ↑
Assembly
       ↑
Machine instructions
       ↓
CPU
```

This is about abstraction, not good versus bad.

## 4. Abstraction

Abstraction hides complicated details behind something easier to use. A car pedal is an everyday example: you use the pedal without manually controlling every combustion event.

## 5. First C lab

Check for GCC:

```bat
gcc --version
```

If GCC is installed:

```bat
mkdir lesson4
cd lesson4
notepad hello.c
```

Paste:

```c
#include <stdio.h>

int main(void)
{
    printf("Hello, computer!\n");
    return 0;
}
```

Compile and run:

```bat
gcc hello.c -o hello.exe
hello.exe
```

If GCC is missing, the correct answer is **NOT AVAILABLE**. Never invent a compiler result.

## 6. Program vs process

```text
hello.exe = program stored on disk
running hello.exe = process
```

## 7. Add maths

```c
#include <stdio.h>

int main(void)
{
    int a = 10;
    int b = 20;
    int result = a + b;

    printf("Result = %d\n", result);
    return 0;
}
```

You are already combining programming and mathematics: variables, numbers, addition and assignment.

## Big chain

```text
SOURCE CODE
     ↓
   COMPILER
     ↓
EXECUTABLE PROGRAM
     ↓
   WINDOWS
     ↓
   PROCESS
     ↓
    CPU
     ↓
MACHINE INSTRUCTIONS
```

## Check yourself

1. What is source code?
2. What does a compiler do?
3. Does the CPU directly understand C source code?
4. What is an ISA?
5. What is abstraction?
6. What is the difference between a program and a process?
7. Why is C useful for systems programming?

Next: **bits, bytes, binary and hexadecimal.**