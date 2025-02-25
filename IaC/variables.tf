# define the variables that will be used in the terraform code

# def a variable for the access key
variable "aws_access_key" {
  description = "The access key for the AWS account"
  type        = string
}

# def a variable for the secret key
variable "aws_secret_key" {
  description = "The secret key for the AWS account"
  type        = string
}

# def a variable for the EC2 instance type
variable "ec2_instance_type" {
  description = "The type of EC2 instance to launch"
  default     = "t2.micro"
}

# def a variable for the EC2 instance coun
variable "ec2_ami" {
  description = "A configuration of AMI to use for the EC2 instances, use ubuntu 24.04"
  type        = string
  default     = "ami-055943271915205db"
}


# def a variable for the team name
variable "tag_team_name" {
  description = "The name of the team that runs the project"
  type        = string
  default     = "HoangNgBot"
}

# def a variable for the owner name
variable "owner_name" {
  description = "The name of the owner of the project"
  type        = string
  default     = "HoangNg"
}

# def a variable for bucket name for raw data
variable "s3_bucket_name_raw_data" {
  description = "The name of the S3 bucket for raw data"
  type        = string
  default     = "ezez-aws-s3-raw-data"
}

# def a variable for bucket name for transformed data
variable "s3_bucket_name_transformed_data" {
  description = "The name of the S3 bucket for raw data"
  type        = string
  default     = "ezez-aws-s3-transformed-data"
}