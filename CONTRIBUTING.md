# Contributing

Contributions that improve correctness, portability, documentation, or low-noise repository checks are welcome.

1. Fork the repository and create a focused branch.
2. Keep checks deterministic, local, and read-only.
3. Never add telemetry, credential collection, or secret values to output.
4. Add or update `unittest` coverage for behavioral changes.
5. Run `python -m unittest discover -s tests -v` and `python -m compileall -q src`.
6. Update both English and Arabic README sections when user-facing behavior changes.
7. Open a pull request describing the problem, solution, and validation performed.

Please keep new checks practical and avoid scoring rules that depend on network access or subjective project popularity.
