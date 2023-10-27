import argparse
import subprocess
import os
import json

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


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--destroy", "--cleanup", action="store_true")
    args = parser.parse_args()

    if "TF_VAR_do_token" not in os.environ:
        raise ValueError("Environment variable TF_VAR_do_token required")

    if args.destroy:
        run_cmd("tofu destroy")
    else:
        run_cmd("tofu apply")
        instances = parse_instances()
        for i in instances:
            print(
                "instance {} is provisioned on {} with address {}".format(
                    i.name, i.provider, i.ipv4
                )
            )
