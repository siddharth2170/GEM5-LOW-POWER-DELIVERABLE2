#include <stdint.h>
#include <stdio.h>
int main(void) {
    uint32_t x=7; volatile uint64_t s=0;
    for (uint64_t i=0;i<2000000ULL;i++){x=x*1103515245u+12345u;if(x&8)s+=x;else s-=x;}
    printf("thread-b=%llu\n",(unsigned long long)s);
    return 0;
}
