### Node status: NotReady
- check the nodes logs: ``kubectl describe node <node_name>``  
Here you can see node related information including different conditions of the node:
```commandline
Conditions:
  Type                 Status  LastHeartbeatTime                 LastTransitionTime                Reason                       Message
  ----                 ------  -----------------                 ------------------                ------                       -------
  NetworkUnavailable   False   Sat, 25 Apr 2020 12:29:32 +0300   Sat, 25 Apr 2020 12:29:32 +0300   FlannelIsUp                  Flannel is running on this node
  MemoryPressure       False   Sat, 25 Apr 2020 12:29:55 +0300   Sun, 19 Apr 2020 21:53:15 +0300   KubeletHasSufficientMemory   kubelet has sufficient memory available
  DiskPressure         False   Sat, 25 Apr 2020 12:29:55 +0300   Sun, 19 Apr 2020 21:53:15 +0300   KubeletHasNoDiskPressure     kubelet has no disk pressure
  PIDPressure          False   Sat, 25 Apr 2020 12:29:55 +0300   Sun, 19 Apr 2020 21:53:15 +0300   KubeletHasSufficientPID      kubelet has sufficient PID available
  Ready                True    Sat, 25 Apr 2020 12:29:55 +0300   Sat, 25 Apr 2020 12:29:35 +0300   KubeletReady                 kubelet is posting ready status. AppArmor enable
```
If you have some problem it's likely you can see it here and reason of it in Reason columns.

- for the further investigations you can ssh to the node check the it from inside.

### Cluster networking
```journalctl -u kubelet -S "2020-04-25 00:00:00" | grep kube-proxy``` to analyze logs of the kube-proxy

### Others (todo)

find docker container pid
```
docker inspect --format '{{ .State.Pid }}' container-id-or-name

```
```nsenter -t ${PID} -n ip addr```


```sudo iptables -t nat -nL```


```kubectl exec -ti dnsutils -- nslookup kubernetes.default```

### Master certificate expiration
```
cd /etc/kubernetes/pki/
mv {apiserver.crt,apiserver-etcd-client.key,apiserver-kubelet-client.crt,front-proxy-ca.crt,front-proxy-client.crt,front-proxy-client.key,front-proxy-ca.key,apiserver-kubelet-client.key,apiserver.key,apiserver-etcd-client.crt} ~/
kubeadm init phase certs all --apiserver-advertise-address <IP>
cd /etc/kubernetes/
mv {admin.conf,controller-manager.conf,kubelet.conf,scheduler.conf} ~/
kubeadm init phase kubeconfig all
reboot
```
and copy new admin config
