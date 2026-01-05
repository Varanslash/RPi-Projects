+--- INTRO ---+
welcome to cobalt, a version of asssembly made by my in an attempt to challenge myself. i have no idea if there's any real use case for this, but if there is then
have at it!

+--- SYNTAX ---+
This section details the many, many operands cobalt operates on.

+--- arithmetic ---+
add [register], [value] - adds the value to the register. the register must be stored in the integer division of memory.
sub [register], [value] - subtracts the value from the register. the register must be stored in the integer division of memory.
mul [register], [value] - multiplies the value by the register. the register must be stored in the integer division of memory.
div [register], [value] - divides the register by the value. the register must be stored in the integer division of memory.
mod [register], [value] - divides the register by the value and stores the remainder in the register.
mov [reg1], [reg2] - makes reg2 equal to reg1. both registers must be in the integer division of memory.
adt [reg1], [reg2] - adds the value of reg2 to reg1.
sut [reg1], [reg2] - subtracts the value of reg2 from reg1.
mut [reg1], [reg2] - multiplies reg1 by reg2.
dit [reg1], [reg2] - divides reg1 by reg2.
mot [reg1], [reg2] - gets the remainder of reg1 divided by reg2.
inc [reg] - increments the value of reg by 1.
dec [reg] - decrements the value of reg by 1.
shl [reg1], [dest] - shifts reg1 one bit to the left and stores the result in dest.
shr [reg1], [dest] - shifts reg1 one bit to the right and stores the result in dest.
rhl [reg] - shifts reg one bit to the left and stores the result in reg.
rhr [reg] - shifts reg one bit to the right and stores the result in reg.

+--- logic ---+
xor [reg1], [reg2], [dest] - does an xor bitwise operation with reg1 and reg2, then stores the resulting value in dest.
or [reg1], [reg2], [dest] - does an or bitwise operation with reg1 and reg2, then stores the resulting value in dest.
not [reg1], [dest] - flips all bits in reg1, then stores the resulting value in dest.
and [reg1], [reg2], [dest] - does an and bitwise operation with reg1 and reg2, then stores the resulting value in dest.

+--- functions ---+
prt [reg] - prints the string stored in reg. the register must be in the string division of memory.
prn [reg] - prints the value stored in an integer division register.
sar [name] - makes a slot for a routine.
sro [name], [instruction] - adds one command to any routine slot.
run [name] - executes the routine slot.
lop [name] - makes a slot for a loop.
lro [name], [instruction] - adds one command to any loop slot.
lup [name], [value] - executes the loop value times.

+--- memory ---+
str [reg] - makes a string division register.
reg [reg] - makes an integer division register.
psh [reg], [value] - pushes a register value to a specific stack index.
pop [value] - removes the value at a specific stack index.
tru - sets general system flag to true.
fal - sets general system flag to false.

+--- conditionals ---+
fif [routine1], [routine2] - executes routine1 if system flag is true, otherwise executes routine2.
rif [routine], [loop], [value] - executes routine if system flag is true, otherwise runs loop.
lif [loop1], [value1], [loop2], [value2] - runs loop1 if system flag is true, otherwise runs loop2.
cmp [reg1], [reg2] - sets system flag to true if reg1 equals reg2.
smp [reg1], [reg2] - sets system flag to true if reg1 does not equal reg2.
fmp [reg1], [reg2] - sets system flag to true if reg1 is less than reg2.
gmp [reg1], [reg2] - sets system flag to true if reg1 is greater than reg2.
cmv [reg], [value] - sets system flag to true if reg equals value.
smv [reg], [value] - sets system flag to true if reg does not equal value.
fmv [reg], [value] - sets system flag to true if reg is less than value.
gmv [reg], [value] - sets system flag to true if reg is greater than value.

+--- misc ---+
lod [filename.extension] - loads a file containing a cobalt script.
; - used to create notes. can't be put on the same line as a command.
brk [value], [routine] - breaks a loop if loop_count is less than value and runs routine.
rst - resets loop execution flags.
frk - stops executing the current routine or loop.
csh - exits the cobalt interpreter.

+--- PI PICO BOARD ---+
This section details the opcodes used for the Raspberry Pi Pico version of Cobalt Assembly.

+--- hardware ---+
pim [pin num], [in, out] - switches the pin mode between in and out.
pow [pin num], [high, low] - switches the pin volt between high and low.
rdi [pin num], [reg] - read a pin into a register.
wri [pin num], [reg] - write a register into a pin.

+--- interrupts ---+
int [rise, fall], [pin num], [rout1], [rout2] - sets an interrupt, then executes rout1 if rise, else executes rout2.
pif [pin num], [routine] - triggers routine if the pin is already high, sets an interrupt

+--- misc ---+
srt - soft reset
hlt - hard reset
slp [time unit], [value] - waits value * time unit. time units can be found in the sleep_units{} dict in the code.

+--- SEMANTICS ---+
This section is mainly to detail "rulings" or certain behaviors that happen when you put certain things together.
- using ; on the same line as a command freezes the interpreter.
- a loop inside a routine creates infinite recursion.
- a routine inside a loop is fine, but the routine will always be called last.
- lod inside a routine or loop loses the original code in favor of the new one (or it'll just crash, this is untested as of now)
- there's a priority list based on what you call, no matter the order in the program. the order is isolated opcodes, loops, then routines, based on the priority
script used to test this in 1.2.

+--- TIPS ---+
This section is for mine (and others') discoveries on how certain things can be done.
- to call a routine/loop inside another routine/loop, you need to split your first routine/loop into two, call the second routine, then continue the first through a
third routine.
example:
rout1 part1
rout2
rout1 part2

+--- CHANGELOG ---+
V 1.1
- .txt compatibility was added
- javascript was removed

V 1.2
- added all arithmetic and comparison commands (adt, sut, mut, dit, mot, inc, dec, shl, shr, rhl, rhr)
- added print integer command (prn)
- added stack addresses from 0 - 65535
- added comparison commands (cmp, smp, fmp, gmp, cmv, smv, fmv, gmv)
- added brk and rst for more advanced loop control
- javascript was removed
