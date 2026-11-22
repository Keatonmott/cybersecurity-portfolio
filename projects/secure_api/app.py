"""Local-only document API with object-level authorization."""

from http.server import BaseHTTPRequestHandler, HTTPServer
import json


DOCUMENTS = {
    "doc-1": {"id": "doc-1", "owner": "alice", "title": "Quarterly plan", "body": "Synthetic Alice data"},
    "doc-2": {"id": "doc-2", "owner": "bob", "title": "Budget", "body": "Synthetic Bob data"},
}
USERS = {"alice", "bob"}


class NotFound(Exception):
    """Document is missing or unavailable to this user."""


class Unauthenticated(Exception):
    """No recognized demonstration identity was supplied."""


def get_document(document_id, user):
    """Return a document only when its owner matches the requester."""
    if user not in USERS:
        raise Unauthenticated()
    document = DOCUMENTS.get(document_id)
    if document is None or document["owner"] != user:
        raise NotFound()
    return document


def document_response(document_id, user):
    try:
        return 200, get_document(document_id, user)
    except Unauthenticated:
        return 401, {"error": "demo identity required"}
    except NotFound:
        return 404, {"error": "not found"}


class Handler(BaseHTTPRequestHandler):
    def respond(self, status, payload):
        data = json.dumps(payload).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.send_header("Cache-Control", "no-store")
        self.send_header("Content-Length", str(len(data)))
        self.end_headers()
        self.wfile.write(data)

    def do_GET(self):
        parts = self.path.split("?")[0].strip("/").split("/")
        if len(parts) != 2 or parts[0] != "documents" or not parts[1]:
            return self.respond(404, {"error": "not found"})
        self.respond(*document_response(parts[1], self.headers.get("X-Demo-User")))


def main():
    server = HTTPServer(("127.0.0.1", 8765), Handler)
    print("Demo API listening at http://127.0.0.1:8765 (Ctrl+C to stop)")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        server.server_close()


if __name__ == "__main__":
    main()
