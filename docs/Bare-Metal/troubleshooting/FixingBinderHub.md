# BinderHub: Failure to launch new servers and HTTPS Issues

## Problem
BinderHub was encountering failures on launching new 


## Solution

Uninstall BinderHub, reinstall BinderHub

Delete the cert-manager pod (cert-manager-xxxxxxxxx under the cert-manager namespace). It will recreate itself since it’s in a ReplicaSet.

Our deployment roughly follows this documentation on BinderHub: https://binderhub.readthedocs.io/en/latest/https.html#cert-manager-for-automatic-tls-certificate-provisioning

**Note:** While we roughly follow the BinderHub guidelines, we used an older form of documentation in which does not reflect our current configuration:
```
apiVersion: certmanager.k8s.io/v1alpha1
kind: ClusterIssuer
metadata:
   name: letsencrypt-production
   namespace: binderhub
 spec:
 acme:
     # You must replace this email address with your own.
     # Let's Encrypt will use this to contact you about expiring
     # certificates, and issues related to your account.
     email: <email>
     server: https://acme-v02.api.letsencrypt.org/directory
     privateKeySecretRef:
       # Secret resource used to store the account's private key.
       name: <something here>
     http01: {}

```


BinderHub utilizes the ACME certificate issuer, which issues TLS certificates. The issuer in the Kubernetes cluster comes in the form of Kubernetes resources called `Issuers` or `ClusterIssuers` (https://cert-manager.io/docs/concepts/issuer/), which are certificate authorities. An `Order` represents a request for a certificate. Each `Order` therefore creates an 
For more information on these Kubernetes types, visit here: https://cert-manager.io/docs/concepts/acme-orders-challenges/

Each certificate is based on a secret, generated for the certificate.

To check if your certificate/secret is generated, try running:
Kubectl get secret -A
NAMESPACE         NAME                                                       TYPE                                  DATA   AGE
binderhub         binder.libretexts.org-tls                                  kubernetes.io/tls                     3      122m

Kubectl get certificates -A

```
NAMESPACE      NAME                               READY   SECRET                             AGE
binderhub      binder.libretexts.org-tls          False    binder.libretexts.org-tls            9m
```
```
$ kubectl describe certificate binder.libretexts.org-tls -n binderhub
…
Status:
  Presented:   true
  Processing:  true
  Reason:      **Waiting for http-01 challenge propagation: wrong status code '404', expected '200'**
  State:       pending
Events:        <none>
```

In this case, the certificate manager could not generate the certificate because port 80 was closed. Port 80 must be open in order for the certificate manager to complete the challenge and verify that you own the domain and are requesting the certificate.

In our cluster, this is done by temporarily tweaking our nginx configuration.

Adding the following allows requests sent to `binder.libretexts.org` through port 80 to be forwarded to the ingress controller at `10.0.1.61`.
```
$ vim /etc/nginx/tcpconf.d/lb
  server {
      listen 128.120.136.56:80;
      proxy_pass 10.0.1.61:80;
    }
```

Commenting out the following disables the error that users usually receive when trying to access the site through port 80.
```
$ vim /etc/nginx/nginx.conf
 # server {
 #         listen 128.120.136.56:80;
 #   server_name binder.libretexts.org;
 #   return 301 https://$server_name$request_uri;
 # }
```

Run `sudo nginx -t` to check for linting errors, then `sudo systemctl restart nginx.service` to restart the nginx.

Wait for ~10-15 minutes for the certificate to generate! We switched our nginx configuration from a correct to incorrect setup, which made the troubleshooting a bit longer than it should have.



After a successful update, your certificate should now look like this:
```
Status:
  Conditions:
    Last Transition Time:  2020-04-07T05:35:09Z
    Message:               Certificate is up to date and has not expired
    Reason:                Ready
    Status:                True
    Type:                  Ready
  Not After:               2020-07-06T04:35:09Z
Events:                    <none>
```


Kubectl get pods 

The certificate manager comes in the form of an Issuer 

https://cert-manager.io/docs/faq/acme/
https://cert-manager.io/docs/configuration/acme/

