00000001400026a0  48895c2418                        mov qword ptr [rsp + 0x18], rbx
00000001400026a5  4889742420                        mov qword ptr [rsp + 0x20], rsi
00000001400026aa  55                                push rbp
00000001400026ab  57                                push rdi
00000001400026ac  4154                              push r12
00000001400026ae  4156                              push r14
00000001400026b0  4157                              push r15
00000001400026b2  488d6c24c9                        lea rbp, [rsp - 0x37]
00000001400026b7  4881ecb0000000                    sub rsp, 0xb0
00000001400026be  488b053b890000                    mov rax, qword ptr [rip + 0x893b]
00000001400026c5  4833c4                            xor rax, rsp
00000001400026c8  48894527                          mov qword ptr [rbp + 0x27], rax
00000001400026cc  488b5110                          mov rdx, qword ptr [rcx + 0x10]
00000001400026d0  4533ff                            xor r15d, r15d
00000001400026d3  488b19                            mov rbx, qword ptr [rcx]
00000001400026d6  4c8bc2                            mov r8, rdx
00000001400026d9  4c2bc3                            sub r8, rbx
00000001400026dc  41bc5c1e0000                      mov r12d, 0x1e5c
00000001400026e2  4c8bf1                            mov r14, rcx
00000001400026e5  4d3bc4                            cmp r8, r12
00000001400026e8  0f8364010000                      jae 0x140002852
00000001400026ee  498bc8                            mov rcx, r8
00000001400026f1  48bfffffffffffffff7f              movabs rdi, 0x7fffffffffffffff
00000001400026fb  48d1e9                            shr rcx, 1
00000001400026fe  488bc7                            mov rax, rdi
0000000140002701  482bc1                            sub rax, rcx
0000000140002704  4c3bc0                            cmp r8, rax
0000000140002707  770b                              ja 0x140002714
0000000140002709  4a8d3c01                          lea rdi, [rcx + r8]
000000014000270d  493bfc                            cmp rdi, r12
0000000140002710  490f42fc                          cmovb rdi, r12
0000000140002714  4885db                            test rbx, rbx
0000000140002717  743d                              je 0x140002756
0000000140002719  482bd3                            sub rdx, rbx
000000014000271c  4881fa00100000                    cmp rdx, 0x1000
0000000140002723  721e                              jb 0x140002743
0000000140002725  488b4bf8                          mov rcx, qword ptr [rbx - 8]
0000000140002729  482bd9                            sub rbx, rcx
000000014000272c  4883eb08                          sub rbx, 8
0000000140002730  4883fb1f                          cmp rbx, 0x1f
0000000140002734  7706                              ja 0x14000273c
0000000140002736  4883c227                          add rdx, 0x27
000000014000273a  eb0a                              jmp 0x140002746
000000014000273c  b905000000                        mov ecx, 5
0000000140002741  cd29                              int 0x29
0000000140002743  488bcb                            mov rcx, rbx
0000000140002746  e8e5350000                        call 0x140005d30
000000014000274b  4d893e                            mov qword ptr [r14], r15
000000014000274e  4d897e08                          mov qword ptr [r14 + 8], r15
0000000140002752  4d897e10                          mov qword ptr [r14 + 0x10], r15
0000000140002756  4885ff                            test rdi, rdi
0000000140002759  7505                              jne 0x140002760
000000014000275b  498bdf                            mov rbx, r15
000000014000275e  eb1b                              jmp 0x14000277b
0000000140002760  488bcf                            mov rcx, rdi
0000000140002763  4881ff00100000                    cmp rdi, 0x1000
000000014000276a  7207                              jb 0x140002773
000000014000276c  e8efeaffff                        call 0x140001260
0000000140002771  eb05                              jmp 0x140002778
0000000140002773  e868350000                        call 0x140005ce0
0000000140002778  488bd8                            mov rbx, rax
000000014000277b  488d043b                          lea rax, [rbx + rdi]
000000014000277f  49891e                            mov qword ptr [r14], rbx
0000000140002782  49894610                          mov qword ptr [r14 + 0x10], rax
0000000140002786  4d8bc4                            mov r8, r12
0000000140002789  33d2                              xor edx, edx
000000014000278b  488bcb                            mov rcx, rbx
000000014000278e  e85df7ffff                        call 0x140001ef0
0000000140002793  488d835c1e0000                    lea rax, [rbx + 0x1e5c]
000000014000279a  0f57c0                            xorps xmm0, xmm0
000000014000279d  4c89ac24e8000000                  mov qword ptr [rsp + 0xe8], r13
00000001400027a5  488d3df44b0000                    lea rdi, [rip + 0x4bf4]
00000001400027ac  6644897d17                        mov word ptr [rbp + 0x17], r15w
00000001400027b1  41ba74000000                      mov r10d, 0x74
00000001400027b7  44887d19                          mov byte ptr [rbp + 0x19], r15b
00000001400027bb  48be44332211edfe0dd0              movabs rsi, 0xd00dfeed11223344
00000001400027c5  44897db7                          mov dword ptr [rbp - 0x49], r15d
00000001400027c9  458bcf                            mov r9d, r15d
00000001400027cc  44887dc7                          mov byte ptr [rbp - 0x39], r15b
00000001400027d0  0f1145d7                          movups xmmword ptr [rbp - 0x29], xmm0
00000001400027d4  48897da7                          mov qword ptr [rbp - 0x59], rdi
00000001400027d8  41bf80841e00                      mov r15d, 0x1e8480
00000001400027de  0f1145e7                          movups xmmword ptr [rbp - 0x19], xmm0
00000001400027e2  4c8955af                          mov qword ptr [rbp - 0x51], r10
00000001400027e6  49bdb9e5e41c6d4758bf              movabs r13, 0xbf58476d1ce4e5b9
00000001400027f0  0f1145f7                          movups xmmword ptr [rbp - 9], xmm0
00000001400027f4  488975bf                          mov qword ptr [rbp - 0x41], rsi
00000001400027f8  4c8d2501d8ffff                    lea r12, [rip - 0x27ff]
00000001400027ff  0f114507                          movups xmmword ptr [rbp + 7], xmm0
0000000140002803  49894608                          mov qword ptr [r14 + 8], rax
0000000140002807  807d1900                          cmp byte ptr [rbp + 0x19], 0
000000014000280b  49bb157c4a7fb979379e              movabs r11, 0x9e3779b97f4a7c15
0000000140002815  48baeb113113bb49d094              movabs rdx, 0x94d049bb133111eb
000000014000281f  0f85df100000                      jne 0x140003904
0000000140002825  807dc700                          cmp byte ptr [rbp - 0x39], 0
0000000140002829  0f85d5100000                      jne 0x140003904
000000014000282f  498bc7                            mov rax, r15
0000000140002832  49ffcf                            dec r15
0000000140002835  4885c0                            test rax, rax
0000000140002838  0f84c6100000                      je 0x140003904
000000014000283e  418bc1                            mov eax, r9d
0000000140002841  493bc2                            cmp rax, r10
0000000140002844  7249                              jb 0x14000288f
0000000140002846  c645c701                          mov byte ptr [rbp - 0x39], 1
000000014000284a  4532db                            xor r11b, r11b
000000014000284d  e9a3000000                        jmp 0x1400028f5
0000000140002852  488b7108                          mov rsi, qword ptr [rcx + 8]
0000000140002856  482bf3                            sub rsi, rbx
0000000140002859  493bf4                            cmp rsi, r12
000000014000285c  0f8324ffffff                      jae 0x140002786
0000000140002862  4c8bc6                            mov r8, rsi
0000000140002865  33d2                              xor edx, edx
0000000140002867  488bcb                            mov rcx, rbx
000000014000286a  e881f6ffff                        call 0x140001ef0
000000014000286f  498b5e08                          mov rbx, qword ptr [r14 + 8]
0000000140002873  498bfc                            mov rdi, r12
0000000140002876  482bfe                            sub rdi, rsi
0000000140002879  33d2                              xor edx, edx
000000014000287b  4c8bc7                            mov r8, rdi
000000014000287e  488bcb                            mov rcx, rbx
0000000140002881  e86af6ffff                        call 0x140001ef0
0000000140002886  488d043b                          lea rax, [rbx + rdi]
000000014000288a  e90bffffff                        jmp 0x14000279a
000000014000288f  418bc1                            mov eax, r9d
0000000140002892  8bc8                              mov ecx, eax
0000000140002894  448bc0                            mov r8d, eax
0000000140002897  490fafcb                          imul rcx, r11
000000014000289b  448d4801                          lea r9d, [rax + 1]
000000014000289f  48c1e020                          shl rax, 0x20
00000001400028a3  4803ce                            add rcx, rsi
00000001400028a6  44894db7                          mov dword ptr [rbp - 0x49], r9d
00000001400028aa  4833c8                            xor rcx, rax
00000001400028ad  488bc1                            mov rax, rcx
00000001400028b0  48c1e81e                          shr rax, 0x1e
00000001400028b4  4833c1                            xor rax, rcx
00000001400028b7  490fafc5                          imul rax, r13
00000001400028bb  488bc8                            mov rcx, rax
00000001400028be  48c1e91b                          shr rcx, 0x1b
00000001400028c2  4833c8                            xor rcx, rax
00000001400028c5  480fafca                          imul rcx, rdx
00000001400028c9  488bd1                            mov rdx, rcx
00000001400028cc  48c1ea1f                          shr rdx, 0x1f
00000001400028d0  4833d1                            xor rdx, rcx
00000001400028d3  4c8bda                            mov r11, rdx
00000001400028d6  488bc2                            mov rax, rdx
00000001400028d9  49c1eb28                          shr r11, 0x28
00000001400028dd  48c1e818                          shr rax, 0x18
00000001400028e1  4432d8                            xor r11b, al
00000001400028e4  488bc2                            mov rax, rdx
00000001400028e7  48c1e808                          shr rax, 8
00000001400028eb  4432d8                            xor r11b, al
00000001400028ee  4432da                            xor r11b, dl
00000001400028f1  45321c38                          xor r11b, byte ptr [r8 + rdi]
00000001400028f5  410fb6c3                          movzx eax, r11b
00000001400028f9  410fb69c0480920000                movzx ebx, byte ptr [r12 + rax + 0x9280]
0000000140002902  450fb6840480930000                movzx r8d, byte ptr [r12 + rax + 0x9380]
000000014000290b  4183e307                          and r11d, 7
000000014000290f  741e                              je 0x14000292f
0000000140002911  410fb6d0                          movzx edx, r8b
0000000140002915  410fb6c0                          movzx eax, r8b
0000000140002919  b908000000                        mov ecx, 8
000000014000291e  412acb                            sub cl, r11b
0000000140002921  d2ea                              shr dl, cl
0000000140002923  418bcb                            mov ecx, r11d
0000000140002926  d2e0                              shl al, cl
0000000140002928  440fb6c2                          movzx r8d, dl
000000014000292c  440ac0                            or r8b, al
000000014000292f  4132d8                            xor bl, r8b
0000000140002932  0fb6c3                            movzx eax, bl
0000000140002935  35a5000000                        xor eax, 0xa5
000000014000293a  83f811                            cmp eax, 0x11
000000014000293d  0f873d0b0000                      ja 0x140003480
0000000140002943  4898                              cdqe 
0000000140002945  418b8c845c390000                  mov ecx, dword ptr [r12 + rax*4 + 0x395c]
000000014000294d  4903cc                            add rcx, r12
0000000140002950  ffe1                              jmp rcx
0000000140002952  418bc1                            mov eax, r9d
0000000140002955  493bc2                            cmp rax, r10
0000000140002958  7217                              jb 0x140002971
000000014000295a  32db                              xor bl, bl
000000014000295c  c645c701                          mov byte ptr [rbp - 0x39], 1
0000000140002960  488d4da7                          lea rcx, [rbp - 0x59]
0000000140002964  e8d7f8ffff                        call 0x140002240
0000000140002969  488bc8                            mov rcx, rax
000000014000296c  e98c000000                        jmp 0x1400029fd
0000000140002971  418d4101                          lea eax, [r9 + 1]
0000000140002975  418bc9                            mov ecx, r9d
0000000140002978  8945b7                            mov dword ptr [rbp - 0x49], eax
000000014000297b  48bbeb113113bb49d094              movabs rbx, 0x94d049bb133111eb
0000000140002985  48b8157c4a7fb979379e              movabs rax, 0x9e3779b97f4a7c15
000000014000298f  458bc1                            mov r8d, r9d
0000000140002992  480fafc8                          imul rcx, rax
0000000140002996  418bc1                            mov eax, r9d
0000000140002999  48c1e020                          shl rax, 0x20
000000014000299d  4803ce                            add rcx, rsi
00000001400029a0  4833c8                            xor rcx, rax
00000001400029a3  488bc1                            mov rax, rcx
00000001400029a6  48c1e81e                          shr rax, 0x1e
00000001400029aa  4833c1                            xor rax, rcx
00000001400029ad  490fafc5                          imul rax, r13
00000001400029b1  488bc8                            mov rcx, rax
00000001400029b4  48c1e91b                          shr rcx, 0x1b
00000001400029b8  4833c8                            xor rcx, rax
00000001400029bb  480fafcb                          imul rcx, rbx
00000001400029bf  488bd1                            mov rdx, rcx
00000001400029c2  48c1ea1f                          shr rdx, 0x1f
00000001400029c6  4833d1                            xor rdx, rcx
00000001400029c9  488d4da7                          lea rcx, [rbp - 0x59]
00000001400029cd  488bda                            mov rbx, rdx
00000001400029d0  488bc2                            mov rax, rdx
00000001400029d3  48c1eb28                          shr rbx, 0x28
00000001400029d7  48c1e818                          shr rax, 0x18
00000001400029db  32d8                              xor bl, al
00000001400029dd  488bc2                            mov rax, rdx
00000001400029e0  48c1e808                          shr rax, 8
00000001400029e4  32d8                              xor bl, al
00000001400029e6  32da                              xor bl, dl
00000001400029e8  41321c38                          xor bl, byte ptr [r8 + rdi]
00000001400029ec  e84ff8ffff                        call 0x140002240
00000001400029f1  488bc8                            mov rcx, rax
00000001400029f4  80fb08                            cmp bl, 8
00000001400029f7  0f83730a0000                      jae 0x140003470
00000001400029fd  0fb6c3                            movzx eax, bl
0000000140002a00  48894cc5d7                        mov qword ptr [rbp + rax*8 - 0x29], rcx
0000000140002a05  448b4db7                          mov r9d, dword ptr [rbp - 0x49]
0000000140002a09  4c8b55af                          mov r10, qword ptr [rbp - 0x51]
0000000140002a0d  488b75bf                          mov rsi, qword ptr [rbp - 0x41]
0000000140002a11  488b7da7                          mov rdi, qword ptr [rbp - 0x59]
0000000140002a15  e96a0a0000                        jmp 0x140003484
0000000140002a1a  418bc1                            mov eax, r9d
0000000140002a1d  48bbeb113113bb49d094              movabs rbx, 0x94d049bb133111eb
0000000140002a27  493bc2                            cmp rax, r10
0000000140002a2a  7209                              jb 0x140002a35
0000000140002a2c  c645c701                          mov byte ptr [rbp - 0x39], 1
0000000140002a30  4532db                            xor r11b, r11b
0000000140002a33  eb73                              jmp 0x140002aa8
0000000140002a35  418bc1                            mov eax, r9d
0000000140002a38  448bc0                            mov r8d, eax
0000000140002a3b  8bc8                              mov ecx, eax
0000000140002a3d  448d4801                          lea r9d, [rax + 1]
0000000140002a41  48b8157c4a7fb979379e              movabs rax, 0x9e3779b97f4a7c15
0000000140002a4b  480fafc8                          imul rcx, rax
0000000140002a4f  418bc0                            mov eax, r8d
0000000140002a52  44894db7                          mov dword ptr [rbp - 0x49], r9d
0000000140002a56  48c1e020                          shl rax, 0x20
0000000140002a5a  4803ce                            add rcx, rsi
0000000140002a5d  4833c8                            xor rcx, rax
0000000140002a60  488bc1                            mov rax, rcx
0000000140002a63  48c1e81e                          shr rax, 0x1e
0000000140002a67  4833c1                            xor rax, rcx
0000000140002a6a  490fafc5                          imul rax, r13
0000000140002a6e  488bc8                            mov rcx, rax
0000000140002a71  48c1e91b                          shr rcx, 0x1b
0000000140002a75  4833c8                            xor rcx, rax
0000000140002a78  480fafcb                          imul rcx, rbx
0000000140002a7c  488bd1                            mov rdx, rcx
0000000140002a7f  48c1ea1f                          shr rdx, 0x1f
0000000140002a83  4833d1                            xor rdx, rcx
0000000140002a86  4c8bda                            mov r11, rdx
0000000140002a89  488bc2                            mov rax, rdx
0000000140002a8c  49c1eb28                          shr r11, 0x28
0000000140002a90  48c1e818                          shr rax, 0x18
0000000140002a94  4432d8                            xor r11b, al
0000000140002a97  488bc2                            mov rax, rdx
0000000140002a9a  48c1e808                          shr rax, 8
0000000140002a9e  4432d8                            xor r11b, al
0000000140002aa1  4432da                            xor r11b, dl
0000000140002aa4  45321c38                          xor r11b, byte ptr [r8 + rdi]
0000000140002aa8  418bc1                            mov eax, r9d
0000000140002aab  493bc2                            cmp rax, r10
0000000140002aae  7208                              jb 0x140002ab8
0000000140002ab0  c645c701                          mov byte ptr [rbp - 0x39], 1
0000000140002ab4  32c9                              xor cl, cl
0000000140002ab6  eb70                              jmp 0x140002b28
0000000140002ab8  418bc1                            mov eax, r9d
0000000140002abb  448bc0                            mov r8d, eax
0000000140002abe  8bc8                              mov ecx, eax
0000000140002ac0  448d4801                          lea r9d, [rax + 1]
0000000140002ac4  48b8157c4a7fb979379e              movabs rax, 0x9e3779b97f4a7c15
0000000140002ace  480fafc8                          imul rcx, rax
0000000140002ad2  418bc0                            mov eax, r8d
0000000140002ad5  44894db7                          mov dword ptr [rbp - 0x49], r9d
0000000140002ad9  4803ce                            add rcx, rsi
0000000140002adc  48c1e020                          shl rax, 0x20
0000000140002ae0  4833c8                            xor rcx, rax
0000000140002ae3  488bc1                            mov rax, rcx
0000000140002ae6  48c1e81e                          shr rax, 0x1e
0000000140002aea  4833c1                            xor rax, rcx
0000000140002aed  490fafc5                          imul rax, r13
0000000140002af1  488bc8                            mov rcx, rax
0000000140002af4  48c1e91b                          shr rcx, 0x1b
0000000140002af8  4833c8                            xor rcx, rax
0000000140002afb  480fafcb                          imul rcx, rbx
0000000140002aff  488bd1                            mov rdx, rcx
0000000140002b02  48c1ea1f                          shr rdx, 0x1f
0000000140002b06  4833d1                            xor rdx, rcx
0000000140002b09  488bca                            mov rcx, rdx
0000000140002b0c  488bc2                            mov rax, rdx
0000000140002b0f  48c1e928                          shr rcx, 0x28
0000000140002b13  48c1e818                          shr rax, 0x18
0000000140002b17  32c8                              xor cl, al
0000000140002b19  488bc2                            mov rax, rdx
0000000140002b1c  48c1e808                          shr rax, 8
0000000140002b20  32c8                              xor cl, al
0000000140002b22  32ca                              xor cl, dl
0000000140002b24  41320c38                          xor cl, byte ptr [r8 + rdi]
0000000140002b28  4180fb08                          cmp r11b, 8
0000000140002b2c  0f834e090000                      jae 0x140003480
0000000140002b32  80f908                            cmp cl, 8
0000000140002b35  0f8345090000                      jae 0x140003480
0000000140002b3b  0fb6c1                            movzx eax, cl
0000000140002b3e  410fb6cb                          movzx ecx, r11b
0000000140002b42  488b44c5d7                        mov rax, qword ptr [rbp + rax*8 - 0x29]
0000000140002b47  488944cdd7                        mov qword ptr [rbp + rcx*8 - 0x29], rax
0000000140002b4c  e933090000                        jmp 0x140003484
0000000140002b51  418bc1                            mov eax, r9d
0000000140002b54  48bbeb113113bb49d094              movabs rbx, 0x94d049bb133111eb
0000000140002b5e  493bc2                            cmp rax, r10
0000000140002b61  7209                              jb 0x140002b6c
0000000140002b63  c645c701                          mov byte ptr [rbp - 0x39], 1
0000000140002b67  4532db                            xor r11b, r11b
0000000140002b6a  eb73                              jmp 0x140002bdf
0000000140002b6c  418bc1                            mov eax, r9d
0000000140002b6f  448bc0                            mov r8d, eax
0000000140002b72  8bc8                              mov ecx, eax
0000000140002b74  448d4801                          lea r9d, [rax + 1]
0000000140002b78  48b8157c4a7fb979379e              movabs rax, 0x9e3779b97f4a7c15
0000000140002b82  480fafc8                          imul rcx, rax
0000000140002b86  418bc0                            mov eax, r8d
0000000140002b89  44894db7                          mov dword ptr [rbp - 0x49], r9d
0000000140002b8d  48c1e020                          shl rax, 0x20
0000000140002b91  4803ce                            add rcx, rsi
0000000140002b94  4833c8                            xor rcx, rax
0000000140002b97  488bc1                            mov rax, rcx
0000000140002b9a  48c1e81e                          shr rax, 0x1e
0000000140002b9e  4833c1                            xor rax, rcx
0000000140002ba1  490fafc5                          imul rax, r13
0000000140002ba5  488bc8                            mov rcx, rax
0000000140002ba8  48c1e91b                          shr rcx, 0x1b
0000000140002bac  4833c8                            xor rcx, rax
0000000140002baf  480fafcb                          imul rcx, rbx
0000000140002bb3  488bd1                            mov rdx, rcx
0000000140002bb6  48c1ea1f                          shr rdx, 0x1f
0000000140002bba  4833d1                            xor rdx, rcx
0000000140002bbd  4c8bda                            mov r11, rdx
0000000140002bc0  488bc2                            mov rax, rdx
0000000140002bc3  49c1eb28                          shr r11, 0x28
0000000140002bc7  48c1e818                          shr rax, 0x18
0000000140002bcb  4432d8                            xor r11b, al
0000000140002bce  488bc2                            mov rax, rdx
0000000140002bd1  48c1e808                          shr rax, 8
0000000140002bd5  4432d8                            xor r11b, al
0000000140002bd8  4432da                            xor r11b, dl
0000000140002bdb  45321c38                          xor r11b, byte ptr [r8 + rdi]
0000000140002bdf  418bc1                            mov eax, r9d
0000000140002be2  493bc2                            cmp rax, r10
0000000140002be5  7208                              jb 0x140002bef
0000000140002be7  c645c701                          mov byte ptr [rbp - 0x39], 1
0000000140002beb  32c9                              xor cl, cl
0000000140002bed  eb70                              jmp 0x140002c5f
0000000140002bef  418bc1                            mov eax, r9d
0000000140002bf2  448bc0                            mov r8d, eax
0000000140002bf5  8bc8                              mov ecx, eax
0000000140002bf7  448d4801                          lea r9d, [rax + 1]
0000000140002bfb  48b8157c4a7fb979379e              movabs rax, 0x9e3779b97f4a7c15
0000000140002c05  480fafc8                          imul rcx, rax
0000000140002c09  418bc0                            mov eax, r8d
0000000140002c0c  44894db7                          mov dword ptr [rbp - 0x49], r9d
0000000140002c10  4803ce                            add rcx, rsi
0000000140002c13  48c1e020                          shl rax, 0x20
0000000140002c17  4833c8                            xor rcx, rax
0000000140002c1a  488bc1                            mov rax, rcx
0000000140002c1d  48c1e81e                          shr rax, 0x1e
0000000140002c21  4833c1                            xor rax, rcx
0000000140002c24  490fafc5                          imul rax, r13
0000000140002c28  488bc8                            mov rcx, rax
0000000140002c2b  48c1e91b                          shr rcx, 0x1b
0000000140002c2f  4833c8                            xor rcx, rax
0000000140002c32  480fafcb                          imul rcx, rbx
0000000140002c36  488bd1                            mov rdx, rcx
0000000140002c39  48c1ea1f                          shr rdx, 0x1f
0000000140002c3d  4833d1                            xor rdx, rcx
0000000140002c40  488bca                            mov rcx, rdx
0000000140002c43  488bc2                            mov rax, rdx
0000000140002c46  48c1e928                          shr rcx, 0x28
0000000140002c4a  48c1e818                          shr rax, 0x18
0000000140002c4e  32c8                              xor cl, al
0000000140002c50  488bc2                            mov rax, rdx
0000000140002c53  48c1e808                          shr rax, 8
0000000140002c57  32c8                              xor cl, al
0000000140002c59  32ca                              xor cl, dl
0000000140002c5b  41320c38                          xor cl, byte ptr [r8 + rdi]
0000000140002c5f  4180fb08                          cmp r11b, 8
0000000140002c63  0f8317080000                      jae 0x140003480
0000000140002c69  80f908                            cmp cl, 8
0000000140002c6c  0f830e080000                      jae 0x140003480
0000000140002c72  0fb6c1                            movzx eax, cl
0000000140002c75  488b4cc5d7                        mov rcx, qword ptr [rbp + rax*8 - 0x29]
0000000140002c7a  4881f95c1e0000                    cmp rcx, 0x1e5c
0000000140002c81  0f83f9070000                      jae 0x140003480
0000000140002c87  410fb68c0c20740000                movzx ecx, byte ptr [r12 + rcx + 0x7420]
0000000140002c90  410fb6c3                          movzx eax, r11b
0000000140002c94  48894cc5d7                        mov qword ptr [rbp + rax*8 - 0x29], rcx
0000000140002c99  e9e6070000                        jmp 0x140003484
0000000140002c9e  418bc1                            mov eax, r9d
0000000140002ca1  48bbeb113113bb49d094              movabs rbx, 0x94d049bb133111eb
0000000140002cab  493bc2                            cmp rax, r10
0000000140002cae  7209                              jb 0x140002cb9
0000000140002cb0  c645c701                          mov byte ptr [rbp - 0x39], 1
0000000140002cb4  4532db                            xor r11b, r11b
0000000140002cb7  eb73                              jmp 0x140002d2c
0000000140002cb9  418bc1                            mov eax, r9d
0000000140002cbc  448bc0                            mov r8d, eax
0000000140002cbf  8bc8                              mov ecx, eax
0000000140002cc1  448d4801                          lea r9d, [rax + 1]
0000000140002cc5  48b8157c4a7fb979379e              movabs rax, 0x9e3779b97f4a7c15
0000000140002ccf  480fafc8                          imul rcx, rax
0000000140002cd3  418bc0                            mov eax, r8d
0000000140002cd6  44894db7                          mov dword ptr [rbp - 0x49], r9d
0000000140002cda  48c1e020                          shl rax, 0x20
0000000140002cde  4803ce                            add rcx, rsi
0000000140002ce1  4833c8                            xor rcx, rax
0000000140002ce4  488bc1                            mov rax, rcx
0000000140002ce7  48c1e81e                          shr rax, 0x1e
0000000140002ceb  4833c1                            xor rax, rcx
0000000140002cee  490fafc5                          imul rax, r13
0000000140002cf2  488bc8                            mov rcx, rax
0000000140002cf5  48c1e91b                          shr rcx, 0x1b
0000000140002cf9  4833c8                            xor rcx, rax
0000000140002cfc  480fafcb                          imul rcx, rbx
0000000140002d00  488bd1                            mov rdx, rcx
0000000140002d03  48c1ea1f                          shr rdx, 0x1f
0000000140002d07  4833d1                            xor rdx, rcx
0000000140002d0a  4c8bda                            mov r11, rdx
0000000140002d0d  488bc2                            mov rax, rdx
0000000140002d10  49c1eb28                          shr r11, 0x28
0000000140002d14  48c1e818                          shr rax, 0x18
0000000140002d18  4432d8                            xor r11b, al
0000000140002d1b  488bc2                            mov rax, rdx
0000000140002d1e  48c1e808                          shr rax, 8
0000000140002d22  4432d8                            xor r11b, al
0000000140002d25  4432da                            xor r11b, dl
0000000140002d28  45321c38                          xor r11b, byte ptr [r8 + rdi]
0000000140002d2c  418bc1                            mov eax, r9d
0000000140002d2f  493bc2                            cmp rax, r10
0000000140002d32  7208                              jb 0x140002d3c
0000000140002d34  c645c701                          mov byte ptr [rbp - 0x39], 1
0000000140002d38  32c9                              xor cl, cl
0000000140002d3a  eb70                              jmp 0x140002dac
0000000140002d3c  418bc1                            mov eax, r9d
0000000140002d3f  448bc0                            mov r8d, eax
0000000140002d42  8bc8                              mov ecx, eax
0000000140002d44  448d4801                          lea r9d, [rax + 1]
0000000140002d48  48b8157c4a7fb979379e              movabs rax, 0x9e3779b97f4a7c15
0000000140002d52  480fafc8                          imul rcx, rax
0000000140002d56  418bc0                            mov eax, r8d
0000000140002d59  44894db7                          mov dword ptr [rbp - 0x49], r9d
0000000140002d5d  4803ce                            add rcx, rsi
0000000140002d60  48c1e020                          shl rax, 0x20
0000000140002d64  4833c8                            xor rcx, rax
0000000140002d67  488bc1                            mov rax, rcx
0000000140002d6a  48c1e81e                          shr rax, 0x1e
0000000140002d6e  4833c1                            xor rax, rcx
0000000140002d71  490fafc5                          imul rax, r13
0000000140002d75  488bc8                            mov rcx, rax
0000000140002d78  48c1e91b                          shr rcx, 0x1b
0000000140002d7c  4833c8                            xor rcx, rax
0000000140002d7f  480fafcb                          imul rcx, rbx
0000000140002d83  488bd1                            mov rdx, rcx
0000000140002d86  48c1ea1f                          shr rdx, 0x1f
0000000140002d8a  4833d1                            xor rdx, rcx
0000000140002d8d  488bca                            mov rcx, rdx
0000000140002d90  488bc2                            mov rax, rdx
0000000140002d93  48c1e928                          shr rcx, 0x28
0000000140002d97  48c1e818                          shr rax, 0x18
0000000140002d9b  32c8                              xor cl, al
0000000140002d9d  488bc2                            mov rax, rdx
0000000140002da0  48c1e808                          shr rax, 8
0000000140002da4  32c8                              xor cl, al
0000000140002da6  32ca                              xor cl, dl
0000000140002da8  41320c38                          xor cl, byte ptr [r8 + rdi]
0000000140002dac  4180fb08                          cmp r11b, 8
0000000140002db0  0f83ca060000                      jae 0x140003480
0000000140002db6  80f908                            cmp cl, 8
0000000140002db9  0f83c1060000                      jae 0x140003480
0000000140002dbf  4d8b06                            mov r8, qword ptr [r14]
0000000140002dc2  410fb6c3                          movzx eax, r11b
0000000140002dc6  488b54c5d7                        mov rdx, qword ptr [rbp + rax*8 - 0x29]
0000000140002dcb  498b4608                          mov rax, qword ptr [r14 + 8]
0000000140002dcf  492bc0                            sub rax, r8
0000000140002dd2  483bd0                            cmp rdx, rax
0000000140002dd5  0f83a5060000                      jae 0x140003480
0000000140002ddb  0fb6c1                            movzx eax, cl
0000000140002dde  0fb64cc5d7                        movzx ecx, byte ptr [rbp + rax*8 - 0x29]
0000000140002de3  41880c10                          mov byte ptr [r8 + rdx], cl
0000000140002de7  e998060000                        jmp 0x140003484
0000000140002dec  418bc1                            mov eax, r9d
0000000140002def  48bbeb113113bb49d094              movabs rbx, 0x94d049bb133111eb
0000000140002df9  493bc2                            cmp rax, r10
0000000140002dfc  7209                              jb 0x140002e07
0000000140002dfe  c645c701                          mov byte ptr [rbp - 0x39], 1
0000000140002e02  4532db                            xor r11b, r11b
0000000140002e05  eb73                              jmp 0x140002e7a
0000000140002e07  418bc1                            mov eax, r9d
0000000140002e0a  448bc0                            mov r8d, eax
0000000140002e0d  8bc8                              mov ecx, eax
0000000140002e0f  448d4801                          lea r9d, [rax + 1]
0000000140002e13  48b8157c4a7fb979379e              movabs rax, 0x9e3779b97f4a7c15
0000000140002e1d  480fafc8                          imul rcx, rax
0000000140002e21  418bc0                            mov eax, r8d
0000000140002e24  44894db7                          mov dword ptr [rbp - 0x49], r9d
0000000140002e28  48c1e020                          shl rax, 0x20
0000000140002e2c  4803ce                            add rcx, rsi
0000000140002e2f  4833c8                            xor rcx, rax
0000000140002e32  488bc1                            mov rax, rcx
0000000140002e35  48c1e81e                          shr rax, 0x1e
0000000140002e39  4833c1                            xor rax, rcx
0000000140002e3c  490fafc5                          imul rax, r13
0000000140002e40  488bc8                            mov rcx, rax
0000000140002e43  48c1e91b                          shr rcx, 0x1b
0000000140002e47  4833c8                            xor rcx, rax
0000000140002e4a  480fafcb                          imul rcx, rbx
0000000140002e4e  488bd1                            mov rdx, rcx
0000000140002e51  48c1ea1f                          shr rdx, 0x1f
0000000140002e55  4833d1                            xor rdx, rcx
0000000140002e58  4c8bda                            mov r11, rdx
0000000140002e5b  488bc2                            mov rax, rdx
0000000140002e5e  49c1eb28                          shr r11, 0x28
0000000140002e62  48c1e818                          shr rax, 0x18
0000000140002e66  4432d8                            xor r11b, al
0000000140002e69  488bc2                            mov rax, rdx
0000000140002e6c  48c1e808                          shr rax, 8
0000000140002e70  4432d8                            xor r11b, al
0000000140002e73  4432da                            xor r11b, dl
0000000140002e76  45321c38                          xor r11b, byte ptr [r8 + rdi]
0000000140002e7a  418bc1                            mov eax, r9d
0000000140002e7d  493bc2                            cmp rax, r10
0000000140002e80  7208                              jb 0x140002e8a
0000000140002e82  c645c701                          mov byte ptr [rbp - 0x39], 1
0000000140002e86  32c9                              xor cl, cl
0000000140002e88  eb70                              jmp 0x140002efa
0000000140002e8a  418bc1                            mov eax, r9d
0000000140002e8d  448bc0                            mov r8d, eax
0000000140002e90  8bc8                              mov ecx, eax
0000000140002e92  448d4801                          lea r9d, [rax + 1]
0000000140002e96  48b8157c4a7fb979379e              movabs rax, 0x9e3779b97f4a7c15
0000000140002ea0  480fafc8                          imul rcx, rax
0000000140002ea4  418bc0                            mov eax, r8d
0000000140002ea7  44894db7                          mov dword ptr [rbp - 0x49], r9d
0000000140002eab  4803ce                            add rcx, rsi
0000000140002eae  48c1e020                          shl rax, 0x20
0000000140002eb2  4833c8                            xor rcx, rax
0000000140002eb5  488bc1                            mov rax, rcx
0000000140002eb8  48c1e81e                          shr rax, 0x1e
0000000140002ebc  4833c1                            xor rax, rcx
0000000140002ebf  490fafc5                          imul rax, r13
0000000140002ec3  488bc8                            mov rcx, rax
0000000140002ec6  48c1e91b                          shr rcx, 0x1b
0000000140002eca  4833c8                            xor rcx, rax
0000000140002ecd  480fafcb                          imul rcx, rbx
0000000140002ed1  488bd1                            mov rdx, rcx
0000000140002ed4  48c1ea1f                          shr rdx, 0x1f
0000000140002ed8  4833d1                            xor rdx, rcx
0000000140002edb  488bca                            mov rcx, rdx
0000000140002ede  488bc2                            mov rax, rdx
0000000140002ee1  48c1e928                          shr rcx, 0x28
0000000140002ee5  48c1e818                          shr rax, 0x18
0000000140002ee9  32c8                              xor cl, al
0000000140002eeb  488bc2                            mov rax, rdx
0000000140002eee  48c1e808                          shr rax, 8
0000000140002ef2  32c8                              xor cl, al
0000000140002ef4  32ca                              xor cl, dl
0000000140002ef6  41320c38                          xor cl, byte ptr [r8 + rdi]
0000000140002efa  4180fb08                          cmp r11b, 8
0000000140002efe  0f837c050000                      jae 0x140003480
0000000140002f04  80f908                            cmp cl, 8
0000000140002f07  0f8373050000                      jae 0x140003480
0000000140002f0d  410fb6c3                          movzx eax, r11b
0000000140002f11  488d55d7                          lea rdx, [rbp - 0x29]
0000000140002f15  488d14c2                          lea rdx, [rdx + rax*8]
0000000140002f19  0fb6c1                            movzx eax, cl
0000000140002f1c  488b4cc5d7                        mov rcx, qword ptr [rbp + rax*8 - 0x29]
0000000140002f21  48310a                            xor qword ptr [rdx], rcx
0000000140002f24  e95b050000                        jmp 0x140003484
0000000140002f29  418bc1                            mov eax, r9d
0000000140002f2c  48bbeb113113bb49d094              movabs rbx, 0x94d049bb133111eb
0000000140002f36  493bc2                            cmp rax, r10
0000000140002f39  7209                              jb 0x140002f44
0000000140002f3b  c645c701                          mov byte ptr [rbp - 0x39], 1
0000000140002f3f  4532db                            xor r11b, r11b
0000000140002f42  eb73                              jmp 0x140002fb7
0000000140002f44  418bc1                            mov eax, r9d
0000000140002f47  448bc0                            mov r8d, eax
0000000140002f4a  8bc8                              mov ecx, eax
0000000140002f4c  448d4801                          lea r9d, [rax + 1]
0000000140002f50  48b8157c4a7fb979379e              movabs rax, 0x9e3779b97f4a7c15
0000000140002f5a  480fafc8                          imul rcx, rax
0000000140002f5e  418bc0                            mov eax, r8d
0000000140002f61  44894db7                          mov dword ptr [rbp - 0x49], r9d
0000000140002f65  48c1e020                          shl rax, 0x20
0000000140002f69  4803ce                            add rcx, rsi
0000000140002f6c  4833c8                            xor rcx, rax
0000000140002f6f  488bc1                            mov rax, rcx
0000000140002f72  48c1e81e                          shr rax, 0x1e
0000000140002f76  4833c1                            xor rax, rcx
0000000140002f79  490fafc5                          imul rax, r13
0000000140002f7d  488bc8                            mov rcx, rax
0000000140002f80  48c1e91b                          shr rcx, 0x1b
0000000140002f84  4833c8                            xor rcx, rax
0000000140002f87  480fafcb                          imul rcx, rbx
0000000140002f8b  488bd1                            mov rdx, rcx
0000000140002f8e  48c1ea1f                          shr rdx, 0x1f
0000000140002f92  4833d1                            xor rdx, rcx
0000000140002f95  4c8bda                            mov r11, rdx
0000000140002f98  488bc2                            mov rax, rdx
0000000140002f9b  49c1eb28                          shr r11, 0x28
0000000140002f9f  48c1e818                          shr rax, 0x18
0000000140002fa3  4432d8                            xor r11b, al
0000000140002fa6  488bc2                            mov rax, rdx
0000000140002fa9  48c1e808                          shr rax, 8
0000000140002fad  4432d8                            xor r11b, al
0000000140002fb0  4432da                            xor r11b, dl
0000000140002fb3  45321c38                          xor r11b, byte ptr [r8 + rdi]
0000000140002fb7  418bc1                            mov eax, r9d
0000000140002fba  493bc2                            cmp rax, r10
0000000140002fbd  7208                              jb 0x140002fc7
0000000140002fbf  c645c701                          mov byte ptr [rbp - 0x39], 1
0000000140002fc3  32c9                              xor cl, cl
0000000140002fc5  eb70                              jmp 0x140003037
0000000140002fc7  418bc1                            mov eax, r9d
0000000140002fca  448bc0                            mov r8d, eax
0000000140002fcd  8bc8                              mov ecx, eax
0000000140002fcf  448d4801                          lea r9d, [rax + 1]
0000000140002fd3  48b8157c4a7fb979379e              movabs rax, 0x9e3779b97f4a7c15
0000000140002fdd  480fafc8                          imul rcx, rax
0000000140002fe1  418bc0                            mov eax, r8d
0000000140002fe4  44894db7                          mov dword ptr [rbp - 0x49], r9d
0000000140002fe8  4803ce                            add rcx, rsi
0000000140002feb  48c1e020                          shl rax, 0x20
0000000140002fef  4833c8                            xor rcx, rax
0000000140002ff2  488bc1                            mov rax, rcx
0000000140002ff5  48c1e81e                          shr rax, 0x1e
0000000140002ff9  4833c1                            xor rax, rcx
0000000140002ffc  490fafc5                          imul rax, r13
0000000140003000  488bc8                            mov rcx, rax
0000000140003003  48c1e91b                          shr rcx, 0x1b
0000000140003007  4833c8                            xor rcx, rax
000000014000300a  480fafcb                          imul rcx, rbx
000000014000300e  488bd1                            mov rdx, rcx
0000000140003011  48c1ea1f                          shr rdx, 0x1f
0000000140003015  4833d1                            xor rdx, rcx
0000000140003018  488bca                            mov rcx, rdx
000000014000301b  488bc2                            mov rax, rdx
000000014000301e  48c1e928                          shr rcx, 0x28
0000000140003022  48c1e818                          shr rax, 0x18
0000000140003026  32c8                              xor cl, al
0000000140003028  488bc2                            mov rax, rdx
000000014000302b  48c1e808                          shr rax, 8
000000014000302f  32c8                              xor cl, al
0000000140003031  32ca                              xor cl, dl
0000000140003033  41320c38                          xor cl, byte ptr [r8 + rdi]
0000000140003037  4180fb08                          cmp r11b, 8
000000014000303b  0f833f040000                      jae 0x140003480
0000000140003041  80f908                            cmp cl, 8
0000000140003044  0f8336040000                      jae 0x140003480
000000014000304a  410fb6c3                          movzx eax, r11b
000000014000304e  488d55d7                          lea rdx, [rbp - 0x29]
0000000140003052  488d14c2                          lea rdx, [rdx + rax*8]
0000000140003056  0fb6c1                            movzx eax, cl
0000000140003059  0fb64cc5d7                        movzx ecx, byte ptr [rbp + rax*8 - 0x29]
000000014000305e  0fb602                            movzx eax, byte ptr [rdx]
0000000140003061  4833c8                            xor rcx, rax
0000000140003064  488b02                            mov rax, qword ptr [rdx]
0000000140003067  482500ffffff                      and rax, 0xffffffffffffff00
000000014000306d  480bc8                            or rcx, rax
0000000140003070  48890a                            mov qword ptr [rdx], rcx
0000000140003073  e90c040000                        jmp 0x140003484
0000000140003078  418bc1                            mov eax, r9d
000000014000307b  48bbeb113113bb49d094              movabs rbx, 0x94d049bb133111eb
0000000140003085  493bc2                            cmp rax, r10
0000000140003088  7209                              jb 0x140003093
000000014000308a  c645c701                          mov byte ptr [rbp - 0x39], 1
000000014000308e  4532db                            xor r11b, r11b
0000000140003091  eb73                              jmp 0x140003106
0000000140003093  418bc1                            mov eax, r9d
0000000140003096  448bc0                            mov r8d, eax
0000000140003099  8bc8                              mov ecx, eax
000000014000309b  448d4801                          lea r9d, [rax + 1]
000000014000309f  48b8157c4a7fb979379e              movabs rax, 0x9e3779b97f4a7c15
00000001400030a9  480fafc8                          imul rcx, rax
00000001400030ad  418bc0                            mov eax, r8d
00000001400030b0  44894db7                          mov dword ptr [rbp - 0x49], r9d
00000001400030b4  48c1e020                          shl rax, 0x20
00000001400030b8  4803ce                            add rcx, rsi
00000001400030bb  4833c8                            xor rcx, rax
00000001400030be  488bc1                            mov rax, rcx
00000001400030c1  48c1e81e                          shr rax, 0x1e
00000001400030c5  4833c1                            xor rax, rcx
00000001400030c8  490fafc5                          imul rax, r13
00000001400030cc  488bc8                            mov rcx, rax
00000001400030cf  48c1e91b                          shr rcx, 0x1b
00000001400030d3  4833c8                            xor rcx, rax
00000001400030d6  480fafcb                          imul rcx, rbx
00000001400030da  488bd1                            mov rdx, rcx
00000001400030dd  48c1ea1f                          shr rdx, 0x1f
00000001400030e1  4833d1                            xor rdx, rcx
00000001400030e4  4c8bda                            mov r11, rdx
00000001400030e7  488bc2                            mov rax, rdx
00000001400030ea  49c1eb28                          shr r11, 0x28
00000001400030ee  48c1e818                          shr rax, 0x18
00000001400030f2  4432d8                            xor r11b, al
00000001400030f5  488bc2                            mov rax, rdx
00000001400030f8  48c1e808                          shr rax, 8
00000001400030fc  4432d8                            xor r11b, al
00000001400030ff  4432da                            xor r11b, dl
0000000140003102  45321c38                          xor r11b, byte ptr [r8 + rdi]
0000000140003106  418bc1                            mov eax, r9d
0000000140003109  493bc2                            cmp rax, r10
000000014000310c  7208                              jb 0x140003116
000000014000310e  c645c701                          mov byte ptr [rbp - 0x39], 1
0000000140003112  32c9                              xor cl, cl
0000000140003114  eb70                              jmp 0x140003186
0000000140003116  418bc1                            mov eax, r9d
0000000140003119  448bc0                            mov r8d, eax
000000014000311c  8bc8                              mov ecx, eax
000000014000311e  448d4801                          lea r9d, [rax + 1]
0000000140003122  48b8157c4a7fb979379e              movabs rax, 0x9e3779b97f4a7c15
000000014000312c  480fafc8                          imul rcx, rax
0000000140003130  418bc0                            mov eax, r8d
0000000140003133  44894db7                          mov dword ptr [rbp - 0x49], r9d
0000000140003137  4803ce                            add rcx, rsi
000000014000313a  48c1e020                          shl rax, 0x20
000000014000313e  4833c8                            xor rcx, rax
0000000140003141  488bc1                            mov rax, rcx
0000000140003144  48c1e81e                          shr rax, 0x1e
0000000140003148  4833c1                            xor rax, rcx
000000014000314b  490fafc5                          imul rax, r13
000000014000314f  488bc8                            mov rcx, rax
0000000140003152  48c1e91b                          shr rcx, 0x1b
0000000140003156  4833c8                            xor rcx, rax
0000000140003159  480fafcb                          imul rcx, rbx
000000014000315d  488bd1                            mov rdx, rcx
0000000140003160  48c1ea1f                          shr rdx, 0x1f
0000000140003164  4833d1                            xor rdx, rcx
0000000140003167  488bca                            mov rcx, rdx
000000014000316a  488bc2                            mov rax, rdx
000000014000316d  48c1e928                          shr rcx, 0x28
0000000140003171  48c1e818                          shr rax, 0x18
0000000140003175  32c8                              xor cl, al
0000000140003177  488bc2                            mov rax, rdx
000000014000317a  48c1e808                          shr rax, 8
000000014000317e  32c8                              xor cl, al
0000000140003180  32ca                              xor cl, dl
0000000140003182  41320c38                          xor cl, byte ptr [r8 + rdi]
0000000140003186  4180fb08                          cmp r11b, 8
000000014000318a  0f83f0020000                      jae 0x140003480
0000000140003190  80f908                            cmp cl, 8
0000000140003193  0f83e7020000                      jae 0x140003480
0000000140003199  410fb6c3                          movzx eax, r11b
000000014000319d  488d55d7                          lea rdx, [rbp - 0x29]
00000001400031a1  488d14c2                          lea rdx, [rdx + rax*8]
00000001400031a5  0fb6c1                            movzx eax, cl
00000001400031a8  488b4cc5d7                        mov rcx, qword ptr [rbp + rax*8 - 0x29]
00000001400031ad  48010a                            add qword ptr [rdx], rcx
00000001400031b0  e9cf020000                        jmp 0x140003484
00000001400031b5  418bc1                            mov eax, r9d
00000001400031b8  48bbeb113113bb49d094              movabs rbx, 0x94d049bb133111eb
00000001400031c2  493bc2                            cmp rax, r10
00000001400031c5  7209                              jb 0x1400031d0
00000001400031c7  c645c701                          mov byte ptr [rbp - 0x39], 1
00000001400031cb  4532db                            xor r11b, r11b
00000001400031ce  eb73                              jmp 0x140003243
00000001400031d0  418bc1                            mov eax, r9d
00000001400031d3  448bc0                            mov r8d, eax
00000001400031d6  8bc8                              mov ecx, eax
00000001400031d8  448d4801                          lea r9d, [rax + 1]
00000001400031dc  48b8157c4a7fb979379e              movabs rax, 0x9e3779b97f4a7c15
00000001400031e6  480fafc8                          imul rcx, rax
00000001400031ea  418bc0                            mov eax, r8d
00000001400031ed  44894db7                          mov dword ptr [rbp - 0x49], r9d
00000001400031f1  48c1e020                          shl rax, 0x20
00000001400031f5  4803ce                            add rcx, rsi
00000001400031f8  4833c8                            xor rcx, rax
00000001400031fb  488bc1                            mov rax, rcx
00000001400031fe  48c1e81e                          shr rax, 0x1e
0000000140003202  4833c1                            xor rax, rcx
0000000140003205  490fafc5                          imul rax, r13
0000000140003209  488bc8                            mov rcx, rax
000000014000320c  48c1e91b                          shr rcx, 0x1b
0000000140003210  4833c8                            xor rcx, rax
0000000140003213  480fafcb                          imul rcx, rbx
0000000140003217  488bd1                            mov rdx, rcx
000000014000321a  48c1ea1f                          shr rdx, 0x1f
000000014000321e  4833d1                            xor rdx, rcx
0000000140003221  4c8bda                            mov r11, rdx
0000000140003224  488bc2                            mov rax, rdx
0000000140003227  49c1eb28                          shr r11, 0x28
000000014000322b  48c1e818                          shr rax, 0x18
000000014000322f  4432d8                            xor r11b, al
0000000140003232  488bc2                            mov rax, rdx
0000000140003235  48c1e808                          shr rax, 8
0000000140003239  4432d8                            xor r11b, al
000000014000323c  4432da                            xor r11b, dl
000000014000323f  45321c38                          xor r11b, byte ptr [r8 + rdi]
0000000140003243  418bc1                            mov eax, r9d
0000000140003246  493bc2                            cmp rax, r10
0000000140003249  7208                              jb 0x140003253
000000014000324b  c645c701                          mov byte ptr [rbp - 0x39], 1
000000014000324f  32c9                              xor cl, cl
0000000140003251  eb70                              jmp 0x1400032c3
0000000140003253  418bc1                            mov eax, r9d
0000000140003256  448bc0                            mov r8d, eax
0000000140003259  8bc8                              mov ecx, eax
000000014000325b  448d4801                          lea r9d, [rax + 1]
000000014000325f  48b8157c4a7fb979379e              movabs rax, 0x9e3779b97f4a7c15
0000000140003269  480fafc8                          imul rcx, rax
000000014000326d  418bc0                            mov eax, r8d
0000000140003270  44894db7                          mov dword ptr [rbp - 0x49], r9d
0000000140003274  4803ce                            add rcx, rsi
0000000140003277  48c1e020                          shl rax, 0x20
000000014000327b  4833c8                            xor rcx, rax
000000014000327e  488bc1                            mov rax, rcx
0000000140003281  48c1e81e                          shr rax, 0x1e
0000000140003285  4833c1                            xor rax, rcx
0000000140003288  490fafc5                          imul rax, r13
000000014000328c  488bc8                            mov rcx, rax
000000014000328f  48c1e91b                          shr rcx, 0x1b
0000000140003293  4833c8                            xor rcx, rax
0000000140003296  480fafcb                          imul rcx, rbx
000000014000329a  488bd1                            mov rdx, rcx
000000014000329d  48c1ea1f                          shr rdx, 0x1f
00000001400032a1  4833d1                            xor rdx, rcx
00000001400032a4  488bca                            mov rcx, rdx
00000001400032a7  488bc2                            mov rax, rdx
00000001400032aa  48c1e928                          shr rcx, 0x28
00000001400032ae  48c1e818                          shr rax, 0x18
00000001400032b2  32c8                              xor cl, al
00000001400032b4  488bc2                            mov rax, rdx
00000001400032b7  48c1e808                          shr rax, 8
00000001400032bb  32c8                              xor cl, al
00000001400032bd  32ca                              xor cl, dl
00000001400032bf  41320c38                          xor cl, byte ptr [r8 + rdi]
00000001400032c3  4180fb08                          cmp r11b, 8
00000001400032c7  0f83b3010000                      jae 0x140003480
00000001400032cd  80f908                            cmp cl, 8
00000001400032d0  0f83aa010000                      jae 0x140003480
00000001400032d6  410fb6c3                          movzx eax, r11b
00000001400032da  488d55d7                          lea rdx, [rbp - 0x29]
00000001400032de  488d14c2                          lea rdx, [rdx + rax*8]
00000001400032e2  0fb6c1                            movzx eax, cl
00000001400032e5  0fb64cc5d7                        movzx ecx, byte ptr [rbp + rax*8 - 0x29]
00000001400032ea  48010a                            add qword ptr [rdx], rcx
00000001400032ed  e992010000                        jmp 0x140003484
00000001400032f2  418bc1                            mov eax, r9d
00000001400032f5  493bc2                            cmp rax, r10
00000001400032f8  721f                              jb 0x140003319
00000001400032fa  488d4da7                          lea rcx, [rbp - 0x59]
00000001400032fe  c645c701                          mov byte ptr [rbp - 0x39], 1
0000000140003302  32db                              xor bl, bl
0000000140003304  e837efffff                        call 0x140002240
0000000140003309  488bc8                            mov rcx, rax
000000014000330c  0fb6c3                            movzx eax, bl
000000014000330f  48014cc5d7                        add qword ptr [rbp + rax*8 - 0x29], rcx
0000000140003314  e9ecf6ffff                        jmp 0x140002a05
0000000140003319  418d4101                          lea eax, [r9 + 1]
000000014000331d  418bc9                            mov ecx, r9d
0000000140003320  8945b7                            mov dword ptr [rbp - 0x49], eax
0000000140003323  48bbeb113113bb49d094              movabs rbx, 0x94d049bb133111eb
000000014000332d  48b8157c4a7fb979379e              movabs rax, 0x9e3779b97f4a7c15
0000000140003337  458bc1                            mov r8d, r9d
000000014000333a  480fafc8                          imul rcx, rax
000000014000333e  418bc1                            mov eax, r9d
0000000140003341  48c1e020                          shl rax, 0x20
0000000140003345  4803ce                            add rcx, rsi
0000000140003348  4833c8                            xor rcx, rax
000000014000334b  488bc1                            mov rax, rcx
000000014000334e  48c1e81e                          shr rax, 0x1e
0000000140003352  4833c1                            xor rax, rcx
0000000140003355  490fafc5                          imul rax, r13
0000000140003359  488bc8                            mov rcx, rax
000000014000335c  48c1e91b                          shr rcx, 0x1b
0000000140003360  4833c8                            xor rcx, rax
0000000140003363  480fafcb                          imul rcx, rbx
0000000140003367  488bd1                            mov rdx, rcx
000000014000336a  48c1ea1f                          shr rdx, 0x1f
000000014000336e  4833d1                            xor rdx, rcx
0000000140003371  488d4da7                          lea rcx, [rbp - 0x59]
0000000140003375  488bda                            mov rbx, rdx
0000000140003378  488bc2                            mov rax, rdx
000000014000337b  48c1eb28                          shr rbx, 0x28
000000014000337f  48c1e818                          shr rax, 0x18
0000000140003383  32d8                              xor bl, al
0000000140003385  488bc2                            mov rax, rdx
0000000140003388  48c1e808                          shr rax, 8
000000014000338c  32d8                              xor bl, al
000000014000338e  32da                              xor bl, dl
0000000140003390  41321c38                          xor bl, byte ptr [r8 + rdi]
0000000140003394  e8a7eeffff                        call 0x140002240
0000000140003399  488bc8                            mov rcx, rax
000000014000339c  80fb08                            cmp bl, 8
000000014000339f  0f83cb000000                      jae 0x140003470
00000001400033a5  0fb6c3                            movzx eax, bl
00000001400033a8  48014cc5d7                        add qword ptr [rbp + rax*8 - 0x29], rcx
00000001400033ad  e953f6ffff                        jmp 0x140002a05
00000001400033b2  418bc1                            mov eax, r9d
00000001400033b5  493bc2                            cmp rax, r10
00000001400033b8  7220                              jb 0x1400033da
00000001400033ba  488d4da7                          lea rcx, [rbp - 0x59]
00000001400033be  c645c701                          mov byte ptr [rbp - 0x39], 1
00000001400033c2  32db                              xor bl, bl
00000001400033c4  e877eeffff                        call 0x140002240
00000001400033c9  488bc8                            mov rcx, rax
00000001400033cc  0fb6c3                            movzx eax, bl
00000001400033cf  480faf4cc5d7                      imul rcx, qword ptr [rbp + rax*8 - 0x29]
00000001400033d5  e926f6ffff                        jmp 0x140002a00
00000001400033da  418d4101                          lea eax, [r9 + 1]
00000001400033de  418bc9                            mov ecx, r9d
00000001400033e1  8945b7                            mov dword ptr [rbp - 0x49], eax
00000001400033e4  48bbeb113113bb49d094              movabs rbx, 0x94d049bb133111eb
00000001400033ee  48b8157c4a7fb979379e              movabs rax, 0x9e3779b97f4a7c15
00000001400033f8  458bc1                            mov r8d, r9d
00000001400033fb  480fafc8                          imul rcx, rax
00000001400033ff  418bc1                            mov eax, r9d
0000000140003402  48c1e020                          shl rax, 0x20
0000000140003406  4803ce                            add rcx, rsi
0000000140003409  4833c8                            xor rcx, rax
000000014000340c  488bc1                            mov rax, rcx
000000014000340f  48c1e81e                          shr rax, 0x1e
0000000140003413  4833c1                            xor rax, rcx
0000000140003416  490fafc5                          imul rax, r13
000000014000341a  488bc8                            mov rcx, rax
000000014000341d  48c1e91b                          shr rcx, 0x1b
0000000140003421  4833c8                            xor rcx, rax
0000000140003424  480fafcb                          imul rcx, rbx
0000000140003428  488bd1                            mov rdx, rcx
000000014000342b  48c1ea1f                          shr rdx, 0x1f
000000014000342f  4833d1                            xor rdx, rcx
0000000140003432  488d4da7                          lea rcx, [rbp - 0x59]
0000000140003436  488bda                            mov rbx, rdx
0000000140003439  488bc2                            mov rax, rdx
000000014000343c  48c1eb28                          shr rbx, 0x28
0000000140003440  48c1e818                          shr rax, 0x18
0000000140003444  32d8                              xor bl, al
0000000140003446  488bc2                            mov rax, rdx
0000000140003449  48c1e808                          shr rax, 8
000000014000344d  32d8                              xor bl, al
000000014000344f  32da                              xor bl, dl
0000000140003451  41321c38                          xor bl, byte ptr [r8 + rdi]
0000000140003455  e8e6edffff                        call 0x140002240
000000014000345a  488bc8                            mov rcx, rax
000000014000345d  80fb08                            cmp bl, 8
0000000140003460  730e                              jae 0x140003470
0000000140003462  0fb6c3                            movzx eax, bl
0000000140003465  480faf4cc5d7                      imul rcx, qword ptr [rbp + rax*8 - 0x29]
000000014000346b  e990f5ffff                        jmp 0x140002a00
0000000140003470  488b75bf                          mov rsi, qword ptr [rbp - 0x41]
0000000140003474  448b4db7                          mov r9d, dword ptr [rbp - 0x49]
0000000140003478  4c8b55af                          mov r10, qword ptr [rbp - 0x51]
000000014000347c  488b7da7                          mov rdi, qword ptr [rbp - 0x59]
0000000140003480  c6451901                          mov byte ptr [rbp + 0x19], 1
0000000140003484  807d1800                          cmp byte ptr [rbp + 0x18], 0
0000000140003488  0f8576040000                      jne 0x140003904
000000014000348e  e974f3ffff                        jmp 0x140002807
0000000140003493  418bc1                            mov eax, r9d
0000000140003496  48bbeb113113bb49d094              movabs rbx, 0x94d049bb133111eb
00000001400034a0  493bc2                            cmp rax, r10
00000001400034a3  7209                              jb 0x1400034ae
00000001400034a5  c645c701                          mov byte ptr [rbp - 0x39], 1
00000001400034a9  4532db                            xor r11b, r11b
00000001400034ac  eb73                              jmp 0x140003521
00000001400034ae  418bc1                            mov eax, r9d
00000001400034b1  448bc0                            mov r8d, eax
00000001400034b4  8bc8                              mov ecx, eax
00000001400034b6  448d4801                          lea r9d, [rax + 1]
00000001400034ba  48b8157c4a7fb979379e              movabs rax, 0x9e3779b97f4a7c15
00000001400034c4  480fafc8                          imul rcx, rax
00000001400034c8  418bc0                            mov eax, r8d
00000001400034cb  44894db7                          mov dword ptr [rbp - 0x49], r9d
00000001400034cf  48c1e020                          shl rax, 0x20
00000001400034d3  4803ce                            add rcx, rsi
00000001400034d6  4833c8                            xor rcx, rax
00000001400034d9  488bc1                            mov rax, rcx
00000001400034dc  48c1e81e                          shr rax, 0x1e
00000001400034e0  4833c1                            xor rax, rcx
00000001400034e3  490fafc5                          imul rax, r13
00000001400034e7  488bc8                            mov rcx, rax
00000001400034ea  48c1e91b                          shr rcx, 0x1b
00000001400034ee  4833c8                            xor rcx, rax
00000001400034f1  480fafcb                          imul rcx, rbx
00000001400034f5  488bd1                            mov rdx, rcx
00000001400034f8  48c1ea1f                          shr rdx, 0x1f
00000001400034fc  4833d1                            xor rdx, rcx
00000001400034ff  4c8bda                            mov r11, rdx
0000000140003502  488bc2                            mov rax, rdx
0000000140003505  49c1eb28                          shr r11, 0x28
0000000140003509  48c1e818                          shr rax, 0x18
000000014000350d  4432d8                            xor r11b, al
0000000140003510  488bc2                            mov rax, rdx
0000000140003513  48c1e808                          shr rax, 8
0000000140003517  4432d8                            xor r11b, al
000000014000351a  4432da                            xor r11b, dl
000000014000351d  45321c38                          xor r11b, byte ptr [r8 + rdi]
0000000140003521  418bc1                            mov eax, r9d
0000000140003524  493bc2                            cmp rax, r10
0000000140003527  7208                              jb 0x140003531
0000000140003529  c645c701                          mov byte ptr [rbp - 0x39], 1
000000014000352d  32c9                              xor cl, cl
000000014000352f  eb70                              jmp 0x1400035a1
0000000140003531  418bc1                            mov eax, r9d
0000000140003534  448bc0                            mov r8d, eax
0000000140003537  8bc8                              mov ecx, eax
0000000140003539  448d4801                          lea r9d, [rax + 1]
000000014000353d  48b8157c4a7fb979379e              movabs rax, 0x9e3779b97f4a7c15
0000000140003547  480fafc8                          imul rcx, rax
000000014000354b  418bc0                            mov eax, r8d
000000014000354e  44894db7                          mov dword ptr [rbp - 0x49], r9d
0000000140003552  4803ce                            add rcx, rsi
0000000140003555  48c1e020                          shl rax, 0x20
0000000140003559  4833c8                            xor rcx, rax
000000014000355c  488bc1                            mov rax, rcx
000000014000355f  48c1e81e                          shr rax, 0x1e
0000000140003563  4833c1                            xor rax, rcx
0000000140003566  490fafc5                          imul rax, r13
000000014000356a  488bc8                            mov rcx, rax
000000014000356d  48c1e91b                          shr rcx, 0x1b
0000000140003571  4833c8                            xor rcx, rax
0000000140003574  480fafcb                          imul rcx, rbx
0000000140003578  488bd1                            mov rdx, rcx
000000014000357b  48c1ea1f                          shr rdx, 0x1f
000000014000357f  4833d1                            xor rdx, rcx
0000000140003582  488bca                            mov rcx, rdx
0000000140003585  488bc2                            mov rax, rdx
0000000140003588  48c1e928                          shr rcx, 0x28
000000014000358c  48c1e818                          shr rax, 0x18
0000000140003590  32c8                              xor cl, al
0000000140003592  488bc2                            mov rax, rdx
0000000140003595  48c1e808                          shr rax, 8
0000000140003599  32c8                              xor cl, al
000000014000359b  32ca                              xor cl, dl
000000014000359d  41320c38                          xor cl, byte ptr [r8 + rdi]
00000001400035a1  4180fb08                          cmp r11b, 8
00000001400035a5  0f83d5feffff                      jae 0x140003480
00000001400035ab  410fb6c3                          movzx eax, r11b
00000001400035af  488d55d7                          lea rdx, [rbp - 0x29]
00000001400035b3  488d14c2                          lea rdx, [rdx + rax*8]
00000001400035b7  488b02                            mov rax, qword ptr [rdx]
00000001400035ba  83e13f                            and ecx, 0x3f
00000001400035bd  7403                              je 0x1400035c2
00000001400035bf  48d3c0                            rol rax, cl
00000001400035c2  488902                            mov qword ptr [rdx], rax
00000001400035c5  e9bafeffff                        jmp 0x140003484
00000001400035ca  418bc1                            mov eax, r9d
00000001400035cd  48bbeb113113bb49d094              movabs rbx, 0x94d049bb133111eb
00000001400035d7  493bc2                            cmp rax, r10
00000001400035da  7208                              jb 0x1400035e4
00000001400035dc  c645c701                          mov byte ptr [rbp - 0x39], 1
00000001400035e0  32c9                              xor cl, cl
00000001400035e2  eb79                              jmp 0x14000365d
00000001400035e4  418bc1                            mov eax, r9d
00000001400035e7  448bc0                            mov r8d, eax
00000001400035ea  8bc8                              mov ecx, eax
00000001400035ec  448d4801                          lea r9d, [rax + 1]
00000001400035f0  48b8157c4a7fb979379e              movabs rax, 0x9e3779b97f4a7c15
00000001400035fa  480fafc8                          imul rcx, rax
00000001400035fe  418bc0                            mov eax, r8d
0000000140003601  44894db7                          mov dword ptr [rbp - 0x49], r9d
0000000140003605  4803ce                            add rcx, rsi
0000000140003608  48c1e020                          shl rax, 0x20
000000014000360c  4833c8                            xor rcx, rax
000000014000360f  488bc1                            mov rax, rcx
0000000140003612  48c1e81e                          shr rax, 0x1e
0000000140003616  4833c1                            xor rax, rcx
0000000140003619  490fafc5                          imul rax, r13
000000014000361d  488bc8                            mov rcx, rax
0000000140003620  48c1e91b                          shr rcx, 0x1b
0000000140003624  4833c8                            xor rcx, rax
0000000140003627  480fafcb                          imul rcx, rbx
000000014000362b  488bd1                            mov rdx, rcx
000000014000362e  48c1ea1f                          shr rdx, 0x1f
0000000140003632  4833d1                            xor rdx, rcx
0000000140003635  488bca                            mov rcx, rdx
0000000140003638  488bc2                            mov rax, rdx
000000014000363b  48c1e928                          shr rcx, 0x28
000000014000363f  48c1e818                          shr rax, 0x18
0000000140003643  32c8                              xor cl, al
0000000140003645  488bc2                            mov rax, rdx
0000000140003648  48c1e808                          shr rax, 8
000000014000364c  32c8                              xor cl, al
000000014000364e  32ca                              xor cl, dl
0000000140003650  41320c38                          xor cl, byte ptr [r8 + rdi]
0000000140003654  80f908                            cmp cl, 8
0000000140003657  0f8323feffff                      jae 0x140003480
000000014000365d  0fb6c1                            movzx eax, cl
0000000140003660  4c8d45d7                          lea r8, [rbp - 0x29]
0000000140003664  4d8d04c0                          lea r8, [r8 + rax*8]
0000000140003668  498b00                            mov rax, qword ptr [r8]
000000014000366b  488bc8                            mov rcx, rax
000000014000366e  48c1e91e                          shr rcx, 0x1e
0000000140003672  4833c8                            xor rcx, rax
0000000140003675  490fafcd                          imul rcx, r13
0000000140003679  488bd1                            mov rdx, rcx
000000014000367c  48c1ea1b                          shr rdx, 0x1b
0000000140003680  4833d1                            xor rdx, rcx
0000000140003683  480fafd3                          imul rdx, rbx
0000000140003687  488bc2                            mov rax, rdx
000000014000368a  48c1e81f                          shr rax, 0x1f
000000014000368e  4833c2                            xor rax, rdx
0000000140003691  498900                            mov qword ptr [r8], rax
0000000140003694  e9ebfdffff                        jmp 0x140003484
0000000140003699  418bc1                            mov eax, r9d
000000014000369c  493bc2                            cmp rax, r10
000000014000369f  7213                              jb 0x1400036b4
00000001400036a1  32c9                              xor cl, cl
00000001400036a3  c645c701                          mov byte ptr [rbp - 0x39], 1
00000001400036a7  0fb6c1                            movzx eax, cl
00000001400036aa  48ff44c5d7                        inc qword ptr [rbp + rax*8 - 0x29]
00000001400036af  e9d0fdffff                        jmp 0x140003484
00000001400036b4  418bc1                            mov eax, r9d
00000001400036b7  48bbeb113113bb49d094              movabs rbx, 0x94d049bb133111eb
00000001400036c1  448bc0                            mov r8d, eax
00000001400036c4  8bc8                              mov ecx, eax
00000001400036c6  448d4801                          lea r9d, [rax + 1]
00000001400036ca  48b8157c4a7fb979379e              movabs rax, 0x9e3779b97f4a7c15
00000001400036d4  480fafc8                          imul rcx, rax
00000001400036d8  418bc0                            mov eax, r8d
00000001400036db  44894db7                          mov dword ptr [rbp - 0x49], r9d
00000001400036df  4803ce                            add rcx, rsi
00000001400036e2  48c1e020                          shl rax, 0x20
00000001400036e6  4833c8                            xor rcx, rax
00000001400036e9  488bc1                            mov rax, rcx
00000001400036ec  48c1e81e                          shr rax, 0x1e
00000001400036f0  4833c1                            xor rax, rcx
00000001400036f3  490fafc5                          imul rax, r13
00000001400036f7  488bc8                            mov rcx, rax
00000001400036fa  48c1e91b                          shr rcx, 0x1b
00000001400036fe  4833c8                            xor rcx, rax
0000000140003701  480fafcb                          imul rcx, rbx
0000000140003705  488bd1                            mov rdx, rcx
0000000140003708  48c1ea1f                          shr rdx, 0x1f
000000014000370c  4833d1                            xor rdx, rcx
000000014000370f  488bca                            mov rcx, rdx
0000000140003712  488bc2                            mov rax, rdx
0000000140003715  48c1e928                          shr rcx, 0x28
0000000140003719  48c1e818                          shr rax, 0x18
000000014000371d  32c8                              xor cl, al
000000014000371f  488bc2                            mov rax, rdx
0000000140003722  48c1e808                          shr rax, 8
0000000140003726  32c8                              xor cl, al
0000000140003728  32ca                              xor cl, dl
000000014000372a  41320c38                          xor cl, byte ptr [r8 + rdi]
000000014000372e  80f908                            cmp cl, 8
0000000140003731  0f8349fdffff                      jae 0x140003480
0000000140003737  0fb6c1                            movzx eax, cl
000000014000373a  48ff44c5d7                        inc qword ptr [rbp + rax*8 - 0x29]
000000014000373f  e940fdffff                        jmp 0x140003484
0000000140003744  418bc1                            mov eax, r9d
0000000140003747  48bbeb113113bb49d094              movabs rbx, 0x94d049bb133111eb
0000000140003751  493bc2                            cmp rax, r10
0000000140003754  7209                              jb 0x14000375f
0000000140003756  c645c701                          mov byte ptr [rbp - 0x39], 1
000000014000375a  4532db                            xor r11b, r11b
000000014000375d  eb73                              jmp 0x1400037d2
000000014000375f  418bc1                            mov eax, r9d
0000000140003762  448bc0                            mov r8d, eax
0000000140003765  8bc8                              mov ecx, eax
0000000140003767  448d4801                          lea r9d, [rax + 1]
000000014000376b  48b8157c4a7fb979379e              movabs rax, 0x9e3779b97f4a7c15
0000000140003775  480fafc8                          imul rcx, rax
0000000140003779  418bc0                            mov eax, r8d
000000014000377c  44894db7                          mov dword ptr [rbp - 0x49], r9d
0000000140003780  48c1e020                          shl rax, 0x20
0000000140003784  4803ce                            add rcx, rsi
0000000140003787  4833c8                            xor rcx, rax
000000014000378a  488bc1                            mov rax, rcx
000000014000378d  48c1e81e                          shr rax, 0x1e
0000000140003791  4833c1                            xor rax, rcx
0000000140003794  490fafc5                          imul rax, r13
0000000140003798  488bc8                            mov rcx, rax
000000014000379b  48c1e91b                          shr rcx, 0x1b
000000014000379f  4833c8                            xor rcx, rax
00000001400037a2  480fafcb                          imul rcx, rbx
00000001400037a6  488bd1                            mov rdx, rcx
00000001400037a9  48c1ea1f                          shr rdx, 0x1f
00000001400037ad  4833d1                            xor rdx, rcx
00000001400037b0  4c8bda                            mov r11, rdx
00000001400037b3  488bc2                            mov rax, rdx
00000001400037b6  49c1eb28                          shr r11, 0x28
00000001400037ba  48c1e818                          shr rax, 0x18
00000001400037be  4432d8                            xor r11b, al
00000001400037c1  488bc2                            mov rax, rdx
00000001400037c4  48c1e808                          shr rax, 8
00000001400037c8  4432d8                            xor r11b, al
00000001400037cb  4432da                            xor r11b, dl
00000001400037ce  45321c38                          xor r11b, byte ptr [r8 + rdi]
00000001400037d2  418bc1                            mov eax, r9d
00000001400037d5  493bc2                            cmp rax, r10
00000001400037d8  7208                              jb 0x1400037e2
00000001400037da  c645c701                          mov byte ptr [rbp - 0x39], 1
00000001400037de  32c9                              xor cl, cl
00000001400037e0  eb70                              jmp 0x140003852
00000001400037e2  418bc1                            mov eax, r9d
00000001400037e5  448bc0                            mov r8d, eax
00000001400037e8  8bc8                              mov ecx, eax
00000001400037ea  448d4801                          lea r9d, [rax + 1]
00000001400037ee  48b8157c4a7fb979379e              movabs rax, 0x9e3779b97f4a7c15
00000001400037f8  480fafc8                          imul rcx, rax
00000001400037fc  418bc0                            mov eax, r8d
00000001400037ff  44894db7                          mov dword ptr [rbp - 0x49], r9d
0000000140003803  4803ce                            add rcx, rsi
0000000140003806  48c1e020                          shl rax, 0x20
000000014000380a  4833c8                            xor rcx, rax
000000014000380d  488bc1                            mov rax, rcx
0000000140003810  48c1e81e                          shr rax, 0x1e
0000000140003814  4833c1                            xor rax, rcx
0000000140003817  490fafc5                          imul rax, r13
000000014000381b  488bc8                            mov rcx, rax
000000014000381e  48c1e91b                          shr rcx, 0x1b
0000000140003822  4833c8                            xor rcx, rax
0000000140003825  480fafcb                          imul rcx, rbx
0000000140003829  488bd1                            mov rdx, rcx
000000014000382c  48c1ea1f                          shr rdx, 0x1f
0000000140003830  4833d1                            xor rdx, rcx
0000000140003833  488bca                            mov rcx, rdx
0000000140003836  488bc2                            mov rax, rdx
0000000140003839  48c1e928                          shr rcx, 0x28
000000014000383d  48c1e818                          shr rax, 0x18
0000000140003841  32c8                              xor cl, al
0000000140003843  488bc2                            mov rax, rdx
0000000140003846  48c1e808                          shr rax, 8
000000014000384a  32c8                              xor cl, al
000000014000384c  32ca                              xor cl, dl
000000014000384e  41320c38                          xor cl, byte ptr [r8 + rdi]
0000000140003852  4180fb08                          cmp r11b, 8
0000000140003856  0f8324fcffff                      jae 0x140003480
000000014000385c  80f908                            cmp cl, 8
000000014000385f  0f831bfcffff                      jae 0x140003480
0000000140003865  0fb6c1                            movzx eax, cl
0000000140003868  410fb6cb                          movzx ecx, r11b
000000014000386c  488b44c5d7                        mov rax, qword ptr [rbp + rax*8 - 0x29]
0000000140003871  483944cdd7                        cmp qword ptr [rbp + rcx*8 - 0x29], rax
0000000140003876  0f924517                          setb byte ptr [rbp + 0x17]
000000014000387a  e905fcffff                        jmp 0x140003484
000000014000387f  488d4da7                          lea rcx, [rbp - 0x59]
0000000140003883  e878e7ffff                        call 0x140002000
0000000140003888  807d1700                          cmp byte ptr [rbp + 0x17], 0
000000014000388c  0f8473f1ffff                      je 0x140002a05
0000000140003892  448b4db7                          mov r9d, dword ptr [rbp - 0x49]
0000000140003896  4863d0                            movsxd rdx, eax
0000000140003899  4903d1                            add rdx, r9
000000014000389c  784d                              js 0x1400038eb
000000014000389e  4c8b55af                          mov r10, qword ptr [rbp - 0x51]
00000001400038a2  493bd2                            cmp rdx, r10
00000001400038a5  7748                              ja 0x1400038ef
00000001400038a7  488b75bf                          mov rsi, qword ptr [rbp - 0x41]
00000001400038ab  448bca                            mov r9d, edx
00000001400038ae  488b7da7                          mov rdi, qword ptr [rbp - 0x59]
00000001400038b2  8955b7                            mov dword ptr [rbp - 0x49], edx
00000001400038b5  e9cafbffff                        jmp 0x140003484
00000001400038ba  488d4da7                          lea rcx, [rbp - 0x59]
00000001400038be  e83de7ffff                        call 0x140002000
00000001400038c3  448b4db7                          mov r9d, dword ptr [rbp - 0x49]
00000001400038c7  4863d0                            movsxd rdx, eax
00000001400038ca  4903d1                            add rdx, r9
00000001400038cd  781c                              js 0x1400038eb
00000001400038cf  4c8b55af                          mov r10, qword ptr [rbp - 0x51]
00000001400038d3  493bd2                            cmp rdx, r10
00000001400038d6  7717                              ja 0x1400038ef
00000001400038d8  488b75bf                          mov rsi, qword ptr [rbp - 0x41]
00000001400038dc  448bca                            mov r9d, edx
00000001400038df  488b7da7                          mov rdi, qword ptr [rbp - 0x59]
00000001400038e3  8955b7                            mov dword ptr [rbp - 0x49], edx
00000001400038e6  e999fbffff                        jmp 0x140003484
00000001400038eb  4c8b55af                          mov r10, qword ptr [rbp - 0x51]
00000001400038ef  488b75bf                          mov rsi, qword ptr [rbp - 0x41]
00000001400038f3  488b7da7                          mov rdi, qword ptr [rbp - 0x59]
00000001400038f7  c645c701                          mov byte ptr [rbp - 0x39], 1
00000001400038fb  e984fbffff                        jmp 0x140003484
0000000140003900  c6451801                          mov byte ptr [rbp + 0x18], 1
0000000140003904  0fb64519                          movzx eax, byte ptr [rbp + 0x19]
0000000140003908  4d85ff                            test r15, r15
000000014000390b  4c8bac24e8000000                  mov r13, qword ptr [rsp + 0xe8]
0000000140003913  b901000000                        mov ecx, 1
0000000140003918  0f44c1                            cmove eax, ecx
000000014000391b  807d1800                          cmp byte ptr [rbp + 0x18], 0
000000014000391f  740e                              je 0x14000392f
