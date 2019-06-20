# Introduction
This document discusses the terms we need to know about load balancer and how to set up load balancer in google cloud engine.
This document is divided into three sections: 
1. Load Balancing in General
2. How to Set Up Load Balancing in Google Cloud Engine
3. Additional Knowledge About Load Balancing 

# Load Balancing in General
## Load Balancer
A load balancer is a device that acts as a reverse proxy and distributes network or application traffic across a number of servers. Load balancers are used to increase capacity (concurrent users) and reliability of applications. They improve the overall performance of applications by decreasing the burden on servers associated with managing and maintaining application and network sessions, as well as by performing application-specific tasks.<br>

## Ingress
Ingress exposes HTTP and HTTPS routes from outside the cluster to services within the cluster. Traffic routing is controlled by rules defined on the Ingress resource. <br>
Read more at [page](https://kubernetes.io/docs/concepts/services-networking/ingress/#terminology)

## SSl termination/offloading
To help offset the extra burden SSL/TLS adds, you can spin up separate Application-Specific Integrated Circuit (ASIC) processers that are limited to just performing the functions required for SSL/TLS, namely the handshake and the encryption/decryption. This frees up processing power for the intended application or website. That’s SSL offloading in a nutshell. Sometimes it’s also called load balancing. You may hear the term load balancer tossed around. A load balancer is any device that helps improve the distribution of workloads across multiple resources, for instance distributing the SSL/TLS workload to ASIC processors.<br>
Read more at [page](https://www.thesslstore.com/blog/ssl-offloading-bridging-termination/)

## Difference between LoadBalancers and Ingress
### Load Balancer
A kubernetes LoadBalancer service is a service that points to external load balancers that are NOT in your kubernetes cluster, but exist elsewhere. They can work with your pods, assuming that your pods are externally routable. <br>

### Ingress
An ingress is really just a set of rules to pass to a controller that is listening for them. You can deploy a bunch of ingress rules, but nothing will happen unless you have a controller that can process them. A LoadBalancer service could listen for ingress rules, if it is configured to do so. An Ingress Controller is simply a pod that is configured to interpret ingress rules. One of the most popular ingress controllers supported by kubernetes is nginx.<br>

Read more at [page](https://stackoverflow.com/questions/45079988/ingress-vs-load-balancer) and [page1](https://medium.com/google-cloud/kubernetes-nodeport-vs-loadbalancer-vs-ingress-when-should-i-use-what-922f010849e0)

# How to Set Up Load Balancing in Google Cloud Engine
There are different types of load balancer to use in google cloud, you can find the type of load balancing you want in this [page](https://cloud.google.com/load-balancing/docs/choosing-load-balancer). For HTTP(S) traffic, HTTP(S) load balancing is recommended instead. <br>
Follow the instructions in this [page](https://cloud.google.com/load-balancing/docs/https/setting-up-https), you can set up load balancer in your server. [Here](https://www.youtube.com/watch?v=FtLhVvSFi84) is a Vedio tutorial that can guide you through the process roughly. 
## Optional Load Balancing Set Up 
We can set auto scaling along with load balancing to easily control our VMs.
### Google cloud load balancer & autoscaling 
Autoscaler is set to monitor virtual machines and virtual machines in that group to make sure that it has not exceeded the 70% CPU. If the CPU in this instance shoots more than 70% , then the autoscaler should spin more instances and then when it comebacks below 70%, it should delete those VMs. [Here](https://www.youtube.com/watch?v=Gn7pGQYkKnA&t=230s) is a vedio that provides specific instructions. 

# Additional Knowledge About Load Balancing
Below are some terminologies that I encountered when I set up load balancing. 
## Target proxies
Target proxies are referenced by one or more forwarding rules. In the case of HTTP(S) load balancing, proxies route incoming requests to a URL map. In the case of SSL proxy and TCP proxy load balancing, target proxies route incoming requests directly to backend services. <br>
Read more on [page](https://cloud.google.com/load-balancing/docs/target-proxies)

## IPv4 & IPv6
### IPv4
IPv4 stands for Internet Protocol version 4. It is the underlying technology that makes it possible for us to connect our devices to the web. Whenever a device access the Internet (whether it's a PC, Mac, smartphone or other device), it is assigned a unique, numerical IP address such as 99.48.227.227. To send data from one computer to another through the web, a data packet must be transferred across the network containing the IP addresses of both devices.
Without IP addresses, computers would not be able to communicate and send data to each other. It's essential to the infrastructure of the web.
### IPv6
IPv6 is the sixth revision to the Internet Protocol and the successor to IPv4. It functions similarly to IPv4 in that it provides the unique, numerical IP addresses necessary for Internet-enabled devices to communicate. However, it does sport one major difference: it utilizes 128-bit addresses. I'll explain why this is important in a moment. <br>
Read more on [page](https://mashable.com/2011/02/03/ipv4-ipv6-guide/)

## Instance group
An instance group is a collection of VM instances that you can manage as a single entity.

## Instance templates
An instance template is a resource that you can use to create VM instances and managed instance groups.
Instance templates define the machine type, boot disk image or container image, labels, and other instance properties. You can then use an instance template to create a managed instance group or to create individual VM instances.



