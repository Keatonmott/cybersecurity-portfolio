# Document ownership review

The first version of the lookup checked whether the caller was known, then returned the requested record. In the original synthetic case, Alice received a document owned by Bob. The ownership check now runs before the API returns any document content.

The seven fixture requests cover both owners, both cross-owner combinations, an absent document, an absent identity and an unknown identity. The two owner reads return 200. Both cross-owner requests and the missing document return 404. Both identity failures return 401. The tests also compare the public error bodies for denied and missing documents. [Recorded decisions](../../evidence/api-authorization.json) · [HTTP and policy tests](../../tests/test_api.py)

The app accepts a demonstration identity header and supports reads only. A deployment would need to derive the caller from a verified session. Adding document updates would require an ownership check on the write path.
