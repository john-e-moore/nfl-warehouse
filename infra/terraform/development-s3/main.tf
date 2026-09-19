terraform {
  required_version = ">= 1.8.0, < 2.0.0"

  # Supply every backend setting at init time. This avoids committing
  # environment-specific state locations and keeps state separate from raw data.
  backend "s3" {}

  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }
}

provider "aws" {
  region = var.aws_region

  default_tags {
    tags = local.tags
  }
}

locals {
  name_prefix    = "${var.project}-${var.environment}"
  raw_key_prefix = "provider=kalshi/entity=markets/*"
  tags = {
    Environment = var.environment
    ManagedBy   = "terraform"
    Project     = var.project
  }
}

resource "aws_s3_bucket" "raw" {
  bucket              = var.bucket_name
  force_destroy       = false
  object_lock_enabled = true
}

resource "aws_s3_bucket_public_access_block" "raw" {
  bucket = aws_s3_bucket.raw.id

  block_public_acls       = true
  block_public_policy     = true
  ignore_public_acls      = true
  restrict_public_buckets = true
}

resource "aws_s3_bucket_ownership_controls" "raw" {
  bucket = aws_s3_bucket.raw.id

  rule {
    object_ownership = "BucketOwnerEnforced"
  }
}

resource "aws_s3_bucket_server_side_encryption_configuration" "raw" {
  bucket = aws_s3_bucket.raw.id

  rule {
    apply_server_side_encryption_by_default {
      sse_algorithm = "AES256"
    }
  }
}

resource "aws_s3_bucket_versioning" "raw" {
  bucket = aws_s3_bucket.raw.id

  versioning_configuration {
    status = "Enabled"
  }
}

resource "aws_s3_bucket_object_lock_configuration" "raw" {
  bucket = aws_s3_bucket.raw.id

  rule {
    default_retention {
      days = var.object_lock_retention_days
      mode = "GOVERNANCE"
    }
  }

  depends_on = [aws_s3_bucket_versioning.raw]
}

data "aws_iam_policy_document" "raw_bucket" {
  statement {
    sid    = "DenyInsecureTransport"
    effect = "Deny"

    actions = ["s3:*"]

    principals {
      type        = "*"
      identifiers = ["*"]
    }

    resources = [
      aws_s3_bucket.raw.arn,
      "${aws_s3_bucket.raw.arn}/*",
    ]

    condition {
      test     = "Bool"
      variable = "aws:SecureTransport"
      values   = ["false"]
    }
  }

  statement {
    sid    = "DenyUnencryptedObjectWrites"
    effect = "Deny"

    actions = ["s3:PutObject"]

    principals {
      type        = "*"
      identifiers = ["*"]
    }

    resources = ["${aws_s3_bucket.raw.arn}/${local.raw_key_prefix}"]

    condition {
      test     = "StringNotEquals"
      variable = "s3:x-amz-server-side-encryption"
      values   = ["AES256"]
    }
  }

  statement {
    sid    = "DenyNonConditionalObjectWrites"
    effect = "Deny"

    actions = ["s3:PutObject"]

    principals {
      type        = "*"
      identifiers = ["*"]
    }

    resources = ["${aws_s3_bucket.raw.arn}/${local.raw_key_prefix}"]

    condition {
      test     = "StringNotEquals"
      variable = "s3:if-none-match"
      values   = ["*"]
    }
  }
}

resource "aws_s3_bucket_policy" "raw" {
  bucket = aws_s3_bucket.raw.id
  policy = data.aws_iam_policy_document.raw_bucket.json
}

data "aws_iam_policy_document" "writer_assume_role" {
  statement {
    sid     = "AllowConfiguredTrustedPrincipals"
    effect  = "Allow"
    actions = ["sts:AssumeRole"]

    principals {
      type        = "AWS"
      identifiers = var.trusted_principal_arns
    }
  }
}

resource "aws_iam_role" "raw_writer" {
  name                 = "${local.name_prefix}-raw-writer"
  assume_role_policy   = data.aws_iam_policy_document.writer_assume_role.json
  max_session_duration = 3600
}

data "aws_iam_policy_document" "raw_writer" {
  statement {
    sid       = "ListRawObservationPrefix"
    effect    = "Allow"
    actions   = ["s3:ListBucket"]
    resources = [aws_s3_bucket.raw.arn]

    condition {
      test     = "StringLike"
      variable = "s3:prefix"
      values   = [local.raw_key_prefix]
    }
  }

  statement {
    sid    = "CreateAndReadRawObservations"
    effect = "Allow"
    actions = [
      "s3:GetObject",
      "s3:PutObject",
    ]
    resources = ["${aws_s3_bucket.raw.arn}/${local.raw_key_prefix}"]
  }
}

resource "aws_iam_role_policy" "raw_writer" {
  name   = "${local.name_prefix}-raw-writer"
  role   = aws_iam_role.raw_writer.id
  policy = data.aws_iam_policy_document.raw_writer.json
}
