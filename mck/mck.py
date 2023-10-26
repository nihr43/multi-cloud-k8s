import argparse
import subprocess


def tofu_apply():
    cmd = "tofu apply"
    err = subprocess.call(cmd, shell=True)
    print("returned value:", err)


def tofu_destroy():
    cmd = "tofu destroy"
    err = subprocess.call(cmd, shell=True)
    print("returned value:", err)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--destroy", action="store_true")
    args = parser.parse_args()

    if args.destroy:
        tofu_destroy()
    else:
        tofu_apply()
