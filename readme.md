# multi-cloud-k8s

This is an exercise in provisioning a kubernetes cluster across multiple cloud providers for the ultimate in infrastructure resiliency.  Whether such an endeavor is worthwhile IRL is up for dabate; this was done for fun.

This is done by wrapping opentofu (formerly terraform) and ansible in python, enabling a single commandline entrypoint for various CRUD tasks.

## usage

The default action is to enforce state:

```
$ export TF_VAR_do_token=asdf1234
$ python3 mck

OpenTofu used the selected providers to generate the following execution plan. Resource actions are indicated with the following symbols:
  + create

OpenTofu will perform the following actions:

  # digitalocean_droplet.instance will be created
  + resource "digitalocean_droplet" "instance" {
      + backups              = false
      + created_at           = (known after apply)
      + disk                 = (known after apply)
      + graceful_shutdown    = false
      + id                   = (known after apply)
      + image                = "debian-12-x64"
      + ipv4_address         = (known after apply)
      + ipv4_address_private = (known after apply)
      + ipv6                 = false
      + ipv6_address         = (known after apply)
      + locked               = (known after apply)
      + memory               = (known after apply)
      + monitoring           = false
      + name                 = "test"
      + price_hourly         = (known after apply)
      + price_monthly        = (known after apply)
      + private_networking   = (known after apply)
      + region               = "nyc1"
      + resize_disk          = true
      + size                 = "s-1vcpu-1gb"
      + ssh_keys             = (known after apply)
      + status               = (known after apply)
      + urn                  = (known after apply)
      + vcpus                = (known after apply)
      + volume_ids           = (known after apply)
      + vpc_uuid             = (known after apply)
    }

  # digitalocean_ssh_key.default will be created
  + resource "digitalocean_ssh_key" "default" {
      + fingerprint = (known after apply)
      + id          = (known after apply)
      + name        = "opentofu"
      + public_key  = <<-EOT
            ssh-ed25519 AAAAC3NzaC1lZDI1NTE5AAAAIKL+1xp+nQIbu02D1NmU+4RTPGblUML21TSzF/Pxg5GM
        EOT
    }

Plan: 2 to add, 0 to change, 0 to destroy.

Do you want to perform these actions?
  OpenTofu will perform the actions described above.
  Only 'yes' will be accepted to approve.

  Enter a value:
```

`--destroy` will remove all resources:

```
$ python2 mck --destroy
```
