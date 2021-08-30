# Z2JH serving HTTP on port 443

## Problem

Recently, after upgrading from Z2JH `0.9.0-n036.hfcf9c2e` to `0.9.0` in our staging namespace, our staging Z2JH is inaccessible via HTTPS. If you go to the website, the browser says "This site can’t provide a secure connection" with an ERR_SSL_PROTOCOL_ERROR. Curl also shows a similar error `curl: (35) error:14094438:SSL routines:ssl3_read_bytes:tlsv1 alert internal error`. This is because for some reason port 443 is not talking TLS at all, and is in fact talking HTTP:
```
rkevin@redshift:~$ curl -v http://staging.jupyter.libretexts.org:443
*   Trying 128.120.136.61:443...
* Connected to staging.jupyter.libretexts.org (128.120.136.61) port 443 (#0)
> GET / HTTP/1.1
> Host: staging.jupyter.libretexts.org:443
> User-Agent: curl/7.70.0
> Accept: */*
> 
* Mark bundle as not supporting multiuse
< HTTP/1.1 404 Not Found
< Content-Type: text/plain; charset=utf-8
< X-Content-Type-Options: nosniff
< Date: Tue, 23 Jun 2020 22:09:26 GMT
< Content-Length: 19
< 
404 page not found
* Connection #0 to host staging.jupyter.libretexts.org left intact
```

In the latest Z2JH, the helm chart uses Traefik for HTTPS termination, and the deployment is called `autohttps`. Traefik is the one with the service of type LoadBalancer, and it handles HTTPS and proxies the request back to proxy-public.
This issue also occurs if I `kubectl exec` into the Traefik pod and `wget -O- https://localhost`, and if I access `http://proxy-http:8000/` in the Traefik pod I don't get the 404, so the issue seems to be Traefik itself and not the nginx proxying that lead up to it or the CHP (Configurable-HTTP-Proxy, the proxy that Z2JH uses before Traefik).

Side note, I got derailed after this point. After digging into the Z2JH helm chart, it seems impossible that the ConfigMap `traefik-proxy-config` had .toml files inside rather than yaml. It should've been removed back in April in [this commit](https://github.com/jupyterhub/zero-to-jupyterhub-k8s/commit/441b0985b57da3451fb901758f753de434c79da5), but for some reason even after deleting it and doing a `helm upgrade`, the configmap is still regenerated with toml files. Another thing that confused me is that in the toml file there is `[log] level = "INFO"`, even though the yaml file clearly says this should be either DEBUG or WARN based on if a debug flag is set. That's when I realized I was looking at the `master` branch, not the `v0.9.0` branch, of the Z2JH repo. I also spent a ridiculously long time reading Traefik documentation, which is cool (I think it might actually be a good idea for our cluster to have one Traefik instance that exposes port 80 and 443 directly, rather than using nginx outside the cluster as a proxy, but that's something to look into another day) but didn't help the problem. There goes a couple hours of work.

To debug Traefik, I grabbed the Traefik configuration by using `kubectl get -n staging-jhub configmaps traefik-proxy-config -o yaml > traefix.yaml`, edited the config by hand and applied it by doing `kubectl replace -f traefix.yaml` (and yes, that pun is glorious, you're welcome). I first enabled debug logging by changing the log level to "DEBUG", and this came up when an HTTPS request is sent to port 443:

```
time="2020-06-23T23:35:03Z" level=debug msg="http: TLS handshake error from 10.0.0.111:45894: strict SNI enabled - No certificate found for domain: \"staging.jupyter.libretexts.org\", closing connection"
```

This explains our issue! Traefik is supposed to get an HTTPS certificate, but when the certificate is not present, we can't offer a valid cert for incoming connections. Since strict SNI is enabled (apparantly one of the "[nice TLS defaults](https://github.com/jupyterhub/zero-to-jupyterhub-k8s/blob/5fd3f0d10cb3ac88c9bc34f37f4b0d7103e790ab/jupyterhub/templates/proxy/autohttps/configmap.yaml#L68)" that Z2JH ships), we can't offer a certificate so Traefik doesn't even try to establish an HTTPS connection. That route fails, and with no other routes for the port 443 entrypoint Traefik just gives out a generic HTTP 404 message, explaining why we were having plain HTTP on port 443. Sure enough, changing the config to `sniStrict = false` fixed that issue, and we get a invalid certificate error in the browser instead. At least one issue is fixed!

All of this doesn't explain why the LetsEncrpyt certificate provisioning failed. The error message before was LetsEncrypt complaining about TLS issues (since why would anyone talk HTTP on port 443), but now that's fixed we get a different error:

```
time="2020-06-23T23:39:14Z" level=error msg="Unable to obtain ACME certificate for domains \"staging.jupyter.libretexts.org\" : unable to generate a certificate for the domains [staging.jupyter.libretexts.org]: error: one or more domains had a problem:\n[staging.jupyter.libretexts.org] acme: error: 403 :: urn:ietf:params:acme:error:unauthorized :: Invalid response from https://staging.jupyter.libretexts.org/hub/.well-known/acme-challenge/MYPYmO0OjLlrBNQf9hhsoLZOLMRA5-90qomj4UPqbs0 [128.120.136.61]: \"\\n\\n\\n<!DOCTYPE HTML>\\n<html>\\n\\n<head>\\n    <meta charset=\\\"utf-8\\\">\\n\\n    <title>JupyterHub</title>\\n    <meta http-equiv=\\\"X-UA-Compatibl\", url: \n" providerName=le.acme
```

It seems like Traefik is proxying the request back to `proxy-public` from Z2JH. Surely Traefik isn't stupid enough to not proxy `.well-known/acme-challenge` requests to itself for certificate issuing? (Spoiler alert: it isn't, and it took a bit of time to verify but that's not the issue). The last piece of the puzzle popped in when I took another long look at curl's request to port 80:

```
rkevin@redshift:~$ curl staging.jupyter.libretexts.org
<html>
<head><title>301 Moved Permanently</title></head>
<body bgcolor="white">
<center><h1>301 Moved Permanently</h1></center>
<hr><center>nginx/1.14.0 (Ubuntu)</center>
</body>
</html>
```

Port 80 is redirecting users to HTTPS (as it should), but the thing that's doing the redirecting is `nginx/1.14.0 (Ubuntu)`! The pods shouldn't know what distro they're on, so this has to be running on rooster somehow. I knew rooster used nginx to proxy requests, but this drove me to look at the configuration for nginx, and sure enough:

```
server {
	listen 128.120.136.61:80;
	server_name staging.jupyter.libretexts.org;
	return 301 https://$server_name$request_uri;
}
```

That's the issue! Traefik is serving the ACME challenge on port 80 only, but port 80 is never actually exposed to the public. HTTP traffic to that domain is rerouted to HTTPS by nginx before it even reaches Traefik.

## Solution

I made an ugly fix by removing the automatic 301 redirect in `nginx.conf`, adding a new `staging-jhub-insecure` upstream that goes to Traefik port 80, and adding a new `server` block to proxy_pass traffic from port 80 to Traefik. This isn't a security issue since Traefik is going to redirect everyone to HTTPS anyway, except for the very occasional time when it's trying to grab new certificates.

In the long run, we should also do this to the other domains we have, or remove `nginx` entirely and make a new Traefik "ingress" that handles all requests and expose its port 80 and 443 directly to the public. We might consider this for the new cluster.
