# ☸️ Kubernetes NodeSelector ensurer
`k8s-nodeselector-ensurer` is a watcher whose role is to ensure that all
the pods running on the kubernetes cluster adhere to their `nodeSelector` label list.

That is, when a node stops offering a particular label (e.g. `foo=bar`) that a pod
needs, `k8s-nodeselector-ensurer` will detect this and thus kill the aforementionned pod.

# Example
```bash
$ kubectl apply -f nodeselector-ensurer.yml
deployment.apps/nodeselector-ensurer created

$ kubectl apply -f example.yml 
deployment.apps/test-nodeselector created

$ kl get pod -l name=test-nodeselector
NAME                                 READY   STATUS    RESTARTS   AGE
test-nodeselector-5c68758d5f-9dhlw   0/1     Pending   0          3s

$ kl label node node-c24v-2 foo=bar
node/node-c24v-2 labeled

$ kl get pod -l name=test-nodeselector
NAME                                 READY   STATUS    RESTARTS   AGE
test-nodeselector-5c68758d5f-9dhlw   1/1     Running   0          28s

$ kl label node node-c24v-2 foo=notbar --overwrite
node/node-c24v-2 labeled

$ kl get pod -l name=test-nodeselector
NAME                                 READY   STATUS    RESTARTS   AGE
test-nodeselector-5c68758d5f-287sj   0/1     Pending   0          88s
```



# How to use it ❓
First of all, this is a POC, so don't use it. But if you still want to, follow these steps:

## Installation
To install this watcher, simply `kubectl apply -f nodeselector-ensurer.yml`

## Pod usage
By default, this watcher does not change the existing nodeSelector logic.

In order to mark pods as being killable when their `nodeSelector` no longer matches their node's,
just annote the pods with `frankkkkk.nodeSelectorDuringExecution: "true"`



# Why this watcher ⁉️
Kubernetes plans on offering the extra `requiredDuringSchedulingRequiredDuringExecution` affinity type.
However it is still (as of k8s 1.18) still not implemented in the node scheduler 😞.

At first I wanted the watcher to implement this feature, however the Pod resource definition is
not customizable.

