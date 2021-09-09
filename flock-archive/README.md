# Flock Archive

This entire directory and its contents can be regarded as out of date. 
Flock was the title of the previously deployed cluster. 

## Ansible ([ansible/](ansible/))

Ansible is an open-source software provisioning, configuration management, and 
application-deployment tool enabling infrastructure as code.<sup>[\[1\]](https://en.wikipedia.org/wiki/Ansible_(software))</sup>
`ansible/` contains configuration files.

## Test Kubernetes Environment ([dev-env/](dev-env/))

The `dev-env/` directory contains files and instructions for implementing a test
cluser of VMs using vagrant. This was useful for testing purposes without using the main cluster.

## Baremetal ([baremetal.md](baremetal.md))

`baremetal.md` is a large master document detailing nearly 
everything necessary for setting up and working on the old flock cluster.
This includes an overview of networking, publishing services, 
instructions on adding nodes, and useful resources.