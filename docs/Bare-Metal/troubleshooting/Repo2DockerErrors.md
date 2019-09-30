# repo2docker Errors

## Problem
I had a lot of problems trying to get repo2docker installed. I also ended up with
a lot of Python permission errors.

A poorly formatted example of the error:

```
Error while fetching server API version: ('Connection aborted.', PermissionError(13, 'Permission denied'))
Error while fetching server API version: ('Connection aborted.', PermissionError                        
(13, 'Permission denied'))Traceback (most recent call last):File "/home/spicy/.local/lib/python3.6/site-packages/urllib3/connectionpool.py                        
", line 603, in urlopenchunked=chunked)File "/home/spicy/.local/lib/python3.6/site-packages/urllib3/connectionpool.py                        
", line 355, in _make_requestconn.request(method, url, **httplib_request_kw)File "/usr/lib/python3.6/http/client.py", line 1239, in requestself._send_request(method, url, body, headers, encode_chunked)
File "/usr/lib/python3.6/http/client.py", line 1285, 
in _send_requestself.endheaders(body, encode_chunked=encode_chunked)
File "/usr/lib/python3.6/http/client.py", line 1234, in endheadersself._send_output(message_body, encode_chunked=encode_chunked)File "/usr/lib/python3.6/http/client.py", line 1026, in _send_outputself.send(msg)
File "/usr/lib/python3.6/http/client.py", line 964, in sendself.connect()File "/home/spicy/.local/lib/python3.6/site-packages/docker/transport/unixconn.py", 
line 43, in connectsock.connect(self.unix_socket)PermissionError: [Errno 13] Permission denied
```

When trying to `docker push`, permission would always be denied.

## Solution
This solved the permission error:
```
$ sudo gpasswd -a $USER docker
$ newgrp docker
```

This solved the `docker push` permission error:
```
$ docker login docker.io
```
It will ask your username and password for your DockerHub account.

