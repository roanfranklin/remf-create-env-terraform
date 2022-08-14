terraform {
  required_version = ">= 1.0.4"
  backend "s3" {
    bucket         = "replybet-terraform-state"
    key            = "DEV/RDS/terraform.tfstate"
    region         = "us-east-2"
    dynamodb_table = "replybet-terraform-locks"
    encrypt        = true
  }
}

provider "aws" {
  region = var.region
}