variable "region" {{
  description = "Default Region AWS in secret.tfvars"
}}

variable "environment" {{
  description = "Environment default in secret.tfvars"
}}

variable "ami_default" {{
  description = "AMI Default Project in secrets.tfvars"
}}

variable "instance_type" {{
  description = "Default Instance Type in secret.tfvar"
}}

variable "ssh_port" {{
  description = "Change Default SSH Port in secret.tfvar"
}}

variable "key_pair_name" {{
  default = "KeyPair Name in secret.tfvar"
}}

variable "public_key" {{
  default = "ID_RSA Public in secret.tfvar"
}}

variable "cidr_env" {{
  description = "VPC CIDR - {env_upper} in secret.tfvars"
}}

variable "vpc_env_id" {{
  description = "VPC ID - {env_upper} in secret.tfvars"
}}
