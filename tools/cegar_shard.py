"""Run one CEGAR shard and log to RUN_MANIFEST.jsonl.

Usage: cegar_shard.py <shard_id> <n> [--cubic] [--cap N] [--time S]
"""
import argparse
import hashlib
import json
import os
import time

import searcher as S
import graphio

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TASK = os.path.join(ROOT, ".agate/tasks/JSP-000082-SEARCH-01")
LOGS = os.path.join(ROOT, "logs")


def sha256_file(p):
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def code_sha():
    return {f: sha256_file(os.path.join(ROOT, "tools", f))
            for f in ["graphio.py", "cyclecheck_a.py", "searcher.py",
                      "check_g6.c"]}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("shard_id")
    ap.add_argument("n", type=int)
    ap.add_argument("--cubic", action="store_true")
    ap.add_argument("--cap", type=int, default=None)
    ap.add_argument("--time", type=float, default=3600)
    a = ap.parse_args()

    kw = dict(edge_minimal=True)
    if a.cubic:
        kw["deg_cap"] = 3          # delta>=3 + deg<=3 = cubic
    if a.cap:
        kw["deg_cap"] = a.cap
    cnf, ev, ge4, pool = S.build_base(a.n, **kw)

    t0 = time.time()
    r = S.cegar_search(a.n, cnf, ev, time_cap=a.time)
    elapsed = time.time() - t0

    cand_path = None
    if r["status"] == "SAT_CANDIDATE":
        cand_path = os.path.join(LOGS, f"{a.shard_id}.candidate.edges")
        graphio.write_edge_file(cand_path, a.n, r["graph"])

    entry = {
        "shard_id": a.shard_id,
        "type": "cegar_sat",
        "constraints": kw,
        "n": a.n,
        "time_cap_s": a.time,
        "TESTED_CODE_SHA": code_sha(),
        "start": time.strftime("%Y-%m-%dT%H:%M:%S%z", time.localtime(t0)),
        "elapsed_wall_s": round(elapsed, 1),
        "status": r["status"],
        "stats": r["stats"],
        "candidate_file": os.path.relpath(cand_path, ROOT)
        if cand_path else None,
        "candidate_sha256": sha256_file(cand_path) if cand_path else None,
    }
    with open(os.path.join(TASK, "RUN_MANIFEST.jsonl"), "a") as f:
        f.write(json.dumps(entry) + "\n")
    print(json.dumps(entry, indent=1))


if __name__ == "__main__":
    main()
