target_bytes = [205, 255, 155, 233, 154, 166, 214, 174, 37, 179, 15, 247, 234, 64, 144, 222, 66, 60, 245, 17]

r9d = 0xffffffaa

flag = []
for i in range(20):
    edx = 0
    eax = 1
    esi = 1
    ecx = 1
    while edx != i:
        ecx = eax
        eax = (eax + esi) & 0xffffffff
        edx += 1
        esi = ecx
        
    fib_val = ecx
    cl_new = target_bytes[i] ^ (r9d & 0xff)
    input_char = (cl_new - (fib_val & 0xff)) % 256
    flag.append(input_char)
    
    ecx_new = (fib_val & 0xffffff00) | cl_new
    r9d = (r9d ^ ecx_new) & 0xffffffff
    
print("Flag: LITCTF{" + bytes(flag).decode() + "}")
