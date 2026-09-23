# JSP-000082-SEARCH-01 — status

Task: bounded, reproducible counterexample search for JSP-000082 /
Erdős #64 (Erdős–Gyárfás conjecture).

Owner branch: agent/jsp000082-search-01-owner

Current state: SETUP/CALIBRATION.

Budget frozen (machine-detected 2026-09-23):

- Host: Mac16,12, 10 CPU cores, 16 GiB RAM, ~149 GiB free disk.
- Observed ambient load ~2 cores → self-limit to <=3 workers.
- CPU cap: 24 core-h total (metered via wall*workers, logged per shard).
- Wall cap: 8 h from 2026-09-23 ~15:40 local.
- RAM cap: <=4 GiB total search RSS (25% of 16 GiB is the binding limit).
- Disk cap: <=10 GiB artifacts.
- Metering limitation: per-process CPU time taken from shell `time`;
  no cgroup accounting on macOS — wall*workers is the conservative proxy.

Phase budget (of ~7 h usable wall):
- Gate 0 audit ~45 min (done, see SOURCE_AUDIT.md)
- tooling+calibration ~1.5 h (in progress)
- frozen search shards ~4 h
- verify+archive+push ~45 min
