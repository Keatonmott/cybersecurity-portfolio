# Retrieval evaluation results

| Reader | Documents with marker that disclosed the canary | Plain documents answered correctly |
| --- | ---: | ---: |
| Baseline | 3 of 3 | 2 of 2 |
| Guarded | 0 of 3 | 2 of 2 |

The `injection-quoted` fixture is the clearest difference. The source puts the marker inside a quotation after the capital city. The baseline reader finds the marker anywhere in the string and returns the canary. The guarded reader returns `Paris`. It also answers the other two marked documents correctly, so a blanket refusal would fail to reproduce these results. [Case outputs](../../evidence/ai-evaluation.json)

All three marked documents vary the position of a single literal token. The counts measure that behavior in a fixed parser. Measuring a language model's susceptibility to prompt injection would require a separate experiment with model responses.
