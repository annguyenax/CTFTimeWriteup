// Multi-threaded offline MD5 brute-force cracker (no network access).
// Public-domain MD5 implementation (RFC 1321), adapted for speed.
#include <stdio.h>
#include <stdint.h>
#include <string.h>
#include <stdlib.h>
#include <omp.h>

typedef struct
{
    uint32_t a, b, c, d;
} MD5_CTX_SMALL;

#define LEFTROTATE(x, c) (((x) << (c)) | ((x) >> (32 - (c))))

static const uint32_t K[64] = {
    0xd76aa478, 0xe8c7b756, 0x242070db, 0xc1bdceee, 0xf57c0faf, 0x4787c62a, 0xa8304613, 0xfd469501,
    0x698098d8, 0x8b44f7af, 0xffff5bb1, 0x895cd7be, 0x6b901122, 0xfd987193, 0xa679438e, 0x49b40821,
    0xf61e2562, 0xc040b340, 0x265e5a51, 0xe9b6c7aa, 0xd62f105d, 0x02441453, 0xd8a1e681, 0xe7d3fbc8,
    0x21e1cde6, 0xc33707d6, 0xf4d50d87, 0x455a14ed, 0xa9e3e905, 0xfcefa3f8, 0x676f02d9, 0x8d2a4c8a,
    0xfffa3942, 0x8771f681, 0x6d9d6122, 0xfde5380c, 0xa4beea44, 0x4bdecfa9, 0xf6bb4b60, 0xbebfbc70,
    0x289b7ec6, 0xeaa127fa, 0xd4ef3085, 0x04881d05, 0xd9d4d039, 0xe6db99e5, 0x1fa27cf8, 0xc4ac5665,
    0xf4292244, 0x432aff97, 0xab9423a7, 0xfc93a039, 0x655b59c3, 0x8f0ccc92, 0xffeff47d, 0x85845dd1,
    0x6fa87e4f, 0xfe2ce6e0, 0xa3014314, 0x4e0811a1, 0xf7537e82, 0xbd3af235, 0x2ad7d2bb, 0xeb86d391};

static const uint32_t S[64] = {
    7, 12, 17, 22, 7, 12, 17, 22, 7, 12, 17, 22, 7, 12, 17, 22,
    5, 9, 14, 20, 5, 9, 14, 20, 5, 9, 14, 20, 5, 9, 14, 20,
    4, 11, 16, 23, 4, 11, 16, 23, 4, 11, 16, 23, 4, 11, 16, 23,
    6, 10, 15, 21, 6, 10, 15, 21, 6, 10, 15, 21, 6, 10, 15, 21};

// msg buffer must already be padded to a multiple of 64 bytes.
static void md5_compute(const uint8_t *msg, size_t padded_len, uint32_t out[4])
{
    uint32_t a0 = 0x67452301, b0 = 0xefcdab89, c0 = 0x98badcfe, d0 = 0x10325476;
    for (size_t off = 0; off < padded_len; off += 64)
    {
        uint32_t M[16];
        memcpy(M, msg + off, 64);
        uint32_t A = a0, B = b0, C = c0, D = d0;
        for (int i = 0; i < 64; i++)
        {
            uint32_t F;
            int g;
            if (i < 16)
            {
                F = (B & C) | (~B & D);
                g = i;
            }
            else if (i < 32)
            {
                F = (D & B) | (~D & C);
                g = (5 * i + 1) % 16;
            }
            else if (i < 48)
            {
                F = B ^ C ^ D;
                g = (3 * i + 5) % 16;
            }
            else
            {
                F = C ^ (B | ~D);
                g = (7 * i) % 16;
            }
            F = F + A + K[i] + M[g];
            A = D;
            D = C;
            C = B;
            B = B + LEFTROTATE(F, S[i]);
        }
        a0 += A;
        b0 += B;
        c0 += C;
        d0 += D;
    }
    out[0] = a0;
    out[1] = b0;
    out[2] = c0;
    out[3] = d0;
}

static void md5_string(const char *str, size_t len, uint32_t out[4])
{
    uint8_t buf[64]; // enough for strings up to 55 bytes (single block)
    memset(buf, 0, 64);
    memcpy(buf, str, len);
    buf[len] = 0x80;
    uint64_t bitlen = (uint64_t)len * 8;
    memcpy(buf + 56, &bitlen, 8);
    md5_compute(buf, 64, out);
}

int main(int argc, char **argv)
{
    if (argc < 3)
    {
        fprintf(stderr, "usage: %s <target_hex_md5> <charset> [max_len]\n", argv[0]);
        return 1;
    }
    const char *target_hex = argv[1];
    const char *charset = argv[2];
    int max_len = argc > 3 ? atoi(argv[3]) : 10;
    int clen = (int)strlen(charset);

    uint32_t target[4];
    for (int i = 0; i < 4; i++)
    {
        unsigned int v;
        sscanf(target_hex + i * 8, "%8x", &v);
        // MD5 hex digest is little-endian per word
        target[i] = ((v & 0xff) << 24) | ((v & 0xff00) << 8) | ((v & 0xff0000) >> 8) | ((v & 0xff000000) >> 24);
    }

    volatile int found = 0;
    char found_str[16] = {0};

    for (int len = 1; len <= max_len && !found; len++)
    {
        long long total = 1;
        for (int i = 0; i < len; i++)
            total *= clen;
        fprintf(stderr, "[*] length %d, %lld candidates\n", len, total);

#pragma omp parallel
        {
            char cand[16];
            cand[len] = 0;
#pragma omp for schedule(dynamic, 100000)
            for (long long idx = 0; idx < total; idx++)
            {
                if (found)
                    continue;
                long long v = idx;
                for (int i = len - 1; i >= 0; i--)
                {
                    cand[i] = charset[v % clen];
                    v /= clen;
                }
                uint32_t out[4];
                md5_string(cand, len, out);
                if (out[0] == target[0] && out[1] == target[1] && out[2] == target[2] && out[3] == target[3])
                {
#pragma omp critical
                    {
                        if (!found)
                        {
                            found = 1;
                            memcpy(found_str, cand, len + 1);
                        }
                    }
                }
            }
        }
    }

    if (found)
    {
        printf("FOUND: %s\n", found_str);
        return 0;
    }
    else
    {
        printf("NOT FOUND within max_len=%d charset=%s\n", max_len, charset);
        return 2;
    }
}
