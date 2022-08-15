resource "aws_db_subnet_group" "env-dbsng" {{
  name       = "{env_lower}-db-subnet-group-rds-mysql"
  subnet_ids = [
    var.subnet_private_az1_id,
    var.subnet_private_az2_id
  ]

  tags = {{
    Name = "{env_lower}-db-subnet-group-rds-mysql"
  }}
}}