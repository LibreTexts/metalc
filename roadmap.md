# Cluster Roadmap

- get the software downloaded on the nodes
  - maybe just keep this as like an ansible script

- get network fabric in place

- set Storage Class provisioner to dynamically provision persistent volumes

  - this will change for the different deployments to allow for more or less
    persistence and also how much data people get.

- configure HA masters

- create a helm chart to...
  - install the dynamic nfs volume provisioner
  - install MetalLB

- an ingress to expose the cluster..
  - it looks like jupyterhub helm already has something and we just need to
    customize the values we pass in.

  - metallb!   https://metallb.universe.tf
    - I think we will need this.
    - plus it makes the whole cluster just way more useable if we want to have
      multiple clusters going at the same time. Like jhub and binderhub
    see this too:
      https://kubernetes.github.io/ingress-nginx/deploy/baremetal/

- configure monitoring of the cluster somehow
  - collect data on:
    - load times
    - which images are being used
    - cpu, memory, and data usage. Per user also.
    - also, all the kubernetes stuff, like pods per node and stuff.

- testing!
  
  - need an automated testing framework where we can put in tests so it
    simulates a bunch of users.
    maybe like this:
    https://httpd.apache.org/docs/2.4/programs/ab.html
    but we need to do more complicated things, like have the clients run
    programs or make graphs

  - also test stuff by bringing down nodes and seeing how the cluster responds
