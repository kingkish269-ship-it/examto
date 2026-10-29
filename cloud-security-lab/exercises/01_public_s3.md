# 01 — Public S3 buckets

Public object storage is one of the most common causes of real-world breaches.

## See it

```bash
python3 -m auditor.audit data/sample_account.json --format table | grep s3
```

`public-marketing-assets` is flagged CRITICAL (public + no Block Public Access);
`customer-exports` is flagged MEDIUM (no default encryption).

## The logic

Read `public_s3_buckets` in `auditor/checks.py`. A bucket is public if it is
marked public or is missing Block Public Access. Encryption is a separate,
lower-severity finding.

## In real AWS

- Enable account-level S3 Block Public Access.
- Enable default encryption (SSE-KMS for sensitive data).
- Detect drift with AWS Config rules `s3-bucket-public-read-prohibited` and
  `s3-bucket-server-side-encryption-enabled`.

## Extend it

Add a check `s3-no-versioning` for buckets without versioning, with a sample
bucket and a test. This is how you grow the auditor into portfolio evidence.
