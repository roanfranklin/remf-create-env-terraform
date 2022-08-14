  
  ingress {{
    cidr_blocks = [
      var.cidr_dev,
      "{ipv4}"
    ]
    description = "{description}"
    from_port = {port}
    to_port   = {port}
    protocol  = "{protocol}"
  }}
  