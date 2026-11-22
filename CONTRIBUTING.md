# Changing the labs

When a rule changes, include a fixture that exercises the new behavior and one ordinary case that should still pass. Document the reason for the change in the relevant case report.

Run the suite and refresh the sample output from the repository root. Review any changes under `evidence/` alongside the code.

```sh
python -m unittest discover -s tests -v
python -m tools.build_evidence
```
