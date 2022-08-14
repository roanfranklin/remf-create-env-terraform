# # ##########################################################
# # RDS Subnet_Group

resource "aws_db_subnet_group" "env-dbsng" {
  name       = "${var.environment}-db-subnet-group-rds-mysql"
  subnet_ids = [
    var.subnet_private_az1_id,
    var.subnet_private_az2_id
  ]

  tags = {
    Name = "${var.environment}-db-subnet-group-rds-mysql"
  }
}


# # ##############
# # RDS 

resource "aws_db_instance" "mydb" {
  allocated_storage         = 40
  max_allocated_storage     = 100
  engine                    = var.rds_engine
  engine_version            = var.rds_engine_version
  identifier                = var.rds_name
  instance_class            = var.rds_instance_class
  name                      = var.rds_database_mysql
  username                  = var.rds_username_mysql
  password                  = var.rds_password_mysql
  parameter_group_name      = var.rds_parameter_group_name
  availability_zone         = "${var.region}b"
  #final_snapshot_identifier = "${var.rds_name}-001"
  #backup_retention_period   = 0
  skip_final_snapshot       = true
  vpc_security_group_ids    = ["${aws_security_group.env-rds-sg.id}"]
  db_subnet_group_name      = aws_db_subnet_group.env-dbsng.name
  publicly_accessible       = true
}