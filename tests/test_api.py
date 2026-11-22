from http.server import HTTPServer
from threading import Thread
from urllib.error import HTTPError
from urllib.request import Request, urlopen
import json
import unittest

from projects.secure_api.app import Handler, NotFound, Unauthenticated, document_response, get_document


class ApiCaseStudyTests(unittest.TestCase):
    def test_denied_and_missing_have_identical_public_responses(self):
        denied = document_response("doc-2", "alice")
        self.assertEqual(denied, (404, {"error": "not found"}))
        self.assertEqual(denied, document_response("missing", "alice"))

    def test_owner_can_read_own_document(self):
        self.assertEqual(get_document("doc-1", "alice")["id"], "doc-1")

    def test_other_user_cannot_read_document(self):
        with self.assertRaises(NotFound):
            get_document("doc-2", "alice")

    def test_missing_identity_is_rejected(self):
        with self.assertRaises(Unauthenticated):
            get_document("doc-1", None)

    def test_missing_and_forbidden_have_same_exception(self):
        for document_id in ("doc-2", "not-present"):
            with self.assertRaises(NotFound):
                get_document(document_id, "alice")

    def test_http_endpoint_enforces_owner_check(self):
        server = HTTPServer(("127.0.0.1", 0), Handler)
        thread = Thread(target=server.serve_forever, daemon=True)
        thread.start()
        base = f"http://127.0.0.1:{server.server_address[1]}"
        try:
            request = Request(f"{base}/documents/doc-1", headers={"X-Demo-User": "alice"})
            with urlopen(request) as response:
                self.assertEqual(response.status, 200)
                self.assertEqual(json.load(response)["id"], "doc-1")
            request = Request(f"{base}/documents/doc-2", headers={"X-Demo-User": "alice"})
            with self.assertRaises(HTTPError) as error:
                urlopen(request)
            self.assertEqual(error.exception.code, 404)
            error.exception.close()
        finally:
            server.shutdown()
            server.server_close()
            thread.join(timeout=2)


if __name__ == "__main__":
    unittest.main()
