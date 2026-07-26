#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

int main(int argc, char **argv) {
    const uint64_t n = argc > 1 ? strtoull(argv[1], NULL, 10) : 2000000ULL;
    uint32_t x = 0x12345678u;
    volatile uint64_t sum = 0;
    for (uint64_t i = 0; i < n; ++i) {
        x = x * 1664525u + 1013904223u;
        if ((x ^ (x >> 7)) & 1u)
            sum += (x & 255u) + i;
        else
            sum -= (x & 127u);
    }
    printf("branch checksum=%llu iterations=%llu\n",
           (unsigned long long)sum, (unsigned long long)n);
    return 0;
}

