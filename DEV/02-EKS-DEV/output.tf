output "aa_kubeconfig" {
  value = "aws eks --region ${var.region} update-kubeconfig --name pxco001-eks-cluster"
}

output "bb_hpa_apply" {
  value = "kubectl apply -f https://github.com/kubernetes-sigs/metrics-server/releases/latest/download/components.yaml"
}

output "vpc_eks_dev_id" {
  value = aws_vpc.project-eks-vpc.id
}

output "xx-endnull" {
  value = "null"
}
