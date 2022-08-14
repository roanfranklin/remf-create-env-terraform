# table lock DynamoDB
resource "aws_dynamodb_table" "project-terraform-locks" {
  name         = "pxco001-terraform-locks"
  billing_mode = "PAY_PER_REQUEST"
  hash_key     = "LockID"

  attribute {
    name = "LockID"
    type = "S"
  }
}