from fabric.api import *
import config as cfg

env.hosts = [
    'ubuntu@192.168.100.3',
    'ubuntu@192.168.100.4',
    'ubuntu@192.168.100.5'
]

env.password = cfg.secure['password']

@parallel
def cmd(command):
    sudo(command)


def pi_ppa():
    cmd("add-apt-repository ppa:ubuntu-raspi2/ppa")
    cmd("apt-get update")

def stress():
    cmd("stress --cpu 4")

def measure_temp():
    cmd("vcgencmd measure_temp")
