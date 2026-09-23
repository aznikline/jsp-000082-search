"""Cycle detector A: DFS enumeration of simple cycles of a target length.

Independent implementation #1. Returns a concrete witness vertex list
[v0, v1, ..., v_{L-1}] with v_{L-1} adjacent to v0, or None.

Canonicalization: only enumerates cycles whose minimum vertex is the
DFS root, and only in one direction (second vertex < last vertex is NOT
enforced; instead each undirected cycle may be found twice -- harmless
for existence queries, dedup not needed).
"""
import sys
sys.setrecursionlimit(1_000_000)

from graphio import adjacency


def find_cycle_of_length(n, edges, L, node_budget=None):
    """Return a witness cycle (list of L vertices) or None.

    node_budget: optional cap on DFS nodes visited; if exceeded returns
    the string "BUDGET_EXCEEDED" instead of None -- callers must NOT
    treat that as absence.
    """
    adj = adjacency(n, edges)
    order = [sorted(a) for a in adj]
    counter = [0]

    def dfs(start, v, path, onpath):
        if node_budget is not None:
            counter[0] += 1
            if counter[0] > node_budget:
                raise _Budget()
        if len(path) == L:
            return path if start in order[v] else None
        for w in order[v]:
            if w == start and len(path) == L:
                return path
            if w > start and not onpath[w]:
                onpath[w] = True
                path.append(w)
                r = dfs(start, w, path, onpath)
                if r is not None:
                    return r
                path.pop()
                onpath[w] = False
        return None

    for s in range(n):
        if len(order[s]) < 2:
            continue
        onpath = [False] * n
        onpath[s] = True
        try:
            r = dfs(s, s, [s], onpath)
        except _Budget:
            return "BUDGET_EXCEEDED"
        if r is not None:
            return r
    return None


class _Budget(Exception):
    pass


def check_witness(n, edges, witness, L):
    """Independent small checker: is `witness` a genuine simple L-cycle?"""
    if witness is None:
        return False
    if len(witness) != L:
        return False
    if len(set(witness)) != L:
        return False
    if any(not (0 <= v < n) for v in witness):
        return False
    eset = set(tuple(sorted(e)) for e in edges)
    for i in range(L):
        a, b = witness[i], witness[(i + 1) % L]
        if tuple(sorted((a, b))) not in eset:
            return False
    return True


def all_cycles_of_length(n, edges, L, cap=100000):
    """Enumerate (up to `cap`) distinct vertex-min-rooted simple L-cycles.

    Returns (list_of_witness_lists, hit_cap_bool). Each cycle reported once
    per direction is avoided by requiring second vertex < last vertex.
    """
    adj = adjacency(n, edges)
    order = [sorted(a) for a in adj]
    found = []
    hit_cap = [False]

    def dfs(start, v, path, onpath):
        if hit_cap[0]:
            return
        if len(path) == L:
            if path[1] < v and start in order[v]:
                found.append(list(path))
                if len(found) >= cap:
                    hit_cap[0] = True
            return
        for w in order[v]:
            if w > start and not onpath[w]:
                onpath[w] = True
                path.append(w)
                dfs(start, w, path, onpath)
                path.pop()
                onpath[w] = False
                if hit_cap[0]:
                    return

    for s in range(n):
        if len(order[s]) < 2:
            continue
        onpath = [False] * n
        onpath[s] = True
        dfs(s, s, [s], onpath)
        if hit_cap[0]:
            break
    return found, hit_cap[0]


def forbidden_lengths(n):
    """All 2^k with k>=2 and 2^k <= n."""
    out = []
    L = 4
    while L <= n:
        out.append(L)
        L *= 2
    return out


def scan_forbidden(n, edges, budget_per_len=None):
    """Check every forbidden length; returns dict L -> witness/None/'BUDGET_EXCEEDED'."""
    return {L: find_cycle_of_length(n, edges, L, budget_per_len)
            for L in forbidden_lengths(n)}
