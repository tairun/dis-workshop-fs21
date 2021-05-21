#!/bin/env python3

from shutil import which

def has_tool(name):
    """Check whether `name` is on PATH and marked as executable."""
   
    return which(name) is not None


if __name__ == "__main__":

    virt_base_name = "aerospike-swarm-"
    swarm_cpus = 1
    swarm_size = 4
    swarm_mem = "1G"

    print(has_tool("multipass"))