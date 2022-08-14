resource "aws_vpc" "vpc_env" {
  cidr_block           = var.cidr_env
  
  enable_dns_hostnames = true
  enable_dns_support   = true
  assign_generated_ipv6_cidr_block = true

  tags = {
    Name = "pxco001-vpc-dev"
  }
}
