resource "digitalocean_droplet" "instance" {
  image    = "debian-12-x64"
  name     = "mck-k8s-${count.index}"
  region   = "nyc1"
  size     = "s-1vcpu-2gb"
  ssh_keys = [digitalocean_ssh_key.default.fingerprint]
  count    = 1
}

resource "linode_instance" "instance" {
  image           = "linode/debian12"
  label           = "mck-k8s-linode-${count.index}"
  region          = "us-ord"
  type            = "g6-standard-1"
  authorized_keys = [linode_sshkey.default.ssh_key]
  count           = 1
}
