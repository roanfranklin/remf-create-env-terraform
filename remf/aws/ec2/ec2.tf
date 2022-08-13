resource "aws_instance" "project" {{
  ami                    = var.ami_default
  instance_type          = var.instance_type
  subnet_id              = var.{az}
  vpc_security_group_ids = ["${{aws_security_group.project_sg.id}}"]
  key_name               = aws_key_pair.id_rsa_devops.key_name
  user_data              = templatefile("script/bootstrap.sh", {{
    VAR_PORT_SSH = var.ssh_port,
    VAR_DIR_CLOUDOPSS = "/remf"
  }})
  #user_data       = file("script/bootstrap.sh")

  tags = {{
    Name        = "{{project}}-{{ec2_name}}-${{var.environment}}"
    Environment = "${{var.environment}}"
  }}
}}
