import argparse
import subprocess
import os
import json
from jinja2 import Environment, FileSystemLoader

import ansible_runner

from models import Instance


def run_cmd(cmd):
    err = subprocess.call(cmd, shell=True)
    if err != 0:
        raise RuntimeError("command `{}` failed".format(cmd))


def parse_instances():
    # inspects tfstate, returns list of Instances
    instances = []
    tofushow = subprocess.run(
        ["tofu", "show", "-json"], check=True, capture_output=True
    )
    state = json.loads(tofushow.stdout)
    for i in state["values"]["root_module"]["resources"]:
        if "digitalocean_droplet" in i["address"]:
            inst = Instance(
                i["values"]["name"], "digitalocean", i["values"]["ipv4_address"]
            )
            instances.append(inst)
        elif "linode_instance" in i["address"]:
            inst = Instance(i["values"]["label"], "linode", i["values"]["ip_address"])
            instances.append(inst)
        elif "aws_instance" in i["address"]:
            inst = Instance(
                i["values"]["tags"]["Name"], "aws", i["values"]["public_ip"]
            )
            instances.append(inst)
    return instances


def configure(instances):
    # generates inventory and applies ansible role microk8s-ansible on instances
    env = Environment(loader=FileSystemLoader("templates"))

    template = env.get_template("inventory.j2")
    with open("inventory", "w") as inventory:
        inventory.truncate()
        inventory.write(template.render(instances=instances))

    ansible_runner.run(
        private_data_dir="./", inventory="inventory", playbook="main.yml"
    )

    print("environment created.  follow-up configuration can be performed with:")
    print("ansible-playbook main.yml -i inventory")


def reconcile_cluster(instances):
    # takes a list of Instances and ensures all have joined cluster
    for i in instances:
        i.get_peers()

    instances.sort(key=lambda x: len(x.peers), reverse=True)
    initiator = instances[0]

    # we've picked the node with the most peers as the initiator.
    # if the initiator itself has no peers, it must be that no cluster exists.
    # ( localhost counts as 1 peer )
    if len(initiator.peers) == 1:
        print("leader is {}".format(initiator.name))
        for i in instances[1:]:
            print("{} will join {}".format(i.name, initiator.name))
            i.join(initiator)
    else:
        # handle the case that a cluster exists but there are unjoined (new) instances
        print("existing cluster found with candidate leader {}".format(initiator.name))
        for i in instances:
            if len(i.peers) == 1:
                print("orphan node {} will join {}".format(i.name, initiator.name))
                i.join(initiator)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--destroy", "--cleanup", action="store_true")
    parser.add_argument("--skip-config", action="store_true")
    args = parser.parse_args()

    if "TF_VAR_do_token" not in os.environ:
        raise ValueError("Environment variable TF_VAR_do_token required")

    if args.destroy:
        run_cmd("tofu destroy --auto-approve")
    else:
        run_cmd("tofu apply --auto-approve")
        instances = parse_instances()
        for i in instances:
            print(
                "instance {} is provisioned on {} with address {}".format(
                    i.name, i.provider, i.ipv4
                )
            )

        if not args.skip_config:
            configure(instances)
        reconcile_cluster(instances)
