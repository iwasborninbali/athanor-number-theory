/* Guide's independent A097160 check, sharded: primes p < N with (prime index % M == R).
   For each such prime, find k consecutive nonzero quadratic residues (Jacobi symbol); for primes with none,
   print "p longest" (exact longest run). Output lines are merged across shards afterwards. */
#include <stdio.h>
#include <stdlib.h>
static int jacobi(long a, long n){ int r=1; a%=n; while(a){ while(!(a&1)){ a>>=1; long m=n&7; if(m==3||m==5) r=-r; } long t=a; a=n; n=t; if((a&3)==3&&(n&3)==3) r=-r; a%=n; } return n==1?r:0; }
int main(int argc,char**argv){ int k=atoi(argv[1]); long N=atol(argv[2]); int M=atoi(argv[3]), R=atoi(argv[4]);
  unsigned char*comp=calloc(N/2+1,1); long idx=0,cnt=0;   /* odd-only sieve: comp[i] for 2i+1 */
  for(long i=3;i*i<N;i+=2) if(!comp[i/2]) for(long j=i*i;j<N;j+=2*i) comp[j/2]=1;
  for(long p=2;p<N;p+=(p==2?1:2)){ if(p>2&&comp[p/2]) continue; if((idx++)%M!=R) continue; cnt++;
    int run=0,longest=0,found=0;
    for(long a=1;a<p;a++){ int s=(p==2)?1:jacobi(a,p); if(s==1){ if(++run>longest) longest=run; if(run>=k){found=1;break;} } else run=0; }
    if(!found) printf("%ld %d\n",p,longest); }
  fprintf(stderr,"k=%d N=%ld shard=%d/%d primes=%ld\n",k,N,R,M,cnt); return 0; }
