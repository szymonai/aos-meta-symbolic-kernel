# Runtime Substrates

AOS defines a control contract before it defines an implementation substrate:

```text
bounded signal -> explicit policy -> deterministic verdict -> audit record
```

The public repository currently exposes a Python reference implementation and a
Lean 4 proof surface for selected abstract verdict properties. Native and GPU
technologies are implementation options only. They do not change the public AOS semantics.

## Current Public Substrates

| Substrate | Role |
| --- | --- |
| Python | Reference runtime, examples, benchmarks, replay, and public audit tooling |
| Lean 4 | Formal surface for selected abstract verdict invariants |
| JSON | Stable public input, output, metric, and evidence format |

## Optional Future Substrates

| Substrate | Appropriate role | Boundary |
| --- | --- | --- |
| Rust | Memory-safe native runtime, FFI, service embedding, WASM target | Must preserve the same verdict contract |
| C++ | Low-latency native runtime, embedded integration, accelerator bridge | Must be tested against the reference contract |
| CUDA | Batch signal extraction, numeric preprocessing, accelerator-side scoring | Should not define policy semantics |
| PTX | Low-level GPU inspection or specialized accelerator kernels | Only useful after a concrete CUDA requirement exists |
| Assembly | Hardware-specific optimization or inspection | Not part of the public architecture |
| WASM | Portable sandboxed gate for edge, browser, or plugin use | Must preserve deterministic replay |
| eBPF | Runtime observation or infrastructure policy hooks | Should remain outside the verdict proof boundary |

## Compliance Rule

Any future backend must be treated as an implementation of the same public
contract, not as a new AOS definition. A backend is acceptable only if it can
show:

- equivalent verdicts for the public reference cases;
- stable JSON input and output shape;
- deterministic replay for the same input and policy;
- audit record compatibility;
- explicit reporting of unsupported numeric, hardware, or deployment behavior.

## Boundary

This repository does not publish C++, Rust, CUDA, PTX, assembly, WASM, or eBPF
runtime code. It also does not claim production latency, accelerator
correctness, hardware certification, or native-runtime equivalence.

The correct reading is narrower: AOS is substrate-independent at the contract
level; this public repo demonstrates the contract through Python, JSON,
benchmarks, replay artifacts, and a small Lean proof surface.
