# multi-cloud-k8s

This is an exercise in provisioning a kubernetes cluster across multiple cloud providers.  Whether such an endeavor is practical or worthwhile IRL is up for debate; this was done for fun.

## usage

The cluster is defined in `instances.tf`.

The default action is to enforce state.  `python3 mck`:

```
$ export TF_VAR_do_token=
$ export TF_VAR_linode_token=
# export TF_VAR_aws_access=
$ export TF_VAR_aws_secret=
$
$ python3 mck
linode_sshkey.default: Refreshing state...
digitalocean_ssh_key.default: Refreshing state... [id=39818938]
linode_instance.instance[0]: Refreshing state... [id=51380107]
linode_instance.instance[1]: Refreshing state... [id=51380422]
data.aws_ami.image: Reading...
aws_key_pair.default: Refreshing state... [id=opentofu]
aws_default_vpc.mainvpc: Refreshing state... [id=vpc-0371ba1712735e722]
aws_default_subnet.default_az1: Refreshing state... [id=subnet-046b3f303365c3333]
digitalocean_droplet.instance[0]: Refreshing state... [id=382118243]
data.aws_ami.image: Read complete after 1s [id=ami-0c2644caf041bb6de]
aws_default_security_group.default: Refreshing state... [id=sg-06d079c63124325e2]

OpenTofu used the selected providers to generate the following execution plan. Resource actions are indicated with the following symbols:
  + create

OpenTofu will perform the following actions:

( tf diff tuncated)

Plan: 3 to add, 0 to change, 0 to destroy.
linode_instance.instance[2]: Creating...
digitalocean_droplet.instance[1]: Creating...
digitalocean_droplet.instance[2]: Creating...
linode_instance.instance[2]: Still creating... [10s elapsed]
digitalocean_droplet.instance[2]: Still creating... [10s elapsed]
digitalocean_droplet.instance[1]: Still creating... [10s elapsed]
linode_instance.instance[2]: Still creating... [20s elapsed]
digitalocean_droplet.instance[1]: Still creating... [20s elapsed]
digitalocean_droplet.instance[2]: Still creating... [20s elapsed]
linode_instance.instance[2]: Still creating... [30s elapsed]
digitalocean_droplet.instance[1]: Still creating... [30s elapsed]
digitalocean_droplet.instance[2]: Still creating... [30s elapsed]
digitalocean_droplet.instance[1]: Creation complete after 30s [id=382122787]
digitalocean_droplet.instance[2]: Creation complete after 31s [id=382122788]
linode_instance.instance[2]: Creation complete after 37s [id=51380582]

Apply complete! Resources: 3 added, 0 changed, 0 destroyed.
instance mck-k8s-do-0 is provisioned on digitalocean with address 206.189.192.42
instance mck-k8s-do-1 is provisioned on digitalocean with address 192.34.61.217
instance mck-k8s-do-2 is provisioned on digitalocean with address 161.35.124.62
instance mck-k8s-linode-0 is provisioned on linode with address 172.232.11.165
instance mck-k8s-linode-1 is provisioned on linode with address 172.234.25.201
instance mck-k8s-linode-2 is provisioned on linode with address 172.233.215.206

PLAY [common] ******************************************************************

( truncated )

PLAY RECAP *********************************************************************
161.35.124.62              : ok=14   changed=11   unreachable=0    failed=0    skipped=4    rescued=0    ignored=0
172.232.11.165             : ok=12   changed=1    unreachable=0    failed=0    skipped=4    rescued=0    ignored=0
172.233.215.206            : ok=14   changed=12   unreachable=0    failed=0    skipped=4    rescued=0    ignored=0
172.234.25.201             : ok=12   changed=1    unreachable=0    failed=0    skipped=4    rescued=0    ignored=0
192.34.61.217              : ok=14   changed=11   unreachable=0    failed=0    skipped=4    rescued=0    ignored=0
206.189.192.42             : ok=12   changed=1    unreachable=0    failed=0    skipped=4    rescued=0    ignored=0
environment created.  follow-up configuration can be performed with:
ansible-playbook main.yml -i inventory
existing cluster found with candidate leader mck-k8s-do-0
orphan node mck-k8s-do-1 will join mck-k8s-do-0
Contacting cluster at 206.189.192.42
Waiting for this node to finish joining the cluster. .. .. .. ..
orphan node mck-k8s-do-2 will join mck-k8s-do-0
Contacting cluster at 206.189.192.42
Waiting for this node to finish joining the cluster. .. .. .. ..
orphan node mck-k8s-linode-2 will join mck-k8s-do-0
Contacting cluster at 206.189.192.42
Waiting for this node to finish joining the cluster. .. .. .. ..
```

```
root@mck-k8s-do-0:~# kubectl get nodes
NAME               STATUS   ROLES    AGE   VERSION
mck-k8s-linode-0   Ready    <none>   34m   v1.28.2
mck-k8s-linode-1   Ready    <none>   17m   v1.28.2
mck-k8s-do-1       Ready    <none>   91s   v1.28.2
mck-k8s-do-2       Ready    <none>   69s   v1.28.2
mck-k8s-do-0       Ready    <none>   38m   v1.28.2
mck-k8s-linode-2   Ready    <none>   19s   v1.28.2
```

`--destroy` will remove all resources:

```
$ python3 mck --destroy
```

## implementation

`mck` wraps opentofu (formerly terraform) and ansible in python, enabling a single commandline entrypoint for various CRUD tasks.  There is zero manual work other than initial API token setup for each provider.

Wrapping opentofu rather than using client libraries directly gives us a well-proven means of provisioning base resources, as well as a well understood user interface - the cluster is described in `intances.tf`.

Once compute resources are provisioned, the tf state is examined and an ansible inventory is generated.  Base software installation is then performed with [ansible_runner](https://ansible.readthedocs.io/projects/runner/en/stable/).

Once instances are provisioned, the status of each node is inspected to determine which nodes need to join the cluster.  If no instances have peers, the cluster is bootstrapped.  If individual instances are found with no peers, they join the leader who has the most peers.

This allows us to provision a cluster, add nodes in `instances.yml`, and run the tool again - resulting in new instances being provisioned and added to the cluster.  Here `mck-k8s-linode-1` is being added o an existing cluster of two:

```
PLAY RECAP *********************************************************************
172.232.11.165             : ok=12   changed=1    unreachable=0    failed=0    skipped=4    rescued=0    ignored=0
172.234.25.201             : ok=14   changed=12   unreachable=0    failed=0    skipped=4    rescued=0    ignored=0
206.189.192.42             : ok=12   changed=1    unreachable=0    failed=0    skipped=4    rescued=0    ignored=0
environment created.  follow-up configuration can be performed with:
ansible-playbook main.yml -i inventory
existing cluster found with candidate leader mck-k8s-do-0
orphan node mck-k8s-linode-1 will join mck-k8s-do-0
Contacting cluster at 206.189.192.42
Waiting for this node to finish joining the cluster. .. .. .. ..
```

Why not use the terraform provisioner feature?  Rather than having tofu configure nodes in isolation, waiting until all the nodes have been provisioned lets us genereate a full inventory file.  The tool spits out a command hint `ansible-playbook main.yml -i inventory`, which we're free to use directly if we ever want to make small changes without reprovisioning the cluster.  We're also templating `/etc/hosts` with ansible, which needs to be updated whenever the infrastructure changes.

## todo

Enable calico's built-in wireguard capability for inter-node encryption.

Resolve issues with aws nat.  microk8s expects public ip to be locally bound.
