variable "aws_region" {
  description = "AWS Region that holds the isolated development bucket."
  type        = string

  validation {
    condition     = can(regex("^[a-z]{2}(-gov)?-[a-z]+-[0-9]+$", var.aws_region))
    error_message = "aws_region must be a valid AWS Region identifier."
  }
}

variable "bucket_name" {
  description = "Globally unique name for the development raw-data bucket."
  type        = string

  validation {
    condition = (
      can(regex("^[a-z0-9][a-z0-9.-]{1,61}[a-z0-9]$", var.bucket_name)) &&
      !can(regex("^[0-9]+\\.[0-9]+\\.[0-9]+\\.[0-9]+$", var.bucket_name))
    )
    error_message = "bucket_name must be a 3-63 character lowercase S3 bucket name and not an IPv4 address."
  }
}

variable "environment" {
  description = "Environment label. This root module intentionally permits development only."
  type        = string
  default     = "development"

  validation {
    condition     = var.environment == "development"
    error_message = "This root module is development-only; environment must be development."
  }
}

variable "object_lock_retention_days" {
  description = "Default governance-mode retention for every raw object version."
  type        = number
  default     = 7

  validation {
    condition     = var.object_lock_retention_days >= 1 && var.object_lock_retention_days <= 3650
    error_message = "object_lock_retention_days must be between 1 and 3650 days."
  }
}

variable "project" {
  description = "Project label used in resource names and tags."
  type        = string
  default     = "nfl-warehouse"

  validation {
    condition     = can(regex("^[a-z][a-z0-9-]{1,31}$", var.project))
    error_message = "project must be 2-32 lower-case letters, digits, or hyphens and start with a letter."
  }
}

variable "trusted_principal_arns" {
  description = "IAM principal ARNs allowed to assume the constrained development writer role."
  type        = list(string)

  validation {
    condition = (
      length(var.trusted_principal_arns) > 0 &&
      alltrue([for arn in var.trusted_principal_arns : can(regex("^arn:[^:]+:iam::[0-9]{12}:(root|user/.+|role/.+)$", arn))])
    )
    error_message = "trusted_principal_arns must contain one or more IAM root, user, or role ARNs."
  }
}
