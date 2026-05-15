# Calibration And Optimization

This public demonstrator describes calibration and optimization only at the
capability level. The private AOS Core and specialist profiles may use
calibration, uncertainty estimation, and runtime optimization to make
PASS/WARN/BLOCK decisions more useful in real workflows.

## Calibration Boundary

Calibration can support:

- uncertainty-aware review triggers
- conservative warning bands
- domain-specific escalation policies
- drift monitoring
- human-review thresholds

The public repository does not publish real calibration curves, thresholds,
clinical policy logic, data lineage, or private validation workflow.

## Optimization Boundary

Private/commercial variants may optimize:

- latency
- throughput
- memory use
- edge or on-prem deployment profile
- Python/C++/CUDA/PTX or other low-level execution layers

The public repository does not publish optimization code, benchmark traces,
hardware-specific tuning, deployment settings, or private performance claims.

## Publication Rule For Metrics

Radiology metrics should be published only when the evidence packet is current,
aggregate-only, reproducible, and explicitly bounded as non-clinical public
evidence. Stale historical metrics should not be presented as current system
performance.
