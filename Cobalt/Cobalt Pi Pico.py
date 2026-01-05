import time
import machine
from machine import Pin
import sys

registers = {f"r{i}": 0 for i in range(8)}
strings = {f"s{i}": " " for i in range(8)}
routines, loops, ifelse = {}, {}, {}
stack = [0] * 256

sleep_units = {
    "nif": 1e-50, "zil": 0.000000001, "mis": 0.000001, "ms": 0.001, "s": 1, "m": 60, "h": 3600, "d": 86400,
    "w": 604800, "mo": 2592000, "y": 31536000, "dec": 315360000, "cen": 3153600000,
    "mil": 31536000000, "spc": 315360000000, "eon": 3153600000000, "inf": 1e50
}

function = False
generalflag = False
loopflag = True
loop_count = 0
userinput = []
name = ""
loopname = ""

def is_int(value):
    return value.lstrip("-").isdigit()

def make_callback(name):
    def cb(pin_obj):
        global userinput, function
        userinput = routines[name]
        function = True
    return cb

while True:
    if function:
        if loop_count > 0 and loopflag:
            userinput = loops[loopname]
            loop_count -= 1
        else:
            userinput = routines[name]
            function = False
    else:
        code = input()
        userinput = [line.split() for line in code.split("\n") if line.strip()]

    for instruction in userinput:
        if not instruction:
            continue
        cmd = instruction[0]

        if cmd == "xor" and len(instruction) == 4:
            r1, r2, dest = instruction[1:4]
            if r1 in registers and r2 in registers and dest in registers:
                registers[dest] = registers[r1] ^ registers[r2]

        elif cmd == "ora" and len(instruction) == 4:
            r1, r2, dest = instruction[1:4]
            if r1 in registers and r2 in registers and dest in registers:
                registers[dest] = registers[r1] | registers[r2]

        elif cmd == "and" and len(instruction) == 4:
            r1, r2, dest = instruction[1:4]
            if r1 in registers and r2 in registers and dest in registers:
                registers[dest] = registers[r1] & registers[r2]

        elif cmd == "not" and len(instruction) == 3:
            r1, dest = instruction[1:3]
            if r1 in registers and dest in registers:
                registers[dest] = ~registers[r1]

        elif cmd == "prt" and len(instruction) == 2:
            reg = instruction[1]
            if reg in strings:
                print(strings[reg])

        elif cmd == "prn" and len(instruction) == 2:
            reg = instruction[1]
            if reg in registers:
                print(registers[reg])

        elif cmd == "sav" and len(instruction) >= 3:
            reg = instruction[1]
            if reg in strings:
                strings[reg] = " ".join(instruction[2:])

        elif cmd in ("add", "sub", "mul", "div", "mod") and len(instruction) == 3:
            reg, val = instruction[1:3]
            if reg in registers and is_int(val):
                val = int(val)
                if cmd == "add":
                    registers[reg] += val
                elif cmd == "sub":
                    registers[reg] -= val
                elif cmd == "mul":
                    registers[reg] *= val
                elif cmd == "div" and val != 0:
                    registers[reg] //= val
                elif cmd == "mod" and val != 0:
                    registers[reg] %= val

        elif cmd == "mov" and len(instruction) == 3:
            r1, r2 = instruction[1:3]
            if r1 in registers and r2 in registers:
                registers[r2] = registers[r1]

        elif cmd == "psh" and len(instruction) == 3:
            reg, val = instruction[1:3]
            if reg in registers and is_int(val):
                idx = int(val)
                if 0 <= idx < len(stack):
                    stack[idx] = registers[reg]

        elif cmd == "pop" and len(instruction) == 2:
            val = instruction[1]
            if is_int(val):
                idx = int(val)
                if 0 <= idx < len(stack):
                    stack[idx] = 0

        elif cmd == "slp" and len(instruction) == 3:
            unit, val = instruction[1:3]
            if unit in sleep_units and is_int(val):
                try:
                    time.sleep(int(val) * sleep_units[unit])
                except OverflowError:
                    print("Overflow Error: Sleep value too large!")

        elif cmd == "pim" and len(instruction) == 3:
            pin, mode = instruction[1:3]
            if pin.isdigit() and mode in ("in", "out"):
                pin_num = int(pin)
                Pin(pin_num, Pin.IN if mode=="in" else Pin.OUT)

        elif cmd == "pow" and len(instruction) == 3:
            pin, state = instruction[1:3]
            if pin.isdigit() and state in ("high", "low"):
                pin_num = int(pin)
                Pin(pin_num, Pin.OUT).value(1 if state=="high" else 0)

        elif cmd == "rdi" and len(instruction) == 3:
            pin, dest = instruction[1:3]
            if pin.isdigit() and dest in registers:
                pin_num = int(pin)
                registers[dest] = Pin(pin_num, Pin.IN).value()

        elif cmd == "wri" and len(instruction) == 3:
            pin, reg = instruction[1:3]
            if pin.isdigit() and reg in registers:
                pin_num = int(pin)
                Pin(pin_num, Pin.OUT).value(registers[reg])

        elif cmd == "int" and len(instruction) == 5:
            state, pin, rout, rout2 = instruction[1:5]
            if state in ("rise","fall") and pin.isdigit() and rout in routines and rout2 in routines:
                pin_num = int(pin)
                pin_obj = Pin(pin_num, Pin.IN)
                name = rout if state=="rise" else rout2
                callback = make_callback(name)
                trigger = Pin.IRQ_RISING if state=="rise" else Pin.IRQ_FALLING
                pin_obj.irq(trigger=trigger, handler=callback)

        elif cmd == "pif" and len(instruction) == 3:
            pin, rout = instruction[1:3]
            if pin.isdigit() and rout in routines:
                pin_num = int(pin)
                pin_obj = Pin(pin_num, Pin.IN)
                callback = make_callback(rout)
                pin_obj.irq(trigger=Pin.IRQ_RISING, handler=callback)
                if pin_obj.value() == 1:
                    userinput = routines.get(rout, [])
                    function = True

        elif cmd == "hlt":
            while True: pass
        elif cmd == "srt":
            machine.soft_reset()
        elif cmd == "csh":
            sys.exit()

        elif cmd == "sar" and len(instruction) == 2:
            reg = instruction[1]
            routines[reg] = []
            name = reg
        elif cmd == "sro" and len(instruction) >= 2:
            reg = instruction[1]
            if reg in routines:
                routines[reg].append(instruction[2:])
        elif cmd == "run" and len(instruction) == 2:
            reg = instruction[1]
            if reg in routines:
                userinput = routines[reg]
                function = True
        elif cmd == "lop" and len(instruction) == 2:
            reg = instruction[1]
            loops[reg] = []
            loopname = reg
        elif cmd == "lro" and len(instruction) >= 2:
            reg = instruction[1]
            if reg in loops:
                loops[reg].append(instruction[2:])
        elif cmd == "lup" and len(instruction) == 3:
            reg, val = instruction[1:3]
            if reg in loops and is_int(val):
                loop_count = int(val)
                userinput = loops[reg]
                function = True

        elif cmd == "cmp" and len(instruction) == 3:
            r1, r2 = instruction[1:3]
            if r1 in registers and r2 in registers:
                generalflag = registers[r1] == registers[r2]

        elif cmd == "smp" and len(instruction) == 3:
            r1, r2 = instruction[1:3]
            if r1 in registers and r2 in registers:
                generalflag = registers[r1] != registers[r2]

        elif cmd == "gmp" and len(instruction) == 3:
            r1, r2 = instruction[1:3]
            if r1 in registers and r2 in registers:
                generalflag = registers[r1] > registers[r2]

        elif cmd == "fmp" and len(instruction) == 3:
            r1, r2 = instruction[1:3]
            if r1 in registers and r2 in registers:
                generalflag = registers[r1] < registers[r2]

        elif cmd == "tru":
            generalflag = True
        elif cmd == "fal":
            generalflag = False


        elif cmd == "lod" and len(instruction) == 2:
            filename = instruction[1]
            try:
                with open(filename,"r") as f:
                    text = f.read()
                userinput = [line.split() for line in text.split("\n") if line.strip()]
                function = True
            except OSError:
                print("File Error, File not found:", filename)

        elif cmd == "nop":
            pass

        elif cmd.startswith(";"):
            continue
