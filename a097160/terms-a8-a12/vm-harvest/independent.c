/* Independent checker: Euler exponentiation, sequential run counting,
   odd-only whole-interval sieve. No search source is imported or executed.
   For composite x, completely multiplicative chi(x)=chi(q)*chi(x/q), where
   q is the smallest prime factor. Prime arguments use Euler's criterion.
   p=2 is explicitly handled. Values beyond CACHE use Euler directly.
   independent K UPPER full|sample exceptions.tsv report.json sample.tsv
   sample selection: splitmix64(p XOR fixed seed) mod 10000 == 0.
   All exceptions are checked in either mode, with their exact maximum.
*/
#define _POSIX_C_SOURCE 200809L
#include <stdlib.h>
#include <stdio.h>
#include <stdint.h>
#include <inttypes.h>
#include <string.h>
#include <time.h>
#define CACHE 1048576u
#define SEED UINT64_C(0xa09716020261111)
static uint32_t factor[CACHE];
static int8_t symbol[CACHE];
static uint64_t powers;
static double seconds(void){struct timespec t;clock_gettime(CLOCK_MONOTONIC,&t);return t.tv_sec+t.tv_nsec/1e9;}
static int euler(uint64_t a,uint64_t p){
    powers++;uint64_t x=1,e=(p-1)/2;
    if(p<=UINT32_MAX){while(e){if(e&1)x=x*a%p;a=a*a%p;e>>=1;}}
    else {while(e){if(e&1)x=(uint64_t)((__uint128_t)x*a%p);a=(uint64_t)((__uint128_t)a*a%p);e>>=1;}}
    return x==1?1:-1;
}
static unsigned measure(uint64_t p,unsigned k,int complete,uint64_t *where){
    if(p==2){*where=1;return 1;}
    unsigned best=0,run=0;*where=0;symbol[1]=1;
    for(uint64_t x=1;x<p;x++){
        int c;
        if(x<CACHE){
            if(x==1)c=1;
            else if(!factor[x])c=euler(x,p);
            else c=symbol[factor[x]]*symbol[x/factor[x]];
            symbol[x]=(int8_t)c;
        }else c=euler(x,p);
        if(c==1){++run;if(run>best){best=run;*where=x-run+1;}}
        else run=0;
        if(!complete && run==k)return k;
    }
    return best;
}
static uint64_t mix(uint64_t x){
    x+=UINT64_C(0x9e3779b97f4a7c15);x=(x^(x>>30))*UINT64_C(0xbf58476d1ce4e5b9);
    x=(x^(x>>27))*UINT64_C(0x94d049bb133111eb);return x^(x>>31);
}
static void die(const char *s,uint64_t p){fprintf(stderr,"FAIL %s: %"PRIu64"\n",s,p);exit(1);}
int main(int argc,char **argv){
    if(argc!=7)return 2;
    unsigned k=(unsigned)strtoul(argv[1],0,10);uint64_t upper=strtoull(argv[2],0,10);
    int full=strcmp(argv[3],"full")==0;
    if(!full && strcmp(argv[3],"sample"))return 2;
    if(upper<3||upper>UINT64_C(50000000000)||k<2||k>30)return 2;
    double begin=seconds();clock_t cpu=clock();
    /* Euler table factorization is independent of the prime sieve. */
    for(uint32_t q=2;q<CACHE;q++)if(!factor[q] && q<=(CACHE-1)/q)
        for(uint32_t x=q*q;x<CACHE;x+=q)if(!factor[x])factor[x]=q;
    /* Index i represents odd integer 2*i+1; bits denote composites. */
    uint64_t odds=upper/2;
    uint8_t *bits=calloc((size_t)((odds+7)/8),1);if(!bits)return 3;
    #define GET(i) ((bits[(i)>>3]>>((i)&7))&1)
    #define SET(i) (bits[(i)>>3]|=(uint8_t)(1u<<((i)&7)))
    SET(0);
    for(uint64_t q=3;q<=(upper-1)/q;q+=2)if(!GET(q/2))
        for(uint64_t x=q*q;x<upper;x+=2*q)SET(x/2);
    FILE *exc=fopen(argv[4],"r"),*sample=fopen(argv[6],"w");if(!exc||!sample)return 3;
    char line[256];if(!fgets(line,sizeof(line),exc)||line[0]!='#')return 3;
    uint64_t want=0,wstart=0;unsigned wmax=0;
    int more=fscanf(exc,"%"SCNu64" %u %"SCNu64,&want,&wmax,&wstart);
    if(more!=3 && more!=EOF)die("malformed exception",0);
    uint64_t primes=0,checked=0,except=0,random=0,endpoint=0;
    fprintf(sample,"# prime measured_or_truncated_maximum first_maximum_start; splitmix64 fixed seed 0xa09716020261111, modulus 10000\n");
    for(uint64_t p=2;p<upper;p+=(p==2?1:2)){
        if(p!=2 && GET(p/2))continue;
        ++primes;
        if(more==3 && want<p)die("exception missing from primes",want);
        int exceptional=more==3 && want==p;
        int selected=mix(p^SEED)%10000==0;
        if(full||exceptional||selected){
            ++checked;uint64_t start;unsigned longest=measure(p,k,exceptional,&start);
            if(exceptional){
                if(longest!=wmax||start!=wstart||longest>=k)die("incorrect exceptional maximum/start",p);
                ++except;if(longest==k-1)endpoint=p;
                more=fscanf(exc,"%"SCNu64" %u %"SCNu64,&want,&wmax,&wstart);
                if(more!=3 && more!=EOF)die("malformed exception tail",p);
            }else if(longest<k)die("unlisted exception",p);
            if(selected){random++;fprintf(sample,"%"PRIu64" %u %"PRIu64"\n",p,longest,start);}
        }
        if(primes%1000000==0){fprintf(stderr,"k=%u primes=%"PRIu64" checked=%"PRIu64" p=%"PRIu64" wall=%.3f\n",k,primes,checked,p,seconds()-begin);fflush(sample);}
    }
    if(more!=EOF)die("exception out of interval",want);
    int ch;while((ch=fgetc(exc))!=EOF)if(ch!=' '&&ch!='\n'&&ch!='\r'&&ch!='\t')die("trailing data",0);
    fclose(exc);fclose(sample);free(bits);
    FILE *out=fopen(argv[5],"w");if(!out)return 3;
    fprintf(out,"{\"method\":\"Euler criterion with multiplicative sequential scan and odd bit sieve\",\"mode\":\"%s\",\"k\":%u,\"upper_exclusive\":%"PRIu64",\"prime_count\":%"PRIu64",\"checked_count\":%"PRIu64",\"exception_count\":%"PRIu64",\"sample_count\":%"PRIu64",\"sample_seed_hex\":\"a09716020261111\",\"sample_modulus\":10000,\"endpoint\":%"PRIu64",\"Euler_evaluations\":%"PRIu64",\"wall_seconds\":%.6f,\"cpu_seconds\":%.6f,\"status\":\"PASS\"}\n",full?"full":"sample",k,upper,primes,checked,except,random,endpoint,powers,seconds()-begin,(double)(clock()-cpu)/CLOCKS_PER_SEC);
    fclose(out);return 0;
}
