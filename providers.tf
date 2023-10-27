# do

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
  }
}

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
