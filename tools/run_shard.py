"""Run one generation shard: geng ... | check_g6 ... , capture manifest.

Usage: run_shard.py <shard_id> <n> <mine:maxe> [extra geng args...]
  e.g. run_shard.py S2_n21m32 21 32:32 -c -f -d3 -D4

Writes:
  logs/<shard_id>.survivors.g6   (any graphs with no forbidden cycle)
  logs/<shard_id>.log            (stderr of both processes + stats)
Appends one JSON line to RUN_MANIFEST.jsonl in the task dir.
"""
import hashlib
import json
import os
import subprocess
import sys
import time

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TASK = os.path.join(ROOT, ".agate/tasks/JSP-000082-SEARCH-01")
LOGS = os.path.join(ROOT, "logs")
CHECK = os.path.join(ROOT, "tools", "check_g6")


def sha256_file(p):
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def code_sha():
    out = {}
    for f in ["graphio.py", "cyclecheck_a.py", "verify_b.py",
              "searcher.py", "check_g6.c"]:
        out[f] = sha256_file(os.path.join(ROOT, "tools", f))
    return out


def main():
    shard_id = sys.argv[1]
    n = int(sys.argv[2])
    erange = sys.argv[3]
    geng_extra = sys.argv[4:]
    resmod = os.environ.get("RESMOD")  # "r/m" optional
    geng_cmd = ["geng"] + geng_extra + [str(n), erange]
    if resmod:
        geng_cmd.append(resmod)
    check_cmd = [CHECK]

    surv_path = os.path.join(LOGS, f"{shard_id}.survivors.g6")
    log_path = os.path.join(LOGS, f"{shard_id}.log")

    t0 = time.time()
    with open(surv_path, "w") as surv, open(log_path, "w") as lg:
        p1 = subprocess.Popen(geng_cmd, stdout=subprocess.PIPE,
                              stderr=lg)
        p2 = subprocess.Popen(check_cmd, stdin=p1.stdout,
                              stdout=surv, stderr=lg)
        p1.stdout.close()
        p2.communicate()
        rc1 = p1.wait()
    elapsed = time.time() - t0

    entry = {
        "shard_id": shard_id,
        "type": "geng_enum",
        "geng_cmd": " ".join(geng_cmd),
        "check_cmd": " ".join(check_cmd),
        "geng_version": "nauty 2.9.3 (homebrew)",
        "checker": "check_g6.c build " + code_sha()["check_g6.c"][:12],
        "TESTED_CODE_SHA": code_sha(),
        "n": n,
        "edge_range": erange,
        "resmod": resmod,
        "start": time.strftime("%Y-%m-%dT%H:%M:%S%z",
                               time.localtime(t0)),
        "elapsed_wall_s": round(elapsed, 1),
        "geng_rc": rc1,
        "check_rc": p2.returncode,
        "survivors_file": os.path.relpath(surv_path, ROOT),
        "survivors_sha256": sha256_file(surv_path),
        "log_sha256": sha256_file(log_path),
        "status": "COMPLETE" if rc1 == 0 and p2.returncode == 0
                  else "ERROR",
    }
    with open(os.path.join(TASK, "RUN_MANIFEST.jsonl"), "a") as f:
        f.write(json.dumps(entry) + "\n")
    print(json.dumps(entry, indent=1))


if __name__ == "__main__":
    main()
