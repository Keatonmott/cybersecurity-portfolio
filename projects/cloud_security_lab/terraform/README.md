# Report storage on AWS

[main.tf](main.tf) defines a versioned S3 bucket with server-side encryption and all four public access block settings enabled. A separate IAM policy grants `s3:GetObject` on the bucket's objects. Attaching it to a principal and enabling account-level logging are separate operations.

The offline exercises use JSON fixtures. This Terraform example has not been validated or deployed to AWS. To inspect it locally, run `terraform init -backend=false` and `terraform validate` in this directory with the provider available. Planning against an account also requires AWS credentials and a globally unique `bucket_name`.
