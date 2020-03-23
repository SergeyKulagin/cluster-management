# overview
The cluster will be set up as following:
* master node will be connected to the router with Internet access via Wi-fi (wlan0 interface name).
The master node will have an ip address from the same subnet as the router.
Also the master node will be connected to a private network where the others nodes will be connected via Ethernet (eth0 interface) 
* the worker nodes will be connected to a private network via eth0

# process
1. List wi-fi interfaces on the master node and get the wi-fi interface name:
```
iwconfig
```
2. On the newer versions of Linux netplan is used to configure the network.
Here the setup for master node:
```yaml
  network:
  version: 2
  renderer: networkd
  wifis:
    wlan0:
      dhcp4: no
      dhcp6: no
      addresses: [192.168.100.33/24]
      gateway4: 192.168.100.1
      nameservers:
        addresses: [192.168.100.1, 8.8.8.8]
      access-points:
        "ZTE_2.4G_nqJTnR":
          password: "***"
  ethernets:
    eth0:
      addresses:
        - 10.0.0.1/24
      gateway4: 10.0.0.1
```
Here ``192.168.100.33`` is a static ip address in the router's network. 
``192.168.100.1`` is the ip of the router. We use this ip as one of the default DNS.

``10.0.0.1`` is the ip address of the master in the private network.

3. Set up the master node as a NAT server
- enable ip forwarding
- set up ip tables
```
iptables -t nat -A POSTROUTING -o wlan0 -j MASQUERADE
iptables -A FORWARD -i wlan0 -o eth0 -m state --state RELATED,ESTABLISHED -j ACCEPT
iptables -A FORWARD -i eth0 -o wlan0 -j ACCEPT
```


