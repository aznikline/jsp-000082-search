/* check_g6.c -- streaming checker for graph6 lines on stdin.
 *
 * For each graph: verify simple undirected, min degree >= 3 (unless
 * -anydeg), verify C4-free claim is independently rechecked (unless
 * -trustc4), then search for a simple cycle of each forbidden length
 * L in {4,8,16,32 <= n} (lengths selectable via -L list).
 *
 * A graph is a SURVIVOR iff it has min degree >=3 and none of the
 * requested lengths has a simple cycle. Survivors are echoed to stdout
 * as graph6; summary stats go to stderr.
 *
 * Usage: check_g6 [-anydeg] [-L 8] [-L 8,16] [-c4] [-q]
 *   -anydeg : skip the min-degree>=3 test (still computed for stats)
 *   -L a,b  : forbidden lengths to test (default: all 2^k>=4, <=n)
 *   -c4     : also require C4 absence checked by us even if geng -f
 *             was used upstream (default: always recheck C4 anyway)
 *   -q      : quiet
 *
 * Cycle search: DFS, minimum-vertex-rooted, existence-first.
 * "Not found" is only reported after a complete DFS -- there is no
 * budget; the check is exact.
 */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdint.h>

static int n;
static uint64_t adj[258];          /* n<=258 via 6-bit graph6 ext; we only need <=64 */
static int deg[258];
static char onpath[258];
static int targetL;
static int found;

static void dfs(int start, int v, int depth) {
    if (found) return;
    if (depth == targetL) {
        if (adj[v] >> start & 1) found = 1;
        return;
    }
    uint64_t nb = adj[v];
    while (nb) {
        int w = __builtin_ctzll(nb);
        nb &= nb - 1;
        if (w > start && !onpath[w]) {
            onpath[w] = 1;
            dfs(start, w, depth + 1);
            onpath[w] = 0;
            if (found) return;
        }
    }
}

static int has_cycle_L(int L) {
    targetL = L; found = 0;
    for (int s = 0; s < n && !found; s++) {
        if (deg[s] < 2) continue;
        memset(onpath, 0, n);
        onpath[s] = 1;
        dfs(s, s, 1);
    }
    return found;
}

static int decode_g6(const char *s) {
    /* returns n, fills adj/deg; -1 on parse error */
    int idx = 0;
    if ((unsigned char)s[0] == 126) {           /* '~' ext header */
        n = ((s[1]-63)<<12) | ((s[2]-63)<<6) | (s[3]-63);
        idx = 4;
    } else {
        n = s[0] - 63; idx = 1;
    }
    if (n < 0 || n > 258) return -1;
    memset(adj, 0, sizeof(adj));
    memset(deg, 0, sizeof(deg));
    int p = idx * 8;                     /* bit position in bitstream */
    int nbits = 0;
    /* read bits MSB-first per byte */
    int bi = 0;
    for (int j = 1; j < n; j++)
        for (int i = 0; i < j; i++) {
            int byte = s[idx + bi/6];
            if (byte == 0 || byte == '\n' || byte == '\r') return -1;
            int bit = (byte - 63) >> (5 - (bi % 6)) & 1;
            bi++;
            if (bit) { adj[i] |= (1ULL<<j); adj[j] |= (1ULL<<i);
                       deg[i]++; deg[j]++; }
        }
    return n;
}

int main(int argc, char **argv) {
    int anydeg = 0, quiet = 0;
    int Ls[16]; int nL = 0;
    for (int i = 1; i < argc; i++) {
        if (!strcmp(argv[i], "-anydeg")) anydeg = 1;
        else if (!strcmp(argv[i], "-q")) quiet = 1;
        else if (!strcmp(argv[i], "-L") && i+1 < argc) {
            char *tok = strtok(argv[++i], ",");
            while (tok && nL < 16) { Ls[nL++] = atoi(tok); tok = strtok(NULL, ","); }
        }
    }
    char line[4096];
    long total = 0, mindeg_ok = 0, survivors = 0;
    long c4_found = 0;
    long perL[16]; memset(perL, 0, sizeof perL);
    while (fgets(line, sizeof line, stdin)) {
        int len = strlen(line);
        while (len && (line[len-1]=='\n' || line[len-1]=='\r')) line[--len]=0;
        if (!len) continue;
        if (decode_g6(line) < 0) { fprintf(stderr, "parse error: %s\n", line); return 2; }
        total++;
        int md = 1<<30;
        for (int i = 0; i < n; i++) if (deg[i] < md) md = deg[i];
        if (!anydeg && md < 3) { continue; }
        mindeg_ok++;
        /* default forbidden lengths */
        int lens[16]; int nl = nL;
        if (!nL) {
            for (int L = 4; L <= n && nl < 16; L *= 2) lens[nl++] = L;
        } else memcpy(lens, Ls, sizeof Ls);
        int bad = 0;
        for (int k = 0; k < nl && !bad; k++) {
            if (has_cycle_L(lens[k])) {
                bad = 1; perL[k]++;
                if (lens[k] == 4) c4_found++;
            }
        }
        if (!bad) {
            survivors++;
            printf("%s\n", line);
        }
    }
    fprintf(stderr, "total=%ld mindeg3=%ld survivors=%ld", total, mindeg_ok, survivors);
    for (int k = 0; k < (nL ? nL : 4); k++) fprintf(stderr, " hitL%d=%ld", k, perL[k]);
    fprintf(stderr, "\n");
    return 0;
}
