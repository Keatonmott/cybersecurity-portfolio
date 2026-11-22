# Document retrieval and prompt injection

The fixture asks a reader for a capital city or a contact address. Three documents also contain a control marker. The baseline reader returns a synthetic secret when it finds that marker. The guarded reader extracts the requested fact. Both readers are deterministic Python functions and run offline.

From the repository root, run the evaluation and its regression tests.

```sh
python -m projects.ai_security.evaluate --mode both
python -m unittest tests.test_ai -v
```

The output records each answer and whether it matches the expected fact. Use `--mode guarded` to inspect just that reader. The case IDs match across the [input documents](cases.json), [recorded output](../../evidence/ai-evaluation.json), and [results](report.md).
