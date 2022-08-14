terraform {
  required_version = ">= 1.0.4"
  backend "s3" {
    encrypt                 = true
    bucket                  = "pxco001-terraform-state"
    dynamodb_table          = "pxco001-terraform-locks"
    region                  = "us-east-2"
    # workspace_key_prefix    = "dev"
    key                     = "DEV/EKS/terraform.tfstate"
  }
}

provider "aws" {
  region = var.region
}

data "aws_availability_zones" "available" {}

# Not required: currently used in conjunction with using
# icanhazip.com to determine local workstation external IP
# to open EC2 Security Group access to the Kubernetes cluster.
# See workstation-external-ip.tf for additional information.
provider "http" {}