# multi-cloud-k8s

This is an exercise in provisioning a kubernetes cluster across multiple cloud providers for the ultimate in infrastructure resiliency.  Whether such an endeavor is worthwhile IRL is up for debate; this was done for fun.

This is done by wrapping opentofu (formerly terraform) and ansible in python, enabling a single commandline entrypoint for various CRUD tasks.

## usage

The default action is to enforce state:

```
$ export TF_VAR_do_token=
$ export TF_VAR_linode_token=
# export TF_VAR_aws_access=
$ export TF_VAR_aws_secret=
$ python3 mck
digitalocean_ssh_key.default: Refreshing state... [id=39804368]
linode_sshkey.default: Refreshing state...
linode_instance.instance[0]: Refreshing state... [id=51324518]
digitalocean_droplet.instance[0]: Refreshing state... [id=381834671]
data.aws_ami.ubuntu: Reading...
aws_key_pair.default: Refreshing state... [id=opentofu]
aws_default_subnet.default_az1: Refreshing state... [id=subnet-046b3f303365c3333]
aws_default_vpc.mainvpc: Refreshing state... [id=vpc-0371ba1712735e722]
data.aws_ami.ubuntu: Read complete after 1s [id=ami-08e2c1a8d17c2fe17]
aws_default_security_group.default: Refreshing state... [id=sg-06d079c63124325e2]
aws_instance.instance[0]: Refreshing state... [id=i-0d8123a6659382ff6]

No changes. Your infrastructure matches the configuration.

OpenTofu has compared your real infrastructure against your configuration and found no differences, so no changes are needed.

Apply complete! Resources: 0 added, 0 changed, 0 destroyed.
instance mck-k8s-aws-0 is provisioned on aws with address 18.236.105.125
instance mck-k8s-do-0 is provisioned on digitalocean with address 159.89.224.39
instance mck-k8s-linode-0 is provisioned on linode with address 172.233.209.96
```

`--destroy` will remove all resources:

```
$ python3 mck --destroy
```
