# Dynastic — evidence
- source.py: encrypt(m) => alpha: chr((ord-0x41 + i)%26 +0x41); non-alpha giữ nguyên.
- output.txt ciphertext: DJF_CTA_SWYH_NPDKK_MBZ_QPHTIGPMZY_KRZSQE?!_ZL_CN_PGLIMCU_YU_KJODME_RYGZXL
- Giải: đảo dấu +i thành -i. Chạy solve.py => flag.
- VERIFY: inner = DID_YOU_KNOW_ABOUT_THE_TRITHEMIUS_CIPHER?!_IT_IS_SIMILAR_TO_CAESAR_CIPHER (đọc được, tự nhất quán).
