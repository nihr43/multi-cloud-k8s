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
    result = subprocess.run(["tofu", "show", "-json"], check=True, capture_output=True)
    state = json.loads(result.stdout)
    for i in state["values"]["root_module"]["resources"]:
        if i["address"] in "digitalocean_droplet.instance":
            inst = Instance(
                i["values"]["name"], "digitalocean", i["values"]["ipv4_address"]
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
            print("instance {} is provisioned on {}".format(i.name, i.provider))
