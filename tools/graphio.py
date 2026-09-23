"""Graph IO: canonical edge list, graph6, SHA-256, validation.

Format:
- vertices are labeled 0..N-1
- edge list is sorted list of (u, v) with u < v
- files: "N\nu v\n..." (one edge per line) or graph6 single line
"""
import hashlib
import sys


def normalize_edges(n, edges):
    """Validate and normalize an edge list for a simple undirected graph.

    Rejects self-loops, duplicate edges, out-of-range endpoints.
    Returns sorted list of (u, v) tuples with u < v.
    """
    if n < 0:
        raise ValueError("negative vertex count")
    out = set()
    for (a, b) in edges:
        if a == b:
            raise ValueError(f"self-loop at {a}")
        if not (0 <= a < n and 0 <= b < n):
            raise ValueError(f"endpoint out of range: ({a},{b}) for N={n}")
        out.add((min(a, b), max(a, b)))
    return sorted(out)


def adjacency(n, edges):
    adj = [set() for _ in range(n)]
    for (u, v) in edges:
        adj[u].add(v)
        adj[v].add(u)
    return adj


def check_simple_undirected(n, edges):
    """Full structural validation; returns normalized edges or raises."""
    return normalize_edges(n, edges)


def degrees(n, edges):
    deg = [0] * n
    for (u, v) in edges:
        deg[u] += 1
        deg[v] += 1
    return deg


def min_degree_at_least(n, edges, d=3):
    return all(x >= d for x in degrees(n, edges))


def edges_to_bytes(n, edges):
    """Canonical serialization for hashing."""
    lines = [str(n)]
    lines += [f"{u} {v}" for (u, v) in edges]
    return ("\n".join(lines) + "\n").encode()


def sha256_edges(n, edges):
    return hashlib.sha256(edges_to_bytes(n, edges)).hexdigest()


def write_edge_file(path, n, edges):
    with open(path, "wb") as f:
        f.write(edges_to_bytes(n, edges))


def read_edge_file(path):
    with open(path) as f:
        toks = f.read().split()
    n = int(toks[0])
    rest = toks[1:]
    if len(rest) % 2 != 0:
        raise ValueError("odd token count in edge file")
    edges = [(int(rest[i]), int(rest[i + 1])) for i in range(0, len(rest), 2)]
    return n, normalize_edges(n, edges)


def to_graph6(n, edges):
    """Encode as graph6 (n <= 62 only needed here; support n<=258 via standard)."""
    adj = adjacency(n, edges)
    if n <= 62:
        header = bytes([n + 63])
    elif n <= 258047:
        header = b"~" + bytes([(n >> 12) + 63, ((n >> 6) & 63) + 63, (n & 63) + 63])
    else:
        raise ValueError("n too large for graph6")
    bits = []
    for j in range(1, n):
        for i in range(j):
            bits.append(1 if i in adj[j] else 0)
    while len(bits) % 6:
        bits.append(0)
    data = bytearray()
    for k in range(0, len(bits), 6):
        val = 0
        for b in bits[k:k + 6]:
            val = (val << 1) | b
        data.append(val + 63)
    return (header + bytes(data)).decode()


def from_graph6(s):
    s = s.strip()
    b = s.encode()
    idx = 0
    if b[0:1] == b"~":
        n = ((b[1] - 63) << 12) | ((b[2] - 63) << 6) | (b[3] - 63)
        idx = 4
    else:
        n = b[0] - 63
        idx = 1
    bits = []
    for c in b[idx:]:
        v = c - 63
        for k in range(5, -1, -1):
            bits.append((v >> k) & 1)
    edges = []
    p = 0
    for j in range(1, n):
        for i in range(j):
            if p < len(bits) and bits[p]:
                edges.append((i, j))
            p += 1
    return n, normalize_edges(n, edges)
