# Reverse engineering notes — "The Wellness Ring Bypass"

## Binary
- amd64 PIE, Full RELRO, Canary, NX, CET (SHSTK + IBT). GLIBC 2.34/2.38/2.39 (Ubuntu 24.04 container).
- No file I/O functions imported (no open/read/system/fopen) -> no direct flag read -> RCE required.

## Custom heap (firmware heap)
- 16 buckets (size 16..256, align16 -> index = align16>>4). Each bucket owns a 0x20000 pool (malloc'd on first use).
- Bucket table @ BSS 0x50a0, stride 0x1028. [entry]=pool, [entry+8]=align16 size, [entry+0x10]=bump offset,
  [entry+0x18]=free-list ring of offsets (0x200 slots), [entry+0x1018]=free-list head idx, [entry+0x1020]=free count.
- Alloc 0x131a(size): bump or reuse free-list offset. Chunk addr = pool + offset.
- Free 0x14e0(ptr,size): bounds+align check, memsets 0, pushes offset to free-list.
- LIVE_BYTES @ BSS 0x5080.

## Globals (BSS)
- 0x50a0: bucket table (0x50a0 + 16*0x1028 = 0x15320)
- 0x16360: descriptor ptr table (64 * 8) ; 0x16560: descriptor count
- 0x16580: sensor cache records (24 bytes: [0]=ptr,[8]=size,[0x10]=active) ; 0x17780: cache count
- 0x177a0: serial buffer (0x20)
- 0x177c0=&0x5020("HRV-DEMO-2026"); 0x177c8=&0x177a0; 0x177e0=&0x177e0; 0x177e8=&0x177e0; 0x177f0=&0x177c0; 0x17800=1; 0x17808=0x20

## Descriptors
- Context descriptor (menu 1): alloc 0x78 (bucket 8, chunk 0x80). Fields: +0x00 type=1,+0x04 id,+0x08 0x2026,
  +0x10 valid=1, +0x18 0x2026, +0x20 handle(input), +0x28 "CNYSCNYQ", +0x30 getpid, +0x38 0x2026,
  +0x40/+0x48/+0x50 = self, +0x58 = handle, +0x68 "GerC", +0x70 = [0x17780].
- Readiness descriptor (menu 2): alloc 0xc0 (bucket 12). Same header; +0x80/+0x88=0x20, +0x90/+0x94=1,
  +0x98=&0x177a0, +0xa0/+0xa8/+0xb0=&0x177e0.

## Menu
1=alloc context  2=alloc readiness  3=alloc sensor cache  4=patch cache qword  5=release cache
6=dump readiness counters(1a04)  7=dump sleep-stage window(1a8c)  8=commit recovery sync(1b90)
9=show debug state  10=exit

## Key primitives (validate via 18e4: [obj+0x10]&1 && [obj+0x18]==0x2026)
- menu6 (1a04): printf 5 fields from obj+0x80..+0x98.
- menu7 (1a8c): desc = align8([obj+0xa0]); p=*(desc+0x10); src=*p; dump `len` bytes at src.
- menu8 (1b90): desc = align8([obj+0xb0]); p=*(desc+0x10); src=*p; dest=*(p+8);
  memmove(dest, src, n) with n=dword(desc+0x28).
- Validation 196d(desc,len): [desc+0x20]==1 (dword), [desc+0x10]!=0,
  dword[desc+0x28] in 1..0x80 AND size >= len (jae).
- menu7 prints `fw-sleep-stage-window: ` then `%02x` bytes then newline.
- menu 10 (0x260a) does NOT call exit(); it `mov eax,0; pop rbp; ret` from main.
  `__libc_start_call_main` then `call exit` at libc+0x2a1cc (saved RIP = libc+0x2a1ca).

## Bug: context descriptor OOB + cache overlap
- Context descriptor chunk is 0x80 bytes but menu6/7/8 read obj+0x80..+0xb8.
- **Trap:** context alloc also calls 0x1d0c which mallocs a lost 0x80 `rx-guard` sentinel
  immediately after the context. Naive `ctx then cache` makes OOB hit the sentinel
  (menu6 shows `64726175672d7872` = "rx-guard"), not a patchable cache.
- **Layout fix:** alloc cache0+cache1 (0x80), **free cache0**, then alloc context.
  Context reuses off 0; sentinel goes to bump 0x100; live cache1 stays at off 0x80
  = context+0x80. menu6 then leaks cache1[0]=heap and cache1[8]=&HRV-DEMO (PIE).
- menu4 on cache1 => control ctx+0xa0/+0xb0. Fake desc in a later cache; pair {src,dest}
  at *(desc+0x10). size at desc+0x28 must be >= dump len.

## RCE plan
- Leak heap (cache0) + PIE via menu6-on-context.
- Fake desc at cache1; {src,dest} pair at cache2; payload at cache3.
- Arbitrary read: pair.src=addr, dump via menu7 (skip the `fw-sleep-stage-window: ` prefix when parsing hex).
- Arbitrary write <=0x80: payload in cache3, pair={cache3, dest}, menu8.
- Do NOT smash stdout (printf still uses it). Two 0x80 writes of House of Apple 2 onto stderr.
- Menu 10 returns from main → libc exit() flushes stderr → system("  sh").
- Flag path: /home/oura/flag.txt
- Old exploit bugs: MAIN_RET 0x2a264 is init not main (real=0x2a1ca); missing extra deref on desc+0x10; size=1 with dump 8 fails 196d; hex parse ate the prefix.
