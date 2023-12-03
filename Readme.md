# LEG Interpreter from the Game "Turing Complete"

Interpreter for the LEG architecture

## Command

32-bit commands with 8 bit addresses
```
<Opcode> <Argument 1> <Argument 2> <Destination>
```

## Registers

```
reg0
reg1
reg2
reg3
reg4
reg5
input
output
pc
stack
```

## Opcodes

```
# logic and math
add
or
not
xor

# jumps
ife
ifn
ifl
ifle
ifg
ifge

# RAM
ld
sv

# function calls
call
ret
```

## Assembler Helpers

```
label
```