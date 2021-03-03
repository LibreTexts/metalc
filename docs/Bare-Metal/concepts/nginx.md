# NGINX

NOTE: This file is outdated for the [current galaxy cluster](https://github.com/LibreTexts/galaxy-control-repo/tree/production/router-configs).

*Relevant files: `/etc/nginx`*
*Summary: http://nginx.org/en/docs/http/load_balancing.html*

## Table of Contents
1. [About NGINX](#about-nginx)
1. [Configuring NGINX](#configuring-nginx)


## About NGINX

Rooster serves as a [reverse proxy](https://www.nginx.com/resources/glossary/reverse-proxy-server/) and load balancer,
meaning that we redirect clients to the appropriate backend
"server". 

<a title="Alextalker / CC BY-SA (https://creativecommons.org/licenses/by-sa/4.0)" href="https://commons.wikimedia.org/wiki/File:Reverse_Proxy.png"><img width="512" alt="Reverse Proxy" src="https://upload.wikimedia.org/wikipedia/commons/a/af/Reverse_Proxy.png"></a>

<a href="https://commons.wikimedia.org/wiki/File:Reverse_Proxy.png" title="via Wikimedia Commons">Alextalker</a> / <a href="https://creativecommons.org/licenses/by-sa/4.0">CC BY-SA</a>

We do this by telling NGINX which IP addresses and domain names of the 
client request to listen to and which "backend servers" to redirect their
requests to.
For us, the "backend server" is actually a service on the Kubernetes
cluster referring to a deployment.

Our NGINX configuration is based on the files `/etc/nginx/nginx.conf` and 
`/etc/nginx/tcpconf.d/lb`. In those files, you can see a format that looks
similar to this: 

```
stream {
    upstream jupyterhub {
        server <External-IP>:443;
    }

    server {
        listen <JupyterHub-IP>:443;
        ssl_preread on;
        proxy_pass jupyterhub;
    }
}
```

If you run `kubectl get svc -A`, you will see that the `EXTERNAL-IP` 
matches that of the `hub` service under the `jhub` namespace. This pattern 
follows for the other deployments we have.

You may also see something like this, which 
[redirects the IP to the specified server name](https://en.wikipedia.org/wiki/HTTP_301).

```
http {
  ##
  # Basic Settings
  ##

  server {
    listen <JupyterHub-IP>:80;
    server_name jupyter.libretexts.org;
    return 301 https://$server_name$request_uri;
  }
```

## Configuring NGINX
To modify the NGINX configuration, make your changes to the files 
`/etc/nginx/nginx.conf` and/or `/etc/nginx/tcpconf.d/lb`.

Run `sudo nginx -t` to test that your syntax is correct.

Then, run `sudo systemctl restart nginx`. 

> **Note:** Restart NGINX carefully, 
preferably when there are not a lot of users on the cluster. If your
NGINX configuration happens to fail, then users will experience some 
downtime. The `/etc/nginx` is under the private configuration repo,
so if you make a mistake, you can roll the file back to the previous 
commit.

Make sure that you commit and push your NGINX configuration changes.
