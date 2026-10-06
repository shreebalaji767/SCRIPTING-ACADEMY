# LESSON 5 — BITS, BYTES, BINARY & HEXADECIMAL

## 🤡 IDIOT MODE

The computer is extremely good at tiny values like `0` and `1`. Those bits eventually become your browser, operating system and programs.

## 1. Bit

A bit is one binary digit: `0` or `1`.

## 2. Byte

```text
1 byte = 8 bits
```

With 8 bits there are `2^8 = 256` possible combinations. An unsigned 8-bit value commonly ranges from 0 through 255.

## 3. Binary

Binary is base 2. The place values are powers of 2:

```text
128 64 32 16 8 4 2 1
```

Example:

```text
101₂ = 1×4 + 0×2 + 1×1 = 5
1101₂ = 13₁₀
```

## 4. Hexadecimal

Hexadecimal is base 16:

```text
0 1 2 3 4 5 6 7 8 9 A B C D E F
```

`A=10`, `B=11`, `C=12`, `D=13`, `E=14`, `F=15`.

One hex digit represents 4 bits. Therefore two hex digits represent one byte.

```text
0xFF = 255
0x10 = 16
0x20 = 32
0x25 = 37
0x2F = 47
```

## 5. Why hex matters

Programmers often use hexadecimal when reading memory, machine data and addresses.

```text
0x7FFDF123
```

`0x` is a common marker meaning the number is written in hexadecimal.

## 6. Bits versus bytes

```text
Mb = megabits
MB = megabytes
8 bits = 1 byte
```

This distinction matters when reading network speeds and storage measurements.

## 7. REAL CMD LAB

```bat
set /a 2+3
set /a 2*8
set /a 128+64+32
set /a 0xFF
set /a 0x10
set /a 0x20
set /a 0x40
set /a 0x80
mkdir binary_lab
cd binary_lab
echo 0 = 00000000 > binary.txt
echo 1 = 00000001 >> binary.txt
echo 2 = 00000010 >> binary.txt
echo 3 = 00000011 >> binary.txt
echo 4 = 00000100 >> binary.txt
echo 5 = 00000101 >> binary.txt
echo 6 = 00000110 >> binary.txt
echo 7 = 00000111 >> binary.txt
echo 8 = 00001000 >> binary.txt
type binary.txt
```

## Challenge

```text
1010₂ = ?
1111₂ = ?
10000₂ = ?
0x0A = ?
0x10 = ?
0xFF = ?
```

Answers: `10`, `15`, `16`, `10`, `16`, `255`.

## Brain card

```text
bit  = 0 or 1
byte = 8 bits
binary = base 2
hex = base 16
1 hex digit = 4 bits
2 hex digits = 1 byte
```

Next: **RAM, memory addresses, variables and pointers.**