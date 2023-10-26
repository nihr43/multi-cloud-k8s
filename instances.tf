resource "digitalocean_droplet" "instance" {
  image    = "debian-12-x64"
  name     = "mck-k8s-${count.index}"
  region   = "nyc1"
  size     = "s-1vcpu-2gb"
  ssh_keys = [digitalocean_ssh_key.default.fingerprint]
  count    = 1
}
