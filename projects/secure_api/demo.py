"""Print the access decisions for the two fixture owners."""

from .app import document_response


def access_matrix():
    cases = [
        ("alice", "doc-1"),
        ("bob", "doc-2"),
        ("alice", "doc-2"),
        ("bob", "doc-1"),
        ("alice", "missing"),
        (None, "doc-1"),
        ("unknown", "doc-1"),
    ]
    rows = []
    for user, document_id in cases:
        status, _ = document_response(document_id, user)
        rows.append({"user": user, "document": document_id, "status": status})
    return rows


def main():
    print("Caller     Document   HTTP")
    for row in access_matrix():
        caller = row["user"] or "(absent)"
        print(f"{caller:10} {row['document']:10} {row['status']}")


if __name__ == "__main__":
    main()
