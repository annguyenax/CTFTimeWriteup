0000000140002000  4053                              push rbx
0000000140002002  55                                push rbp
0000000140002003  56                                push rsi
0000000140002004  57                                push rdi
0000000140002005  4156                              push r14
0000000140002007  4c8b5908                          mov r11, qword ptr [rcx + 8]
000000014000200b  4c8bc9                            mov r9, rcx
000000014000200e  448b5110                          mov r10d, dword ptr [rcx + 0x10]
0000000140002012  48be157c4a7fb979379e              movabs rsi, 0x9e3779b97f4a7c15
000000014000201c  48bdb9e5e41c6d4758bf              movabs rbp, 0xbf58476d1ce4e5b9
0000000140002026  49beeb113113bb49d094              movabs r14, 0x94d049bb133111eb
0000000140002030  4d3bd3                            cmp r10, r11
0000000140002033  7208                              jb 0x14000203d
0000000140002035  c6412001                          mov byte ptr [rcx + 0x20], 1
0000000140002039  32db                              xor bl, bl
000000014000203b  eb68                              jmp 0x1400020a5
000000014000203d  458d4201                          lea r8d, [r10 + 1]
0000000140002041  498bc2                            mov rax, r10
0000000140002044  44894110                          mov dword ptr [rcx + 0x10], r8d
0000000140002048  498bca                            mov rcx, r10
000000014000204b  48c1e020                          shl rax, 0x20
000000014000204f  480fafce                          imul rcx, rsi
0000000140002053  49034918                          add rcx, qword ptr [r9 + 0x18]
0000000140002057  4833c8                            xor rcx, rax
000000014000205a  488bc1                            mov rax, rcx
000000014000205d  48c1e81e                          shr rax, 0x1e
0000000140002061  4833c1                            xor rax, rcx
0000000140002064  480fafc5                          imul rax, rbp
0000000140002068  488bc8                            mov rcx, rax
000000014000206b  48c1e91b                          shr rcx, 0x1b
000000014000206f  4833c8                            xor rcx, rax
0000000140002072  490fafce                          imul rcx, r14
0000000140002076  488bd1                            mov rdx, rcx
0000000140002079  48c1ea1f                          shr rdx, 0x1f
000000014000207d  4833d1                            xor rdx, rcx
0000000140002080  498b09                            mov rcx, qword ptr [r9]
0000000140002083  488bda                            mov rbx, rdx
0000000140002086  488bc2                            mov rax, rdx
0000000140002089  48c1eb28                          shr rbx, 0x28
000000014000208d  48c1e818                          shr rax, 0x18
0000000140002091  32d8                              xor bl, al
0000000140002093  488bc2                            mov rax, rdx
0000000140002096  48c1e808                          shr rax, 8
000000014000209a  32d8                              xor bl, al
000000014000209c  32da                              xor bl, dl
000000014000209e  41321c0a                          xor bl, byte ptr [r10 + rcx]
00000001400020a2  458bd0                            mov r10d, r8d
00000001400020a5  0fb6fb                            movzx edi, bl
00000001400020a8  418bda                            mov ebx, r10d
00000001400020ab  493bdb                            cmp rbx, r11
00000001400020ae  720a                              jb 0x1400020ba
00000001400020b0  41c6412001                        mov byte ptr [r9 + 0x20], 1
00000001400020b5  4532c0                            xor r8b, r8b
00000001400020b8  eb68                              jmp 0x140002122
00000001400020ba  418d4201                          lea eax, [r10 + 1]
00000001400020be  488bcb                            mov rcx, rbx
00000001400020c1  41894110                          mov dword ptr [r9 + 0x10], eax
00000001400020c5  488bc3                            mov rax, rbx
00000001400020c8  48c1e020                          shl rax, 0x20
00000001400020cc  480fafce                          imul rcx, rsi
00000001400020d0  49034918                          add rcx, qword ptr [r9 + 0x18]
00000001400020d4  4833c8                            xor rcx, rax
00000001400020d7  488bc1                            mov rax, rcx
00000001400020da  48c1e81e                          shr rax, 0x1e
00000001400020de  4833c1                            xor rax, rcx
00000001400020e1  480fafc5                          imul rax, rbp
00000001400020e5  488bc8                            mov rcx, rax
00000001400020e8  48c1e91b                          shr rcx, 0x1b
00000001400020ec  4833c8                            xor rcx, rax
00000001400020ef  490fafce                          imul rcx, r14
00000001400020f3  488bd1                            mov rdx, rcx
00000001400020f6  48c1ea1f                          shr rdx, 0x1f
00000001400020fa  4833d1                            xor rdx, rcx
00000001400020fd  498b09                            mov rcx, qword ptr [r9]
0000000140002100  4c8bc2                            mov r8, rdx
0000000140002103  488bc2                            mov rax, rdx
0000000140002106  49c1e828                          shr r8, 0x28
000000014000210a  48c1e818                          shr rax, 0x18
000000014000210e  4432c0                            xor r8b, al
0000000140002111  488bc2                            mov rax, rdx
0000000140002114  48c1e808                          shr rax, 8
0000000140002118  4432c0                            xor r8b, al
000000014000211b  4432c2                            xor r8b, dl
000000014000211e  4432040b                          xor r8b, byte ptr [rbx + rcx]
0000000140002122  418b5910                          mov ebx, dword ptr [r9 + 0x10]
0000000140002126  450fb6d0                          movzx r10d, r8b
000000014000212a  41c1e208                          shl r10d, 8
000000014000212e  440bd7                            or r10d, edi
0000000140002131  493bdb                            cmp rbx, r11
0000000140002134  720a                              jb 0x140002140
0000000140002136  41c6412001                        mov byte ptr [r9 + 0x20], 1
000000014000213b  4532c0                            xor r8b, r8b
000000014000213e  eb67                              jmp 0x1400021a7
0000000140002140  8d4301                            lea eax, [rbx + 1]
0000000140002143  488bcb                            mov rcx, rbx
0000000140002146  41894110                          mov dword ptr [r9 + 0x10], eax
000000014000214a  488bc3                            mov rax, rbx
000000014000214d  48c1e020                          shl rax, 0x20
0000000140002151  480fafce                          imul rcx, rsi
0000000140002155  49034918                          add rcx, qword ptr [r9 + 0x18]
0000000140002159  4833c8                            xor rcx, rax
000000014000215c  488bc1                            mov rax, rcx
000000014000215f  48c1e81e                          shr rax, 0x1e
0000000140002163  4833c1                            xor rax, rcx
0000000140002166  480fafc5                          imul rax, rbp
000000014000216a  488bc8                            mov rcx, rax
000000014000216d  48c1e91b                          shr rcx, 0x1b
0000000140002171  4833c8                            xor rcx, rax
0000000140002174  490fafce                          imul rcx, r14
0000000140002178  488bd1                            mov rdx, rcx
000000014000217b  48c1ea1f                          shr rdx, 0x1f
000000014000217f  4833d1                            xor rdx, rcx
0000000140002182  498b09                            mov rcx, qword ptr [r9]
0000000140002185  4c8bc2                            mov r8, rdx
0000000140002188  488bc2                            mov rax, rdx
000000014000218b  49c1e828                          shr r8, 0x28
000000014000218f  48c1e818                          shr rax, 0x18
0000000140002193  4432c0                            xor r8b, al
0000000140002196  488bc2                            mov rax, rdx
0000000140002199  48c1e808                          shr rax, 8
000000014000219d  4432c0                            xor r8b, al
00000001400021a0  4432c2                            xor r8b, dl
00000001400021a3  4432040b                          xor r8b, byte ptr [rbx + rcx]
00000001400021a7  450fb6c0                          movzx r8d, r8b
00000001400021ab  41c1e010                          shl r8d, 0x10
00000001400021af  450bc2                            or r8d, r10d
00000001400021b2  458b5110                          mov r10d, dword ptr [r9 + 0x10]
00000001400021b6  4d3bd3                            cmp r10, r11
00000001400021b9  720a                              jb 0x1400021c5
00000001400021bb  41c6412001                        mov byte ptr [r9 + 0x20], 1
00000001400021c0  4532c9                            xor r9b, r9b
00000001400021c3  eb68                              jmp 0x14000222d
00000001400021c5  418d4201                          lea eax, [r10 + 1]
00000001400021c9  498bca                            mov rcx, r10
00000001400021cc  41894110                          mov dword ptr [r9 + 0x10], eax
00000001400021d0  498bc2                            mov rax, r10
00000001400021d3  48c1e020                          shl rax, 0x20
00000001400021d7  480fafce                          imul rcx, rsi
00000001400021db  49034918                          add rcx, qword ptr [r9 + 0x18]
00000001400021df  4833c8                            xor rcx, rax
00000001400021e2  488bc1                            mov rax, rcx
00000001400021e5  48c1e81e                          shr rax, 0x1e
00000001400021e9  4833c1                            xor rax, rcx
00000001400021ec  480fafc5                          imul rax, rbp
00000001400021f0  488bc8                            mov rcx, rax
00000001400021f3  48c1e91b                          shr rcx, 0x1b
00000001400021f7  4833c8                            xor rcx, rax
00000001400021fa  490fafce                          imul rcx, r14
00000001400021fe  488bd1                            mov rdx, rcx
0000000140002201  48c1ea1f                          shr rdx, 0x1f
0000000140002205  4833d1                            xor rdx, rcx
0000000140002208  498b09                            mov rcx, qword ptr [r9]
000000014000220b  4c8bca                            mov r9, rdx
000000014000220e  488bc2                            mov rax, rdx
0000000140002211  49c1e928                          shr r9, 0x28
0000000140002215  48c1e818                          shr rax, 0x18
0000000140002219  4432c8                            xor r9b, al
000000014000221c  488bc2                            mov rax, rdx
000000014000221f  48c1e808                          shr rax, 8
0000000140002223  4432c8                            xor r9b, al
0000000140002226  4432ca                            xor r9b, dl
0000000140002229  45320c0a                          xor r9b, byte ptr [r10 + rcx]
000000014000222d  410fb6c1                          movzx eax, r9b
0000000140002231  c1e018                            shl eax, 0x18
0000000140002234  410bc0                            or eax, r8d
0000000140002237  415e                              pop r14
0000000140002239  5f                                pop rdi
000000014000223a  5e                                pop rsi
000000014000223b  5d                                pop rbp
000000014000223c  5b                                pop rbx
000000014000223d  c3                                ret 
