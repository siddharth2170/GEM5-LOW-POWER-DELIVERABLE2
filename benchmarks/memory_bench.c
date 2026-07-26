#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

int main(int argc, char **argv) {
    const size_t count = argc > 1 ? strtoull(argv[1], NULL, 10) : 262144;
    uint32_t *a = malloc(count * sizeof(*a));
    if (!a) return 2;
    for (size_t i=0; i<count; ++i) a[i] = (uint32_t)(i * 17u + 3u);
    volatile uint64_t sum = 0;
    for (int pass=0; pass<8; ++pass)
        for (size_t i=0; i<count; i += 16) sum += a[i];
    printf("memory checksum=%llu elements=%zu\n",
           (unsigned long long)sum, count);
    free(a);
    return 0;
}

