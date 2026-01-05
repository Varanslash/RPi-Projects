.global _start
_start:
    mov x0, #3
    mov x1, #4
    mul x0, x0, x0
    mul x1, x1, x1
    add x2, x1, x0

nomovingforu:
    b nomovingforu