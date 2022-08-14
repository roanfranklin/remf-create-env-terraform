resource "aws_security_group" "project_sg" {
  name   = "sg_dev_ec2_project"
  vpc_id = var.vpc_dev_id

  ingress {
    cidr_blocks = [
      "0.0.0.0/0"
    ]
    from_port = var.ssh_port
    to_port   = var.ssh_port
    protocol  = "tcp"
  }
  
  ingress {
    cidr_blocks = [
      var.cidr_dev,
      "0.0.0.0/0"
    ]
    description = "http"
    from_port = 80
    to_port   = 80
    protocol  = "tcp"
  }
    
  ingress {
    cidr_blocks = [
      var.cidr_dev,
      "0.0.0.0/0"
    ]
    description = "https"
    from_port = 443
    to_port   = 443
    protocol  = "tcp"
  }
    
  ingress {
    cidr_blocks = [
      var.cidr_dev,
      "201.201.201.201/32"
    ]
    description = "ip do roan"
    from_port = 500
    to_port   = 500
    protocol  = "tcp"
  }
  
  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
    ipv6_cidr_blocks = ["::/0"]
  }
}