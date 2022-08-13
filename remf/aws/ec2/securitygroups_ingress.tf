  ingress {{
    cidr_blocks = [
      var.cidr_dev,
      {list_ip}
    ]
    from_port = {port}
    to_port   = {port}
    protocol  = "{protocol}"
  }}