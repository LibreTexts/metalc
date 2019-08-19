# HTTPS Errors on JupyterHub

## Problem
I wanted to start fresh on JupyterHub, so I deleted the namespace and reinstalled via helm.
However, when accessing JupyterHub on the Internet, I got this error:
```
Did Not Connect: Potential Security Issue

Websites prove their identity via certificates. Firefox does not trust this site because it uses a certificate that is not valid for jupyter.libretexts.org. The certificate is only valid for ingress.local.

Error code: MOZILLA_PKIX_ERROR_SELF_SIGNED_CERT
```

## Solution
First, JupyterHub needs port 80 open so it could create an SSL certificate.
Check the files in the `/etc/nginx` folder to make sure port 80 is open.

In `/etc/nginx/nginx.conf`, I had to comment this out, since it would return an error if you try
to access the website at port 80.
```
#       server {
#               listen 128.120.136.54:80;
#               server_name jupyter.libretexts.org;
#               return 301 https://$server_name$request_uri;
#       }

```

In `/etc/nginx/tcpconf.d/lb`, added this for a good measure.
```
        server {
                listen 128.120.136.54:80;
                proxy_pass 10.0.1.54:80;
        }
```

Make sure everything is working fine and restart nginx.
```
$ sudo nginx -t
nginx: the configuration file /etc/nginx/nginx.conf syntax is ok
nginx: configuration file /etc/nginx/nginx.conf test is successful
$ sudo systemctl restart nginx.service
```

Make sure that the `autohttps-<random-string>` pod from JupyterHub has been
restarted recently. If not, delete it (so it could recreate itself) or run a 
`helm upgrade` with the flag `--recreate-pods`.
```
$ kubectl get pods -n jhub
NAME                         READY   STATUS    RESTARTS   AGE
autohttps-<random-string>    2/2     Running   0          35m
$ kubectl delete pod autohttps-<random-string> -n jhub
```

JupyterHub should now be accessible, and you can now revert the nginx 
files to their previous states.
