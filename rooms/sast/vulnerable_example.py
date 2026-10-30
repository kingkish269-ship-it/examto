"""A small vulnerable script for the SAST room. Do not fix it — scan it."""

import subprocess


def ping_host(host):
    # The host comes from a user. It is placed straight into a shell command.
    return subprocess.run("ping -c1 " + host, shell=True, capture_output=True, text=True)
