terraform {
  required_version = ">= 1.0.4"
  backend "s3" {
    encrypt        = true
    bucket         = "pxco001-terraform-state"
    dynamodb_table = "pxco001-terraform-locks"    
    region         = "us-east-2"
    key            = "DEV/NETWORK/terraform.tfstate"
  }
}

provider "aws" {
  region = var.region
}

data "aws_availability_zones" "available" {}
