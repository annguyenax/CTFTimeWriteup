00000001400039b0  4c8bdc                            mov r11, rsp
00000001400039b3  55                                push rbp
00000001400039b4  498d6be8                          lea rbp, [r11 - 0x18]
00000001400039b8  4881ec10010000                    sub rsp, 0x110
00000001400039bf  488b053a760000                    mov rax, qword ptr [rip + 0x763a]
00000001400039c6  4833c4                            xor rax, rsp
00000001400039c9  488945e0                          mov qword ptr [rbp - 0x20], rax
00000001400039cd  4c8b5108                          mov r10, qword ptr [rcx + 8]
00000001400039d1  0f57c0                            xorps xmm0, xmm0
00000001400039d4  49897318                          mov qword ptr [r11 + 0x18], rsi
00000001400039d8  48be00df0deeffc0ad0b              movabs rsi, 0xbadc0ffee0ddf00
00000001400039e2  49897b20                          mov qword ptr [r11 + 0x20], rdi
00000001400039e6  488b39                            mov rdi, qword ptr [rcx]
00000001400039e9  4d8963f0                          mov qword ptr [r11 - 0x10], r12
00000001400039ed  4c2bd7                            sub r10, rdi
00000001400039f0  4d896be8                          mov qword ptr [r11 - 0x18], r13
00000001400039f4  4533c9                            xor r9d, r9d
00000001400039f7  4d8973e0                          mov qword ptr [r11 - 0x20], r14
00000001400039fb  4c8bea                            mov r13, rdx
00000001400039fe  4d897bd8                          mov qword ptr [r11 - 0x28], r15
0000000140003a02  4d8bf0                            mov r14, r8
0000000140003a05  44894c2430                        mov dword ptr [rsp + 0x30], r9d
0000000140003a0a  41bc00093d00                      mov r12d, 0x3d0900
0000000140003a10  44884c2440                        mov byte ptr [rsp + 0x40], r9b
0000000140003a15  4c89442448                        mov qword ptr [rsp + 0x48], r8
0000000140003a1a  0f11442450                        movups xmmword ptr [rsp + 0x50], xmm0
0000000140003a1f  c745d000000000                    mov dword ptr [rbp - 0x30], 0
0000000140003a26  0f11442460                        movups xmmword ptr [rsp + 0x60], xmm0
0000000140003a2b  48897c2420                        mov qword ptr [rsp + 0x20], rdi
0000000140003a30  0f11442470                        movups xmmword ptr [rsp + 0x70], xmm0
0000000140003a35  4c89542428                        mov qword ptr [rsp + 0x28], r10
0000000140003a3a  0f114580                          movups xmmword ptr [rbp - 0x80], xmm0
0000000140003a3e  4889742438                        mov qword ptr [rsp + 0x38], rsi
0000000140003a43  0f114590                          movups xmmword ptr [rbp - 0x70], xmm0
0000000140003a47  49895b10                          mov qword ptr [r11 + 0x10], rbx
0000000140003a4b  0f1145a0                          movups xmmword ptr [rbp - 0x60], xmm0
0000000140003a4f  0f1145b0                          movups xmmword ptr [rbp - 0x50], xmm0
0000000140003a53  0f1145c0                          movups xmmword ptr [rbp - 0x40], xmm0
0000000140003a57  807dd300                          cmp byte ptr [rbp - 0x2d], 0
0000000140003a5b  49bbeb113113bb49d094              movabs r11, 0x94d049bb133111eb
0000000140003a65  49bf157c4a7fb979379e              movabs r15, 0x9e3779b97f4a7c15
0000000140003a6f  48bab9e5e41c6d4758bf              movabs rdx, 0xbf58476d1ce4e5b9
0000000140003a79  0f8512200000                      jne 0x140005a91
0000000140003a7f  807c244000                        cmp byte ptr [rsp + 0x40], 0
0000000140003a84  0f8507200000                      jne 0x140005a91
0000000140003a8a  498bc4                            mov rax, r12
0000000140003a8d  49ffcc                            dec r12
0000000140003a90  4885c0                            test rax, rax
0000000140003a93  0f84f81f0000                      je 0x140005a91
0000000140003a99  418bc1                            mov eax, r9d
0000000140003a9c  493bc2                            cmp rax, r10
0000000140003a9f  720a                              jb 0x140003aab
0000000140003aa1  c644244001                        mov byte ptr [rsp + 0x40], 1
0000000140003aa6  4532db                            xor r11b, r11b
0000000140003aa9  eb67                              jmp 0x140003b12
0000000140003aab  418bc1                            mov eax, r9d
0000000140003aae  8bc8                              mov ecx, eax
0000000140003ab0  448bc0                            mov r8d, eax
0000000140003ab3  490fafcf                          imul rcx, r15
0000000140003ab7  448d4801                          lea r9d, [rax + 1]
0000000140003abb  48c1e020                          shl rax, 0x20
0000000140003abf  4803ce                            add rcx, rsi
0000000140003ac2  44894c2430                        mov dword ptr [rsp + 0x30], r9d
0000000140003ac7  4833c8                            xor rcx, rax
0000000140003aca  488bc1                            mov rax, rcx
0000000140003acd  48c1e81e                          shr rax, 0x1e
0000000140003ad1  4833c1                            xor rax, rcx
0000000140003ad4  480fafc2                          imul rax, rdx
0000000140003ad8  488bc8                            mov rcx, rax
0000000140003adb  48c1e91b                          shr rcx, 0x1b
0000000140003adf  4833c8                            xor rcx, rax
0000000140003ae2  490fafcb                          imul rcx, r11
0000000140003ae6  488bd1                            mov rdx, rcx
0000000140003ae9  48c1ea1f                          shr rdx, 0x1f
0000000140003aed  4833d1                            xor rdx, rcx
0000000140003af0  4c8bda                            mov r11, rdx
0000000140003af3  488bc2                            mov rax, rdx
0000000140003af6  49c1eb28                          shr r11, 0x28
0000000140003afa  48c1e818                          shr rax, 0x18
0000000140003afe  4432d8                            xor r11b, al
0000000140003b01  488bc2                            mov rax, rdx
0000000140003b04  48c1e808                          shr rax, 8
0000000140003b08  4432d8                            xor r11b, al
0000000140003b0b  4432da                            xor r11b, dl
0000000140003b0e  45321c38                          xor r11b, byte ptr [r8 + rdi]
0000000140003b12  410fb6c3                          movzx eax, r11b
0000000140003b16  488d15e3c4ffff                    lea rdx, [rip - 0x3b1d]
0000000140003b1d  0fb69c0280940000                  movzx ebx, byte ptr [rdx + rax + 0x9480]
0000000140003b25  440fb6840280950000                movzx r8d, byte ptr [rdx + rax + 0x9580]
0000000140003b2e  4183e307                          and r11d, 7
0000000140003b32  7425                              je 0x140003b59
0000000140003b34  410fb6d0                          movzx edx, r8b
0000000140003b38  410fb6c0                          movzx eax, r8b
0000000140003b3c  b908000000                        mov ecx, 8
0000000140003b41  412acb                            sub cl, r11b
0000000140003b44  d2ea                              shr dl, cl
0000000140003b46  418bcb                            mov ecx, r11d
0000000140003b49  440fb6c2                          movzx r8d, dl
0000000140003b4d  d2e0                              shl al, cl
0000000140003b4f  440ac0                            or r8b, al
0000000140003b52  488d15a7c4ffff                    lea rdx, [rip - 0x3b59]
0000000140003b59  4132d8                            xor bl, r8b
0000000140003b5c  0fb6c3                            movzx eax, bl
0000000140003b5f  35a5000000                        xor eax, 0xa5
0000000140003b64  83f81e                            cmp eax, 0x1e
0000000140003b67  0f87111f0000                      ja 0x140005a7e
0000000140003b6d  4898                              cdqe 
0000000140003b6f  8b8c821c5b0000                    mov ecx, dword ptr [rdx + rax*4 + 0x5b1c]
0000000140003b76  4803ca                            add rcx, rdx
0000000140003b79  ffe1                              jmp rcx
0000000140003b7b  418bc1                            mov eax, r9d
0000000140003b7e  493bc2                            cmp rax, r10
0000000140003b81  7219                              jb 0x140003b9c
0000000140003b83  32db                              xor bl, bl
0000000140003b85  c644244001                        mov byte ptr [rsp + 0x40], 1
0000000140003b8a  488d4c2420                        lea rcx, [rsp + 0x20]
0000000140003b8f  e8ace6ffff                        call 0x140002240
0000000140003b94  488bc8                            mov rcx, rax
0000000140003b97  e98e000000                        jmp 0x140003c2a
0000000140003b9c  418d4101                          lea eax, [r9 + 1]
0000000140003ba0  418bc9                            mov ecx, r9d
0000000140003ba3  89442430                          mov dword ptr [rsp + 0x30], eax
0000000140003ba7  490fafcf                          imul rcx, r15
0000000140003bab  418bc1                            mov eax, r9d
0000000140003bae  48c1e020                          shl rax, 0x20
0000000140003bb2  4803ce                            add rcx, rsi
0000000140003bb5  4833c8                            xor rcx, rax
0000000140003bb8  458bc1                            mov r8d, r9d
0000000140003bbb  488bc1                            mov rax, rcx
0000000140003bbe  48c1e81e                          shr rax, 0x1e
0000000140003bc2  4833c1                            xor rax, rcx
0000000140003bc5  48b9b9e5e41c6d4758bf              movabs rcx, 0xbf58476d1ce4e5b9
0000000140003bcf  480fafc1                          imul rax, rcx
0000000140003bd3  488bc8                            mov rcx, rax
0000000140003bd6  48c1e91b                          shr rcx, 0x1b
0000000140003bda  4833c8                            xor rcx, rax
0000000140003bdd  48b8eb113113bb49d094              movabs rax, 0x94d049bb133111eb
0000000140003be7  480fafc8                          imul rcx, rax
0000000140003beb  488bd1                            mov rdx, rcx
0000000140003bee  48c1ea1f                          shr rdx, 0x1f
0000000140003bf2  4833d1                            xor rdx, rcx
0000000140003bf5  488d4c2420                        lea rcx, [rsp + 0x20]
0000000140003bfa  488bda                            mov rbx, rdx
0000000140003bfd  488bc2                            mov rax, rdx
0000000140003c00  48c1eb28                          shr rbx, 0x28
0000000140003c04  48c1e818                          shr rax, 0x18
0000000140003c08  32d8                              xor bl, al
0000000140003c0a  488bc2                            mov rax, rdx
0000000140003c0d  48c1e808                          shr rax, 8
0000000140003c11  32d8                              xor bl, al
0000000140003c13  32da                              xor bl, dl
0000000140003c15  41321c38                          xor bl, byte ptr [r8 + rdi]
0000000140003c19  e822e6ffff                        call 0x140002240
0000000140003c1e  488bc8                            mov rcx, rax
0000000140003c21  80fb10                            cmp bl, 0x10
0000000140003c24  0f83401e0000                      jae 0x140005a6a
0000000140003c2a  0fb6c3                            movzx eax, bl
0000000140003c2d  48894cc450                        mov qword ptr [rsp + rax*8 + 0x50], rcx
0000000140003c32  448b4c2430                        mov r9d, dword ptr [rsp + 0x30]
0000000140003c37  4c8b542428                        mov r10, qword ptr [rsp + 0x28]
0000000140003c3c  488b742438                        mov rsi, qword ptr [rsp + 0x38]
0000000140003c41  488b7c2420                        mov rdi, qword ptr [rsp + 0x20]
0000000140003c46  e93c1e0000                        jmp 0x140005a87
0000000140003c4b  418bc1                            mov eax, r9d
0000000140003c4e  48bbb9e5e41c6d4758bf              movabs rbx, 0xbf58476d1ce4e5b9
0000000140003c58  493bc2                            cmp rax, r10
0000000140003c5b  720a                              jb 0x140003c67
0000000140003c5d  c644244001                        mov byte ptr [rsp + 0x40], 1
0000000140003c62  4532db                            xor r11b, r11b
0000000140003c65  eb71                              jmp 0x140003cd8
0000000140003c67  418bc1                            mov eax, r9d
0000000140003c6a  8bc8                              mov ecx, eax
0000000140003c6c  448bc0                            mov r8d, eax
0000000140003c6f  490fafcf                          imul rcx, r15
0000000140003c73  448d4801                          lea r9d, [rax + 1]
0000000140003c77  48c1e020                          shl rax, 0x20
0000000140003c7b  4803ce                            add rcx, rsi
0000000140003c7e  44894c2430                        mov dword ptr [rsp + 0x30], r9d
0000000140003c83  4833c8                            xor rcx, rax
0000000140003c86  488bc1                            mov rax, rcx
0000000140003c89  48c1e81e                          shr rax, 0x1e
0000000140003c8d  4833c1                            xor rax, rcx
0000000140003c90  480fafc3                          imul rax, rbx
0000000140003c94  488bc8                            mov rcx, rax
0000000140003c97  48c1e91b                          shr rcx, 0x1b
0000000140003c9b  4833c8                            xor rcx, rax
0000000140003c9e  48b8eb113113bb49d094              movabs rax, 0x94d049bb133111eb
0000000140003ca8  480fafc8                          imul rcx, rax
0000000140003cac  488bd1                            mov rdx, rcx
0000000140003caf  48c1ea1f                          shr rdx, 0x1f
0000000140003cb3  4833d1                            xor rdx, rcx
0000000140003cb6  4c8bda                            mov r11, rdx
0000000140003cb9  488bc2                            mov rax, rdx
0000000140003cbc  49c1eb28                          shr r11, 0x28
0000000140003cc0  48c1e818                          shr rax, 0x18
0000000140003cc4  4432d8                            xor r11b, al
0000000140003cc7  488bc2                            mov rax, rdx
0000000140003cca  48c1e808                          shr rax, 8
0000000140003cce  4432d8                            xor r11b, al
0000000140003cd1  4432da                            xor r11b, dl
0000000140003cd4  45321c38                          xor r11b, byte ptr [r8 + rdi]
0000000140003cd8  418bc1                            mov eax, r9d
0000000140003cdb  493bc2                            cmp rax, r10
0000000140003cde  7209                              jb 0x140003ce9
0000000140003ce0  c644244001                        mov byte ptr [rsp + 0x40], 1
0000000140003ce5  32c9                              xor cl, cl
0000000140003ce7  eb6e                              jmp 0x140003d57
0000000140003ce9  418bc1                            mov eax, r9d
0000000140003cec  8bc8                              mov ecx, eax
0000000140003cee  448bc0                            mov r8d, eax
0000000140003cf1  490fafcf                          imul rcx, r15
0000000140003cf5  448d4801                          lea r9d, [rax + 1]
0000000140003cf9  48c1e020                          shl rax, 0x20
0000000140003cfd  4803ce                            add rcx, rsi
0000000140003d00  44894c2430                        mov dword ptr [rsp + 0x30], r9d
0000000140003d05  4833c8                            xor rcx, rax
0000000140003d08  488bc1                            mov rax, rcx
0000000140003d0b  48c1e81e                          shr rax, 0x1e
0000000140003d0f  4833c1                            xor rax, rcx
0000000140003d12  480fafc3                          imul rax, rbx
0000000140003d16  488bc8                            mov rcx, rax
0000000140003d19  48c1e91b                          shr rcx, 0x1b
0000000140003d1d  4833c8                            xor rcx, rax
0000000140003d20  48b8eb113113bb49d094              movabs rax, 0x94d049bb133111eb
0000000140003d2a  480fafc8                          imul rcx, rax
0000000140003d2e  488bd1                            mov rdx, rcx
0000000140003d31  48c1ea1f                          shr rdx, 0x1f
0000000140003d35  4833d1                            xor rdx, rcx
0000000140003d38  488bca                            mov rcx, rdx
0000000140003d3b  488bc2                            mov rax, rdx
0000000140003d3e  48c1e928                          shr rcx, 0x28
0000000140003d42  48c1e818                          shr rax, 0x18
0000000140003d46  32c8                              xor cl, al
0000000140003d48  488bc2                            mov rax, rdx
0000000140003d4b  48c1e808                          shr rax, 8
0000000140003d4f  32c8                              xor cl, al
0000000140003d51  32ca                              xor cl, dl
0000000140003d53  41320c38                          xor cl, byte ptr [r8 + rdi]
0000000140003d57  4180fb10                          cmp r11b, 0x10
0000000140003d5b  0f831d1d0000                      jae 0x140005a7e
0000000140003d61  80f910                            cmp cl, 0x10
0000000140003d64  0f83141d0000                      jae 0x140005a7e
0000000140003d6a  0fb6c1                            movzx eax, cl
0000000140003d6d  410fb6cb                          movzx ecx, r11b
0000000140003d71  488b44c450                        mov rax, qword ptr [rsp + rax*8 + 0x50]
0000000140003d76  488944cc50                        mov qword ptr [rsp + rcx*8 + 0x50], rax
0000000140003d7b  e9071d0000                        jmp 0x140005a87
0000000140003d80  418bc1                            mov eax, r9d
0000000140003d83  48bbb9e5e41c6d4758bf              movabs rbx, 0xbf58476d1ce4e5b9
0000000140003d8d  493bc2                            cmp rax, r10
0000000140003d90  720a                              jb 0x140003d9c
0000000140003d92  c644244001                        mov byte ptr [rsp + 0x40], 1
0000000140003d97  4532db                            xor r11b, r11b
0000000140003d9a  eb71                              jmp 0x140003e0d
0000000140003d9c  418bc1                            mov eax, r9d
0000000140003d9f  8bc8                              mov ecx, eax
0000000140003da1  448bc0                            mov r8d, eax
0000000140003da4  490fafcf                          imul rcx, r15
0000000140003da8  448d4801                          lea r9d, [rax + 1]
0000000140003dac  48c1e020                          shl rax, 0x20
0000000140003db0  4803ce                            add rcx, rsi
0000000140003db3  44894c2430                        mov dword ptr [rsp + 0x30], r9d
0000000140003db8  4833c8                            xor rcx, rax
0000000140003dbb  488bc1                            mov rax, rcx
0000000140003dbe  48c1e81e                          shr rax, 0x1e
0000000140003dc2  4833c1                            xor rax, rcx
0000000140003dc5  480fafc3                          imul rax, rbx
0000000140003dc9  488bc8                            mov rcx, rax
0000000140003dcc  48c1e91b                          shr rcx, 0x1b
0000000140003dd0  4833c8                            xor rcx, rax
0000000140003dd3  48b8eb113113bb49d094              movabs rax, 0x94d049bb133111eb
0000000140003ddd  480fafc8                          imul rcx, rax
0000000140003de1  488bd1                            mov rdx, rcx
0000000140003de4  48c1ea1f                          shr rdx, 0x1f
0000000140003de8  4833d1                            xor rdx, rcx
0000000140003deb  4c8bda                            mov r11, rdx
0000000140003dee  488bc2                            mov rax, rdx
0000000140003df1  49c1eb28                          shr r11, 0x28
0000000140003df5  48c1e818                          shr rax, 0x18
0000000140003df9  4432d8                            xor r11b, al
0000000140003dfc  488bc2                            mov rax, rdx
0000000140003dff  48c1e808                          shr rax, 8
0000000140003e03  4432d8                            xor r11b, al
0000000140003e06  4432da                            xor r11b, dl
0000000140003e09  45321c38                          xor r11b, byte ptr [r8 + rdi]
0000000140003e0d  418bc1                            mov eax, r9d
0000000140003e10  493bc2                            cmp rax, r10
0000000140003e13  7209                              jb 0x140003e1e
0000000140003e15  c644244001                        mov byte ptr [rsp + 0x40], 1
0000000140003e1a  32c9                              xor cl, cl
0000000140003e1c  eb6e                              jmp 0x140003e8c
0000000140003e1e  418bc1                            mov eax, r9d
0000000140003e21  8bc8                              mov ecx, eax
0000000140003e23  448bc0                            mov r8d, eax
0000000140003e26  490fafcf                          imul rcx, r15
0000000140003e2a  448d4801                          lea r9d, [rax + 1]
0000000140003e2e  48c1e020                          shl rax, 0x20
0000000140003e32  4803ce                            add rcx, rsi
0000000140003e35  44894c2430                        mov dword ptr [rsp + 0x30], r9d
0000000140003e3a  4833c8                            xor rcx, rax
0000000140003e3d  488bc1                            mov rax, rcx
0000000140003e40  48c1e81e                          shr rax, 0x1e
0000000140003e44  4833c1                            xor rax, rcx
0000000140003e47  480fafc3                          imul rax, rbx
0000000140003e4b  488bc8                            mov rcx, rax
0000000140003e4e  48c1e91b                          shr rcx, 0x1b
0000000140003e52  4833c8                            xor rcx, rax
0000000140003e55  48b8eb113113bb49d094              movabs rax, 0x94d049bb133111eb
0000000140003e5f  480fafc8                          imul rcx, rax
0000000140003e63  488bd1                            mov rdx, rcx
0000000140003e66  48c1ea1f                          shr rdx, 0x1f
0000000140003e6a  4833d1                            xor rdx, rcx
0000000140003e6d  488bca                            mov rcx, rdx
0000000140003e70  488bc2                            mov rax, rdx
0000000140003e73  48c1e928                          shr rcx, 0x28
0000000140003e77  48c1e818                          shr rax, 0x18
0000000140003e7b  32c8                              xor cl, al
0000000140003e7d  488bc2                            mov rax, rdx
0000000140003e80  48c1e808                          shr rax, 8
0000000140003e84  32c8                              xor cl, al
0000000140003e86  32ca                              xor cl, dl
0000000140003e88  41320c38                          xor cl, byte ptr [r8 + rdi]
0000000140003e8c  4180fb10                          cmp r11b, 0x10
0000000140003e90  0f83e81b0000                      jae 0x140005a7e
0000000140003e96  0fb6d1                            movzx edx, cl
0000000140003e99  493b5508                          cmp rdx, qword ptr [r13 + 8]
0000000140003e9d  0f83db1b0000                      jae 0x140005a7e
0000000140003ea3  498b4500                          mov rax, qword ptr [r13]
0000000140003ea7  0fb60c02                          movzx ecx, byte ptr [rdx + rax]
0000000140003eab  410fb6c3                          movzx eax, r11b
0000000140003eaf  48894cc450                        mov qword ptr [rsp + rax*8 + 0x50], rcx
0000000140003eb4  e9ce1b0000                        jmp 0x140005a87
0000000140003eb9  418bc1                            mov eax, r9d
0000000140003ebc  48bbb9e5e41c6d4758bf              movabs rbx, 0xbf58476d1ce4e5b9
0000000140003ec6  493bc2                            cmp rax, r10
0000000140003ec9  720a                              jb 0x140003ed5
0000000140003ecb  c644244001                        mov byte ptr [rsp + 0x40], 1
0000000140003ed0  4532db                            xor r11b, r11b
0000000140003ed3  eb71                              jmp 0x140003f46
0000000140003ed5  418bc1                            mov eax, r9d
0000000140003ed8  8bc8                              mov ecx, eax
0000000140003eda  448bc0                            mov r8d, eax
0000000140003edd  490fafcf                          imul rcx, r15
0000000140003ee1  448d4801                          lea r9d, [rax + 1]
0000000140003ee5  48c1e020                          shl rax, 0x20
0000000140003ee9  4803ce                            add rcx, rsi
0000000140003eec  44894c2430                        mov dword ptr [rsp + 0x30], r9d
0000000140003ef1  4833c8                            xor rcx, rax
0000000140003ef4  488bc1                            mov rax, rcx
0000000140003ef7  48c1e81e                          shr rax, 0x1e
0000000140003efb  4833c1                            xor rax, rcx
0000000140003efe  480fafc3                          imul rax, rbx
0000000140003f02  488bc8                            mov rcx, rax
0000000140003f05  48c1e91b                          shr rcx, 0x1b
0000000140003f09  4833c8                            xor rcx, rax
0000000140003f0c  48b8eb113113bb49d094              movabs rax, 0x94d049bb133111eb
0000000140003f16  480fafc8                          imul rcx, rax
0000000140003f1a  488bd1                            mov rdx, rcx
0000000140003f1d  48c1ea1f                          shr rdx, 0x1f
0000000140003f21  4833d1                            xor rdx, rcx
0000000140003f24  4c8bda                            mov r11, rdx
0000000140003f27  488bc2                            mov rax, rdx
0000000140003f2a  49c1eb28                          shr r11, 0x28
0000000140003f2e  48c1e818                          shr rax, 0x18
0000000140003f32  4432d8                            xor r11b, al
0000000140003f35  488bc2                            mov rax, rdx
0000000140003f38  48c1e808                          shr rax, 8
0000000140003f3c  4432d8                            xor r11b, al
0000000140003f3f  4432da                            xor r11b, dl
0000000140003f42  45321c38                          xor r11b, byte ptr [r8 + rdi]
0000000140003f46  418bc1                            mov eax, r9d
0000000140003f49  493bc2                            cmp rax, r10
0000000140003f4c  7209                              jb 0x140003f57
0000000140003f4e  c644244001                        mov byte ptr [rsp + 0x40], 1
0000000140003f53  32c9                              xor cl, cl
0000000140003f55  eb6e                              jmp 0x140003fc5
0000000140003f57  418bc1                            mov eax, r9d
0000000140003f5a  8bc8                              mov ecx, eax
0000000140003f5c  448bc0                            mov r8d, eax
0000000140003f5f  490fafcf                          imul rcx, r15
0000000140003f63  448d4801                          lea r9d, [rax + 1]
0000000140003f67  48c1e020                          shl rax, 0x20
0000000140003f6b  4803ce                            add rcx, rsi
0000000140003f6e  44894c2430                        mov dword ptr [rsp + 0x30], r9d
0000000140003f73  4833c8                            xor rcx, rax
0000000140003f76  488bc1                            mov rax, rcx
0000000140003f79  48c1e81e                          shr rax, 0x1e
0000000140003f7d  4833c1                            xor rax, rcx
0000000140003f80  480fafc3                          imul rax, rbx
0000000140003f84  488bc8                            mov rcx, rax
0000000140003f87  48c1e91b                          shr rcx, 0x1b
0000000140003f8b  4833c8                            xor rcx, rax
0000000140003f8e  48b8eb113113bb49d094              movabs rax, 0x94d049bb133111eb
0000000140003f98  480fafc8                          imul rcx, rax
0000000140003f9c  488bd1                            mov rdx, rcx
0000000140003f9f  48c1ea1f                          shr rdx, 0x1f
0000000140003fa3  4833d1                            xor rdx, rcx
0000000140003fa6  488bca                            mov rcx, rdx
0000000140003fa9  488bc2                            mov rax, rdx
0000000140003fac  48c1e928                          shr rcx, 0x28
0000000140003fb0  48c1e818                          shr rax, 0x18
0000000140003fb4  32c8                              xor cl, al
0000000140003fb6  488bc2                            mov rax, rdx
0000000140003fb9  48c1e808                          shr rax, 8
0000000140003fbd  32c8                              xor cl, al
0000000140003fbf  32ca                              xor cl, dl
0000000140003fc1  41320c38                          xor cl, byte ptr [r8 + rdi]
0000000140003fc5  4180fb10                          cmp r11b, 0x10
0000000140003fc9  0f83af1a0000                      jae 0x140005a7e
0000000140003fcf  80f910                            cmp cl, 0x10
0000000140003fd2  0f83a61a0000                      jae 0x140005a7e
0000000140003fd8  410fb6c3                          movzx eax, r11b
0000000140003fdc  488d542450                        lea rdx, [rsp + 0x50]
0000000140003fe1  488d14c2                          lea rdx, [rdx + rax*8]
0000000140003fe5  0fb6c1                            movzx eax, cl
0000000140003fe8  488b4cc450                        mov rcx, qword ptr [rsp + rax*8 + 0x50]
0000000140003fed  48310a                            xor qword ptr [rdx], rcx
0000000140003ff0  e9921a0000                        jmp 0x140005a87
0000000140003ff5  418bc1                            mov eax, r9d
0000000140003ff8  493bc2                            cmp rax, r10
0000000140003ffb  7221                              jb 0x14000401e
0000000140003ffd  488d4c2420                        lea rcx, [rsp + 0x20]
0000000140004002  c644244001                        mov byte ptr [rsp + 0x40], 1
0000000140004007  32db                              xor bl, bl
0000000140004009  e832e2ffff                        call 0x140002240
000000014000400e  488bc8                            mov rcx, rax
0000000140004011  0fb6c3                            movzx eax, bl
0000000140004014  48314cc450                        xor qword ptr [rsp + rax*8 + 0x50], rcx
0000000140004019  e914fcffff                        jmp 0x140003c32
000000014000401e  418d4101                          lea eax, [r9 + 1]
0000000140004022  418bc9                            mov ecx, r9d
0000000140004025  89442430                          mov dword ptr [rsp + 0x30], eax
0000000140004029  490fafcf                          imul rcx, r15
000000014000402d  418bc1                            mov eax, r9d
0000000140004030  48c1e020                          shl rax, 0x20
0000000140004034  4803ce                            add rcx, rsi
0000000140004037  4833c8                            xor rcx, rax
000000014000403a  458bc1                            mov r8d, r9d
000000014000403d  488bc1                            mov rax, rcx
0000000140004040  48c1e81e                          shr rax, 0x1e
0000000140004044  4833c1                            xor rax, rcx
0000000140004047  48b9b9e5e41c6d4758bf              movabs rcx, 0xbf58476d1ce4e5b9
0000000140004051  480fafc1                          imul rax, rcx
0000000140004055  488bc8                            mov rcx, rax
0000000140004058  48c1e91b                          shr rcx, 0x1b
000000014000405c  4833c8                            xor rcx, rax
000000014000405f  48b8eb113113bb49d094              movabs rax, 0x94d049bb133111eb
0000000140004069  480fafc8                          imul rcx, rax
000000014000406d  488bd1                            mov rdx, rcx
0000000140004070  48c1ea1f                          shr rdx, 0x1f
0000000140004074  4833d1                            xor rdx, rcx
0000000140004077  488d4c2420                        lea rcx, [rsp + 0x20]
000000014000407c  488bda                            mov rbx, rdx
000000014000407f  488bc2                            mov rax, rdx
0000000140004082  48c1eb28                          shr rbx, 0x28
0000000140004086  48c1e818                          shr rax, 0x18
000000014000408a  32d8                              xor bl, al
000000014000408c  488bc2                            mov rax, rdx
000000014000408f  48c1e808                          shr rax, 8
0000000140004093  32d8                              xor bl, al
0000000140004095  32da                              xor bl, dl
0000000140004097  41321c38                          xor bl, byte ptr [r8 + rdi]
000000014000409b  e8a0e1ffff                        call 0x140002240
00000001400040a0  488bc8                            mov rcx, rax
00000001400040a3  80fb10                            cmp bl, 0x10
00000001400040a6  0f83be190000                      jae 0x140005a6a
00000001400040ac  0fb6c3                            movzx eax, bl
00000001400040af  48314cc450                        xor qword ptr [rsp + rax*8 + 0x50], rcx
00000001400040b4  e979fbffff                        jmp 0x140003c32
00000001400040b9  418bc1                            mov eax, r9d
00000001400040bc  48bbb9e5e41c6d4758bf              movabs rbx, 0xbf58476d1ce4e5b9
00000001400040c6  493bc2                            cmp rax, r10
00000001400040c9  720a                              jb 0x1400040d5
00000001400040cb  c644244001                        mov byte ptr [rsp + 0x40], 1
00000001400040d0  4532db                            xor r11b, r11b
00000001400040d3  eb71                              jmp 0x140004146
00000001400040d5  418bc1                            mov eax, r9d
00000001400040d8  8bc8                              mov ecx, eax
00000001400040da  448bc0                            mov r8d, eax
00000001400040dd  490fafcf                          imul rcx, r15
00000001400040e1  448d4801                          lea r9d, [rax + 1]
00000001400040e5  48c1e020                          shl rax, 0x20
00000001400040e9  4803ce                            add rcx, rsi
00000001400040ec  44894c2430                        mov dword ptr [rsp + 0x30], r9d
00000001400040f1  4833c8                            xor rcx, rax
00000001400040f4  488bc1                            mov rax, rcx
00000001400040f7  48c1e81e                          shr rax, 0x1e
00000001400040fb  4833c1                            xor rax, rcx
00000001400040fe  480fafc3                          imul rax, rbx
0000000140004102  488bc8                            mov rcx, rax
0000000140004105  48c1e91b                          shr rcx, 0x1b
0000000140004109  4833c8                            xor rcx, rax
000000014000410c  48b8eb113113bb49d094              movabs rax, 0x94d049bb133111eb
0000000140004116  480fafc8                          imul rcx, rax
000000014000411a  488bd1                            mov rdx, rcx
000000014000411d  48c1ea1f                          shr rdx, 0x1f
0000000140004121  4833d1                            xor rdx, rcx
0000000140004124  4c8bda                            mov r11, rdx
0000000140004127  488bc2                            mov rax, rdx
000000014000412a  49c1eb28                          shr r11, 0x28
000000014000412e  48c1e818                          shr rax, 0x18
0000000140004132  4432d8                            xor r11b, al
0000000140004135  488bc2                            mov rax, rdx
0000000140004138  48c1e808                          shr rax, 8
000000014000413c  4432d8                            xor r11b, al
000000014000413f  4432da                            xor r11b, dl
0000000140004142  45321c38                          xor r11b, byte ptr [r8 + rdi]
0000000140004146  418bc1                            mov eax, r9d
0000000140004149  493bc2                            cmp rax, r10
000000014000414c  7209                              jb 0x140004157
000000014000414e  c644244001                        mov byte ptr [rsp + 0x40], 1
0000000140004153  32c9                              xor cl, cl
0000000140004155  eb6e                              jmp 0x1400041c5
0000000140004157  418bc1                            mov eax, r9d
000000014000415a  8bc8                              mov ecx, eax
000000014000415c  448bc0                            mov r8d, eax
000000014000415f  490fafcf                          imul rcx, r15
0000000140004163  448d4801                          lea r9d, [rax + 1]
0000000140004167  48c1e020                          shl rax, 0x20
000000014000416b  4803ce                            add rcx, rsi
000000014000416e  44894c2430                        mov dword ptr [rsp + 0x30], r9d
0000000140004173  4833c8                            xor rcx, rax
0000000140004176  488bc1                            mov rax, rcx
0000000140004179  48c1e81e                          shr rax, 0x1e
000000014000417d  4833c1                            xor rax, rcx
0000000140004180  480fafc3                          imul rax, rbx
0000000140004184  488bc8                            mov rcx, rax
0000000140004187  48c1e91b                          shr rcx, 0x1b
000000014000418b  4833c8                            xor rcx, rax
000000014000418e  48b8eb113113bb49d094              movabs rax, 0x94d049bb133111eb
0000000140004198  480fafc8                          imul rcx, rax
000000014000419c  488bd1                            mov rdx, rcx
000000014000419f  48c1ea1f                          shr rdx, 0x1f
00000001400041a3  4833d1                            xor rdx, rcx
00000001400041a6  488bca                            mov rcx, rdx
00000001400041a9  488bc2                            mov rax, rdx
00000001400041ac  48c1e928                          shr rcx, 0x28
00000001400041b0  48c1e818                          shr rax, 0x18
00000001400041b4  32c8                              xor cl, al
00000001400041b6  488bc2                            mov rax, rdx
00000001400041b9  48c1e808                          shr rax, 8
00000001400041bd  32c8                              xor cl, al
00000001400041bf  32ca                              xor cl, dl
00000001400041c1  41320c38                          xor cl, byte ptr [r8 + rdi]
00000001400041c5  4180fb10                          cmp r11b, 0x10
00000001400041c9  0f83af180000                      jae 0x140005a7e
00000001400041cf  80f910                            cmp cl, 0x10
00000001400041d2  0f83a6180000                      jae 0x140005a7e
00000001400041d8  410fb6c3                          movzx eax, r11b
00000001400041dc  488d542450                        lea rdx, [rsp + 0x50]
00000001400041e1  488d14c2                          lea rdx, [rdx + rax*8]
00000001400041e5  0fb6c1                            movzx eax, cl
00000001400041e8  488b4cc450                        mov rcx, qword ptr [rsp + rax*8 + 0x50]
00000001400041ed  48010a                            add qword ptr [rdx], rcx
00000001400041f0  e992180000                        jmp 0x140005a87
00000001400041f5  418bc1                            mov eax, r9d
00000001400041f8  493bc2                            cmp rax, r10
00000001400041fb  7221                              jb 0x14000421e
00000001400041fd  488d4c2420                        lea rcx, [rsp + 0x20]
0000000140004202  c644244001                        mov byte ptr [rsp + 0x40], 1
0000000140004207  32db                              xor bl, bl
0000000140004209  e832e0ffff                        call 0x140002240
000000014000420e  488bc8                            mov rcx, rax
0000000140004211  0fb6c3                            movzx eax, bl
0000000140004214  48014cc450                        add qword ptr [rsp + rax*8 + 0x50], rcx
0000000140004219  e914faffff                        jmp 0x140003c32
000000014000421e  418d4101                          lea eax, [r9 + 1]
0000000140004222  418bc9                            mov ecx, r9d
0000000140004225  89442430                          mov dword ptr [rsp + 0x30], eax
0000000140004229  490fafcf                          imul rcx, r15
000000014000422d  418bc1                            mov eax, r9d
0000000140004230  48c1e020                          shl rax, 0x20
0000000140004234  4803ce                            add rcx, rsi
0000000140004237  4833c8                            xor rcx, rax
000000014000423a  458bc1                            mov r8d, r9d
000000014000423d  488bc1                            mov rax, rcx
0000000140004240  48c1e81e                          shr rax, 0x1e
0000000140004244  4833c1                            xor rax, rcx
0000000140004247  48b9b9e5e41c6d4758bf              movabs rcx, 0xbf58476d1ce4e5b9
0000000140004251  480fafc1                          imul rax, rcx
0000000140004255  488bc8                            mov rcx, rax
0000000140004258  48c1e91b                          shr rcx, 0x1b
000000014000425c  4833c8                            xor rcx, rax
000000014000425f  48b8eb113113bb49d094              movabs rax, 0x94d049bb133111eb
0000000140004269  480fafc8                          imul rcx, rax
000000014000426d  488bd1                            mov rdx, rcx
0000000140004270  48c1ea1f                          shr rdx, 0x1f
0000000140004274  4833d1                            xor rdx, rcx
0000000140004277  488d4c2420                        lea rcx, [rsp + 0x20]
000000014000427c  488bda                            mov rbx, rdx
000000014000427f  488bc2                            mov rax, rdx
0000000140004282  48c1eb28                          shr rbx, 0x28
0000000140004286  48c1e818                          shr rax, 0x18
000000014000428a  32d8                              xor bl, al
000000014000428c  488bc2                            mov rax, rdx
000000014000428f  48c1e808                          shr rax, 8
0000000140004293  32d8                              xor bl, al
0000000140004295  32da                              xor bl, dl
0000000140004297  41321c38                          xor bl, byte ptr [r8 + rdi]
000000014000429b  e8a0dfffff                        call 0x140002240
00000001400042a0  488bc8                            mov rcx, rax
00000001400042a3  80fb10                            cmp bl, 0x10
00000001400042a6  0f83be170000                      jae 0x140005a6a
00000001400042ac  0fb6c3                            movzx eax, bl
00000001400042af  48014cc450                        add qword ptr [rsp + rax*8 + 0x50], rcx
00000001400042b4  e979f9ffff                        jmp 0x140003c32
00000001400042b9  418bc1                            mov eax, r9d
00000001400042bc  48bbb9e5e41c6d4758bf              movabs rbx, 0xbf58476d1ce4e5b9
00000001400042c6  493bc2                            cmp rax, r10
00000001400042c9  720a                              jb 0x1400042d5
00000001400042cb  c644244001                        mov byte ptr [rsp + 0x40], 1
00000001400042d0  4532db                            xor r11b, r11b
00000001400042d3  eb71                              jmp 0x140004346
00000001400042d5  418bc1                            mov eax, r9d
00000001400042d8  8bc8                              mov ecx, eax
00000001400042da  448bc0                            mov r8d, eax
00000001400042dd  490fafcf                          imul rcx, r15
00000001400042e1  448d4801                          lea r9d, [rax + 1]
00000001400042e5  48c1e020                          shl rax, 0x20
00000001400042e9  4803ce                            add rcx, rsi
00000001400042ec  44894c2430                        mov dword ptr [rsp + 0x30], r9d
00000001400042f1  4833c8                            xor rcx, rax
00000001400042f4  488bc1                            mov rax, rcx
00000001400042f7  48c1e81e                          shr rax, 0x1e
00000001400042fb  4833c1                            xor rax, rcx
00000001400042fe  480fafc3                          imul rax, rbx
0000000140004302  488bc8                            mov rcx, rax
0000000140004305  48c1e91b                          shr rcx, 0x1b
0000000140004309  4833c8                            xor rcx, rax
000000014000430c  48b8eb113113bb49d094              movabs rax, 0x94d049bb133111eb
0000000140004316  480fafc8                          imul rcx, rax
000000014000431a  488bd1                            mov rdx, rcx
000000014000431d  48c1ea1f                          shr rdx, 0x1f
0000000140004321  4833d1                            xor rdx, rcx
0000000140004324  4c8bda                            mov r11, rdx
0000000140004327  488bc2                            mov rax, rdx
000000014000432a  49c1eb28                          shr r11, 0x28
000000014000432e  48c1e818                          shr rax, 0x18
0000000140004332  4432d8                            xor r11b, al
0000000140004335  488bc2                            mov rax, rdx
0000000140004338  48c1e808                          shr rax, 8
000000014000433c  4432d8                            xor r11b, al
000000014000433f  4432da                            xor r11b, dl
0000000140004342  45321c38                          xor r11b, byte ptr [r8 + rdi]
0000000140004346  418bc1                            mov eax, r9d
0000000140004349  493bc2                            cmp rax, r10
000000014000434c  7209                              jb 0x140004357
000000014000434e  c644244001                        mov byte ptr [rsp + 0x40], 1
0000000140004353  32c9                              xor cl, cl
0000000140004355  eb6e                              jmp 0x1400043c5
0000000140004357  418bc1                            mov eax, r9d
000000014000435a  8bc8                              mov ecx, eax
000000014000435c  448bc0                            mov r8d, eax
000000014000435f  490fafcf                          imul rcx, r15
0000000140004363  448d4801                          lea r9d, [rax + 1]
0000000140004367  48c1e020                          shl rax, 0x20
000000014000436b  4803ce                            add rcx, rsi
000000014000436e  44894c2430                        mov dword ptr [rsp + 0x30], r9d
0000000140004373  4833c8                            xor rcx, rax
0000000140004376  488bc1                            mov rax, rcx
0000000140004379  48c1e81e                          shr rax, 0x1e
000000014000437d  4833c1                            xor rax, rcx
0000000140004380  480fafc3                          imul rax, rbx
0000000140004384  488bc8                            mov rcx, rax
0000000140004387  48c1e91b                          shr rcx, 0x1b
000000014000438b  4833c8                            xor rcx, rax
000000014000438e  48b8eb113113bb49d094              movabs rax, 0x94d049bb133111eb
0000000140004398  480fafc8                          imul rcx, rax
000000014000439c  488bd1                            mov rdx, rcx
000000014000439f  48c1ea1f                          shr rdx, 0x1f
00000001400043a3  4833d1                            xor rdx, rcx
00000001400043a6  488bca                            mov rcx, rdx
00000001400043a9  488bc2                            mov rax, rdx
00000001400043ac  48c1e928                          shr rcx, 0x28
00000001400043b0  48c1e818                          shr rax, 0x18
00000001400043b4  32c8                              xor cl, al
00000001400043b6  488bc2                            mov rax, rdx
00000001400043b9  48c1e808                          shr rax, 8
00000001400043bd  32c8                              xor cl, al
00000001400043bf  32ca                              xor cl, dl
00000001400043c1  41320c38                          xor cl, byte ptr [r8 + rdi]
00000001400043c5  4180fb10                          cmp r11b, 0x10
00000001400043c9  0f83af160000                      jae 0x140005a7e
00000001400043cf  80f910                            cmp cl, 0x10
00000001400043d2  0f83a6160000                      jae 0x140005a7e
00000001400043d8  410fb6c3                          movzx eax, r11b
00000001400043dc  488d542450                        lea rdx, [rsp + 0x50]
00000001400043e1  488d14c2                          lea rdx, [rdx + rax*8]
00000001400043e5  0fb6c1                            movzx eax, cl
00000001400043e8  488b4cc450                        mov rcx, qword ptr [rsp + rax*8 + 0x50]
00000001400043ed  48290a                            sub qword ptr [rdx], rcx
00000001400043f0  e992160000                        jmp 0x140005a87
00000001400043f5  418bc1                            mov eax, r9d
00000001400043f8  48bbb9e5e41c6d4758bf              movabs rbx, 0xbf58476d1ce4e5b9
0000000140004402  493bc2                            cmp rax, r10
0000000140004405  720a                              jb 0x140004411
0000000140004407  c644244001                        mov byte ptr [rsp + 0x40], 1
000000014000440c  4532db                            xor r11b, r11b
000000014000440f  eb71                              jmp 0x140004482
0000000140004411  418bc1                            mov eax, r9d
0000000140004414  8bc8                              mov ecx, eax
0000000140004416  448bc0                            mov r8d, eax
0000000140004419  490fafcf                          imul rcx, r15
000000014000441d  448d4801                          lea r9d, [rax + 1]
0000000140004421  48c1e020                          shl rax, 0x20
0000000140004425  4803ce                            add rcx, rsi
0000000140004428  44894c2430                        mov dword ptr [rsp + 0x30], r9d
000000014000442d  4833c8                            xor rcx, rax
0000000140004430  488bc1                            mov rax, rcx
0000000140004433  48c1e81e                          shr rax, 0x1e
0000000140004437  4833c1                            xor rax, rcx
000000014000443a  480fafc3                          imul rax, rbx
000000014000443e  488bc8                            mov rcx, rax
0000000140004441  48c1e91b                          shr rcx, 0x1b
0000000140004445  4833c8                            xor rcx, rax
0000000140004448  48b8eb113113bb49d094              movabs rax, 0x94d049bb133111eb
0000000140004452  480fafc8                          imul rcx, rax
0000000140004456  488bd1                            mov rdx, rcx
0000000140004459  48c1ea1f                          shr rdx, 0x1f
000000014000445d  4833d1                            xor rdx, rcx
0000000140004460  4c8bda                            mov r11, rdx
0000000140004463  488bc2                            mov rax, rdx
0000000140004466  49c1eb28                          shr r11, 0x28
000000014000446a  48c1e818                          shr rax, 0x18
000000014000446e  4432d8                            xor r11b, al
0000000140004471  488bc2                            mov rax, rdx
0000000140004474  48c1e808                          shr rax, 8
0000000140004478  4432d8                            xor r11b, al
000000014000447b  4432da                            xor r11b, dl
000000014000447e  45321c38                          xor r11b, byte ptr [r8 + rdi]
0000000140004482  418bc1                            mov eax, r9d
0000000140004485  493bc2                            cmp rax, r10
0000000140004488  7209                              jb 0x140004493
000000014000448a  c644244001                        mov byte ptr [rsp + 0x40], 1
000000014000448f  32c9                              xor cl, cl
0000000140004491  eb6e                              jmp 0x140004501
0000000140004493  418bc1                            mov eax, r9d
0000000140004496  8bc8                              mov ecx, eax
0000000140004498  448bc0                            mov r8d, eax
000000014000449b  490fafcf                          imul rcx, r15
000000014000449f  448d4801                          lea r9d, [rax + 1]
00000001400044a3  48c1e020                          shl rax, 0x20
00000001400044a7  4803ce                            add rcx, rsi
00000001400044aa  44894c2430                        mov dword ptr [rsp + 0x30], r9d
00000001400044af  4833c8                            xor rcx, rax
00000001400044b2  488bc1                            mov rax, rcx
00000001400044b5  48c1e81e                          shr rax, 0x1e
00000001400044b9  4833c1                            xor rax, rcx
00000001400044bc  480fafc3                          imul rax, rbx
00000001400044c0  488bc8                            mov rcx, rax
00000001400044c3  48c1e91b                          shr rcx, 0x1b
00000001400044c7  4833c8                            xor rcx, rax
00000001400044ca  48b8eb113113bb49d094              movabs rax, 0x94d049bb133111eb
00000001400044d4  480fafc8                          imul rcx, rax
00000001400044d8  488bd1                            mov rdx, rcx
00000001400044db  48c1ea1f                          shr rdx, 0x1f
00000001400044df  4833d1                            xor rdx, rcx
00000001400044e2  488bca                            mov rcx, rdx
00000001400044e5  488bc2                            mov rax, rdx
00000001400044e8  48c1e928                          shr rcx, 0x28
00000001400044ec  48c1e818                          shr rax, 0x18
00000001400044f0  32c8                              xor cl, al
00000001400044f2  488bc2                            mov rax, rdx
00000001400044f5  48c1e808                          shr rax, 8
00000001400044f9  32c8                              xor cl, al
00000001400044fb  32ca                              xor cl, dl
00000001400044fd  41320c38                          xor cl, byte ptr [r8 + rdi]
0000000140004501  4180fb10                          cmp r11b, 0x10
0000000140004505  0f8373150000                      jae 0x140005a7e
000000014000450b  80f910                            cmp cl, 0x10
000000014000450e  0f836a150000                      jae 0x140005a7e
0000000140004514  410fb6c3                          movzx eax, r11b
0000000140004518  488d542450                        lea rdx, [rsp + 0x50]
000000014000451d  488d14c2                          lea rdx, [rdx + rax*8]
0000000140004521  0fb6c1                            movzx eax, cl
0000000140004524  488b0a                            mov rcx, qword ptr [rdx]
0000000140004527  480faf4cc450                      imul rcx, qword ptr [rsp + rax*8 + 0x50]
000000014000452d  48890a                            mov qword ptr [rdx], rcx
0000000140004530  e952150000                        jmp 0x140005a87
0000000140004535  418bc1                            mov eax, r9d
0000000140004538  493bc2                            cmp rax, r10
000000014000453b  7222                              jb 0x14000455f
000000014000453d  488d4c2420                        lea rcx, [rsp + 0x20]
0000000140004542  c644244001                        mov byte ptr [rsp + 0x40], 1
0000000140004547  32db                              xor bl, bl
0000000140004549  e8f2dcffff                        call 0x140002240
000000014000454e  488bc8                            mov rcx, rax
0000000140004551  0fb6c3                            movzx eax, bl
0000000140004554  480faf4cc450                      imul rcx, qword ptr [rsp + rax*8 + 0x50]
000000014000455a  e9cef6ffff                        jmp 0x140003c2d
000000014000455f  418d4101                          lea eax, [r9 + 1]
0000000140004563  418bc9                            mov ecx, r9d
0000000140004566  89442430                          mov dword ptr [rsp + 0x30], eax
000000014000456a  490fafcf                          imul rcx, r15
000000014000456e  418bc1                            mov eax, r9d
0000000140004571  48c1e020                          shl rax, 0x20
0000000140004575  4803ce                            add rcx, rsi
0000000140004578  4833c8                            xor rcx, rax
000000014000457b  458bc1                            mov r8d, r9d
000000014000457e  488bc1                            mov rax, rcx
0000000140004581  48c1e81e                          shr rax, 0x1e
0000000140004585  4833c1                            xor rax, rcx
0000000140004588  48b9b9e5e41c6d4758bf              movabs rcx, 0xbf58476d1ce4e5b9
0000000140004592  480fafc1                          imul rax, rcx
0000000140004596  488bc8                            mov rcx, rax
0000000140004599  48c1e91b                          shr rcx, 0x1b
000000014000459d  4833c8                            xor rcx, rax
00000001400045a0  48b8eb113113bb49d094              movabs rax, 0x94d049bb133111eb
00000001400045aa  480fafc8                          imul rcx, rax
00000001400045ae  488bd1                            mov rdx, rcx
00000001400045b1  48c1ea1f                          shr rdx, 0x1f
00000001400045b5  4833d1                            xor rdx, rcx
00000001400045b8  488d4c2420                        lea rcx, [rsp + 0x20]
00000001400045bd  488bda                            mov rbx, rdx
00000001400045c0  488bc2                            mov rax, rdx
00000001400045c3  48c1eb28                          shr rbx, 0x28
00000001400045c7  48c1e818                          shr rax, 0x18
00000001400045cb  32d8                              xor bl, al
00000001400045cd  488bc2                            mov rax, rdx
00000001400045d0  48c1e808                          shr rax, 8
00000001400045d4  32d8                              xor bl, al
00000001400045d6  32da                              xor bl, dl
00000001400045d8  41321c38                          xor bl, byte ptr [r8 + rdi]
00000001400045dc  e85fdcffff                        call 0x140002240
00000001400045e1  488bc8                            mov rcx, rax
00000001400045e4  80fb10                            cmp bl, 0x10
00000001400045e7  0f837d140000                      jae 0x140005a6a
00000001400045ed  0fb6c3                            movzx eax, bl
00000001400045f0  480faf4cc450                      imul rcx, qword ptr [rsp + rax*8 + 0x50]
00000001400045f6  e932f6ffff                        jmp 0x140003c2d
00000001400045fb  418bc1                            mov eax, r9d
00000001400045fe  48bbb9e5e41c6d4758bf              movabs rbx, 0xbf58476d1ce4e5b9
0000000140004608  493bc2                            cmp rax, r10
000000014000460b  720a                              jb 0x140004617
000000014000460d  c644244001                        mov byte ptr [rsp + 0x40], 1
0000000140004612  4532db                            xor r11b, r11b
0000000140004615  eb71                              jmp 0x140004688
0000000140004617  418bc1                            mov eax, r9d
000000014000461a  8bc8                              mov ecx, eax
000000014000461c  448bc0                            mov r8d, eax
000000014000461f  490fafcf                          imul rcx, r15
0000000140004623  448d4801                          lea r9d, [rax + 1]
0000000140004627  48c1e020                          shl rax, 0x20
000000014000462b  4803ce                            add rcx, rsi
000000014000462e  44894c2430                        mov dword ptr [rsp + 0x30], r9d
0000000140004633  4833c8                            xor rcx, rax
0000000140004636  488bc1                            mov rax, rcx
0000000140004639  48c1e81e                          shr rax, 0x1e
000000014000463d  4833c1                            xor rax, rcx
0000000140004640  480fafc3                          imul rax, rbx
0000000140004644  488bc8                            mov rcx, rax
0000000140004647  48c1e91b                          shr rcx, 0x1b
000000014000464b  4833c8                            xor rcx, rax
000000014000464e  48b8eb113113bb49d094              movabs rax, 0x94d049bb133111eb
0000000140004658  480fafc8                          imul rcx, rax
000000014000465c  488bd1                            mov rdx, rcx
000000014000465f  48c1ea1f                          shr rdx, 0x1f
0000000140004663  4833d1                            xor rdx, rcx
0000000140004666  4c8bda                            mov r11, rdx
0000000140004669  488bc2                            mov rax, rdx
000000014000466c  49c1eb28                          shr r11, 0x28
0000000140004670  48c1e818                          shr rax, 0x18
0000000140004674  4432d8                            xor r11b, al
0000000140004677  488bc2                            mov rax, rdx
000000014000467a  48c1e808                          shr rax, 8
000000014000467e  4432d8                            xor r11b, al
0000000140004681  4432da                            xor r11b, dl
0000000140004684  45321c38                          xor r11b, byte ptr [r8 + rdi]
0000000140004688  418bc1                            mov eax, r9d
000000014000468b  493bc2                            cmp rax, r10
000000014000468e  7209                              jb 0x140004699
0000000140004690  c644244001                        mov byte ptr [rsp + 0x40], 1
0000000140004695  32c9                              xor cl, cl
0000000140004697  eb6e                              jmp 0x140004707
0000000140004699  418bc1                            mov eax, r9d
000000014000469c  8bc8                              mov ecx, eax
000000014000469e  448bc0                            mov r8d, eax
00000001400046a1  490fafcf                          imul rcx, r15
00000001400046a5  448d4801                          lea r9d, [rax + 1]
00000001400046a9  48c1e020                          shl rax, 0x20
00000001400046ad  4803ce                            add rcx, rsi
00000001400046b0  44894c2430                        mov dword ptr [rsp + 0x30], r9d
00000001400046b5  4833c8                            xor rcx, rax
00000001400046b8  488bc1                            mov rax, rcx
00000001400046bb  48c1e81e                          shr rax, 0x1e
00000001400046bf  4833c1                            xor rax, rcx
00000001400046c2  480fafc3                          imul rax, rbx
00000001400046c6  488bc8                            mov rcx, rax
00000001400046c9  48c1e91b                          shr rcx, 0x1b
00000001400046cd  4833c8                            xor rcx, rax
00000001400046d0  48b8eb113113bb49d094              movabs rax, 0x94d049bb133111eb
00000001400046da  480fafc8                          imul rcx, rax
00000001400046de  488bd1                            mov rdx, rcx
00000001400046e1  48c1ea1f                          shr rdx, 0x1f
00000001400046e5  4833d1                            xor rdx, rcx
00000001400046e8  488bca                            mov rcx, rdx
00000001400046eb  488bc2                            mov rax, rdx
00000001400046ee  48c1e928                          shr rcx, 0x28
00000001400046f2  48c1e818                          shr rax, 0x18
00000001400046f6  32c8                              xor cl, al
00000001400046f8  488bc2                            mov rax, rdx
00000001400046fb  48c1e808                          shr rax, 8
00000001400046ff  32c8                              xor cl, al
0000000140004701  32ca                              xor cl, dl
0000000140004703  41320c38                          xor cl, byte ptr [r8 + rdi]
0000000140004707  4180fb10                          cmp r11b, 0x10
000000014000470b  0f836d130000                      jae 0x140005a7e
0000000140004711  410fb6c3                          movzx eax, r11b
0000000140004715  488d542450                        lea rdx, [rsp + 0x50]
000000014000471a  488d14c2                          lea rdx, [rdx + rax*8]
000000014000471e  488b02                            mov rax, qword ptr [rdx]
0000000140004721  83e13f                            and ecx, 0x3f
0000000140004724  7403                              je 0x140004729
0000000140004726  48d3c0                            rol rax, cl
0000000140004729  488902                            mov qword ptr [rdx], rax
000000014000472c  e956130000                        jmp 0x140005a87
0000000140004731  418bc1                            mov eax, r9d
0000000140004734  48bbb9e5e41c6d4758bf              movabs rbx, 0xbf58476d1ce4e5b9
000000014000473e  493bc2                            cmp rax, r10
0000000140004741  720a                              jb 0x14000474d
0000000140004743  c644244001                        mov byte ptr [rsp + 0x40], 1
0000000140004748  4532db                            xor r11b, r11b
000000014000474b  eb71                              jmp 0x1400047be
000000014000474d  418bc1                            mov eax, r9d
0000000140004750  8bc8                              mov ecx, eax
0000000140004752  448bc0                            mov r8d, eax
0000000140004755  490fafcf                          imul rcx, r15
0000000140004759  448d4801                          lea r9d, [rax + 1]
000000014000475d  48c1e020                          shl rax, 0x20
0000000140004761  4803ce                            add rcx, rsi
0000000140004764  44894c2430                        mov dword ptr [rsp + 0x30], r9d
0000000140004769  4833c8                            xor rcx, rax
000000014000476c  488bc1                            mov rax, rcx
000000014000476f  48c1e81e                          shr rax, 0x1e
0000000140004773  4833c1                            xor rax, rcx
0000000140004776  480fafc3                          imul rax, rbx
000000014000477a  488bc8                            mov rcx, rax
000000014000477d  48c1e91b                          shr rcx, 0x1b
0000000140004781  4833c8                            xor rcx, rax
0000000140004784  48b8eb113113bb49d094              movabs rax, 0x94d049bb133111eb
000000014000478e  480fafc8                          imul rcx, rax
0000000140004792  488bd1                            mov rdx, rcx
0000000140004795  48c1ea1f                          shr rdx, 0x1f
0000000140004799  4833d1                            xor rdx, rcx
000000014000479c  4c8bda                            mov r11, rdx
000000014000479f  488bc2                            mov rax, rdx
00000001400047a2  49c1eb28                          shr r11, 0x28
00000001400047a6  48c1e818                          shr rax, 0x18
00000001400047aa  4432d8                            xor r11b, al
00000001400047ad  488bc2                            mov rax, rdx
00000001400047b0  48c1e808                          shr rax, 8
00000001400047b4  4432d8                            xor r11b, al
00000001400047b7  4432da                            xor r11b, dl
00000001400047ba  45321c38                          xor r11b, byte ptr [r8 + rdi]
00000001400047be  418bc1                            mov eax, r9d
00000001400047c1  493bc2                            cmp rax, r10
00000001400047c4  7209                              jb 0x1400047cf
00000001400047c6  c644244001                        mov byte ptr [rsp + 0x40], 1
00000001400047cb  32c9                              xor cl, cl
00000001400047cd  eb6e                              jmp 0x14000483d
00000001400047cf  418bc1                            mov eax, r9d
00000001400047d2  8bc8                              mov ecx, eax
00000001400047d4  448bc0                            mov r8d, eax
00000001400047d7  490fafcf                          imul rcx, r15
00000001400047db  448d4801                          lea r9d, [rax + 1]
00000001400047df  48c1e020                          shl rax, 0x20
00000001400047e3  4803ce                            add rcx, rsi
00000001400047e6  44894c2430                        mov dword ptr [rsp + 0x30], r9d
00000001400047eb  4833c8                            xor rcx, rax
00000001400047ee  488bc1                            mov rax, rcx
00000001400047f1  48c1e81e                          shr rax, 0x1e
00000001400047f5  4833c1                            xor rax, rcx
00000001400047f8  480fafc3                          imul rax, rbx
00000001400047fc  488bc8                            mov rcx, rax
00000001400047ff  48c1e91b                          shr rcx, 0x1b
0000000140004803  4833c8                            xor rcx, rax
0000000140004806  48b8eb113113bb49d094              movabs rax, 0x94d049bb133111eb
0000000140004810  480fafc8                          imul rcx, rax
0000000140004814  488bd1                            mov rdx, rcx
0000000140004817  48c1ea1f                          shr rdx, 0x1f
000000014000481b  4833d1                            xor rdx, rcx
000000014000481e  488bca                            mov rcx, rdx
0000000140004821  488bc2                            mov rax, rdx
0000000140004824  48c1e928                          shr rcx, 0x28
0000000140004828  48c1e818                          shr rax, 0x18
000000014000482c  32c8                              xor cl, al
000000014000482e  488bc2                            mov rax, rdx
0000000140004831  48c1e808                          shr rax, 8
0000000140004835  32c8                              xor cl, al
0000000140004837  32ca                              xor cl, dl
0000000140004839  41320c38                          xor cl, byte ptr [r8 + rdi]
000000014000483d  4180fb10                          cmp r11b, 0x10
0000000140004841  0f8337120000                      jae 0x140005a7e
0000000140004847  410fb6c3                          movzx eax, r11b
000000014000484b  488d542450                        lea rdx, [rsp + 0x50]
0000000140004850  488d14c2                          lea rdx, [rdx + rax*8]
0000000140004854  488b02                            mov rax, qword ptr [rdx]
0000000140004857  83e13f                            and ecx, 0x3f
000000014000485a  7403                              je 0x14000485f
000000014000485c  48d3c8                            ror rax, cl
000000014000485f  488902                            mov qword ptr [rdx], rax
0000000140004862  e920120000                        jmp 0x140005a87
0000000140004867  418bc1                            mov eax, r9d
000000014000486a  48bbb9e5e41c6d4758bf              movabs rbx, 0xbf58476d1ce4e5b9
0000000140004874  493bc2                            cmp rax, r10
0000000140004877  720a                              jb 0x140004883
0000000140004879  c644244001                        mov byte ptr [rsp + 0x40], 1
000000014000487e  4532db                            xor r11b, r11b
0000000140004881  eb71                              jmp 0x1400048f4
0000000140004883  418bc1                            mov eax, r9d
0000000140004886  8bc8                              mov ecx, eax
0000000140004888  448bc0                            mov r8d, eax
000000014000488b  490fafcf                          imul rcx, r15
000000014000488f  448d4801                          lea r9d, [rax + 1]
0000000140004893  48c1e020                          shl rax, 0x20
0000000140004897  4803ce                            add rcx, rsi
000000014000489a  44894c2430                        mov dword ptr [rsp + 0x30], r9d
000000014000489f  4833c8                            xor rcx, rax
00000001400048a2  488bc1                            mov rax, rcx
00000001400048a5  48c1e81e                          shr rax, 0x1e
00000001400048a9  4833c1                            xor rax, rcx
00000001400048ac  480fafc3                          imul rax, rbx
00000001400048b0  488bc8                            mov rcx, rax
00000001400048b3  48c1e91b                          shr rcx, 0x1b
00000001400048b7  4833c8                            xor rcx, rax
00000001400048ba  48b8eb113113bb49d094              movabs rax, 0x94d049bb133111eb
00000001400048c4  480fafc8                          imul rcx, rax
00000001400048c8  488bd1                            mov rdx, rcx
00000001400048cb  48c1ea1f                          shr rdx, 0x1f
00000001400048cf  4833d1                            xor rdx, rcx
00000001400048d2  4c8bda                            mov r11, rdx
00000001400048d5  488bc2                            mov rax, rdx
00000001400048d8  49c1eb28                          shr r11, 0x28
00000001400048dc  48c1e818                          shr rax, 0x18
00000001400048e0  4432d8                            xor r11b, al
00000001400048e3  488bc2                            mov rax, rdx
00000001400048e6  48c1e808                          shr rax, 8
00000001400048ea  4432d8                            xor r11b, al
00000001400048ed  4432da                            xor r11b, dl
00000001400048f0  45321c38                          xor r11b, byte ptr [r8 + rdi]
00000001400048f4  418bc1                            mov eax, r9d
00000001400048f7  493bc2                            cmp rax, r10
00000001400048fa  7209                              jb 0x140004905
00000001400048fc  c644244001                        mov byte ptr [rsp + 0x40], 1
0000000140004901  32c9                              xor cl, cl
0000000140004903  eb6e                              jmp 0x140004973
0000000140004905  418bc1                            mov eax, r9d
0000000140004908  8bc8                              mov ecx, eax
000000014000490a  448bc0                            mov r8d, eax
000000014000490d  490fafcf                          imul rcx, r15
0000000140004911  448d4801                          lea r9d, [rax + 1]
0000000140004915  48c1e020                          shl rax, 0x20
0000000140004919  4803ce                            add rcx, rsi
000000014000491c  44894c2430                        mov dword ptr [rsp + 0x30], r9d
0000000140004921  4833c8                            xor rcx, rax
0000000140004924  488bc1                            mov rax, rcx
0000000140004927  48c1e81e                          shr rax, 0x1e
000000014000492b  4833c1                            xor rax, rcx
000000014000492e  480fafc3                          imul rax, rbx
0000000140004932  488bc8                            mov rcx, rax
0000000140004935  48c1e91b                          shr rcx, 0x1b
0000000140004939  4833c8                            xor rcx, rax
000000014000493c  48b8eb113113bb49d094              movabs rax, 0x94d049bb133111eb
0000000140004946  480fafc8                          imul rcx, rax
000000014000494a  488bd1                            mov rdx, rcx
000000014000494d  48c1ea1f                          shr rdx, 0x1f
0000000140004951  4833d1                            xor rdx, rcx
0000000140004954  488bca                            mov rcx, rdx
0000000140004957  488bc2                            mov rax, rdx
000000014000495a  48c1e928                          shr rcx, 0x28
000000014000495e  48c1e818                          shr rax, 0x18
0000000140004962  32c8                              xor cl, al
0000000140004964  488bc2                            mov rax, rdx
0000000140004967  48c1e808                          shr rax, 8
000000014000496b  32c8                              xor cl, al
000000014000496d  32ca                              xor cl, dl
000000014000496f  41320c38                          xor cl, byte ptr [r8 + rdi]
0000000140004973  4180fb10                          cmp r11b, 0x10
0000000140004977  0f8301110000                      jae 0x140005a7e
000000014000497d  80f910                            cmp cl, 0x10
0000000140004980  0f83f8100000                      jae 0x140005a7e
0000000140004986  410fb6c3                          movzx eax, r11b
000000014000498a  4c8d442450                        lea r8, [rsp + 0x50]
000000014000498f  498b14c0                          mov rdx, qword ptr [r8 + rax*8]
0000000140004993  4d8d04c0                          lea r8, [r8 + rax*8]
0000000140004997  0fb6c1                            movzx eax, cl
000000014000499a  8b4cc450                          mov ecx, dword ptr [rsp + rax*8 + 0x50]
000000014000499e  83e13f                            and ecx, 0x3f
00000001400049a1  7403                              je 0x1400049a6
00000001400049a3  48d3c2                            rol rdx, cl
00000001400049a6  498910                            mov qword ptr [r8], rdx
00000001400049a9  e9d9100000                        jmp 0x140005a87
00000001400049ae  418bc1                            mov eax, r9d
00000001400049b1  48bbb9e5e41c6d4758bf              movabs rbx, 0xbf58476d1ce4e5b9
00000001400049bb  493bc2                            cmp rax, r10
00000001400049be  720a                              jb 0x1400049ca
00000001400049c0  c644244001                        mov byte ptr [rsp + 0x40], 1
00000001400049c5  4532db                            xor r11b, r11b
00000001400049c8  eb71                              jmp 0x140004a3b
00000001400049ca  418bc1                            mov eax, r9d
00000001400049cd  8bc8                              mov ecx, eax
00000001400049cf  448bc0                            mov r8d, eax
00000001400049d2  490fafcf                          imul rcx, r15
00000001400049d6  448d4801                          lea r9d, [rax + 1]
00000001400049da  48c1e020                          shl rax, 0x20
00000001400049de  4803ce                            add rcx, rsi
00000001400049e1  44894c2430                        mov dword ptr [rsp + 0x30], r9d
00000001400049e6  4833c8                            xor rcx, rax
00000001400049e9  488bc1                            mov rax, rcx
00000001400049ec  48c1e81e                          shr rax, 0x1e
00000001400049f0  4833c1                            xor rax, rcx
00000001400049f3  480fafc3                          imul rax, rbx
00000001400049f7  488bc8                            mov rcx, rax
00000001400049fa  48c1e91b                          shr rcx, 0x1b
00000001400049fe  4833c8                            xor rcx, rax
0000000140004a01  48b8eb113113bb49d094              movabs rax, 0x94d049bb133111eb
0000000140004a0b  480fafc8                          imul rcx, rax
0000000140004a0f  488bd1                            mov rdx, rcx
0000000140004a12  48c1ea1f                          shr rdx, 0x1f
0000000140004a16  4833d1                            xor rdx, rcx
0000000140004a19  4c8bda                            mov r11, rdx
0000000140004a1c  488bc2                            mov rax, rdx
0000000140004a1f  49c1eb28                          shr r11, 0x28
0000000140004a23  48c1e818                          shr rax, 0x18
0000000140004a27  4432d8                            xor r11b, al
0000000140004a2a  488bc2                            mov rax, rdx
0000000140004a2d  48c1e808                          shr rax, 8
0000000140004a31  4432d8                            xor r11b, al
0000000140004a34  4432da                            xor r11b, dl
0000000140004a37  45321c38                          xor r11b, byte ptr [r8 + rdi]
0000000140004a3b  418bc1                            mov eax, r9d
0000000140004a3e  493bc2                            cmp rax, r10
0000000140004a41  7209                              jb 0x140004a4c
0000000140004a43  c644244001                        mov byte ptr [rsp + 0x40], 1
0000000140004a48  32c9                              xor cl, cl
0000000140004a4a  eb6e                              jmp 0x140004aba
0000000140004a4c  418bc1                            mov eax, r9d
0000000140004a4f  8bc8                              mov ecx, eax
0000000140004a51  448bc0                            mov r8d, eax
0000000140004a54  490fafcf                          imul rcx, r15
0000000140004a58  448d4801                          lea r9d, [rax + 1]
0000000140004a5c  48c1e020                          shl rax, 0x20
0000000140004a60  4803ce                            add rcx, rsi
0000000140004a63  44894c2430                        mov dword ptr [rsp + 0x30], r9d
0000000140004a68  4833c8                            xor rcx, rax
0000000140004a6b  488bc1                            mov rax, rcx
0000000140004a6e  48c1e81e                          shr rax, 0x1e
0000000140004a72  4833c1                            xor rax, rcx
0000000140004a75  480fafc3                          imul rax, rbx
0000000140004a79  488bc8                            mov rcx, rax
0000000140004a7c  48c1e91b                          shr rcx, 0x1b
0000000140004a80  4833c8                            xor rcx, rax
0000000140004a83  48b8eb113113bb49d094              movabs rax, 0x94d049bb133111eb
0000000140004a8d  480fafc8                          imul rcx, rax
0000000140004a91  488bd1                            mov rdx, rcx
0000000140004a94  48c1ea1f                          shr rdx, 0x1f
0000000140004a98  4833d1                            xor rdx, rcx
0000000140004a9b  488bca                            mov rcx, rdx
0000000140004a9e  488bc2                            mov rax, rdx
0000000140004aa1  48c1e928                          shr rcx, 0x28
0000000140004aa5  48c1e818                          shr rax, 0x18
0000000140004aa9  32c8                              xor cl, al
0000000140004aab  488bc2                            mov rax, rdx
0000000140004aae  48c1e808                          shr rax, 8
0000000140004ab2  32c8                              xor cl, al
0000000140004ab4  32ca                              xor cl, dl
0000000140004ab6  41320c38                          xor cl, byte ptr [r8 + rdi]
0000000140004aba  4180fb10                          cmp r11b, 0x10
0000000140004abe  0f83ba0f0000                      jae 0x140005a7e
0000000140004ac4  80f940                            cmp cl, 0x40
0000000140004ac7  0f83b10f0000                      jae 0x140005a7e
0000000140004acd  410fb6c3                          movzx eax, r11b
0000000140004ad1  48d36cc450                        shr qword ptr [rsp + rax*8 + 0x50], cl
0000000140004ad6  e9ac0f0000                        jmp 0x140005a87
0000000140004adb  418bc1                            mov eax, r9d
0000000140004ade  48bbb9e5e41c6d4758bf              movabs rbx, 0xbf58476d1ce4e5b9
0000000140004ae8  493bc2                            cmp rax, r10
0000000140004aeb  720a                              jb 0x140004af7
0000000140004aed  c644244001                        mov byte ptr [rsp + 0x40], 1
0000000140004af2  4532db                            xor r11b, r11b
0000000140004af5  eb71                              jmp 0x140004b68
0000000140004af7  418bc1                            mov eax, r9d
0000000140004afa  8bc8                              mov ecx, eax
0000000140004afc  448bc0                            mov r8d, eax
0000000140004aff  490fafcf                          imul rcx, r15
0000000140004b03  448d4801                          lea r9d, [rax + 1]
0000000140004b07  48c1e020                          shl rax, 0x20
0000000140004b0b  4803ce                            add rcx, rsi
0000000140004b0e  44894c2430                        mov dword ptr [rsp + 0x30], r9d
0000000140004b13  4833c8                            xor rcx, rax
0000000140004b16  488bc1                            mov rax, rcx
0000000140004b19  48c1e81e                          shr rax, 0x1e
0000000140004b1d  4833c1                            xor rax, rcx
0000000140004b20  480fafc3                          imul rax, rbx
0000000140004b24  488bc8                            mov rcx, rax
0000000140004b27  48c1e91b                          shr rcx, 0x1b
0000000140004b2b  4833c8                            xor rcx, rax
0000000140004b2e  48b8eb113113bb49d094              movabs rax, 0x94d049bb133111eb
0000000140004b38  480fafc8                          imul rcx, rax
0000000140004b3c  488bd1                            mov rdx, rcx
0000000140004b3f  48c1ea1f                          shr rdx, 0x1f
0000000140004b43  4833d1                            xor rdx, rcx
0000000140004b46  4c8bda                            mov r11, rdx
0000000140004b49  488bc2                            mov rax, rdx
0000000140004b4c  49c1eb28                          shr r11, 0x28
0000000140004b50  48c1e818                          shr rax, 0x18
0000000140004b54  4432d8                            xor r11b, al
0000000140004b57  488bc2                            mov rax, rdx
0000000140004b5a  48c1e808                          shr rax, 8
0000000140004b5e  4432d8                            xor r11b, al
0000000140004b61  4432da                            xor r11b, dl
0000000140004b64  45321c38                          xor r11b, byte ptr [r8 + rdi]
0000000140004b68  418bc1                            mov eax, r9d
0000000140004b6b  493bc2                            cmp rax, r10
0000000140004b6e  7209                              jb 0x140004b79
0000000140004b70  c644244001                        mov byte ptr [rsp + 0x40], 1
0000000140004b75  32c9                              xor cl, cl
0000000140004b77  eb6e                              jmp 0x140004be7
0000000140004b79  418bc1                            mov eax, r9d
0000000140004b7c  8bc8                              mov ecx, eax
0000000140004b7e  448bc0                            mov r8d, eax
0000000140004b81  490fafcf                          imul rcx, r15
0000000140004b85  448d4801                          lea r9d, [rax + 1]
0000000140004b89  48c1e020                          shl rax, 0x20
0000000140004b8d  4803ce                            add rcx, rsi
0000000140004b90  44894c2430                        mov dword ptr [rsp + 0x30], r9d
0000000140004b95  4833c8                            xor rcx, rax
0000000140004b98  488bc1                            mov rax, rcx
0000000140004b9b  48c1e81e                          shr rax, 0x1e
0000000140004b9f  4833c1                            xor rax, rcx
0000000140004ba2  480fafc3                          imul rax, rbx
0000000140004ba6  488bc8                            mov rcx, rax
0000000140004ba9  48c1e91b                          shr rcx, 0x1b
0000000140004bad  4833c8                            xor rcx, rax
0000000140004bb0  48b8eb113113bb49d094              movabs rax, 0x94d049bb133111eb
0000000140004bba  480fafc8                          imul rcx, rax
0000000140004bbe  488bd1                            mov rdx, rcx
0000000140004bc1  48c1ea1f                          shr rdx, 0x1f
0000000140004bc5  4833d1                            xor rdx, rcx
0000000140004bc8  488bca                            mov rcx, rdx
0000000140004bcb  488bc2                            mov rax, rdx
0000000140004bce  48c1e928                          shr rcx, 0x28
0000000140004bd2  48c1e818                          shr rax, 0x18
0000000140004bd6  32c8                              xor cl, al
0000000140004bd8  488bc2                            mov rax, rdx
0000000140004bdb  48c1e808                          shr rax, 8
0000000140004bdf  32c8                              xor cl, al
0000000140004be1  32ca                              xor cl, dl
0000000140004be3  41320c38                          xor cl, byte ptr [r8 + rdi]
0000000140004be7  4180fb10                          cmp r11b, 0x10
0000000140004beb  0f838d0e0000                      jae 0x140005a7e
0000000140004bf1  80f940                            cmp cl, 0x40
0000000140004bf4  0f83840e0000                      jae 0x140005a7e
0000000140004bfa  410fb6c3                          movzx eax, r11b
0000000140004bfe  48d364c450                        shl qword ptr [rsp + rax*8 + 0x50], cl
0000000140004c03  e97f0e0000                        jmp 0x140005a87
0000000140004c08  418bc1                            mov eax, r9d
0000000140004c0b  493bc2                            cmp rax, r10
0000000140004c0e  7221                              jb 0x140004c31
0000000140004c10  488d4c2420                        lea rcx, [rsp + 0x20]
0000000140004c15  c644244001                        mov byte ptr [rsp + 0x40], 1
0000000140004c1a  32db                              xor bl, bl
0000000140004c1c  e81fd6ffff                        call 0x140002240
0000000140004c21  488bc8                            mov rcx, rax
0000000140004c24  0fb6c3                            movzx eax, bl
0000000140004c27  48214cc450                        and qword ptr [rsp + rax*8 + 0x50], rcx
0000000140004c2c  e901f0ffff                        jmp 0x140003c32
0000000140004c31  418d4101                          lea eax, [r9 + 1]
0000000140004c35  418bc9                            mov ecx, r9d
0000000140004c38  89442430                          mov dword ptr [rsp + 0x30], eax
0000000140004c3c  490fafcf                          imul rcx, r15
0000000140004c40  418bc1                            mov eax, r9d
0000000140004c43  48c1e020                          shl rax, 0x20
0000000140004c47  4803ce                            add rcx, rsi
0000000140004c4a  4833c8                            xor rcx, rax
0000000140004c4d  458bc1                            mov r8d, r9d
0000000140004c50  488bc1                            mov rax, rcx
0000000140004c53  48c1e81e                          shr rax, 0x1e
0000000140004c57  4833c1                            xor rax, rcx
0000000140004c5a  48b9b9e5e41c6d4758bf              movabs rcx, 0xbf58476d1ce4e5b9
0000000140004c64  480fafc1                          imul rax, rcx
0000000140004c68  488bc8                            mov rcx, rax
0000000140004c6b  48c1e91b                          shr rcx, 0x1b
0000000140004c6f  4833c8                            xor rcx, rax
0000000140004c72  48b8eb113113bb49d094              movabs rax, 0x94d049bb133111eb
0000000140004c7c  480fafc8                          imul rcx, rax
0000000140004c80  488bd1                            mov rdx, rcx
0000000140004c83  48c1ea1f                          shr rdx, 0x1f
0000000140004c87  4833d1                            xor rdx, rcx
0000000140004c8a  488d4c2420                        lea rcx, [rsp + 0x20]
0000000140004c8f  488bda                            mov rbx, rdx
0000000140004c92  488bc2                            mov rax, rdx
0000000140004c95  48c1eb28                          shr rbx, 0x28
0000000140004c99  48c1e818                          shr rax, 0x18
0000000140004c9d  32d8                              xor bl, al
0000000140004c9f  488bc2                            mov rax, rdx
0000000140004ca2  48c1e808                          shr rax, 8
0000000140004ca6  32d8                              xor bl, al
0000000140004ca8  32da                              xor bl, dl
0000000140004caa  41321c38                          xor bl, byte ptr [r8 + rdi]
0000000140004cae  e88dd5ffff                        call 0x140002240
0000000140004cb3  488bc8                            mov rcx, rax
0000000140004cb6  80fb10                            cmp bl, 0x10
0000000140004cb9  0f83ab0d0000                      jae 0x140005a6a
0000000140004cbf  0fb6c3                            movzx eax, bl
0000000140004cc2  48214cc450                        and qword ptr [rsp + rax*8 + 0x50], rcx
0000000140004cc7  e966efffff                        jmp 0x140003c32
0000000140004ccc  418bc1                            mov eax, r9d
0000000140004ccf  48bbb9e5e41c6d4758bf              movabs rbx, 0xbf58476d1ce4e5b9
0000000140004cd9  493bc2                            cmp rax, r10
0000000140004cdc  720a                              jb 0x140004ce8
0000000140004cde  c644244001                        mov byte ptr [rsp + 0x40], 1
0000000140004ce3  4532db                            xor r11b, r11b
0000000140004ce6  eb71                              jmp 0x140004d59
0000000140004ce8  418bc1                            mov eax, r9d
0000000140004ceb  8bc8                              mov ecx, eax
0000000140004ced  448bc0                            mov r8d, eax
0000000140004cf0  490fafcf                          imul rcx, r15
0000000140004cf4  448d4801                          lea r9d, [rax + 1]
0000000140004cf8  48c1e020                          shl rax, 0x20
0000000140004cfc  4803ce                            add rcx, rsi
0000000140004cff  44894c2430                        mov dword ptr [rsp + 0x30], r9d
0000000140004d04  4833c8                            xor rcx, rax
0000000140004d07  488bc1                            mov rax, rcx
0000000140004d0a  48c1e81e                          shr rax, 0x1e
0000000140004d0e  4833c1                            xor rax, rcx
0000000140004d11  480fafc3                          imul rax, rbx
0000000140004d15  488bc8                            mov rcx, rax
0000000140004d18  48c1e91b                          shr rcx, 0x1b
0000000140004d1c  4833c8                            xor rcx, rax
0000000140004d1f  48b8eb113113bb49d094              movabs rax, 0x94d049bb133111eb
0000000140004d29  480fafc8                          imul rcx, rax
0000000140004d2d  488bd1                            mov rdx, rcx
0000000140004d30  48c1ea1f                          shr rdx, 0x1f
0000000140004d34  4833d1                            xor rdx, rcx
0000000140004d37  4c8bda                            mov r11, rdx
0000000140004d3a  488bc2                            mov rax, rdx
0000000140004d3d  49c1eb28                          shr r11, 0x28
0000000140004d41  48c1e818                          shr rax, 0x18
0000000140004d45  4432d8                            xor r11b, al
0000000140004d48  488bc2                            mov rax, rdx
0000000140004d4b  48c1e808                          shr rax, 8
0000000140004d4f  4432d8                            xor r11b, al
0000000140004d52  4432da                            xor r11b, dl
0000000140004d55  45321c38                          xor r11b, byte ptr [r8 + rdi]
0000000140004d59  418bc1                            mov eax, r9d
0000000140004d5c  493bc2                            cmp rax, r10
0000000140004d5f  7209                              jb 0x140004d6a
0000000140004d61  c644244001                        mov byte ptr [rsp + 0x40], 1
0000000140004d66  32c9                              xor cl, cl
0000000140004d68  eb6e                              jmp 0x140004dd8
0000000140004d6a  418bc1                            mov eax, r9d
0000000140004d6d  8bc8                              mov ecx, eax
0000000140004d6f  448bc0                            mov r8d, eax
0000000140004d72  490fafcf                          imul rcx, r15
0000000140004d76  448d4801                          lea r9d, [rax + 1]
0000000140004d7a  48c1e020                          shl rax, 0x20
0000000140004d7e  4803ce                            add rcx, rsi
0000000140004d81  44894c2430                        mov dword ptr [rsp + 0x30], r9d
0000000140004d86  4833c8                            xor rcx, rax
0000000140004d89  488bc1                            mov rax, rcx
0000000140004d8c  48c1e81e                          shr rax, 0x1e
0000000140004d90  4833c1                            xor rax, rcx
0000000140004d93  480fafc3                          imul rax, rbx
0000000140004d97  488bc8                            mov rcx, rax
0000000140004d9a  48c1e91b                          shr rcx, 0x1b
0000000140004d9e  4833c8                            xor rcx, rax
0000000140004da1  48b8eb113113bb49d094              movabs rax, 0x94d049bb133111eb
0000000140004dab  480fafc8                          imul rcx, rax
0000000140004daf  488bd1                            mov rdx, rcx
0000000140004db2  48c1ea1f                          shr rdx, 0x1f
0000000140004db6  4833d1                            xor rdx, rcx
0000000140004db9  488bca                            mov rcx, rdx
0000000140004dbc  488bc2                            mov rax, rdx
0000000140004dbf  48c1e928                          shr rcx, 0x28
0000000140004dc3  48c1e818                          shr rax, 0x18
0000000140004dc7  32c8                              xor cl, al
0000000140004dc9  488bc2                            mov rax, rdx
0000000140004dcc  48c1e808                          shr rax, 8
0000000140004dd0  32c8                              xor cl, al
0000000140004dd2  32ca                              xor cl, dl
0000000140004dd4  41320c38                          xor cl, byte ptr [r8 + rdi]
0000000140004dd8  4180fb10                          cmp r11b, 0x10
0000000140004ddc  0f839c0c0000                      jae 0x140005a7e
0000000140004de2  80f910                            cmp cl, 0x10
0000000140004de5  0f83930c0000                      jae 0x140005a7e
0000000140004deb  410fb6c3                          movzx eax, r11b
0000000140004def  488d542450                        lea rdx, [rsp + 0x50]
0000000140004df4  488d14c2                          lea rdx, [rdx + rax*8]
0000000140004df8  0fb6c1                            movzx eax, cl
0000000140004dfb  488b4cc450                        mov rcx, qword ptr [rsp + rax*8 + 0x50]
0000000140004e00  48090a                            or qword ptr [rdx], rcx
0000000140004e03  e97f0c0000                        jmp 0x140005a87
0000000140004e08  418bc1                            mov eax, r9d
0000000140004e0b  48bbeb113113bb49d094              movabs rbx, 0x94d049bb133111eb
0000000140004e15  49beb9e5e41c6d4758bf              movabs r14, 0xbf58476d1ce4e5b9
0000000140004e1f  493bc2                            cmp rax, r10
0000000140004e22  720a                              jb 0x140004e2e
0000000140004e24  c644244001                        mov byte ptr [rsp + 0x40], 1
0000000140004e29  4532db                            xor r11b, r11b
0000000140004e2c  eb67                              jmp 0x140004e95
0000000140004e2e  418bc1                            mov eax, r9d
0000000140004e31  8bc8                              mov ecx, eax
0000000140004e33  448bc0                            mov r8d, eax
0000000140004e36  490fafcf                          imul rcx, r15
0000000140004e3a  448d4801                          lea r9d, [rax + 1]
0000000140004e3e  48c1e020                          shl rax, 0x20
0000000140004e42  4803ce                            add rcx, rsi
0000000140004e45  44894c2430                        mov dword ptr [rsp + 0x30], r9d
0000000140004e4a  4833c8                            xor rcx, rax
0000000140004e4d  488bc1                            mov rax, rcx
0000000140004e50  48c1e81e                          shr rax, 0x1e
0000000140004e54  4833c1                            xor rax, rcx
0000000140004e57  490fafc6                          imul rax, r14
0000000140004e5b  488bc8                            mov rcx, rax
0000000140004e5e  48c1e91b                          shr rcx, 0x1b
0000000140004e62  4833c8                            xor rcx, rax
0000000140004e65  480fafcb                          imul rcx, rbx
0000000140004e69  488bd1                            mov rdx, rcx
0000000140004e6c  48c1ea1f                          shr rdx, 0x1f
0000000140004e70  4833d1                            xor rdx, rcx
0000000140004e73  4c8bda                            mov r11, rdx
0000000140004e76  488bc2                            mov rax, rdx
0000000140004e79  49c1eb28                          shr r11, 0x28
0000000140004e7d  48c1e818                          shr rax, 0x18
0000000140004e81  4432d8                            xor r11b, al
0000000140004e84  488bc2                            mov rax, rdx
0000000140004e87  48c1e808                          shr rax, 8
0000000140004e8b  4432d8                            xor r11b, al
0000000140004e8e  4432da                            xor r11b, dl
0000000140004e91  45321c38                          xor r11b, byte ptr [r8 + rdi]
0000000140004e95  418bc1                            mov eax, r9d
0000000140004e98  493bc2                            cmp rax, r10
0000000140004e9b  7209                              jb 0x140004ea6
0000000140004e9d  c644244001                        mov byte ptr [rsp + 0x40], 1
0000000140004ea2  32db                              xor bl, bl
0000000140004ea4  eb64                              jmp 0x140004f0a
0000000140004ea6  418bc1                            mov eax, r9d
0000000140004ea9  8bc8                              mov ecx, eax
0000000140004eab  448bc0                            mov r8d, eax
0000000140004eae  490fafcf                          imul rcx, r15
0000000140004eb2  448d4801                          lea r9d, [rax + 1]
0000000140004eb6  48c1e020                          shl rax, 0x20
0000000140004eba  4803ce                            add rcx, rsi
0000000140004ebd  44894c2430                        mov dword ptr [rsp + 0x30], r9d
0000000140004ec2  4833c8                            xor rcx, rax
0000000140004ec5  488bc1                            mov rax, rcx
0000000140004ec8  48c1e81e                          shr rax, 0x1e
0000000140004ecc  4833c1                            xor rax, rcx
0000000140004ecf  490fafc6                          imul rax, r14
0000000140004ed3  488bc8                            mov rcx, rax
0000000140004ed6  48c1e91b                          shr rcx, 0x1b
0000000140004eda  4833c8                            xor rcx, rax
0000000140004edd  480fafcb                          imul rcx, rbx
0000000140004ee1  488bd1                            mov rdx, rcx
0000000140004ee4  48c1ea1f                          shr rdx, 0x1f
0000000140004ee8  4833d1                            xor rdx, rcx
0000000140004eeb  488bda                            mov rbx, rdx
0000000140004eee  488bc2                            mov rax, rdx
0000000140004ef1  48c1eb28                          shr rbx, 0x28
0000000140004ef5  48c1e818                          shr rax, 0x18
0000000140004ef9  32d8                              xor bl, al
0000000140004efb  488bc2                            mov rax, rdx
0000000140004efe  48c1e808                          shr rax, 8
0000000140004f02  32d8                              xor bl, al
0000000140004f04  32da                              xor bl, dl
0000000140004f06  41321c38                          xor bl, byte ptr [r8 + rdi]
0000000140004f0a  418bc1                            mov eax, r9d
0000000140004f0d  493bc2                            cmp rax, r10
0000000140004f10  720a                              jb 0x140004f1c
0000000140004f12  c644244001                        mov byte ptr [rsp + 0x40], 1
0000000140004f17  4532f6                            xor r14b, r14b
0000000140004f1a  eb71                              jmp 0x140004f8d
0000000140004f1c  418bc1                            mov eax, r9d
0000000140004f1f  8bc8                              mov ecx, eax
0000000140004f21  448bc0                            mov r8d, eax
0000000140004f24  490fafcf                          imul rcx, r15
0000000140004f28  448d4801                          lea r9d, [rax + 1]
0000000140004f2c  48c1e020                          shl rax, 0x20
0000000140004f30  4803ce                            add rcx, rsi
0000000140004f33  44894c2430                        mov dword ptr [rsp + 0x30], r9d
0000000140004f38  4833c8                            xor rcx, rax
0000000140004f3b  488bc1                            mov rax, rcx
0000000140004f3e  48c1e81e                          shr rax, 0x1e
0000000140004f42  4833c1                            xor rax, rcx
0000000140004f45  490fafc6                          imul rax, r14
0000000140004f49  488bc8                            mov rcx, rax
0000000140004f4c  48c1e91b                          shr rcx, 0x1b
0000000140004f50  4833c8                            xor rcx, rax
0000000140004f53  48b8eb113113bb49d094              movabs rax, 0x94d049bb133111eb
0000000140004f5d  480fafc8                          imul rcx, rax
0000000140004f61  488bd1                            mov rdx, rcx
0000000140004f64  48c1ea1f                          shr rdx, 0x1f
0000000140004f68  4833d1                            xor rdx, rcx
0000000140004f6b  4c8bf2                            mov r14, rdx
0000000140004f6e  488bc2                            mov rax, rdx
0000000140004f71  49c1ee28                          shr r14, 0x28
0000000140004f75  48c1e818                          shr rax, 0x18
0000000140004f79  4432f0                            xor r14b, al
0000000140004f7c  488bc2                            mov rax, rdx
0000000140004f7f  48c1e808                          shr rax, 8
0000000140004f83  4432f0                            xor r14b, al
0000000140004f86  4432f2                            xor r14b, dl
0000000140004f89  45323438                          xor r14b, byte ptr [r8 + rdi]
0000000140004f8d  418bc1                            mov eax, r9d
0000000140004f90  493bc2                            cmp rax, r10
0000000140004f93  720a                              jb 0x140004f9f
0000000140004f95  c644244001                        mov byte ptr [rsp + 0x40], 1
0000000140004f9a  4532ff                            xor r15b, r15b
0000000140004f9d  eb7b                              jmp 0x14000501a
0000000140004f9f  418bc1                            mov eax, r9d
0000000140004fa2  8bc8                              mov ecx, eax
0000000140004fa4  448bc0                            mov r8d, eax
0000000140004fa7  490fafcf                          imul rcx, r15
0000000140004fab  448d4801                          lea r9d, [rax + 1]
0000000140004faf  48c1e020                          shl rax, 0x20
0000000140004fb3  4803ce                            add rcx, rsi
0000000140004fb6  44894c2430                        mov dword ptr [rsp + 0x30], r9d
0000000140004fbb  4833c8                            xor rcx, rax
0000000140004fbe  488bc1                            mov rax, rcx
0000000140004fc1  48c1e81e                          shr rax, 0x1e
0000000140004fc5  4833c1                            xor rax, rcx
0000000140004fc8  48b9b9e5e41c6d4758bf              movabs rcx, 0xbf58476d1ce4e5b9
0000000140004fd2  480fafc1                          imul rax, rcx
0000000140004fd6  488bc8                            mov rcx, rax
0000000140004fd9  48c1e91b                          shr rcx, 0x1b
0000000140004fdd  4833c8                            xor rcx, rax
0000000140004fe0  48b8eb113113bb49d094              movabs rax, 0x94d049bb133111eb
0000000140004fea  480fafc8                          imul rcx, rax
0000000140004fee  488bd1                            mov rdx, rcx
0000000140004ff1  48c1ea1f                          shr rdx, 0x1f
0000000140004ff5  4833d1                            xor rdx, rcx
0000000140004ff8  4c8bfa                            mov r15, rdx
0000000140004ffb  488bc2                            mov rax, rdx
0000000140004ffe  49c1ef28                          shr r15, 0x28
0000000140005002  48c1e818                          shr rax, 0x18
0000000140005006  4432f8                            xor r15b, al
0000000140005009  488bc2                            mov rax, rdx
000000014000500c  48c1e808                          shr rax, 8
0000000140005010  4432f8                            xor r15b, al
0000000140005013  4432fa                            xor r15b, dl
0000000140005016  45323c38                          xor r15b, byte ptr [r8 + rdi]
000000014000501a  4180fb10                          cmp r11b, 0x10
000000014000501e  0f835a0a0000                      jae 0x140005a7e
0000000140005024  80fb10                            cmp bl, 0x10
0000000140005027  0f83510a0000                      jae 0x140005a7e
000000014000502d  4180fe38                          cmp r14b, 0x38
0000000140005031  0f87470a0000                      ja 0x140005a7e
0000000140005037  4180ff38                          cmp r15b, 0x38
000000014000503b  0f873d0a0000                      ja 0x140005a7e
0000000140005041  410fb6ce                          movzx ecx, r14b
0000000140005045  410fb6c3                          movzx eax, r11b
0000000140005049  4c8b742448                        mov r14, qword ptr [rsp + 0x48]
000000014000504e  4c8d442450                        lea r8, [rsp + 0x50]
0000000140005053  4d8d04c0                          lea r8, [r8 + rax*8]
0000000140005057  0fb6c3                            movzx eax, bl
000000014000505a  488b54c450                        mov rdx, qword ptr [rsp + rax*8 + 0x50]
000000014000505f  48d3ea                            shr rdx, cl
0000000140005062  410fb6cf                          movzx ecx, r15b
0000000140005066  0fb6c2                            movzx eax, dl
0000000140005069  410fb61406                        movzx edx, byte ptr [r14 + rax]
000000014000506e  48d3e2                            shl rdx, cl
0000000140005071  493110                            xor qword ptr [r8], rdx
0000000140005074  e90e0a0000                        jmp 0x140005a87
0000000140005079  418bc1                            mov eax, r9d
000000014000507c  48bbb9e5e41c6d4758bf              movabs rbx, 0xbf58476d1ce4e5b9
0000000140005086  493bc2                            cmp rax, r10
0000000140005089  720a                              jb 0x140005095
000000014000508b  c644244001                        mov byte ptr [rsp + 0x40], 1
0000000140005090  4532db                            xor r11b, r11b
0000000140005093  eb71                              jmp 0x140005106
0000000140005095  418bc1                            mov eax, r9d
0000000140005098  8bc8                              mov ecx, eax
000000014000509a  448bc0                            mov r8d, eax
000000014000509d  490fafcf                          imul rcx, r15
00000001400050a1  448d4801                          lea r9d, [rax + 1]
00000001400050a5  48c1e020                          shl rax, 0x20
00000001400050a9  4803ce                            add rcx, rsi
00000001400050ac  44894c2430                        mov dword ptr [rsp + 0x30], r9d
00000001400050b1  4833c8                            xor rcx, rax
00000001400050b4  488bc1                            mov rax, rcx
00000001400050b7  48c1e81e                          shr rax, 0x1e
00000001400050bb  4833c1                            xor rax, rcx
00000001400050be  480fafc3                          imul rax, rbx
00000001400050c2  488bc8                            mov rcx, rax
00000001400050c5  48c1e91b                          shr rcx, 0x1b
00000001400050c9  4833c8                            xor rcx, rax
00000001400050cc  48b8eb113113bb49d094              movabs rax, 0x94d049bb133111eb
00000001400050d6  480fafc8                          imul rcx, rax
00000001400050da  488bd1                            mov rdx, rcx
00000001400050dd  48c1ea1f                          shr rdx, 0x1f
00000001400050e1  4833d1                            xor rdx, rcx
00000001400050e4  4c8bda                            mov r11, rdx
00000001400050e7  488bc2                            mov rax, rdx
00000001400050ea  49c1eb28                          shr r11, 0x28
00000001400050ee  48c1e818                          shr rax, 0x18
00000001400050f2  4432d8                            xor r11b, al
00000001400050f5  488bc2                            mov rax, rdx
00000001400050f8  48c1e808                          shr rax, 8
00000001400050fc  4432d8                            xor r11b, al
00000001400050ff  4432da                            xor r11b, dl
0000000140005102  45321c38                          xor r11b, byte ptr [r8 + rdi]
0000000140005106  418bc1                            mov eax, r9d
0000000140005109  493bc2                            cmp rax, r10
000000014000510c  7209                              jb 0x140005117
000000014000510e  c644244001                        mov byte ptr [rsp + 0x40], 1
0000000140005113  32db                              xor bl, bl
0000000140005115  eb6e                              jmp 0x140005185
0000000140005117  418bc1                            mov eax, r9d
000000014000511a  8bc8                              mov ecx, eax
000000014000511c  448bc0                            mov r8d, eax
000000014000511f  490fafcf                          imul rcx, r15
0000000140005123  448d4801                          lea r9d, [rax + 1]
0000000140005127  48c1e020                          shl rax, 0x20
000000014000512b  4803ce                            add rcx, rsi
000000014000512e  44894c2430                        mov dword ptr [rsp + 0x30], r9d
0000000140005133  4833c8                            xor rcx, rax
0000000140005136  488bc1                            mov rax, rcx
0000000140005139  48c1e81e                          shr rax, 0x1e
000000014000513d  4833c1                            xor rax, rcx
0000000140005140  480fafc3                          imul rax, rbx
0000000140005144  488bc8                            mov rcx, rax
0000000140005147  48c1e91b                          shr rcx, 0x1b
000000014000514b  4833c8                            xor rcx, rax
000000014000514e  48b8eb113113bb49d094              movabs rax, 0x94d049bb133111eb
0000000140005158  480fafc8                          imul rcx, rax
000000014000515c  488bd1                            mov rdx, rcx
000000014000515f  48c1ea1f                          shr rdx, 0x1f
0000000140005163  4833d1                            xor rdx, rcx
0000000140005166  488bda                            mov rbx, rdx
0000000140005169  488bc2                            mov rax, rdx
000000014000516c  48c1eb28                          shr rbx, 0x28
0000000140005170  48c1e818                          shr rax, 0x18
0000000140005174  32d8                              xor bl, al
0000000140005176  488bc2                            mov rax, rdx
0000000140005179  48c1e808                          shr rax, 8
000000014000517d  32d8                              xor bl, al
000000014000517f  32da                              xor bl, dl
0000000140005181  41321c38                          xor bl, byte ptr [r8 + rdi]
0000000140005185  418bc1                            mov eax, r9d
0000000140005188  493bc2                            cmp rax, r10
000000014000518b  7209                              jb 0x140005196
000000014000518d  c644244001                        mov byte ptr [rsp + 0x40], 1
0000000140005192  32c9                              xor cl, cl
0000000140005194  eb78                              jmp 0x14000520e
0000000140005196  418bc1                            mov eax, r9d
0000000140005199  8bc8                              mov ecx, eax
000000014000519b  448bc0                            mov r8d, eax
000000014000519e  490fafcf                          imul rcx, r15
00000001400051a2  448d4801                          lea r9d, [rax + 1]
00000001400051a6  48c1e020                          shl rax, 0x20
00000001400051aa  4803ce                            add rcx, rsi
00000001400051ad  44894c2430                        mov dword ptr [rsp + 0x30], r9d
00000001400051b2  4833c8                            xor rcx, rax
00000001400051b5  488bc1                            mov rax, rcx
00000001400051b8  48c1e81e                          shr rax, 0x1e
00000001400051bc  4833c1                            xor rax, rcx
00000001400051bf  48b9b9e5e41c6d4758bf              movabs rcx, 0xbf58476d1ce4e5b9
00000001400051c9  480fafc1                          imul rax, rcx
00000001400051cd  488bc8                            mov rcx, rax
00000001400051d0  48c1e91b                          shr rcx, 0x1b
00000001400051d4  4833c8                            xor rcx, rax
00000001400051d7  48b8eb113113bb49d094              movabs rax, 0x94d049bb133111eb
00000001400051e1  480fafc8                          imul rcx, rax
00000001400051e5  488bd1                            mov rdx, rcx
00000001400051e8  48c1ea1f                          shr rdx, 0x1f
00000001400051ec  4833d1                            xor rdx, rcx
00000001400051ef  488bca                            mov rcx, rdx
00000001400051f2  488bc2                            mov rax, rdx
00000001400051f5  48c1e928                          shr rcx, 0x28
00000001400051f9  48c1e818                          shr rax, 0x18
00000001400051fd  32c8                              xor cl, al
00000001400051ff  488bc2                            mov rax, rdx
0000000140005202  48c1e808                          shr rax, 8
0000000140005206  32c8                              xor cl, al
0000000140005208  32ca                              xor cl, dl
000000014000520a  41320c38                          xor cl, byte ptr [r8 + rdi]
000000014000520e  4180fb10                          cmp r11b, 0x10
0000000140005212  0f8366080000                      jae 0x140005a7e
0000000140005218  80fb10                            cmp bl, 0x10
000000014000521b  0f835d080000                      jae 0x140005a7e
0000000140005221  80f938                            cmp cl, 0x38
0000000140005224  0f8754080000                      ja 0x140005a7e
000000014000522a  0fb6c3                            movzx eax, bl
000000014000522d  488b54c450                        mov rdx, qword ptr [rsp + rax*8 + 0x50]
0000000140005232  48d3ea                            shr rdx, cl
0000000140005235  0fb6c2                            movzx eax, dl
0000000140005238  410fb60c06                        movzx ecx, byte ptr [r14 + rax]
000000014000523d  410fb6c3                          movzx eax, r11b
0000000140005241  48894cc450                        mov qword ptr [rsp + rax*8 + 0x50], rcx
0000000140005246  e93c080000                        jmp 0x140005a87
000000014000524b  418bc1                            mov eax, r9d
000000014000524e  48bbb9e5e41c6d4758bf              movabs rbx, 0xbf58476d1ce4e5b9
0000000140005258  493bc2                            cmp rax, r10
000000014000525b  720a                              jb 0x140005267
000000014000525d  c644244001                        mov byte ptr [rsp + 0x40], 1
0000000140005262  4532db                            xor r11b, r11b
0000000140005265  eb71                              jmp 0x1400052d8
0000000140005267  418bc1                            mov eax, r9d
000000014000526a  8bc8                              mov ecx, eax
000000014000526c  448bc0                            mov r8d, eax
000000014000526f  490fafcf                          imul rcx, r15
0000000140005273  448d4801                          lea r9d, [rax + 1]
0000000140005277  48c1e020                          shl rax, 0x20
000000014000527b  4803ce                            add rcx, rsi
000000014000527e  44894c2430                        mov dword ptr [rsp + 0x30], r9d
0000000140005283  4833c8                            xor rcx, rax
0000000140005286  488bc1                            mov rax, rcx
0000000140005289  48c1e81e                          shr rax, 0x1e
000000014000528d  4833c1                            xor rax, rcx
0000000140005290  480fafc3                          imul rax, rbx
0000000140005294  488bc8                            mov rcx, rax
0000000140005297  48c1e91b                          shr rcx, 0x1b
000000014000529b  4833c8                            xor rcx, rax
000000014000529e  48b8eb113113bb49d094              movabs rax, 0x94d049bb133111eb
00000001400052a8  480fafc8                          imul rcx, rax
00000001400052ac  488bd1                            mov rdx, rcx
00000001400052af  48c1ea1f                          shr rdx, 0x1f
00000001400052b3  4833d1                            xor rdx, rcx
00000001400052b6  4c8bda                            mov r11, rdx
00000001400052b9  488bc2                            mov rax, rdx
00000001400052bc  49c1eb28                          shr r11, 0x28
00000001400052c0  48c1e818                          shr rax, 0x18
00000001400052c4  4432d8                            xor r11b, al
00000001400052c7  488bc2                            mov rax, rdx
00000001400052ca  48c1e808                          shr rax, 8
00000001400052ce  4432d8                            xor r11b, al
00000001400052d1  4432da                            xor r11b, dl
00000001400052d4  45321c38                          xor r11b, byte ptr [r8 + rdi]
00000001400052d8  418bc1                            mov eax, r9d
00000001400052db  493bc2                            cmp rax, r10
00000001400052de  7209                              jb 0x1400052e9
00000001400052e0  c644244001                        mov byte ptr [rsp + 0x40], 1
00000001400052e5  32c9                              xor cl, cl
00000001400052e7  eb6e                              jmp 0x140005357
00000001400052e9  418bc1                            mov eax, r9d
00000001400052ec  8bc8                              mov ecx, eax
00000001400052ee  448bc0                            mov r8d, eax
00000001400052f1  490fafcf                          imul rcx, r15
00000001400052f5  448d4801                          lea r9d, [rax + 1]
00000001400052f9  48c1e020                          shl rax, 0x20
00000001400052fd  4803ce                            add rcx, rsi
0000000140005300  44894c2430                        mov dword ptr [rsp + 0x30], r9d
0000000140005305  4833c8                            xor rcx, rax
0000000140005308  488bc1                            mov rax, rcx
000000014000530b  48c1e81e                          shr rax, 0x1e
000000014000530f  4833c1                            xor rax, rcx
0000000140005312  480fafc3                          imul rax, rbx
0000000140005316  488bc8                            mov rcx, rax
0000000140005319  48c1e91b                          shr rcx, 0x1b
000000014000531d  4833c8                            xor rcx, rax
0000000140005320  48b8eb113113bb49d094              movabs rax, 0x94d049bb133111eb
000000014000532a  480fafc8                          imul rcx, rax
000000014000532e  488bd1                            mov rdx, rcx
0000000140005331  48c1ea1f                          shr rdx, 0x1f
0000000140005335  4833d1                            xor rdx, rcx
0000000140005338  488bca                            mov rcx, rdx
000000014000533b  488bc2                            mov rax, rdx
000000014000533e  48c1e928                          shr rcx, 0x28
0000000140005342  48c1e818                          shr rax, 0x18
0000000140005346  32c8                              xor cl, al
0000000140005348  488bc2                            mov rax, rdx
000000014000534b  48c1e808                          shr rax, 8
000000014000534f  32c8                              xor cl, al
0000000140005351  32ca                              xor cl, dl
0000000140005353  41320c38                          xor cl, byte ptr [r8 + rdi]
0000000140005357  4180fb10                          cmp r11b, 0x10
000000014000535b  0f831d070000                      jae 0x140005a7e
0000000140005361  80f910                            cmp cl, 0x10
0000000140005364  0f8314070000                      jae 0x140005a7e
000000014000536a  0fb6c1                            movzx eax, cl
000000014000536d  410fb6cb                          movzx ecx, r11b
0000000140005371  488b44c450                        mov rax, qword ptr [rsp + rax*8 + 0x50]
0000000140005376  483944cc50                        cmp qword ptr [rsp + rcx*8 + 0x50], rax
000000014000537b  0f9445d0                          sete byte ptr [rbp - 0x30]
000000014000537f  e903070000                        jmp 0x140005a87
0000000140005384  418bc1                            mov eax, r9d
0000000140005387  48bbb9e5e41c6d4758bf              movabs rbx, 0xbf58476d1ce4e5b9
0000000140005391  493bc2                            cmp rax, r10
0000000140005394  720a                              jb 0x1400053a0
0000000140005396  c644244001                        mov byte ptr [rsp + 0x40], 1
000000014000539b  4532db                            xor r11b, r11b
000000014000539e  eb71                              jmp 0x140005411
00000001400053a0  418bc1                            mov eax, r9d
00000001400053a3  8bc8                              mov ecx, eax
00000001400053a5  448bc0                            mov r8d, eax
00000001400053a8  490fafcf                          imul rcx, r15
00000001400053ac  448d4801                          lea r9d, [rax + 1]
00000001400053b0  48c1e020                          shl rax, 0x20
00000001400053b4  4803ce                            add rcx, rsi
00000001400053b7  44894c2430                        mov dword ptr [rsp + 0x30], r9d
00000001400053bc  4833c8                            xor rcx, rax
00000001400053bf  488bc1                            mov rax, rcx
00000001400053c2  48c1e81e                          shr rax, 0x1e
00000001400053c6  4833c1                            xor rax, rcx
00000001400053c9  480fafc3                          imul rax, rbx
00000001400053cd  488bc8                            mov rcx, rax
00000001400053d0  48c1e91b                          shr rcx, 0x1b
00000001400053d4  4833c8                            xor rcx, rax
00000001400053d7  48b8eb113113bb49d094              movabs rax, 0x94d049bb133111eb
00000001400053e1  480fafc8                          imul rcx, rax
00000001400053e5  488bd1                            mov rdx, rcx
00000001400053e8  48c1ea1f                          shr rdx, 0x1f
00000001400053ec  4833d1                            xor rdx, rcx
00000001400053ef  4c8bda                            mov r11, rdx
00000001400053f2  488bc2                            mov rax, rdx
00000001400053f5  49c1eb28                          shr r11, 0x28
00000001400053f9  48c1e818                          shr rax, 0x18
00000001400053fd  4432d8                            xor r11b, al
0000000140005400  488bc2                            mov rax, rdx
0000000140005403  48c1e808                          shr rax, 8
0000000140005407  4432d8                            xor r11b, al
000000014000540a  4432da                            xor r11b, dl
000000014000540d  45321c38                          xor r11b, byte ptr [r8 + rdi]
0000000140005411  418bc1                            mov eax, r9d
0000000140005414  493bc2                            cmp rax, r10
0000000140005417  7209                              jb 0x140005422
0000000140005419  c644244001                        mov byte ptr [rsp + 0x40], 1
000000014000541e  32c9                              xor cl, cl
0000000140005420  eb6e                              jmp 0x140005490
0000000140005422  418bc1                            mov eax, r9d
0000000140005425  8bc8                              mov ecx, eax
0000000140005427  448bc0                            mov r8d, eax
000000014000542a  490fafcf                          imul rcx, r15
000000014000542e  448d4801                          lea r9d, [rax + 1]
0000000140005432  48c1e020                          shl rax, 0x20
0000000140005436  4803ce                            add rcx, rsi
0000000140005439  44894c2430                        mov dword ptr [rsp + 0x30], r9d
000000014000543e  4833c8                            xor rcx, rax
0000000140005441  488bc1                            mov rax, rcx
0000000140005444  48c1e81e                          shr rax, 0x1e
0000000140005448  4833c1                            xor rax, rcx
000000014000544b  480fafc3                          imul rax, rbx
000000014000544f  488bc8                            mov rcx, rax
0000000140005452  48c1e91b                          shr rcx, 0x1b
0000000140005456  4833c8                            xor rcx, rax
0000000140005459  48b8eb113113bb49d094              movabs rax, 0x94d049bb133111eb
0000000140005463  480fafc8                          imul rcx, rax
0000000140005467  488bd1                            mov rdx, rcx
000000014000546a  48c1ea1f                          shr rdx, 0x1f
000000014000546e  4833d1                            xor rdx, rcx
0000000140005471  488bca                            mov rcx, rdx
0000000140005474  488bc2                            mov rax, rdx
0000000140005477  48c1e928                          shr rcx, 0x28
000000014000547b  48c1e818                          shr rax, 0x18
000000014000547f  32c8                              xor cl, al
0000000140005481  488bc2                            mov rax, rdx
0000000140005484  48c1e808                          shr rax, 8
0000000140005488  32c8                              xor cl, al
000000014000548a  32ca                              xor cl, dl
000000014000548c  41320c38                          xor cl, byte ptr [r8 + rdi]
0000000140005490  4180fb10                          cmp r11b, 0x10
0000000140005494  0f83e4050000                      jae 0x140005a7e
000000014000549a  80f910                            cmp cl, 0x10
000000014000549d  0f83db050000                      jae 0x140005a7e
00000001400054a3  0fb6c1                            movzx eax, cl
00000001400054a6  410fb6cb                          movzx ecx, r11b
00000001400054aa  488b44c450                        mov rax, qword ptr [rsp + rax*8 + 0x50]
00000001400054af  483944cc50                        cmp qword ptr [rsp + rcx*8 + 0x50], rax
00000001400054b4  0f9545d0                          setne byte ptr [rbp - 0x30]
00000001400054b8  e9ca050000                        jmp 0x140005a87
00000001400054bd  488d4c2420                        lea rcx, [rsp + 0x20]
00000001400054c2  e839cbffff                        call 0x140002000
00000001400054c7  807dd000                          cmp byte ptr [rbp - 0x30], 0
00000001400054cb  0f8461e7ffff                      je 0x140003c32
00000001400054d1  448b4c2430                        mov r9d, dword ptr [rsp + 0x30]
00000001400054d6  4c8b542428                        mov r10, qword ptr [rsp + 0x28]
00000001400054db  4863d0                            movsxd rdx, eax
00000001400054de  4903d1                            add rdx, r9
00000001400054e1  783d                              js 0x140005520
00000001400054e3  493bd2                            cmp rdx, r10
00000001400054e6  7738                              ja 0x140005520
00000001400054e8  488b742438                        mov rsi, qword ptr [rsp + 0x38]
00000001400054ed  448bca                            mov r9d, edx
00000001400054f0  488b7c2420                        mov rdi, qword ptr [rsp + 0x20]
00000001400054f5  89542430                          mov dword ptr [rsp + 0x30], edx
00000001400054f9  e989050000                        jmp 0x140005a87
00000001400054fe  488d4c2420                        lea rcx, [rsp + 0x20]
0000000140005503  e8f8caffff                        call 0x140002000
0000000140005508  807dd000                          cmp byte ptr [rbp - 0x30], 0
000000014000550c  0f8520e7ffff                      jne 0x140003c32
0000000140005512  ebbd                              jmp 0x1400054d1
0000000140005514  488d4c2420                        lea rcx, [rsp + 0x20]
0000000140005519  e8e2caffff                        call 0x140002000
000000014000551e  ebb1                              jmp 0x1400054d1
0000000140005520  488b742438                        mov rsi, qword ptr [rsp + 0x38]
0000000140005525  488b7c2420                        mov rdi, qword ptr [rsp + 0x20]
000000014000552a  c644244001                        mov byte ptr [rsp + 0x40], 1
000000014000552f  e953050000                        jmp 0x140005a87
0000000140005534  418bc1                            mov eax, r9d
0000000140005537  48bbb9e5e41c6d4758bf              movabs rbx, 0xbf58476d1ce4e5b9
0000000140005541  493bc2                            cmp rax, r10
0000000140005544  720a                              jb 0x140005550
0000000140005546  c644244001                        mov byte ptr [rsp + 0x40], 1
000000014000554b  4532db                            xor r11b, r11b
000000014000554e  eb71                              jmp 0x1400055c1
0000000140005550  418bc1                            mov eax, r9d
0000000140005553  8bc8                              mov ecx, eax
0000000140005555  448bc0                            mov r8d, eax
0000000140005558  490fafcf                          imul rcx, r15
000000014000555c  448d4801                          lea r9d, [rax + 1]
0000000140005560  48c1e020                          shl rax, 0x20
0000000140005564  4803ce                            add rcx, rsi
0000000140005567  44894c2430                        mov dword ptr [rsp + 0x30], r9d
000000014000556c  4833c8                            xor rcx, rax
000000014000556f  488bc1                            mov rax, rcx
0000000140005572  48c1e81e                          shr rax, 0x1e
0000000140005576  4833c1                            xor rax, rcx
0000000140005579  480fafc3                          imul rax, rbx
000000014000557d  488bc8                            mov rcx, rax
0000000140005580  48c1e91b                          shr rcx, 0x1b
0000000140005584  4833c8                            xor rcx, rax
0000000140005587  48b8eb113113bb49d094              movabs rax, 0x94d049bb133111eb
0000000140005591  480fafc8                          imul rcx, rax
0000000140005595  488bd1                            mov rdx, rcx
0000000140005598  48c1ea1f                          shr rdx, 0x1f
000000014000559c  4833d1                            xor rdx, rcx
000000014000559f  4c8bda                            mov r11, rdx
00000001400055a2  488bc2                            mov rax, rdx
00000001400055a5  49c1eb28                          shr r11, 0x28
00000001400055a9  48c1e818                          shr rax, 0x18
00000001400055ad  4432d8                            xor r11b, al
00000001400055b0  488bc2                            mov rax, rdx
00000001400055b3  48c1e808                          shr rax, 8
00000001400055b7  4432d8                            xor r11b, al
00000001400055ba  4432da                            xor r11b, dl
00000001400055bd  45321c38                          xor r11b, byte ptr [r8 + rdi]
00000001400055c1  418bc1                            mov eax, r9d
00000001400055c4  493bc2                            cmp rax, r10
00000001400055c7  7209                              jb 0x1400055d2
00000001400055c9  c644244001                        mov byte ptr [rsp + 0x40], 1
00000001400055ce  32c9                              xor cl, cl
00000001400055d0  eb6e                              jmp 0x140005640
00000001400055d2  418bc1                            mov eax, r9d
00000001400055d5  8bc8                              mov ecx, eax
00000001400055d7  448bc0                            mov r8d, eax
00000001400055da  490fafcf                          imul rcx, r15
00000001400055de  448d4801                          lea r9d, [rax + 1]
00000001400055e2  48c1e020                          shl rax, 0x20
00000001400055e6  4803ce                            add rcx, rsi
00000001400055e9  44894c2430                        mov dword ptr [rsp + 0x30], r9d
00000001400055ee  4833c8                            xor rcx, rax
00000001400055f1  488bc1                            mov rax, rcx
00000001400055f4  48c1e81e                          shr rax, 0x1e
00000001400055f8  4833c1                            xor rax, rcx
00000001400055fb  480fafc3                          imul rax, rbx
00000001400055ff  488bc8                            mov rcx, rax
0000000140005602  48c1e91b                          shr rcx, 0x1b
0000000140005606  4833c8                            xor rcx, rax
0000000140005609  48b8eb113113bb49d094              movabs rax, 0x94d049bb133111eb
0000000140005613  480fafc8                          imul rcx, rax
0000000140005617  488bd1                            mov rdx, rcx
000000014000561a  48c1ea1f                          shr rdx, 0x1f
000000014000561e  4833d1                            xor rdx, rcx
0000000140005621  488bca                            mov rcx, rdx
0000000140005624  488bc2                            mov rax, rdx
0000000140005627  48c1e928                          shr rcx, 0x28
000000014000562b  48c1e818                          shr rax, 0x18
000000014000562f  32c8                              xor cl, al
0000000140005631  488bc2                            mov rax, rdx
0000000140005634  48c1e808                          shr rax, 8
0000000140005638  32c8                              xor cl, al
000000014000563a  32ca                              xor cl, dl
000000014000563c  41320c38                          xor cl, byte ptr [r8 + rdi]
0000000140005640  4180fb10                          cmp r11b, 0x10
0000000140005644  0f8334040000                      jae 0x140005a7e
000000014000564a  80f910                            cmp cl, 0x10
000000014000564d  0f832b040000                      jae 0x140005a7e
0000000140005653  410fb6c3                          movzx eax, r11b
0000000140005657  488d542450                        lea rdx, [rsp + 0x50]
000000014000565c  4c8b04c2                          mov r8, qword ptr [rdx + rax*8]
0000000140005660  488d14c2                          lea rdx, [rdx + rax*8]
0000000140005664  0fb6c1                            movzx eax, cl
0000000140005667  488d4c2450                        lea rcx, [rsp + 0x50]
000000014000566c  488d0cc1                          lea rcx, [rcx + rax*8]
0000000140005670  488b01                            mov rax, qword ptr [rcx]
0000000140005673  488902                            mov qword ptr [rdx], rax
0000000140005676  4c8901                            mov qword ptr [rcx], r8
0000000140005679  e909040000                        jmp 0x140005a87
000000014000567e  418bc1                            mov eax, r9d
0000000140005681  493bc2                            cmp rax, r10
0000000140005684  721c                              jb 0x1400056a2
0000000140005686  32c9                              xor cl, cl
0000000140005688  c644244001                        mov byte ptr [rsp + 0x40], 1
000000014000568d  0fb6c1                            movzx eax, cl
0000000140005690  488d4c2450                        lea rcx, [rsp + 0x50]
0000000140005695  48f714c1                          not qword ptr [rcx + rax*8]
0000000140005699  488d0cc1                          lea rcx, [rcx + rax*8]
000000014000569d  e9e5030000                        jmp 0x140005a87
00000001400056a2  418bc1                            mov eax, r9d
00000001400056a5  8bc8                              mov ecx, eax
00000001400056a7  448bc0                            mov r8d, eax
00000001400056aa  490fafcf                          imul rcx, r15
00000001400056ae  448d4801                          lea r9d, [rax + 1]
00000001400056b2  48c1e020                          shl rax, 0x20
00000001400056b6  4803ce                            add rcx, rsi
00000001400056b9  44894c2430                        mov dword ptr [rsp + 0x30], r9d
00000001400056be  4833c8                            xor rcx, rax
00000001400056c1  488bc1                            mov rax, rcx
00000001400056c4  48c1e81e                          shr rax, 0x1e
00000001400056c8  4833c1                            xor rax, rcx
00000001400056cb  48b9b9e5e41c6d4758bf              movabs rcx, 0xbf58476d1ce4e5b9
00000001400056d5  480fafc1                          imul rax, rcx
00000001400056d9  488bc8                            mov rcx, rax
00000001400056dc  48c1e91b                          shr rcx, 0x1b
00000001400056e0  4833c8                            xor rcx, rax
00000001400056e3  48b8eb113113bb49d094              movabs rax, 0x94d049bb133111eb
00000001400056ed  480fafc8                          imul rcx, rax
00000001400056f1  488bd1                            mov rdx, rcx
00000001400056f4  48c1ea1f                          shr rdx, 0x1f
00000001400056f8  4833d1                            xor rdx, rcx
00000001400056fb  488bca                            mov rcx, rdx
00000001400056fe  488bc2                            mov rax, rdx
0000000140005701  48c1e928                          shr rcx, 0x28
0000000140005705  48c1e818                          shr rax, 0x18
0000000140005709  32c8                              xor cl, al
000000014000570b  488bc2                            mov rax, rdx
000000014000570e  48c1e808                          shr rax, 8
0000000140005712  32c8                              xor cl, al
0000000140005714  32ca                              xor cl, dl
0000000140005716  41320c38                          xor cl, byte ptr [r8 + rdi]
000000014000571a  80f910                            cmp cl, 0x10
000000014000571d  0f835b030000                      jae 0x140005a7e
0000000140005723  0fb6c1                            movzx eax, cl
0000000140005726  488d4c2450                        lea rcx, [rsp + 0x50]
000000014000572b  48f714c1                          not qword ptr [rcx + rax*8]
000000014000572f  488d0cc1                          lea rcx, [rcx + rax*8]
0000000140005733  e94f030000                        jmp 0x140005a87
0000000140005738  418bc1                            mov eax, r9d
000000014000573b  48bbb9e5e41c6d4758bf              movabs rbx, 0xbf58476d1ce4e5b9
0000000140005745  493bc2                            cmp rax, r10
0000000140005748  720a                              jb 0x140005754
000000014000574a  c644244001                        mov byte ptr [rsp + 0x40], 1
000000014000574f  4532db                            xor r11b, r11b
0000000140005752  eb71                              jmp 0x1400057c5
0000000140005754  418bc1                            mov eax, r9d
0000000140005757  8bc8                              mov ecx, eax
0000000140005759  448bc0                            mov r8d, eax
000000014000575c  490fafcf                          imul rcx, r15
0000000140005760  448d4801                          lea r9d, [rax + 1]
0000000140005764  48c1e020                          shl rax, 0x20
0000000140005768  4803ce                            add rcx, rsi
000000014000576b  44894c2430                        mov dword ptr [rsp + 0x30], r9d
0000000140005770  4833c8                            xor rcx, rax
0000000140005773  488bc1                            mov rax, rcx
0000000140005776  48c1e81e                          shr rax, 0x1e
000000014000577a  4833c1                            xor rax, rcx
000000014000577d  480fafc3                          imul rax, rbx
0000000140005781  488bc8                            mov rcx, rax
0000000140005784  48c1e91b                          shr rcx, 0x1b
0000000140005788  4833c8                            xor rcx, rax
000000014000578b  48b8eb113113bb49d094              movabs rax, 0x94d049bb133111eb
0000000140005795  480fafc8                          imul rcx, rax
0000000140005799  488bd1                            mov rdx, rcx
000000014000579c  48c1ea1f                          shr rdx, 0x1f
00000001400057a0  4833d1                            xor rdx, rcx
00000001400057a3  4c8bda                            mov r11, rdx
00000001400057a6  488bc2                            mov rax, rdx
00000001400057a9  49c1eb28                          shr r11, 0x28
00000001400057ad  48c1e818                          shr rax, 0x18
00000001400057b1  4432d8                            xor r11b, al
00000001400057b4  488bc2                            mov rax, rdx
00000001400057b7  48c1e808                          shr rax, 8
00000001400057bb  4432d8                            xor r11b, al
00000001400057be  4432da                            xor r11b, dl
00000001400057c1  45321c38                          xor r11b, byte ptr [r8 + rdi]
00000001400057c5  418bc1                            mov eax, r9d
00000001400057c8  493bc2                            cmp rax, r10
00000001400057cb  7209                              jb 0x1400057d6
00000001400057cd  c644244001                        mov byte ptr [rsp + 0x40], 1
00000001400057d2  32c9                              xor cl, cl
00000001400057d4  eb6e                              jmp 0x140005844
00000001400057d6  418bc1                            mov eax, r9d
00000001400057d9  8bc8                              mov ecx, eax
00000001400057db  448bc0                            mov r8d, eax
00000001400057de  490fafcf                          imul rcx, r15
00000001400057e2  448d4801                          lea r9d, [rax + 1]
00000001400057e6  48c1e020                          shl rax, 0x20
00000001400057ea  4803ce                            add rcx, rsi
00000001400057ed  44894c2430                        mov dword ptr [rsp + 0x30], r9d
00000001400057f2  4833c8                            xor rcx, rax
00000001400057f5  488bc1                            mov rax, rcx
00000001400057f8  48c1e81e                          shr rax, 0x1e
00000001400057fc  4833c1                            xor rax, rcx
00000001400057ff  480fafc3                          imul rax, rbx
0000000140005803  488bc8                            mov rcx, rax
0000000140005806  48c1e91b                          shr rcx, 0x1b
000000014000580a  4833c8                            xor rcx, rax
000000014000580d  48b8eb113113bb49d094              movabs rax, 0x94d049bb133111eb
0000000140005817  480fafc8                          imul rcx, rax
000000014000581b  488bd1                            mov rdx, rcx
000000014000581e  48c1ea1f                          shr rdx, 0x1f
0000000140005822  4833d1                            xor rdx, rcx
0000000140005825  488bca                            mov rcx, rdx
0000000140005828  488bc2                            mov rax, rdx
000000014000582b  48c1e928                          shr rcx, 0x28
000000014000582f  48c1e818                          shr rax, 0x18
0000000140005833  32c8                              xor cl, al
0000000140005835  488bc2                            mov rax, rdx
0000000140005838  48c1e808                          shr rax, 8
000000014000583c  32c8                              xor cl, al
000000014000583e  32ca                              xor cl, dl
0000000140005840  41320c38                          xor cl, byte ptr [r8 + rdi]
0000000140005844  4180fb10                          cmp r11b, 0x10
0000000140005848  0f8330020000                      jae 0x140005a7e
000000014000584e  80f910                            cmp cl, 0x10
0000000140005851  0f8327020000                      jae 0x140005a7e
0000000140005857  807dd000                          cmp byte ptr [rbp - 0x30], 0
000000014000585b  0f8426020000                      je 0x140005a87
0000000140005861  0fb6c1                            movzx eax, cl
0000000140005864  410fb6cb                          movzx ecx, r11b
0000000140005868  488b44c450                        mov rax, qword ptr [rsp + rax*8 + 0x50]
000000014000586d  488944cc50                        mov qword ptr [rsp + rcx*8 + 0x50], rax
0000000140005872  e910020000                        jmp 0x140005a87
0000000140005877  418bc1                            mov eax, r9d
000000014000587a  48bbb9e5e41c6d4758bf              movabs rbx, 0xbf58476d1ce4e5b9
0000000140005884  49bbeb113113bb49d094              movabs r11, 0x94d049bb133111eb
000000014000588e  493bc2                            cmp rax, r10
0000000140005891  720a                              jb 0x14000589d
0000000140005893  c644244001                        mov byte ptr [rsp + 0x40], 1
0000000140005898  4532f6                            xor r14b, r14b
000000014000589b  eb67                              jmp 0x140005904
000000014000589d  418bc1                            mov eax, r9d
00000001400058a0  8bc8                              mov ecx, eax
00000001400058a2  448bc0                            mov r8d, eax
00000001400058a5  490fafcf                          imul rcx, r15
00000001400058a9  448d4801                          lea r9d, [rax + 1]
00000001400058ad  48c1e020                          shl rax, 0x20
00000001400058b1  4803ce                            add rcx, rsi
00000001400058b4  44894c2430                        mov dword ptr [rsp + 0x30], r9d
00000001400058b9  4833c8                            xor rcx, rax
00000001400058bc  488bc1                            mov rax, rcx
00000001400058bf  48c1e81e                          shr rax, 0x1e
00000001400058c3  4833c1                            xor rax, rcx
00000001400058c6  480fafc3                          imul rax, rbx
00000001400058ca  488bc8                            mov rcx, rax
00000001400058cd  48c1e91b                          shr rcx, 0x1b
00000001400058d1  4833c8                            xor rcx, rax
00000001400058d4  490fafcb                          imul rcx, r11
00000001400058d8  488bd1                            mov rdx, rcx
00000001400058db  48c1ea1f                          shr rdx, 0x1f
00000001400058df  4833d1                            xor rdx, rcx
00000001400058e2  4c8bf2                            mov r14, rdx
00000001400058e5  488bc2                            mov rax, rdx
00000001400058e8  49c1ee28                          shr r14, 0x28
00000001400058ec  48c1e818                          shr rax, 0x18
00000001400058f0  4432f0                            xor r14b, al
00000001400058f3  488bc2                            mov rax, rdx
00000001400058f6  48c1e808                          shr rax, 8
00000001400058fa  4432f0                            xor r14b, al
00000001400058fd  4432f2                            xor r14b, dl
0000000140005900  45323438                          xor r14b, byte ptr [r8 + rdi]
0000000140005904  418bc1                            mov eax, r9d
0000000140005907  493bc2                            cmp rax, r10
000000014000590a  720a                              jb 0x140005916
000000014000590c  c644244001                        mov byte ptr [rsp + 0x40], 1
0000000140005911  4032f6                            xor sil, sil
0000000140005914  eb67                              jmp 0x14000597d
0000000140005916  418d4101                          lea eax, [r9 + 1]
000000014000591a  418bc9                            mov ecx, r9d
000000014000591d  89442430                          mov dword ptr [rsp + 0x30], eax
0000000140005921  490fafcf                          imul rcx, r15
0000000140005925  418bc1                            mov eax, r9d
0000000140005928  4803ce                            add rcx, rsi
000000014000592b  48c1e020                          shl rax, 0x20
000000014000592f  4833c8                            xor rcx, rax
0000000140005932  458bc1                            mov r8d, r9d
0000000140005935  488bc1                            mov rax, rcx
0000000140005938  48c1e81e                          shr rax, 0x1e
000000014000593c  4833c1                            xor rax, rcx
000000014000593f  480fafc3                          imul rax, rbx
0000000140005943  488bc8                            mov rcx, rax
0000000140005946  48c1e91b                          shr rcx, 0x1b
000000014000594a  4833c8                            xor rcx, rax
000000014000594d  490fafcb                          imul rcx, r11
0000000140005951  488bd1                            mov rdx, rcx
0000000140005954  48c1ea1f                          shr rdx, 0x1f
0000000140005958  4833d1                            xor rdx, rcx
000000014000595b  488bf2                            mov rsi, rdx
000000014000595e  488bc2                            mov rax, rdx
0000000140005961  48c1ee28                          shr rsi, 0x28
0000000140005965  48c1e818                          shr rax, 0x18
0000000140005969  4032f0                            xor sil, al
000000014000596c  488bc2                            mov rax, rdx
000000014000596f  48c1e808                          shr rax, 8
0000000140005973  4032f0                            xor sil, al
0000000140005976  4032f2                            xor sil, dl
0000000140005979  41323438                          xor sil, byte ptr [r8 + rdi]
000000014000597d  488d4c2420                        lea rcx, [rsp + 0x20]
0000000140005982  e8b9c8ffff                        call 0x140002240
0000000140005987  8b542430                          mov edx, dword ptr [rsp + 0x30]
000000014000598b  488bf8                            mov rdi, rax
000000014000598e  483b542428                        cmp rdx, qword ptr [rsp + 0x28]
0000000140005993  7209                              jb 0x14000599e
0000000140005995  c644244001                        mov byte ptr [rsp + 0x40], 1
000000014000599a  32db                              xor bl, bl
000000014000599c  eb74                              jmp 0x140005a12
000000014000599e  8d4201                            lea eax, [rdx + 1]
00000001400059a1  488bca                            mov rcx, rdx
00000001400059a4  89442430                          mov dword ptr [rsp + 0x30], eax
00000001400059a8  4c8bc2                            mov r8, rdx
00000001400059ab  490fafcf                          imul rcx, r15
00000001400059af  488bc2                            mov rax, rdx
00000001400059b2  48034c2438                        add rcx, qword ptr [rsp + 0x38]
00000001400059b7  48c1e020                          shl rax, 0x20
00000001400059bb  4833c8                            xor rcx, rax
00000001400059be  488bc1                            mov rax, rcx
00000001400059c1  48c1e81e                          shr rax, 0x1e
00000001400059c5  4833c1                            xor rax, rcx
00000001400059c8  480fafc3                          imul rax, rbx
00000001400059cc  488bc8                            mov rcx, rax
00000001400059cf  48c1e91b                          shr rcx, 0x1b
00000001400059d3  4833c8                            xor rcx, rax
00000001400059d6  48b8eb113113bb49d094              movabs rax, 0x94d049bb133111eb
00000001400059e0  480fafc8                          imul rcx, rax
00000001400059e4  488bd1                            mov rdx, rcx
00000001400059e7  48c1ea1f                          shr rdx, 0x1f
00000001400059eb  4833d1                            xor rdx, rcx
00000001400059ee  488bda                            mov rbx, rdx
00000001400059f1  488bc2                            mov rax, rdx
00000001400059f4  48c1e818                          shr rax, 0x18
00000001400059f8  48c1eb28                          shr rbx, 0x28
00000001400059fc  32d8                              xor bl, al
00000001400059fe  488bc2                            mov rax, rdx
0000000140005a01  48c1e808                          shr rax, 8
0000000140005a05  32d8                              xor bl, al
0000000140005a07  488b442420                        mov rax, qword ptr [rsp + 0x20]
0000000140005a0c  32da                              xor bl, dl
0000000140005a0e  41321c00                          xor bl, byte ptr [r8 + rax]
0000000140005a12  488d4c2420                        lea rcx, [rsp + 0x20]
0000000140005a17  e824c8ffff                        call 0x140002240
0000000140005a1c  4c8bc8                            mov r9, rax
0000000140005a1f  4180fe10                          cmp r14b, 0x10
0000000140005a23  7345                              jae 0x140005a6a
0000000140005a25  4080fe10                          cmp sil, 0x10
0000000140005a29  733f                              jae 0x140005a6a
0000000140005a2b  400fb6ce                          movzx ecx, sil
0000000140005a2f  4c8b44cc50                        mov r8, qword ptr [rsp + rcx*8 + 0x50]
0000000140005a34  4c03c7                            add r8, rdi
0000000140005a37  83e33f                            and ebx, 0x3f
0000000140005a3a  7406                              je 0x140005a42
0000000140005a3c  0fb6cb                            movzx ecx, bl
0000000140005a3f  49d3c0                            rol r8, cl
0000000140005a42  488b742438                        mov rsi, qword ptr [rsp + 0x38]
0000000140005a47  4c8b542428                        mov r10, qword ptr [rsp + 0x28]
0000000140005a4c  488b7c2420                        mov rdi, qword ptr [rsp + 0x20]
0000000140005a51  410fb6c6                          movzx eax, r14b
0000000140005a55  4c3344c450                        xor r8, qword ptr [rsp + rax*8 + 0x50]
0000000140005a5a  4d0fafc1                          imul r8, r9
0000000140005a5e  448b4c2430                        mov r9d, dword ptr [rsp + 0x30]
0000000140005a63  4c8944c450                        mov qword ptr [rsp + rax*8 + 0x50], r8
0000000140005a68  eb18                              jmp 0x140005a82
0000000140005a6a  488b742438                        mov rsi, qword ptr [rsp + 0x38]
0000000140005a6f  448b4c2430                        mov r9d, dword ptr [rsp + 0x30]
0000000140005a74  4c8b542428                        mov r10, qword ptr [rsp + 0x28]
0000000140005a79  488b7c2420                        mov rdi, qword ptr [rsp + 0x20]
0000000140005a7e  c645d301                          mov byte ptr [rbp - 0x2d], 1
0000000140005a82  4c8b742448                        mov r14, qword ptr [rsp + 0x48]
0000000140005a87  807dd100                          cmp byte ptr [rbp - 0x2f], 0
0000000140005a8b  0f84c6dfffff                      je 0x140003a57
0000000140005a91  0fb645d2                          movzx eax, byte ptr [rbp - 0x2e]
0000000140005a95  0fb64dd3                          movzx ecx, byte ptr [rbp - 0x2d]
0000000140005a99  4d85e4                            test r12, r12
0000000140005a9c  4c8bbc24f0000000                  mov r15, qword ptr [rsp + 0xf0]
0000000140005aa4  ba01000000                        mov edx, 1
0000000140005aa9  4c8bb424f8000000                  mov r14, qword ptr [rsp + 0xf8]
0000000140005ab1  0f44ca                            cmove ecx, edx
0000000140005ab4  807dd100                          cmp byte ptr [rbp - 0x2f], 0
0000000140005ab8  4c8bac2400010000                  mov r13, qword ptr [rsp + 0x100]
0000000140005ac0  4c8ba42408010000                  mov r12, qword ptr [rsp + 0x108]
0000000140005ac8  488bbc2438010000                  mov rdi, qword ptr [rsp + 0x138]
0000000140005ad0  488bb42430010000                  mov rsi, qword ptr [rsp + 0x130]
0000000140005ad8  488b9c2428010000                  mov rbx, qword ptr [rsp + 0x128]
0000000140005ae0  7422                              je 0x140005b04
