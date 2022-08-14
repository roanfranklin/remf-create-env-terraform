# ##############
# RDS

variable "rds_instance_class" {
  default = "db.t3.small"
}

variable "rds_name" {
  default = "rds-prd-mysql"
}

variable "rds_engine" {
  default = "mysql"
}

variable "rds_engine_version" {
  default = "5.7"
}

variable "rds_parameter_group_name" {
  default = "default.mysql5.7"
}