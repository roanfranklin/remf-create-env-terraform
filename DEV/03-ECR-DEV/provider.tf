terraform {
  required_version = ">= 1.0.4"
  backend "s3" {
    encrypt                 = true
    bucket                  = "pxco001-terraform-state"
    dynamodb_table          = "pxco001-terraform-locks"
    region                  = "us-east-2"
    # workspace_key_prefix    = "dev"
    key                     = "DEV/ECR/terraform.tfstate"
  }
}

provider "aws" {
  region = var.region
}