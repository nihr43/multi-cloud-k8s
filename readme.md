# multi-cloud-k8s

This is an exercise in provisioning a kubernetes cluster across multiple cloud providers.  Whether such an endeavor is worthwhile IRL is up for debate; this was done for fun.

This is done by wrapping opentofu (formerly terraform) and ansible in python, enabling a single commandline entrypoint for various CRUD tasks.  There is zero manual work other than initial API token setup for each provider.

Wrapping opentofu rather than using client libraries directly gives us a well-proven means of provisioning base resources, as well as a well understood user interface - the cluster is described in `intances.tf`.

Once compute resources are provisioned, the tf state is examined and an ansible inventory is generated.  Base software installation is then performed with `ansible_runner`.

## usage

The default action is to enforce state:

```
$ export TF_VAR_do_token=
$ export TF_VAR_linode_token=
# export TF_VAR_aws_access=
$ export TF_VAR_aws_secret=
$ python3 mck
digitalocean_ssh_key.default: Refreshing state... [id=39804483]
linode_sshkey.default: Refreshing state...
linode_instance.instance[0]: Refreshing state... [id=51324967]
linode_instance.instance[1]: Refreshing state... [id=51324969]
aws_key_pair.default: Refreshing state... [id=opentofu]
data.aws_ami.ubuntu: Reading...
aws_default_vpc.mainvpc: Refreshing state... [id=vpc-0371ba1712735e722]
aws_default_subnet.default_az1: Refreshing state... [id=subnet-046b3f303365c3333]
digitalocean_droplet.instance[0]: Refreshing state... [id=381837561]
digitalocean_droplet.instance[1]: Refreshing state... [id=381837560]
data.aws_ami.ubuntu: Read complete after 0s [id=ami-08e2c1a8d17c2fe17]
aws_default_security_group.default: Refreshing state... [id=sg-06d079c63124325e2]
aws_instance.instance[1]: Refreshing state... [id=i-02936bd6bd18a8990]
aws_instance.instance[0]: Refreshing state... [id=i-0b369eca9f25fbfba]

No changes. Your infrastructure matches the configuration.

OpenTofu has compared your real infrastructure against your configuration and found no differences, so no changes are needed.

Apply complete! Resources: 0 added, 0 changed, 0 destroyed.
instance mck-k8s-aws-0 is provisioned on aws with address 34.216.64.59
instance mck-k8s-aws-1 is provisioned on aws with address 52.13.14.113
instance mck-k8s-do-0 is provisioned on digitalocean with address 157.230.185.177
instance mck-k8s-do-1 is provisioned on digitalocean with address 157.230.185.144
instance mck-k8s-linode-0 is provisioned on linode with address 172.232.26.204
instance mck-k8s-linode-1 is provisioned on linode with address 172.232.26.123
```

`--destroy` will remove all resources:

```
$ python3 mck --destroy
```
