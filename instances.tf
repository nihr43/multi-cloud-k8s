resource "digitalocean_droplet" "instance" {
  image    = "debian-12-x64"
  name     = "test"
  region   = "nyc1"
  size     = "s-1vcpu-1gb"
  ssh_keys = [digitalocean_ssh_key.default.fingerprint]
}
