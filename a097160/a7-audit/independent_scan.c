/* Independent verification; no source or executable from the submission used.
 * Build QR tables by the recurrence (x+1)^2 = x^2 + 2*x + 1 (mod p).
 * Enumerate candidate primes by exact trial division, then find a run directly.
 */
#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <string.h>
#include <time.h>

static unsigned char qr[600626];

static int prime(uint32_t n) {
    if (n < 2) return 0;
    if (!(n & 1)) return n == 2;
    for (uint32_t d = 3; d <= n / d; d += 2)
        if (n % d == 0) return 0;
    return 1;
}

static void squares(uint32_t p) {
    memset(qr, 0, p);
    uint32_t r = 1;
    for (uint32_t x = 1; x <= (p-1)/2; ++x) {
        qr[r] = 1;
        r += 2*x + 1;
        if (r >= p) r -= p;
    }
}

static void endpoint(uint32_t p) {
    if (!prime(p)) exit(2);
    squares(p);
    uint32_t run = 0, best = 0, first = 0, ones = 0;
    char name[80];
    snprintf(name, sizeof name, "independent-endpoint-%u.txt", p);
    FILE *f = fopen(name, "w");
    if (!f) exit(2);
    for (uint32_t a = 0; a < p; ++a) {
        fputc('0' + qr[a], f);
        ones += qr[a];
        run = qr[a] ? run + 1 : 0;
        if (run > best) { best = run; first = a - run + 1; }
    }
    fputc('\n', f);
    if (fclose(f) || ones != (p-1)/2 || qr[0]) exit(2);
    printf("ENDPOINT p=%u max=%u first=%u ones=%u\n", p, best, first, ones);
    printf("MAXIMAL_STARTS p=%u:", p);
    run = 0;
    for (uint32_t a = 0; a < p; ++a) {
        run = qr[a] ? run + 1 : 0;
        if (run == best) printf(" %u", a - best + 1);
    }
    printf("\n");
}

static void scan(uint32_t lo, uint32_t hi, uint32_t k, const char *name) {
    FILE *f = fopen(name, "w");
    if (!f) exit(2);
    uint32_t count = 0, first_prime = 0, last_prime = 0;
    uint32_t largest_start = 0, largest_start_prime = 0;
    uint64_t marked = 0;
    clock_t begin = clock();
    for (uint32_t p = lo + 1; p <= hi; ++p) {
        if (!prime(p)) continue;
        squares(p);
        marked += (p-1)/2;
        uint32_t run = 0, start = 0;
        for (uint32_t a = 1; a < p; ++a) {
            run = qr[a] ? run + 1 : 0;
            if (run == k) { start = a-k+1; break; }
        }
        if (!start) {
            fprintf(stderr, "COUNTEREXAMPLE p=%u k=%u\n", p, k);
            exit(1);
        }
        if (!first_prime) first_prime = p;
        last_prime = p;
        if (start > largest_start) {
            largest_start = start;
            largest_start_prime = p;
        }
        fprintf(f, "%u %u\n", p, start);
        ++count;
        if (count % 5000 == 0) {
            printf("PROGRESS k=%u count=%u p=%u cpu=%.3f\n", k, count, p,
                   (double)(clock()-begin)/CLOCKS_PER_SEC);
            fflush(stdout);
        }
    }
    if (fclose(f)) exit(2);
    printf("PASS k=%u interval=(%u,%u] primes=%u first=%u last=%u "
           "largest_start=%u at_prime=%u largest_end=%u square_marks=%llu cpu=%.3f\n",
           k, lo, hi, count, first_prime, last_prime, largest_start,
           largest_start_prime, largest_start+k-1, (unsigned long long)marked,
           (double)(clock()-begin)/CLOCKS_PER_SEC);
}

int main(void) {
    endpoint(4481);
    endpoint(2153);
    scan(2153, 108900, 7, "independent-a6-witnesses.txt");
    scan(4481, 600625, 8, "independent-a7-witnesses.txt");
    return 0;
}
