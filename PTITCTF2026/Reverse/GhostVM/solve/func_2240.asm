0000000140002240  4053                              push rbx
0000000140002242  55                                push rbp
0000000140002243  56                                push rsi
0000000140002244  57                                push rdi
0000000140002245  4156                              push r14
0000000140002247  4c8b5108                          mov r10, qword ptr [rcx + 8]
000000014000224b  4c8bc9                            mov r9, rcx
000000014000224e  448b5910                          mov r11d, dword ptr [rcx + 0x10]
0000000140002252  48be157c4a7fb979379e              movabs rsi, 0x9e3779b97f4a7c15
000000014000225c  48bdb9e5e41c6d4758bf              movabs rbp, 0xbf58476d1ce4e5b9
0000000140002266  49beeb113113bb49d094              movabs r14, 0x94d049bb133111eb
0000000140002270  4d3bda                            cmp r11, r10
0000000140002273  7208                              jb 0x14000227d
0000000140002275  c6412001                          mov byte ptr [rcx + 0x20], 1
0000000140002279  32db                              xor bl, bl
000000014000227b  eb68                              jmp 0x1400022e5
000000014000227d  458d4301                          lea r8d, [r11 + 1]
0000000140002281  498bc3                            mov rax, r11
0000000140002284  44894110                          mov dword ptr [rcx + 0x10], r8d
0000000140002288  498bcb                            mov rcx, r11
000000014000228b  48c1e020                          shl rax, 0x20
000000014000228f  480fafce                          imul rcx, rsi
0000000140002293  49034918                          add rcx, qword ptr [r9 + 0x18]
0000000140002297  4833c8                            xor rcx, rax
000000014000229a  488bc1                            mov rax, rcx
000000014000229d  48c1e81e                          shr rax, 0x1e
00000001400022a1  4833c1                            xor rax, rcx
00000001400022a4  480fafc5                          imul rax, rbp
00000001400022a8  488bc8                            mov rcx, rax
00000001400022ab  48c1e91b                          shr rcx, 0x1b
00000001400022af  4833c8                            xor rcx, rax
00000001400022b2  490fafce                          imul rcx, r14
00000001400022b6  488bd1                            mov rdx, rcx
00000001400022b9  48c1ea1f                          shr rdx, 0x1f
00000001400022bd  4833d1                            xor rdx, rcx
00000001400022c0  498b09                            mov rcx, qword ptr [r9]
00000001400022c3  488bda                            mov rbx, rdx
00000001400022c6  488bc2                            mov rax, rdx
00000001400022c9  48c1eb28                          shr rbx, 0x28
00000001400022cd  48c1e818                          shr rax, 0x18
00000001400022d1  32d8                              xor bl, al
00000001400022d3  488bc2                            mov rax, rdx
00000001400022d6  48c1e808                          shr rax, 8
00000001400022da  32d8                              xor bl, al
00000001400022dc  32da                              xor bl, dl
00000001400022de  41321c0b                          xor bl, byte ptr [r11 + rcx]
00000001400022e2  458bd8                            mov r11d, r8d
00000001400022e5  0fb6fb                            movzx edi, bl
00000001400022e8  418bdb                            mov ebx, r11d
00000001400022eb  493bda                            cmp rbx, r10
00000001400022ee  720a                              jb 0x1400022fa
00000001400022f0  41c6412001                        mov byte ptr [r9 + 0x20], 1
00000001400022f5  4532c0                            xor r8b, r8b
00000001400022f8  eb68                              jmp 0x140002362
00000001400022fa  418d4301                          lea eax, [r11 + 1]
00000001400022fe  488bcb                            mov rcx, rbx
0000000140002301  41894110                          mov dword ptr [r9 + 0x10], eax
0000000140002305  488bc3                            mov rax, rbx
0000000140002308  48c1e020                          shl rax, 0x20
000000014000230c  480fafce                          imul rcx, rsi
0000000140002310  49034918                          add rcx, qword ptr [r9 + 0x18]
0000000140002314  4833c8                            xor rcx, rax
0000000140002317  488bc1                            mov rax, rcx
000000014000231a  48c1e81e                          shr rax, 0x1e
000000014000231e  4833c1                            xor rax, rcx
0000000140002321  480fafc5                          imul rax, rbp
0000000140002325  488bc8                            mov rcx, rax
0000000140002328  48c1e91b                          shr rcx, 0x1b
000000014000232c  4833c8                            xor rcx, rax
000000014000232f  490fafce                          imul rcx, r14
0000000140002333  488bd1                            mov rdx, rcx
0000000140002336  48c1ea1f                          shr rdx, 0x1f
000000014000233a  4833d1                            xor rdx, rcx
000000014000233d  498b09                            mov rcx, qword ptr [r9]
0000000140002340  4c8bc2                            mov r8, rdx
0000000140002343  488bc2                            mov rax, rdx
0000000140002346  49c1e828                          shr r8, 0x28
000000014000234a  48c1e818                          shr rax, 0x18
000000014000234e  4432c0                            xor r8b, al
0000000140002351  488bc2                            mov rax, rdx
0000000140002354  48c1e808                          shr rax, 8
0000000140002358  4432c0                            xor r8b, al
000000014000235b  4432c2                            xor r8b, dl
000000014000235e  4432040b                          xor r8b, byte ptr [rbx + rcx]
0000000140002362  418b5910                          mov ebx, dword ptr [r9 + 0x10]
0000000140002366  450fb6c0                          movzx r8d, r8b
000000014000236a  49c1e008                          shl r8, 8
000000014000236e  4c0bc7                            or r8, rdi
0000000140002371  493bda                            cmp rbx, r10
0000000140002374  720a                              jb 0x140002380
0000000140002376  41c6412001                        mov byte ptr [r9 + 0x20], 1
000000014000237b  4532db                            xor r11b, r11b
000000014000237e  eb67                              jmp 0x1400023e7
0000000140002380  8d4301                            lea eax, [rbx + 1]
0000000140002383  488bcb                            mov rcx, rbx
0000000140002386  41894110                          mov dword ptr [r9 + 0x10], eax
000000014000238a  488bc3                            mov rax, rbx
000000014000238d  48c1e020                          shl rax, 0x20
0000000140002391  480fafce                          imul rcx, rsi
0000000140002395  49034918                          add rcx, qword ptr [r9 + 0x18]
0000000140002399  4833c8                            xor rcx, rax
000000014000239c  488bc1                            mov rax, rcx
000000014000239f  48c1e81e                          shr rax, 0x1e
00000001400023a3  4833c1                            xor rax, rcx
00000001400023a6  480fafc5                          imul rax, rbp
00000001400023aa  488bc8                            mov rcx, rax
00000001400023ad  48c1e91b                          shr rcx, 0x1b
00000001400023b1  4833c8                            xor rcx, rax
00000001400023b4  490fafce                          imul rcx, r14
00000001400023b8  488bd1                            mov rdx, rcx
00000001400023bb  48c1ea1f                          shr rdx, 0x1f
00000001400023bf  4833d1                            xor rdx, rcx
00000001400023c2  498b09                            mov rcx, qword ptr [r9]
00000001400023c5  4c8bda                            mov r11, rdx
00000001400023c8  488bc2                            mov rax, rdx
00000001400023cb  49c1eb28                          shr r11, 0x28
00000001400023cf  48c1e818                          shr rax, 0x18
00000001400023d3  4432d8                            xor r11b, al
00000001400023d6  488bc2                            mov rax, rdx
00000001400023d9  48c1e808                          shr rax, 8
00000001400023dd  4432d8                            xor r11b, al
00000001400023e0  4432da                            xor r11b, dl
00000001400023e3  44321c0b                          xor r11b, byte ptr [rbx + rcx]
00000001400023e7  418b5910                          mov ebx, dword ptr [r9 + 0x10]
00000001400023eb  450fb6db                          movzx r11d, r11b
00000001400023ef  49c1e310                          shl r11, 0x10
00000001400023f3  4d0bd8                            or r11, r8
00000001400023f6  493bda                            cmp rbx, r10
00000001400023f9  720a                              jb 0x140002405
00000001400023fb  41c6412001                        mov byte ptr [r9 + 0x20], 1
0000000140002400  4532c0                            xor r8b, r8b
0000000140002403  eb67                              jmp 0x14000246c
0000000140002405  8d4301                            lea eax, [rbx + 1]
0000000140002408  488bcb                            mov rcx, rbx
000000014000240b  41894110                          mov dword ptr [r9 + 0x10], eax
000000014000240f  488bc3                            mov rax, rbx
0000000140002412  48c1e020                          shl rax, 0x20
0000000140002416  480fafce                          imul rcx, rsi
000000014000241a  49034918                          add rcx, qword ptr [r9 + 0x18]
000000014000241e  4833c8                            xor rcx, rax
0000000140002421  488bc1                            mov rax, rcx
0000000140002424  48c1e81e                          shr rax, 0x1e
0000000140002428  4833c1                            xor rax, rcx
000000014000242b  480fafc5                          imul rax, rbp
000000014000242f  488bc8                            mov rcx, rax
0000000140002432  48c1e91b                          shr rcx, 0x1b
0000000140002436  4833c8                            xor rcx, rax
0000000140002439  490fafce                          imul rcx, r14
000000014000243d  488bd1                            mov rdx, rcx
0000000140002440  48c1ea1f                          shr rdx, 0x1f
0000000140002444  4833d1                            xor rdx, rcx
0000000140002447  498b09                            mov rcx, qword ptr [r9]
000000014000244a  4c8bc2                            mov r8, rdx
000000014000244d  488bc2                            mov rax, rdx
0000000140002450  49c1e828                          shr r8, 0x28
0000000140002454  48c1e818                          shr rax, 0x18
0000000140002458  4432c0                            xor r8b, al
000000014000245b  488bc2                            mov rax, rdx
000000014000245e  48c1e808                          shr rax, 8
0000000140002462  4432c0                            xor r8b, al
0000000140002465  4432c2                            xor r8b, dl
0000000140002468  4432040b                          xor r8b, byte ptr [rbx + rcx]
000000014000246c  418b5910                          mov ebx, dword ptr [r9 + 0x10]
0000000140002470  450fb6c0                          movzx r8d, r8b
0000000140002474  49c1e018                          shl r8, 0x18
0000000140002478  4d0bc3                            or r8, r11
000000014000247b  493bda                            cmp rbx, r10
000000014000247e  720a                              jb 0x14000248a
0000000140002480  41c6412001                        mov byte ptr [r9 + 0x20], 1
0000000140002485  4532db                            xor r11b, r11b
0000000140002488  eb67                              jmp 0x1400024f1
000000014000248a  8d4301                            lea eax, [rbx + 1]
000000014000248d  488bcb                            mov rcx, rbx
0000000140002490  41894110                          mov dword ptr [r9 + 0x10], eax
0000000140002494  488bc3                            mov rax, rbx
0000000140002497  48c1e020                          shl rax, 0x20
000000014000249b  480fafce                          imul rcx, rsi
000000014000249f  49034918                          add rcx, qword ptr [r9 + 0x18]
00000001400024a3  4833c8                            xor rcx, rax
00000001400024a6  488bc1                            mov rax, rcx
00000001400024a9  48c1e81e                          shr rax, 0x1e
00000001400024ad  4833c1                            xor rax, rcx
00000001400024b0  480fafc5                          imul rax, rbp
00000001400024b4  488bc8                            mov rcx, rax
00000001400024b7  48c1e91b                          shr rcx, 0x1b
00000001400024bb  4833c8                            xor rcx, rax
00000001400024be  490fafce                          imul rcx, r14
00000001400024c2  488bd1                            mov rdx, rcx
00000001400024c5  48c1ea1f                          shr rdx, 0x1f
00000001400024c9  4833d1                            xor rdx, rcx
00000001400024cc  498b09                            mov rcx, qword ptr [r9]
00000001400024cf  4c8bda                            mov r11, rdx
00000001400024d2  488bc2                            mov rax, rdx
00000001400024d5  49c1eb28                          shr r11, 0x28
00000001400024d9  48c1e818                          shr rax, 0x18
00000001400024dd  4432d8                            xor r11b, al
00000001400024e0  488bc2                            mov rax, rdx
00000001400024e3  48c1e808                          shr rax, 8
00000001400024e7  4432d8                            xor r11b, al
00000001400024ea  4432da                            xor r11b, dl
00000001400024ed  44321c0b                          xor r11b, byte ptr [rbx + rcx]
00000001400024f1  418b5910                          mov ebx, dword ptr [r9 + 0x10]
00000001400024f5  450fb6db                          movzx r11d, r11b
00000001400024f9  49c1e320                          shl r11, 0x20
00000001400024fd  4d0bd8                            or r11, r8
0000000140002500  493bda                            cmp rbx, r10
0000000140002503  720a                              jb 0x14000250f
0000000140002505  41c6412001                        mov byte ptr [r9 + 0x20], 1
000000014000250a  4532c0                            xor r8b, r8b
000000014000250d  eb67                              jmp 0x140002576
000000014000250f  8d4301                            lea eax, [rbx + 1]
0000000140002512  488bcb                            mov rcx, rbx
0000000140002515  41894110                          mov dword ptr [r9 + 0x10], eax
0000000140002519  488bc3                            mov rax, rbx
000000014000251c  48c1e020                          shl rax, 0x20
0000000140002520  480fafce                          imul rcx, rsi
0000000140002524  49034918                          add rcx, qword ptr [r9 + 0x18]
0000000140002528  4833c8                            xor rcx, rax
000000014000252b  488bc1                            mov rax, rcx
000000014000252e  48c1e81e                          shr rax, 0x1e
0000000140002532  4833c1                            xor rax, rcx
0000000140002535  480fafc5                          imul rax, rbp
0000000140002539  488bc8                            mov rcx, rax
000000014000253c  48c1e91b                          shr rcx, 0x1b
0000000140002540  4833c8                            xor rcx, rax
0000000140002543  490fafce                          imul rcx, r14
0000000140002547  488bd1                            mov rdx, rcx
000000014000254a  48c1ea1f                          shr rdx, 0x1f
000000014000254e  4833d1                            xor rdx, rcx
0000000140002551  498b09                            mov rcx, qword ptr [r9]
0000000140002554  4c8bc2                            mov r8, rdx
0000000140002557  488bc2                            mov rax, rdx
000000014000255a  49c1e828                          shr r8, 0x28
000000014000255e  48c1e818                          shr rax, 0x18
0000000140002562  4432c0                            xor r8b, al
0000000140002565  488bc2                            mov rax, rdx
0000000140002568  48c1e808                          shr rax, 8
000000014000256c  4432c0                            xor r8b, al
000000014000256f  4432c2                            xor r8b, dl
0000000140002572  4432040b                          xor r8b, byte ptr [rbx + rcx]
0000000140002576  410fb6d8                          movzx ebx, r8b
000000014000257a  48c1e328                          shl rbx, 0x28
000000014000257e  490bdb                            or rbx, r11
0000000140002581  458b5910                          mov r11d, dword ptr [r9 + 0x10]
0000000140002585  4d3bda                            cmp r11, r10
0000000140002588  720a                              jb 0x140002594
000000014000258a  41c6412001                        mov byte ptr [r9 + 0x20], 1
000000014000258f  4532c0                            xor r8b, r8b
0000000140002592  eb68                              jmp 0x1400025fc
0000000140002594  418d4301                          lea eax, [r11 + 1]
0000000140002598  498bcb                            mov rcx, r11
000000014000259b  41894110                          mov dword ptr [r9 + 0x10], eax
000000014000259f  498bc3                            mov rax, r11
00000001400025a2  48c1e020                          shl rax, 0x20
00000001400025a6  480fafce                          imul rcx, rsi
00000001400025aa  49034918                          add rcx, qword ptr [r9 + 0x18]
00000001400025ae  4833c8                            xor rcx, rax
00000001400025b1  488bc1                            mov rax, rcx
00000001400025b4  48c1e81e                          shr rax, 0x1e
00000001400025b8  4833c1                            xor rax, rcx
00000001400025bb  480fafc5                          imul rax, rbp
00000001400025bf  488bc8                            mov rcx, rax
00000001400025c2  48c1e91b                          shr rcx, 0x1b
00000001400025c6  4833c8                            xor rcx, rax
00000001400025c9  490fafce                          imul rcx, r14
00000001400025cd  488bd1                            mov rdx, rcx
00000001400025d0  48c1ea1f                          shr rdx, 0x1f
00000001400025d4  4833d1                            xor rdx, rcx
00000001400025d7  498b09                            mov rcx, qword ptr [r9]
00000001400025da  4c8bc2                            mov r8, rdx
00000001400025dd  488bc2                            mov rax, rdx
00000001400025e0  49c1e828                          shr r8, 0x28
00000001400025e4  48c1e818                          shr rax, 0x18
00000001400025e8  4432c0                            xor r8b, al
00000001400025eb  488bc2                            mov rax, rdx
00000001400025ee  48c1e808                          shr rax, 8
00000001400025f2  4432c0                            xor r8b, al
00000001400025f5  4432c2                            xor r8b, dl
00000001400025f8  4532040b                          xor r8b, byte ptr [r11 + rcx]
00000001400025fc  458b5910                          mov r11d, dword ptr [r9 + 0x10]
0000000140002600  450fb6c0                          movzx r8d, r8b
0000000140002604  49c1e030                          shl r8, 0x30
0000000140002608  4c0bc3                            or r8, rbx
000000014000260b  4d3bda                            cmp r11, r10
000000014000260e  720a                              jb 0x14000261a
0000000140002610  41c6412001                        mov byte ptr [r9 + 0x20], 1
0000000140002615  4532c9                            xor r9b, r9b
0000000140002618  eb68                              jmp 0x140002682
000000014000261a  418d4301                          lea eax, [r11 + 1]
000000014000261e  498bcb                            mov rcx, r11
0000000140002621  41894110                          mov dword ptr [r9 + 0x10], eax
0000000140002625  498bc3                            mov rax, r11
0000000140002628  48c1e020                          shl rax, 0x20
000000014000262c  480fafce                          imul rcx, rsi
0000000140002630  49034918                          add rcx, qword ptr [r9 + 0x18]
0000000140002634  4833c8                            xor rcx, rax
0000000140002637  488bc1                            mov rax, rcx
000000014000263a  48c1e81e                          shr rax, 0x1e
000000014000263e  4833c1                            xor rax, rcx
0000000140002641  480fafc5                          imul rax, rbp
0000000140002645  488bc8                            mov rcx, rax
0000000140002648  48c1e91b                          shr rcx, 0x1b
000000014000264c  4833c8                            xor rcx, rax
000000014000264f  490fafce                          imul rcx, r14
0000000140002653  488bd1                            mov rdx, rcx
0000000140002656  48c1ea1f                          shr rdx, 0x1f
000000014000265a  4833d1                            xor rdx, rcx
000000014000265d  498b09                            mov rcx, qword ptr [r9]
0000000140002660  4c8bca                            mov r9, rdx
0000000140002663  488bc2                            mov rax, rdx
0000000140002666  49c1e928                          shr r9, 0x28
000000014000266a  48c1e818                          shr rax, 0x18
000000014000266e  4432c8                            xor r9b, al
0000000140002671  488bc2                            mov rax, rdx
0000000140002674  48c1e808                          shr rax, 8
0000000140002678  4432c8                            xor r9b, al
000000014000267b  4432ca                            xor r9b, dl
000000014000267e  45320c0b                          xor r9b, byte ptr [r11 + rcx]
0000000140002682  410fb6c1                          movzx eax, r9b
0000000140002686  48c1e038                          shl rax, 0x38
000000014000268a  490bc0                            or rax, r8
000000014000268d  415e                              pop r14
000000014000268f  5f                                pop rdi
0000000140002690  5e                                pop rsi
0000000140002691  5d                                pop rbp
0000000140002692  5b                                pop rbx
0000000140002693  c3                                ret 
