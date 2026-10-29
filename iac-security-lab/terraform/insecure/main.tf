# INSECURE Terraform for study. Do not apply. Every resource here is flagged by
# scanner/tf_scan.py and by Checkov. The secure version is in ../secure/main.tf.

resource "aws_s3_bucket" "data" {
  bucket = "lab-insecure-data"
  acl    = "public-read" # CRITICAL: public bucket
}

resource "aws_security_group" "admin" {
  name = "admin"
  ingress {
    from_port   = 22
    to_port     = 22
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"] # HIGH: SSH open to the internet
  }
}

resource "aws_db_instance" "orders" {
  identifier          = "orders"
  publicly_accessible = true  # CRITICAL
  storage_encrypted   = false # HIGH
}

resource "aws_ebs_volume" "scratch" {
  availability_zone = "us-east-1a"
  size              = 20
  encrypted         = false # MEDIUM
}

resource "aws_iam_policy" "admin" {
  name   = "admin"
  policy = jsonencode({
    Statement = [{ Effect = "Allow", Action = "*", Resource = "*" }] # HIGH
  })
}
