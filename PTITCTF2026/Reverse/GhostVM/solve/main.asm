0000000140001cd0  4053                              push rbx
0000000140001cd2  4883ec70                          sub rsp, 0x70
0000000140001cd6  488b0523930000                    mov rax, qword ptr [rip + 0x9323]
0000000140001cdd  4833c4                            xor rax, rsp
0000000140001ce0  4889442460                        mov qword ptr [rsp + 0x60], rax
0000000140001ce5  488b1db4530000                    mov rbx, qword ptr [rip + 0x53b4]
0000000140001cec  41b1b7                            mov r9b, 0xb7
0000000140001cef  41b80c000000                      mov r8d, 0xc
0000000140001cf5  488d156c560000                    lea rdx, [rip + 0x566c]
0000000140001cfc  488d4c2420                        lea rcx, [rsp + 0x20]
0000000140001d01  e8aafdffff                        call 0x140001ab0
0000000140001d06  90                                nop 
0000000140001d07  488bd0                            mov rdx, rax
0000000140001d0a  488bcb                            mov rcx, rbx
0000000140001d0d  e8eef2ffff                        call 0x140001000
0000000140001d12  90                                nop 
0000000140001d13  488b542438                        mov rdx, qword ptr [rsp + 0x38]
0000000140001d18  4883fa0f                          cmp rdx, 0xf
0000000140001d1c  7632                              jbe 0x140001d50
0000000140001d1e  48ffc2                            inc rdx
0000000140001d21  488b4c2420                        mov rcx, qword ptr [rsp + 0x20]
0000000140001d26  4881fa00100000                    cmp rdx, 0x1000
0000000140001d2d  721c                              jb 0x140001d4b
0000000140001d2f  488b41f8                          mov rax, qword ptr [rcx - 8]
0000000140001d33  482bc8                            sub rcx, rax
0000000140001d36  4883e908                          sub rcx, 8
0000000140001d3a  4883f91f                          cmp rcx, 0x1f
0000000140001d3e  0f879f010000                      ja 0x140001ee3
0000000140001d44  4883c227                          add rdx, 0x27
0000000140001d48  488bc8                            mov rcx, rax
0000000140001d4b  e8e03f0000                        call 0x140005d30
0000000140001d50  0f57c0                            xorps xmm0, xmm0
0000000140001d53  0f11442440                        movups xmmword ptr [rsp + 0x40], xmm0
0000000140001d58  48c744245000000000                mov qword ptr [rsp + 0x50], 0
0000000140001d61  48c74424580f000000                mov qword ptr [rsp + 0x58], 0xf
0000000140001d6a  c644244000                        mov byte ptr [rsp + 0x40], 0
0000000140001d6f  488d542440                        lea rdx, [rsp + 0x40]
0000000140001d74  488b0d1d530000                    mov rcx, qword ptr [rip + 0x531d]
0000000140001d7b  e830f9ffff                        call 0x1400016b0
0000000140001d80  488d4c2440                        lea rcx, [rsp + 0x40]
0000000140001d85  48837c24580f                      cmp qword ptr [rsp + 0x58], 0xf
0000000140001d8b  480f474c2440                      cmova rcx, qword ptr [rsp + 0x40]
0000000140001d91  488b442450                        mov rax, qword ptr [rsp + 0x50]
0000000140001d96  48894c2420                        mov qword ptr [rsp + 0x20], rcx
0000000140001d9b  4889442428                        mov qword ptr [rsp + 0x28], rax
0000000140001da0  488d4c2420                        lea rcx, [rsp + 0x20]
0000000140001da5  e8f63d0000                        call 0x140005ba0
0000000140001daa  488b1def520000                    mov rbx, qword ptr [rip + 0x52ef]
0000000140001db1  41b197                            mov r9b, 0x97
0000000140001db4  488d4c2420                        lea rcx, [rsp + 0x20]
0000000140001db9  84c0                              test al, al
0000000140001dbb  746a                              je 0x140001e27
0000000140001dbd  41b80d000000                      mov r8d, 0xd
0000000140001dc3  488d15ae550000                    lea rdx, [rip + 0x55ae]
0000000140001dca  e8e1fcffff                        call 0x140001ab0
0000000140001dcf  90                                nop 
0000000140001dd0  488bd0                            mov rdx, rax
0000000140001dd3  488bcb                            mov rcx, rbx
0000000140001dd6  e825f2ffff                        call 0x140001000
0000000140001ddb  488bc8                            mov rcx, rax
0000000140001dde  b20a                              mov dl, 0xa
0000000140001de0  e84bf2ffff                        call 0x140001030
0000000140001de5  90                                nop 
0000000140001de6  488b542438                        mov rdx, qword ptr [rsp + 0x38]
0000000140001deb  4883fa0f                          cmp rdx, 0xf
0000000140001def  7632                              jbe 0x140001e23
0000000140001df1  48ffc2                            inc rdx
0000000140001df4  488b4c2420                        mov rcx, qword ptr [rsp + 0x20]
0000000140001df9  4881fa00100000                    cmp rdx, 0x1000
0000000140001e00  721c                              jb 0x140001e1e
0000000140001e02  488b41f8                          mov rax, qword ptr [rcx - 8]
0000000140001e06  482bc8                            sub rcx, rax
0000000140001e09  4883e908                          sub rcx, 8
0000000140001e0d  4883f91f                          cmp rcx, 0x1f
0000000140001e11  0f87c5000000                      ja 0x140001edc
0000000140001e17  4883c227                          add rdx, 0x27
0000000140001e1b  488bc8                            mov rcx, rax
0000000140001e1e  e80d3f0000                        call 0x140005d30
0000000140001e23  33db                              xor ebx, ebx
0000000140001e25  eb67                              jmp 0x140001e8e
0000000140001e27  41b80b000000                      mov r8d, 0xb
0000000140001e2d  488d1554550000                    lea rdx, [rip + 0x5554]
0000000140001e34  e877fcffff                        call 0x140001ab0
0000000140001e39  90                                nop 
0000000140001e3a  488bd0                            mov rdx, rax
0000000140001e3d  488bcb                            mov rcx, rbx
0000000140001e40  e8bbf1ffff                        call 0x140001000
0000000140001e45  488bc8                            mov rcx, rax
0000000140001e48  b20a                              mov dl, 0xa
0000000140001e4a  e8e1f1ffff                        call 0x140001030
0000000140001e4f  90                                nop 
0000000140001e50  488b542438                        mov rdx, qword ptr [rsp + 0x38]
0000000140001e55  4883fa0f                          cmp rdx, 0xf
0000000140001e59  762e                              jbe 0x140001e89
0000000140001e5b  48ffc2                            inc rdx
0000000140001e5e  488b4c2420                        mov rcx, qword ptr [rsp + 0x20]
0000000140001e63  4881fa00100000                    cmp rdx, 0x1000
0000000140001e6a  7218                              jb 0x140001e84
0000000140001e6c  488b41f8                          mov rax, qword ptr [rcx - 8]
0000000140001e70  482bc8                            sub rcx, rax
0000000140001e73  4883e908                          sub rcx, 8
0000000140001e77  4883f91f                          cmp rcx, 0x1f
0000000140001e7b  775f                              ja 0x140001edc
0000000140001e7d  4883c227                          add rdx, 0x27
0000000140001e81  488bc8                            mov rcx, rax
0000000140001e84  e8a73e0000                        call 0x140005d30
0000000140001e89  bb01000000                        mov ebx, 1
0000000140001e8e  488b542458                        mov rdx, qword ptr [rsp + 0x58]
0000000140001e93  4883fa0f                          cmp rdx, 0xf
0000000140001e97  762e                              jbe 0x140001ec7
0000000140001e99  48ffc2                            inc rdx
0000000140001e9c  488b4c2440                        mov rcx, qword ptr [rsp + 0x40]
0000000140001ea1  4881fa00100000                    cmp rdx, 0x1000
0000000140001ea8  7218                              jb 0x140001ec2
0000000140001eaa  488b41f8                          mov rax, qword ptr [rcx - 8]
0000000140001eae  482bc8                            sub rcx, rax
0000000140001eb1  4883e908                          sub rcx, 8
0000000140001eb5  4883f91f                          cmp rcx, 0x1f
0000000140001eb9  7728                              ja 0x140001ee3
0000000140001ebb  4883c227                          add rdx, 0x27
0000000140001ebf  488bc8                            mov rcx, rax
0000000140001ec2  e8693e0000                        call 0x140005d30
0000000140001ec7  8bc3                              mov eax, ebx
0000000140001ec9  488b4c2460                        mov rcx, qword ptr [rsp + 0x60]
0000000140001ece  4833cc                            xor rcx, rsp
0000000140001ed1  e8ea3e0000                        call 0x140005dc0
0000000140001ed6  4883c470                          add rsp, 0x70
0000000140001eda  5b                                pop rbx
0000000140001edb  c3                                ret 
0000000140001edc  b905000000                        mov ecx, 5
0000000140001ee1  cd29                              int 0x29
0000000140001ee3  b905000000                        mov ecx, 5
0000000140001ee8  cd29                              int 0x29
