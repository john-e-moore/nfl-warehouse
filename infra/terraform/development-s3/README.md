# Development S3 infrastructure

This Terraform root module creates only the Milestone 2 development raw-data
bucket and its writer role. It does not create a Terraform state backend,
application credentials, an S3 client, a scheduler, or any production resource.

## Resources and guardrails

- The bucket is development-only; the `environment` input is fixed to
  `development`.
- S3 Block Public Access, `BucketOwnerEnforced` ownership, HTTPS-only access,
  and SSE-S3 (`AES256`) protect the bucket.
- Versioning and governance-mode S3 Object Lock retain each object version for
  at least the configured number of days. `force_destroy` is disabled, so a
  non-empty bucket cannot be removed by Terraform.
- A bucket policy requires `x-amz-server-side-encryption: AES256` and
  `If-None-Match: *` on every writer `PutObject` request under the Kalshi
  markets prefix. The latter makes a duplicate key fail instead of replacing an
  existing current object.
- The writer role can list only
  `provider=kalshi/entity=markets/*`, create and read objects there, and cannot
  delete objects, change retention, administer the bucket, or access another
  prefix.

The writer must use signed, direct `PutObject` requests carrying both required
headers. Multipart upload and `CopyObject` are intentionally outside this
initial writer boundary. M2-T4 will use the contract's deterministic keys and
publish payload objects before a manifest.

## Prerequisites

- Terraform 1.8.x or later (but before 2.0) and AWS CLI v2.
- An existing, encrypted, access-restricted S3 bucket for Terraform state. The
  state backend is deliberately external to this raw-data bucket, avoiding a
  self-referential bootstrap and keeping state separate by environment.
- An authorized development-account identity that can create the declared S3
  and IAM resources. Its identity policy must also permit `sts:AssumeRole` on
  the writer role if it will perform the later M2-T4 demonstration.

Do not place AWS access keys in `.tfvars`, command history, repository files,
or Terraform variables. Use an approved AWS profile, SSO, or other ambient
credential provider.

## Configure and review

Copy the tracked example; the resulting file is ignored by Git:

```bash
cd infra/terraform/development-s3
cp development.tfvars.example development.tfvars
```

Replace the bucket placeholder with a globally unique development name and
replace the trusted principal with the exact development user or role ARN. Do
not use a production principal or a whole-account root principal.

Initialize against the pre-existing remote state bucket. Set the shell values
locally; do not commit them. The state key below is intentionally separate from
the raw-object key grammar:

```bash
terraform init \
  -backend-config="bucket=$TF_STATE_BUCKET" \
  -backend-config="key=nfl-warehouse/development/s3-infrastructure.tfstate" \
  -backend-config="region=$TF_STATE_REGION" \
  -backend-config="encrypt=true" \
  -backend-config="use_lockfile=true"
terraform fmt -check
terraform validate
terraform plan -var-file=development.tfvars -out=development-s3.tfplan
terraform show -no-color development-s3.tfplan
```

Review that the plan contains exactly one bucket, its protection resources, one
bucket policy, and one constrained IAM role/policy. Confirm its account and
Region before any apply. The plan must be reviewed, but not applied, as part of
this repository task.

## Apply and verify

An authorized operator may apply only the reviewed saved plan:

```bash
terraform apply development-s3.tfplan
terraform output
```

Record the output role ARN in approved environment-specific configuration for
the later persistence task; it is not an application argument or manifest
field. M2-T4 must assume this role, use `If-None-Match: *` and SSE-S3 on every
write, and verify the returned payload and manifest. Do not grant the writer
role deletion, retention-bypass, broad bucket, or production access.

## Safe teardown

Development raw observations are append-only and protected by Object Lock, so
teardown is exceptional. Do not run `terraform destroy` as routine cleanup.
First preserve or formally retire the data, wait for every protected version's
retention period to expire, and have an authorized account operator confirm the
bucket is empty. The writer role cannot perform that deletion. Then create and
review a destroy plan; `force_destroy = false` will cause the operation to fail
if any object remains:

```bash
terraform plan -destroy -var-file=development.tfvars -out=development-s3-destroy.tfplan
terraform show -no-color development-s3-destroy.tfplan
terraform apply development-s3-destroy.tfplan
```

Never use `-auto-approve` for apply or destroy. Remove local plan files when
they are no longer needed; they can contain environment-specific resource
identifiers.
