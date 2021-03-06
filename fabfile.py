from fabric.api import *
import config as cfg

master_host = ['ubuntu@192.168.100.33']
nodes = [
    'ubuntu@192.168.100.34',
    'ubuntu@192.168.100.35'
    'ubuntu@192.168.100.36',
    'ubuntu@192.168.100.37'
]
all_hosts = master_host + nodes

env.hosts = all_hosts

env.password = cfg.secure['password']

@parallel
def cmd(command):
    sudo(command)

@parallel
def pi_ppa():
    cmd("yes | add-apt-repository ppa:ubuntu-raspi2/ppa")
    cmd("apt-get update")

@parallel
def nfs():
    sudo("yes | apt-get install nfs-common")

@parallel
def reboot():
    sudo("reboot now")


@parallel
def install_util():
    cmd("apt-get install stress")


@parallel
def stress():
    cmd("stress --cpu 4")


@parallel
def measure_temp():
    cmd("vcgencmd measure_temp")


@parallel
@hosts(nodes)
def make_k8s_node():
    pi_ppa()
    install_util()
    kubernetes_package_prepare()
    docker()
    kubernetes_tools()
    nfs()


@parallel
def kubernetes_package_prepare():
    cmd("curl -s https://packages.cloud.google.com/apt/doc/apt-key.gpg | apt-key add -")
    cmd("apt-add-repository 'deb http://apt.kubernetes.io/ kubernetes-xenial main'")

@parallel
@hosts(nodes)
def kubernetes_tools():
    cmd("yes | apt install kubeadm")


@hosts(nodes)
def docker():
    cmd("apt-get update")
    cmd("yes | apt install docker.io")
    cmd("systemctl enable docker")


@hosts(master_host)
def kubernetes_master():
    cmd("yes | kubeadm init --pod-network-cidr=10.244.0.0/16 --apiserver-advertise-address 10.0.0.1 --apiserver-cert-extra-sans kubernetes.cluster.home")
    run("mkdir -p $HOME/.kube")
    cmd("cp -i /etc/kubernetes/admin.conf $HOME/.kube/config")
    cmd("chown $(id -u):$(id -g) $HOME/.kube/config")

