resource "aws_route53_zone" "main_domain" {
  name         = var.domain
  tags         = {
    Name = "pxco001-route53-${var.environment}"
  }
}

resource "aws_route53_record" "traefik" {
  zone_id    = aws_route53_zone.main_domain.zone_id
  name       = "traefik.${var.domain}"
  type       = "A"
  alias {
    name                   = "abcd123a456bc7def8a901a2b34c5d6e-1234567890.us-east-2.elb.amazonaws.com"
    zone_id                = "A0BCDEFG1HIJK2"
    evaluate_target_health = true
  }
}

resource "aws_route53_record" "argocd" {
  zone_id    = aws_route53_zone.main_domain.zone_id
  name       = "argocd.${var.domain}"
  type       = "A"
  alias {
    name                   = "abcd123a456bc7def8a901a2b34c5d6e-1234567890.us-east-2.elb.amazonaws.com"
    zone_id                = "A0BCDEFG1HIJK2"
    evaluate_target_health = true
  }
}

resource "aws_route53_record" "app1" {
  zone_id    = aws_route53_zone.main_domain.zone_id
  name       = "app1.${var.domain}"
  type       = "A"
  alias {
    name                   = "abcd123a456bc7def8a901a2b34c5d6e-1234567890.us-east-2.elb.amazonaws.com"
    zone_id                = "A0BCDEFG1HIJK2"
    evaluate_target_health = true
  }
}

resource "aws_route53_record" "app2" {
  zone_id    = aws_route53_zone.main_domain.zone_id
  name       = "app2.${var.domain}"
  type       = "A"
  alias {
    name                   = "abcd123a456bc7def8a901a2b34c5d6e-1234567890.us-east-2.elb.amazonaws.com"
    zone_id                = "A0BCDEFG1HIJK2"
    evaluate_target_health = true
  }
}

resource "aws_route53_record" "app3" {
  zone_id    = aws_route53_zone.main_domain.zone_id
  name       = "app3.${var.domain}"
  type       = "A"
  alias {
    name                   = "abcd123a456bc7def8a901a2b34c5d6e-1234567890.us-east-2.elb.amazonaws.com"
    zone_id                = "A0BCDEFG1HIJK2"
    evaluate_target_health = true
  }
}
