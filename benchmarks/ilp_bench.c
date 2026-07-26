#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

int main(int argc, char **argv) {
    const uint64_t n = argc > 1 ? strtoull(argv[1], NULL, 10) : 3000000ULL;
    uint64_t a=1,b=3,c=5,d=7,e=11,f=13,g=17,h=19;
    for (uint64_t i=0; i<n; ++i) {
        a = a * 33 + i; b = b * 35 + i + 1;
        c = c * 37 + i + 2; d = d * 39 + i + 3;
        e = e * 41 + i + 4; f = f * 43 + i + 5;
        g = g * 45 + i + 6; h = h * 47 + i + 7;
    }
    printf("ilp checksum=%llu iterations=%llu\n",
           (unsigned long long)(a^b^c^d^e^f^g^h),
           (unsigned long long)n);
    return 0;
}

