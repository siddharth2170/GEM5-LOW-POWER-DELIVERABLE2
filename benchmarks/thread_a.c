#include <stdint.h>
#include <stdio.h>
int main(void) {
    uint64_t a=1,b=2,c=3,d=4;
    for (uint64_t i=0;i<2500000ULL;i++){a=a*33+i;b=b*35+i;c=c*37+i;d=d*39+i;}
    printf("thread-a=%llu\n",(unsigned long long)(a^b^c^d));
    return 0;
}

