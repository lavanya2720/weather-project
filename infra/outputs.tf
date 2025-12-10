output "bucket_name" {
  value = aws_s3_bucket.weather_bucket.bucket
}

output "public_bucket_url" {
  value = "https://${aws_s3_bucket.weather_bucket.bucket}.s3.${var.aws_region}.amazonaws.com/"
}

