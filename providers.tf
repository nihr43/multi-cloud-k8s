terraform {
  required_providers {
    digitalocean = {
      source  = "digitalocean/digitalocean"
      version = "~> 2.0"
    }
    linode = {
      source  = "linode/linode"
      version = "2.9.1"
    }
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }
}

# digitalocean
variable "do_token" {}

provider "digitalocean" {
  token = var.do_token
}

resource "digitalocean_ssh_key" "default" {
  name       = "opentofu"
  public_key = file("~/.ssh/id_ed25519.pub")
}

# linode
variable "linode_token" {}

provider "linode" {
  token = var.linode_token
}

resource "linode_sshkey" "default" {
  label   = "opentofu"
  ssh_key = chomp(file("~/.ssh/id_ed25519.pub"))
}

# aws
variable "aws_access" {}
variable "aws_secret" {}

provider "aws" {
  region     = "us-west-2"
  access_key = var.aws_access
  secret_key = var.aws_secret
}

resource "aws_key_pair" "default" {
  key_name   = "opentofu"
  public_key = chomp(file("~/.ssh/id_ed25519.pub"))
}
