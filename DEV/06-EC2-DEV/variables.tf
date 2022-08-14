variable "region" {
  description = "Default Region AWS in secret.tfvars"
}

variable "ami_default" {
  description = "AMI Default Project in secrets.tfvars"
}

variable "instance_type" {
  description = "Default Instance Type in secret.tfvar"
}

variable "ssh_port" {
  description = "Change Default SSH Port in secret.tfvar"
}

variable "public_key" {
  default = "ID_RSA Public in secret.tfvar"
}

variable "cidr_env" {
  description = "VPC CIDR - DEV in secret.tfvars"
}

variable "vpc_env_id" {
  description = "VPC ID - DEV in secret.tfvars"
}

variable "subnet_private_az1_id" {
  description = "Subnet Private da AZ A in secret.tfvars"
}

variable "subnet_private_az2_id" {
  description = "Subnet Private da AZ B in secret.tfvars"
}

variable "subnet_public_az1_id" {
  description = "Subnet Public da AZ A in secret.tfvars"
}

variable "subnet_public_az2_id" {
  description = "Subnet Public da AZ B in secret.tfvars"
}
