import argparse
import subprocess
import os
import json


def run_cmd(cmd):
    err = subprocess.call(cmd, shell=True)
    if err != 0:
        raise RuntimeError("command `{}` failed".format(cmd))


def parse_instances():
    result = subprocess.run(["tofu", "show", "-json"], check=True, capture_output=True)
    state = json.loads(result.stdout)
    for i in state["values"]["root_module"]["resources"]:
        if i["address"] in "digitalocean_droplet.instance":
            print(i["values"]["ipv4_address"])


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
        parse_instances()
