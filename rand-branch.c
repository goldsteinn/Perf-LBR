#include <assert.h>
#include <immintrin.h>
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <time.h>
#include <x86intrin.h>


#define ALWAYS_INLINE inline __attribute__((always_inline))
#define NEVER_INLINE  __attribute__((noinline))
#define CONST_ATTR    __attribute__((const))
#define PURE_ATTR     __attribute__((pure))
#define BENCH_ATTR    __attribute__((noinline, noclone, aligned(4096)))

#define COMPILER_OOE_BARRIER() asm volatile("lfence" : : : "memory")
#define OOE_BARRIER()          asm volatile("lfence" : : :)
#define COMPILER_BARRIER()     asm volatile("" : : : "memory");
#define COMPILER_DO_NOT_OPTIMIZE_OUT(X)                                        \
    asm volatile("" : : "i,r,m"(X) : "memory")

#define _CAT(X, Y)   X##Y
#define CAT(X, Y)    _CAT(X, Y)
#define _V_TO_STR(X) #X
#define V_TO_STR(X)  _V_TO_STR(X)

#define NO_LSD_RD(tmp, r) "pop " #tmp "\nmovq " #r ", %%rsp\n"
#define NO_LSD_WR(tmp, r) "push " #tmp "\nmovq " #r ", %%rsp\n"

#define IMPOSSIBLE(X)                                                          \
    if (X) {                                                                   \
        __builtin_unreachable();                                               \
    }

#define PRINT(...) fprintf(stderr, __VA_ARGS__)

int BENCH_ATTR
pred_rand() {
    int a = 0, b = 0;
    for (int i = (1 << 26); i; --i) {
        if (rand() % 2) {
            ++a;
        }
        else {
            b ^= 1;
        }
    }
    return a + b;
}
int
main(int argc, char ** argv) {
    pred_rand();
}
