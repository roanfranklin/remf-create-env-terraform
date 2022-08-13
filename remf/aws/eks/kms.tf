resource "aws_kms_key" "eks" {{
  description             = "EKS Secret Encryption Key"
  deletion_window_in_days = var.eks_encryption_config_deletion_window_in_days
  enable_key_rotation     = var.eks_encryption_config_enable_key_rotation

  tags = {{
    Name = "${{var.project}}-eks-cluster"
    Env = "${{var.environment}}"
  }}
}}