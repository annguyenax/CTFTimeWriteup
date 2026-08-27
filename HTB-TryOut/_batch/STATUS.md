# HTB Try Out — batch status
rev/FlagCasino | SOLVED (HTB, local writeup thiếu)
rev/LootStash | SOLVED (HTB, local writeup thiếu)
rev/Don't Panic! | SOLVED (HTB, local writeup thiếu)
rev/Satellite Hijack | SOLVED HTB{l4y3r5_0n_l4y3r5_0n_l4y3r5!}
web/Jailbreak | SOLVED HTB{b1om3tric_l0cks_4nd_fl1cker1ng_l1ghts_...}
web/OmniWatch | SOLVED HTB{h3110_41w4y5_i_s3e_y0u4nd_1m_w4tch1ng_...}
crypto/Dynastic | SOLVED HTB{DID_YOU_KNOW_ABOUT_THE_TRITHEMIUS_CIPHER?!_IT_IS_SIMILAR_TO_CAESAR_CIPHER} (by Claude)
web/TimeKORP | SOLVED HTB{t1m3_f0r_th3_ult1m4t3_pwn4g3_...} (Grok)
web/Flag Command | SOLVED HTB{D3v3l0p3r_t00l5_4r3_b35t_...} (Grok)
web/Guild | SOLVED HTB{mult1pl3_lo0p5_mult1pl3_h0les_...} (Grok)

# DeepSeek batch (this process) — file-based offline solves, sequential
# 1. rev/Don't Panic! | SOLVED HTB{d0nt_p4n1c_c4tch_the_3rror}
# 2. rev/FlagCasino | SOLVED HTB{r4nd_1s_v3ry_pr3d1ct4bl3}
# 3. rev/LootStash | SOLVED HTB{n33dl3_1n_a_l00t_stack}
# 4. rev/TunnelMadness | SOLVED HTB{UUURFURURRFRRFFUUFURRUFUFFRFUFUUUUFFRRUUUFURFDFFUFFRRRRRFRR}
# 5. crypto/Blessed | DEFERRED (hard oracle, BLS+P-256 HNP, evidence saved, will revisit)
# 6. crypto/Dynastic | SOLVED by Claude (not re-run)
# 7. forensics/An unusual sighting | SOLVED HTB{4n_unusual_s1ght1ng_1n_SSH_l0gs!} (interactive remote quiz; offline IP guess was wrong)
# 8. forensics/Phreaky | SOLVED HTB{Th3Phr3aksReadyT0Att4ck}
# 9. forensics/Silicon Data Sleuthing | SOLVED HTB{Y0u'v3_m4st3r3d_0p3nWRT_d4t4_3xtr4ct10n!!_cdd8ffe941b895c60208f37f33acd324} (interactive remote quiz)
# 10. misc/Chrono Mind | SOLVED HTB{1nj3c73d_c0n73x7_c0p1l07_3x3cu73_c8d54761407a230c952d20dd2a655ff9} (LLM prompt-injection + RCE, remote web) [re-fetched on reloaded instance]
# 11. misc/Hidden Path | SOLVED HTB{1nvi5IBl3_cH4r4cT3rS_n0t_sO_v1SIbL3_21415c87faa75cdd4afe9fd95c26b6c0} [re-fetched on reloaded instance 154.57.164.75:30683]
# 12. misc/Locked Away | SOLVED HTB{bYp4sSeD_tH3_fIlT3r5?_aLw4Ys_b3_c4RefUL!_3462bed930bb8122f0049078751a9f2f} (sandbox escape) [re-fetched on reloaded instance]
# 13. misc/Prison Pipeline | SOLVED HTB{pr1s0n_br34k_w1th_supply_ch41n!_561be77f7a5a0d4c8b69583ce2fbe1ad} (SSRF -> npm supply-chain RCE) [re-fetched on reloaded instance]
# 14. hw/Critical Flight | SOLVED by another agent (offline Gerber) HTB{533_7h3_1nn32_w02k1n95_0f_313c720n1c5#$@}
# 15. hw/It's Oops PM | DEFERRED — offline analysis complete (backdoor trigger 0xFFE9 = 1111111111101001, leaked key 0x63E1, verified via VHDL sim); flag requires live satellite remote, NO target.txt provided for hw
# 16. hw/Debug | SOLVED HTB{547311173_n37w02k_c0mp20m153d} (UART 8N1 @ 115200 decode of .sal)
# 17. ics/Shush Protocol | SOLVED (by other solver, ICS already done per user)
# 18. blockchain/NotADemocraticElection | SOLVED HTB{h4sh_c0ll1s10n_t0_br1ng_b4ck_d3m0cr4cy} (abi.encodePacked hash collision -> vote exploit, remote RPC)
# 19. coding/Dynamic Paths | SOLVED HTB{b3h3M07H_5h0uld_H4v3_57ud13D_dYM4m1C_pr09r4mm1n9_70_C47ch_y0u_991d7f7b4f430cfd2a9b79af13d03203} (grid DP, 100/100 tests, remote) [reloaded instance 154.57.164.78:30321]
# 20. pwn/Getting Started | SOLVED HTB{b0f_tut0r14l5_4r3_g00d} (bof, remote) [live 154.57.164.71:31025]
# 21. pwn/Labyrinth | SOLVED HTB{3sc4p3_fr0m_4b0v3} (bof + stack-alignment ret, remote) [live 154.57.164.71:32089]
# 22. pwn/Void | SOLVED HTB{pwnt00l5_h0mep4g3_15_u54ful} (ret2dlresolve 2-stage, remote) [live 154.57.164.83:30313]
crypto/Blessed | DEFERRED — analysis xong (BLS rogue-key + PRNG-predict verify bypass); exploit chưa build (Claude)
