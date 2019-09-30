# Persistent Volumes
## Resources
* [Kubernetes documentation](https://kubernetes.io/docs/concepts/storage/persistent-volumes/)

## About
* **Persistent volume** (PV) - storage in cluster that is either provisioned by
the administrator or dynamically
* **Persistent volume claim** (PVC) - request for storage by the user. It's
analogous to a pod, in which pods consume node resources like persistent volume
claims consume persistent volume resources.

We have persistent volume claims to store each user's notebooks so they could
be accessed later.

The master node looks for new PVCs, then finds a matching PV if possible, then
binds the PVC and PV together. It's a one-to-one mapping.

If you delete a PVC while in active use by a pod, then PVC removal is delayed.
IF you delete a PV bound to a PVC, then PV removal is delayed until the PV is
not bound to a PVC.

To delete a PVC, I think this is a good rough outline:
1. Delete the pod (note that the pod could regenerate depending on its settings): `kubectl delete pod <pod name>`
1. Delete the PVC: `kubectl delete pvc <pvc name>`. This will release the persistent volume. 
If you run `kubectl get pv -A`, you will see that the PV that was initially bound to the PVC
will be marked as `Released`.
1. Delete the PV (if you want to): `kubectl delete pv <pv name>`. I don't think it's
necessary though if it's already released.
