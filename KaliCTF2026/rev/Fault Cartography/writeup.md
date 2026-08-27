# Fault Cartography (REV) - Writeup

## Analysis
The binary `faultline` reads `faultline.map` which contains a 78-byte header and 256 nodes of 24 bytes each, representing a 16x16 grid of VM nodes.

1. **Header Parsing**: 
   - `r9_key` is extracted from bytes `0x0e-0x16` of the header.
   - Initial `state_x` and `state_y` are derived from the key and header bytes `0x0c` and `0x0d`.

2. **Node Decryption**:
   The nodes are encrypted. The VM loop dynamically decrypts each accessed node using `r9_key`, `index`, and several hardcoded constants in a 3-iteration PRNG loop.

3. **VM Execution**:
   - The VM runs for exactly 104 steps (extracted from header bytes `0x06-0x08`).
   - At each step, it executes a node which consists of 3 QWORDS, defining one of several operations (Type 0, 1, 2) acting on a virtual register state of 6 QWORDS (48 bytes).
   - After each step, `state_x` and `state_y` are updated based on a direction derived from the node's 6th byte.
   - The PRNG state (`PRNG_VAL`) is also updated using `step`, `state_x`, `state_y`, and the node's 3rd QWORD.

4. **Target Verification**:
   After 104 steps, a target stream is generated using the final `PRNG_VAL` and bytes `0x16-0x45` of the header. The final VM register state must match this target stream.

## Solution
1. Pre-decrypt all 256 nodes.
2. Trace the path through the grid for 104 steps, recording the sequence of nodes and calculating the final `PRNG_VAL`.
3. Generate the target stream using the final `PRNG_VAL` and XOR it with the header bytes.
4. Run the path backwards, applying the inverse of each VM operation to the target registers.
5. XOR the initial VM state with the initial stream generated from `r9_key` to recover the flag.

## Flag
`KaliTeam{faults_draw_the_only_honest_path}`
