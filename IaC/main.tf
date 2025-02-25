# declare the required provider and its version
terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }
}

# configure the AWS provider
provider "aws" {
  region     = "ca-central-1"
  access_key = var.aws_access_key
  secret_key = var.aws_secret_key
}

# # create a VPC
# resource "aws_vpc" "learning-aws-vpc" {
#   cidr_block           = "10.0.0.0/16" # This custom CIDR block allows 65,536 IP addresses for flexibility
#   enable_dns_hostnames = true          # This is set to true to allow instances to receive DNS hostnames
#   enable_dns_support   = true          # This is set to true to allow instances to receive DNS support

#   tags = {
#     Name    = "learning-aws-vpc"
#     Team    = var.tag_team_name
#     Owner   = var.owner_name
#     Purpose = "learning AWS and terraform"
#   }
# }

# # create a public subnet
# resource "aws_subnet" "learning-aws-public-subnet" {
#   vpc_id                  = aws_vpc.learning-aws-vpc.id
#   cidr_block              = "10.0.1.0/24" # allows 256 IP addresses (254 usable)
#   map_public_ip_on_launch = true          # assign public IP addresses to instances launched in this subnet (i.e., public subnet)

#   tags = {
#     Name    = "learning-aws-public-subnet"
#     Team    = var.tag_team_name
#     Owner   = var.owner_name
#     Purpose = "learning AWS and terraform"
#   }
# }

# # create a private subnet
# resource "aws_subnet" "learning-aws-private-subnet" {
#   vpc_id                  = aws_vpc.learning-aws-vpc.id
#   cidr_block              = "10.0.2.0/24" # allows 256 IP addresses (254 usable)
#   map_public_ip_on_launch = false         # prevent assigning public IP addresses to instances launched in this subnet (i.e., private subnet)

#   tags = {
#     Name    = "learning-aws-private-subnet"
#     Team    = var.tag_team_name
#     Owner   = var.owner_name
#     Purpose = "learning AWS and terraform"
#   }
# }

# # create an EC2 instance using mimimal compute resources (i.e., a free tier eligible instance)
# resource "aws_instance" "learning-aws-instance0" {
#   ami           = var.ec2_ami           # Ubuntu 24.04
#   instance_type = var.ec2_instance_type # free tier eligible instance type
#   subnet_id     = aws_subnet.learning-aws-public-subnet.id

#   tags = {
#     Name    = "learning-aws-instance0"
#     Team    = var.tag_team_name
#     Owner   = var.owner_name
#     Purpose = "learning AWS and terraform"
#   }
# }

# # create an EC2 instance using mimimal compute resources (i.e., a free tier eligible instance)
# resource "aws_instance" "learning-aws-instance1" {
#   ami           = var.ec2_ami           # Ubuntu 24.04
#   instance_type = var.ec2_instance_type # free tier eligible instance type
#   subnet_id     = aws_subnet.learning-aws-public-subnet.id

#   tags = {
#     Name    = "learning-aws-instance1"
#     Team    = var.tag_team_name
#     Owner   = var.owner_name
#     Purpose = "learning AWS and terraform"
#   }
# }

# create a S3 buckets for raw data and transformed data
resource "aws_s3_bucket" "aws-s3-bucket-ezez-raw-data" {
  bucket = var.s3_bucket_name_raw_data

  tags = {
    Name    = var.s3_bucket_name_raw_data
    Team    = var.tag_team_name
    Owner   = var.owner_name
    Purpose = "store raw data from ezez project"
  }
}

resource "aws_s3_bucket" "aws-s3-bucket-ezez-transformed-data" {
  bucket = var.s3_bucket_name_transformed_data

  tags = {
    Name    = var.s3_bucket_name_transformed_data
    Team    = var.tag_team_name
    Owner   = var.owner_name
    Purpose = "store transformed data from ezez project"
  }
}





