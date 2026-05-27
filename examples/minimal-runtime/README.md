# Minimal Runtime

Run the smallest public runtime path:

```bash
python examples/minimal-runtime/minimal_runtime.py
```

The script builds one bounded signal, derives a `PASS` / `WARN` / `BLOCK`
verdict, emits audit identifiers, and verifies replay from the evidence packet.
