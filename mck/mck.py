import argparse
import subprocess
import os


def run_cmd(cmd):
    err = subprocess.call(cmd, shell=True)
    if err != 0:
        raise RuntimeError("command `{}` failed".format(cmd))


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--destroy", action="store_true")
    args = parser.parse_args()

    if "TF_VAR_do_token" not in os.environ:
        raise ValueError("Environment variable TF_VAR_do_token required")

    if args.destroy:
        run_cmd("tofu destroy")
    else:
        run_cmd("tofu apply")
