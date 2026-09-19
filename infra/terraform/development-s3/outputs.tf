output "raw_bucket_name" {
  description = "Name of the development raw-data bucket."
  value       = aws_s3_bucket.raw.bucket
}

output "raw_bucket_arn" {
  description = "ARN of the development raw-data bucket."
  value       = aws_s3_bucket.raw.arn
}

output "raw_key_prefix" {
  description = "Only S3 key prefix available to the writer role."
  value       = local.raw_key_prefix
}

output "raw_writer_role_arn" {
  description = "ARN to assume for create-only raw writes and read-back."
  value       = aws_iam_role.raw_writer.arn
}
