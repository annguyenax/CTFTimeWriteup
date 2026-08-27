0000000140005ba0  4053                              push rbx
0000000140005ba2  4881ec50020000                    sub rsp, 0x250
0000000140005ba9  488bd9                            mov rbx, rcx
0000000140005bac  4883790820                        cmp qword ptr [rcx + 8], 0x20
0000000140005bb1  740b                              je 0x140005bbe
0000000140005bb3  32c0                              xor al, al
0000000140005bb5  4881c450020000                    add rsp, 0x250
0000000140005bbc  5b                                pop rbx
0000000140005bbd  c3                                ret 
0000000140005bbe  0f57c0                            xorps xmm0, xmm0
0000000140005bc1  f30f7f442420                      movdqu xmmword ptr [rsp + 0x20], xmm0
0000000140005bc7  48c744243000000000                mov qword ptr [rsp + 0x30], 0
0000000140005bd0  488d4c2420                        lea rcx, [rsp + 0x20]
0000000140005bd5  e8c6caffff                        call 0x1400026a0
0000000140005bda  84c0                              test al, al
0000000140005bdc  7507                              jne 0x140005be5
0000000140005bde  32db                              xor bl, bl
0000000140005be0  e98c000000                        jmp 0x140005c71
0000000140005be5  488d8c2450010000                  lea rcx, [rsp + 0x150]
0000000140005bed  e86ec3ffff                        call 0x140001f60
0000000140005bf2  488d4c2450                        lea rcx, [rsp + 0x50]
0000000140005bf7  ba02000000                        mov edx, 2
0000000140005bfc  0f1f4000                          nop dword ptr [rax]
0000000140005c00  0f1000                            movups xmm0, xmmword ptr [rax]
0000000140005c03  0f1101                            movups xmmword ptr [rcx], xmm0
0000000140005c06  0f104810                          movups xmm1, xmmword ptr [rax + 0x10]
0000000140005c0a  0f114910                          movups xmmword ptr [rcx + 0x10], xmm1
0000000140005c0e  0f104020                          movups xmm0, xmmword ptr [rax + 0x20]
0000000140005c12  0f114120                          movups xmmword ptr [rcx + 0x20], xmm0
0000000140005c16  0f104830                          movups xmm1, xmmword ptr [rax + 0x30]
0000000140005c1a  0f114930                          movups xmmword ptr [rcx + 0x30], xmm1
0000000140005c1e  0f104040                          movups xmm0, xmmword ptr [rax + 0x40]
0000000140005c22  0f114140                          movups xmmword ptr [rcx + 0x40], xmm0
0000000140005c26  0f104850                          movups xmm1, xmmword ptr [rax + 0x50]
0000000140005c2a  0f114950                          movups xmmword ptr [rcx + 0x50], xmm1
0000000140005c2e  0f104060                          movups xmm0, xmmword ptr [rax + 0x60]
0000000140005c32  0f114160                          movups xmmword ptr [rcx + 0x60], xmm0
0000000140005c36  0f104870                          movups xmm1, xmmword ptr [rax + 0x70]
0000000140005c3a  0f114970                          movups xmmword ptr [rcx + 0x70], xmm1
0000000140005c3e  488d8980000000                    lea rcx, [rcx + 0x80]
0000000140005c45  488d8080000000                    lea rax, [rax + 0x80]
0000000140005c4c  4883ea01                          sub rdx, 1
0000000140005c50  75ae                              jne 0x140005c00
0000000140005c52  0f1003                            movups xmm0, xmmword ptr [rbx]
0000000140005c55  0f29442440                        movaps xmmword ptr [rsp + 0x40], xmm0
0000000140005c5a  4c8d442450                        lea r8, [rsp + 0x50]
0000000140005c5f  488d542440                        lea rdx, [rsp + 0x40]
0000000140005c64  488d4c2420                        lea rcx, [rsp + 0x20]
0000000140005c69  e842ddffff                        call 0x1400039b0
0000000140005c6e  0fb6d8                            movzx ebx, al
0000000140005c71  488b4c2420                        mov rcx, qword ptr [rsp + 0x20]
0000000140005c76  4885c9                            test rcx, rcx
0000000140005c79  7449                              je 0x140005cc4
0000000140005c7b  488b542430                        mov rdx, qword ptr [rsp + 0x30]
0000000140005c80  482bd1                            sub rdx, rcx
0000000140005c83  4881fa00100000                    cmp rdx, 0x1000
0000000140005c8a  7230                              jb 0x140005cbc
0000000140005c8c  4c8b41f8                          mov r8, qword ptr [rcx - 8]
0000000140005c90  492bc8                            sub rcx, r8
0000000140005c93  4883e908                          sub rcx, 8
0000000140005c97  4883f91f                          cmp rcx, 0x1f
0000000140005c9b  7718                              ja 0x140005cb5
0000000140005c9d  4883c227                          add rdx, 0x27
0000000140005ca1  498bc8                            mov rcx, r8
0000000140005ca4  e887000000                        call 0x140005d30
0000000140005ca9  0fb6c3                            movzx eax, bl
0000000140005cac  4881c450020000                    add rsp, 0x250
0000000140005cb3  5b                                pop rbx
0000000140005cb4  c3                                ret 
0000000140005cb5  b905000000                        mov ecx, 5
0000000140005cba  cd29                              int 0x29
0000000140005cbc  4c8bc1                            mov r8, rcx
0000000140005cbf  e86c000000                        call 0x140005d30
0000000140005cc4  0fb6c3                            movzx eax, bl
0000000140005cc7  4881c450020000                    add rsp, 0x250
0000000140005cce  5b                                pop rbx
0000000140005ccf  c3                                ret 
