"""Audit an extremal .s6/.g6 file: min-degree histogram + edge count check.

Usage: mindeg_audit.py FILE
Detects sparse6 ('...' lines starting with ':') vs graph6.
Prints: graphs, edge counts, min-degree histogram, whether any graph
has min degree >= 3.
"""
import sys
import graphio


def read_any(path):
    graphs = []
    for line in open(path):
        line = line.strip()
        if not line or line.startswith(">"):
            continue
        if line.startswith(":"):
            graphs.append(from_sparse6(line))
        else:
            graphs.append(graphio.from_graph6(line))
    return graphs


def from_sparse6(s):
    """Decode sparse6 (':...') to (n, edges)."""
    b = s.encode()[1:]
    # n: 1 byte if <=62 (char n+63 in [63,125]), '~'+3 bytes if <=258047
    if b[0] != 126:
        n = b[0] - 63; idx = 1
    elif b[1] != 126:
        n = ((b[1]-63)<<12)|((b[2]-63)<<6)|(b[3]-63); idx = 4
    else:
        raise ValueError("big sparse6 unsupported")
    # k = ceil(log2(n-1)) bits... k satisfies 2^k >= n-1? nauty: k = smallest
    # with (1<<k) > n-1 i.e. 2^k >= n
    k = 1
    while (1 << k) < n:
        k += 1
    bits = []
    for c in b[idx:]:
        v = c - 63
        for j in range(5, -1, -1):
            bits.append((v >> j) & 1)
    edges = []
    v = 0; i = 0
    while i + k < len(bits) + 1:
        # need b+1+k bits: b, then k bits of x
        if i + 1 + k > len(bits):
            break
        bb = bits[i]
        x = 0
        for j in range(k):
            x = (x << 1) | bits[i + 1 + j]
        i += 1 + k
        if bb == 1:
            v += 1
        if x > v:
            v = x
        else:
            edges.append((x, v))
    return n, graphio.normalize_edges(n, edges)


def main():
    graphs = read_any(sys.argv[1])
    md = {}
    ec = {}
    bad = 0
    for (n, e) in graphs:
        d = min(graphio.degrees(n, e)) if n else 0
        md[d] = md.get(d, 0) + 1
        ec[len(e)] = ec.get(len(e), 0) + 1
        if d >= 3:
            bad += 1
    print("file:", sys.argv[1])
    print("graphs:", len(graphs), "edges hist:", ec,
          "min-degree hist:", md)
    print("delta>=3 count:", bad)


if __name__ == "__main__":
    main()
