/* Search only. The independent checker does not use this file. */
#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <time.h>

static int jacobi(uint32_t a, uint32_t n) {
    int s=1;
    a%=n;
    while (a) {
        while (!(a&1)) { a>>=1; if ((n&7)==3 || (n&7)==5) s=-s; }
        uint32_t t=a; a=n; n=t;
        if ((a&3)==3 && (n&3)==3) s=-s;
        a%=n;
    }
    return n==1?s:0;
}
int main(int argc,char **argv) {
    if(argc!=4) {fprintf(stderr,"usage: generate K LOWER UPPER\n");return 2;}
    unsigned k=atoi(argv[1]), lo=atoi(argv[2]), hi=atoi(argv[3]);
    unsigned char *composite=calloc(hi+1,1);
    if(!composite)return 2;
    for(unsigned q=2;q<=hi/q;q++)if(!composite[q])
        for(unsigned m=q*q;m<=hi;m+=q)composite[m]=1;
    unsigned count=0,fail=0,maxend=0;uint64_t tests=0;
    clock_t start=clock();
    for(unsigned p=lo+1;p<=hi;p++)if(!composite[p]) {
        unsigned run=0,end=0;
        for(unsigned a=1;a<p;a++) {
            tests++;
            run=jacobi(a,p)==1?run+1:0;
            if(run==k){end=a;break;}
        }
        if(!end){fprintf(stderr,"NO RUN k=%u p=%u\n",k,p);fail++;}
        else {printf("%u %u\n",p,end-k+1);count++;if(end>maxend)maxend=end;}
    }
    fprintf(stderr,"k=%u lower=%u upper=%u primes=%u failures=%u tests=%llu max_end=%u cpu_seconds=%.6f\n",k,lo,hi,count,fail,(unsigned long long)tests,maxend,(double)(clock()-start)/CLOCKS_PER_SEC);
    free(composite);return fail?1:0;
}
