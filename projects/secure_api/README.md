# Document API access control

Alice and Bob each own one document. A recognized caller can read a document only when its owner matches the caller. A missing or unknown identity receives HTTP 401. A recognized caller receives HTTP 404 for both a missing document and another user's document.

## Run the access checks

From the repository root, print the decisions and run the tests. The integration test starts a server on a temporary loopback port.

```sh
python -m projects.secure_api.demo
python -m unittest tests.test_api -v
```

For an interactive session, start the API with `python -m projects.secure_api.app`. The server listens on `127.0.0.1:8765` until you press Ctrl+C. In a second PowerShell window, read Alice's own report.

```powershell
Invoke-RestMethod -Uri http://127.0.0.1:8765/documents/doc-1 -Headers @{ 'X-Demo-User' = 'alice' }
```

The header selects a fixture identity. Any caller can set it, so keep this service on loopback. [Case report](report.md) · [Access decisions](../../evidence/api-authorization.json)
