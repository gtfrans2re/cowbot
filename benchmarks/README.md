# Benchmarks

Hardware performance measurements for the Cowbot edge deployment
(Raspberry Pi 4 Model B, 4 GB RAM, ARMv8).

## Contents

- `latency/`  Per-stage end-to-end latency breakdown
- `energy/`   Dynamic energy per inference
- `memory/`   Memory bandwidth utilization

## Measurement setup

- Device: Raspberry Pi 4 Model B (4 GB)
- OS / kernel:
- Ambient temperature:
- Measurement window:
- Tools:
  - Latency: Python time.perf_counter() timestamps per pipeline stage
  - Energy: <inline USB power meter / DFRobot power module reading>
  - Memory bandwidth: <perf stat / tinymembench / pmbw>

## Notes

Report mean +/- std across the run, not single readings.
