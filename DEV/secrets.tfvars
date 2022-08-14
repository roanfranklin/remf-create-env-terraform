
# ###############################
# NETWORK

cidr_env = "10.0.0.0/16"
cidr_2octectos = "10.0"
subnets_public_total = "2"
subnets_private_total = "2"

# ###############################
# EKS

eks_worker_nodes_instance_type = ["t3.medium"]
eks_node_scaling_desired_size = "1"
eks_node_scaling_max_size = "1"
eks_node_scaling_min_size = "1"
eks_encryption_config_resources = ["secrets"]
eks_encryption_config_deletion_window_in_days = "7"
eks_encryption_config_enable_key_rotation = "true"

# ###############################
# ECR

# ###############################
# ROUTE53

domain = "meudominio.com.br"

# ###############################
# EC2

ami_default = "ami-02f3416038bdb17fb"
instance_type = "t2.micro"
ssh_port = "7122"
public_key = "ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAACAQDM4W8ozuKd835FRP4kx3t6Lg3dUhBf139I/u2f8h0PlgXOImyHJPUil++XXC8JtfkJEa4y/BSxkxrjbQLqeV5z81JvnLeYHTo5muAgs1IOZ1jgfmfUN2pO367V4F4QCNCUC80xmHor9IcuUgvPvJn8yCJPdcPK/aas6qqkOEo8DzQTWOcLxWrKxj+WmX6cpM4tt013wLkcDVN0FBQHBnRTay/ro0MyaNSno+WQN81yTs7BiYUUF/c0ZvtKeqav93xX0nxUY7vxT+pGSbvjnnJCjvTunc/YRvNhLqnsFmHfN75M/LMjxYgXpZM+vm6x+9QiTdLNJ2d6qabI3VvyTLyrbXNDJcHX1S1THNWM6cqcwym20mtCy1qSKstfLEg4xbceMqFIi6MS0KZ0vFuMFUFuhD5ooCMREaJbUbsVaSOsJIlbaU5Ec0+wwaeta7r9IkA1L77WZiJGKoYD+8EAL+R2hO/9lwSGmVjFV6l7i2XsthHPm7uRzqfRQQkSueAyaMkGi4AL1zcxltBpRFY9vTYe4yaKy8jarCeNY3LrX3LEhBlOESoR3YPVd23hI/vOnW1a6SY57y979/s9AEJEkbt0mFV/I+MPcqj/9fQ4iAC9mG93vXjbpWCuhyiGRIpuwwwQUBYFAofsjII00DaS3bN70vRZZxI8+EB5d1n98m6y0w== wordpress@cloudopss.com.br"
