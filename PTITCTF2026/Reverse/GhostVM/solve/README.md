# GhostVM solver

```text
python solve_ghostvm.py     # emulate VM1, write vm2_bytecode.bin
python disasm_vm2.py        # disassemble VM2 → vm2.asm
python invert_feistel.py    # invert 16 Feistel rounds, print flag
```

Binary used: `D:\download\ctf-scratch\ptitctf2026_ghostvm\GhostVM.exe`
(extracted from `files/GhostVM.zip`).

Live check: pipe the 32-byte flag to `GhostVM.exe`; expect `Correct flag!`.
