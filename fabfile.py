from fabric.api import *
import config as cfg

env.hosts = [
    'ubuntu@192.168.100.4',
    'ubuntu@192.168.100.6',
    'ubuntu@192.168.100.7'
]

env.password = cfg.secure['password']

@parallel
def cmd(command):
    sudo(command)

@parallel
def pi_ppa():
    cmd("add-apt-repository ppa:ubuntu-raspi2/ppa")
    cmd("apt-get update")

@parallel
def install_util():
    cmd("apt-get install stress")

@parallel
def stress():
    cmd("stress --cpu 4")

def measure_temp():
    cmd("vcgencmd measure_temp")
