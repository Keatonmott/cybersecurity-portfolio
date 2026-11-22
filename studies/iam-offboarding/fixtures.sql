-- Synthetic approvals and normalized, read-only permission observations.
-- All times are UTC on 2026-01-12. IDs refer to fictional GitHub users.
CREATE TABLE scope (
    ticket TEXT, user_id INTEGER, repo TEXT, expected TEXT NOT NULL CHECK (expected IN ('none', 'read')), effective_from TEXT,
    owner TEXT, PRIMARY KEY (ticket, user_id, repo)
);
INSERT INTO scope VALUES
    ('IAM-104', 831, 'billing',       'none', '10:00', 'Billing maintainers'),
    ('IAM-104', 831, 'release-tools', 'none', '10:00', 'Release engineering'),
    ('IAM-105', 912, 'payments-api',  'read', '10:00', 'Payments team owner');

CREATE TABLE evidence (
    user_id INTEGER, repo TEXT, seen_at TEXT, role TEXT, complete INTEGER,
    PRIMARY KEY (user_id, repo, seen_at),
    CHECK (complete IN (0, 1))
);
-- "none" is an explicit negative from a complete effective-access review.
-- NULL on the release-tools row means the export ended before all pages arrived.
INSERT INTO evidence VALUES
    (831, 'billing',       '10:09', 'write', 1),
    (831, 'release-tools', '09:50', 'read',  1),
    (831, 'release-tools', '10:08', NULL,    0),
    (912, 'payments-api',  '10:10', 'write', 1),
    (831, 'billing',       '10:38', 'none',  1),
    (912, 'payments-api',  '10:45', 'read',  1),
    (831, 'release-tools', '10:53', 'none',  1);
