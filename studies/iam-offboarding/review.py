"""Compare approved and observed access for two GitHub IAM tickets."""

import sqlite3
from contextlib import closing
from pathlib import Path


ROOT = Path(__file__).resolve().parent


def main():
    sql = (ROOT / "review.sql").read_text(encoding="utf-8")
    with closing(sqlite3.connect(":memory:")) as db:
        db.executescript((ROOT / "fixtures.sql").read_text(encoding="utf-8"))
        for as_of in ("10:15", "11:00"):
            print(f"\nReview at {as_of} UTC")
            print("Ticket   Repository     Approved  Observed  Evidence  Decision                 Owner")
            for ticket, repo, expected, role, seen, decision, owner in db.execute(sql, {"as_of": as_of}):
                print(f"{ticket:9}{repo:15}{expected:10}{role or '?':10}{seen or '?':10}"
                      f"{decision:25}{owner}")


if __name__ == "__main__":
    main()
