/* Guide's independent check of A097160 terms: for each prime p < cutoff, find a run of k consecutive nonzero
   quadratic residues in 1..p-1 (Jacobi symbol); for primes with none, record the exact longest run.
   a(n) (k = n+1) is the largest such prime whose longest run equals n. */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
static int jacobi(long a, long n){ int r=1; a%=n; while(a){ while(!(a&1)){ a>>=1; long m=n&7; if(m==3||m==5) r=-r; } long t=a; a=n; n=t; if((a&3)==3&&(n&3)==3) r=-r; a%=n; } return n==1?r:0; }
int main(int argc,char**argv){ int k=atoi(argv[1]); long N=atol(argv[2]); char*comp=calloc(N,1); long best=-1,exc=0,cnt=0;
  for(long i=2;i*i<N;i++) if(!comp[i]) for(long j=i*i;j<N;j+=i) comp[j]=1;
  for(long p=2;p<N;p++){ if(comp[p]) continue; cnt++; int run=0,longest=0,found=0;
    for(long a=1;a<p;a++){ int s = (p==2)?1:jacobi(a,p); if(s==1){ run++; if(run>longest) longest=run; if(run>=k){found=1;break;} } else run=0; }
    if(!found){ exc++; if(longest==k-1) best=p; } }
  printf("k=%d cutoff=%ld primes=%ld exceptions=%ld a(%d)=%ld\n",k,N,cnt,exc,k-1,best); return 0; }
