
# installing Ubuntu 22.04 LTS (GNU/Linux 5.15.0-37-generic x86_64)

prerequisites

download https://ubuntu.com/download/server to a thumbdrive

install Ubuntu on the NUC and connect to local network.

installing some utility packages 

``` bash
#enabling ssh
leaver2000@nuc:~$ sudo apt update
leaver2000@nuc:~$ sudo apt install openssh-server net-tools
# verify
leaver2000@nuc:~$ sudo systemctl status ssh
# allow ssh connections
leaver2000@nuc:~$ sudo ufw allow ssh
# 
leaver2000@nuc:~$ ifconfig

# wlp1s0: flags=4163<UP,BROADCAST,RUNNING,MULTICAST>  mtu 1500
# ------> inet 192.xxx.x.xxx  netmask 255.255.255.0  broadcast 192.

```
from the localmachine


``` bash
leaver2000@inwin:~$ ssh leaver2000@192.xxx.x.xxx 
# Welcome to Ubuntu 22.04 LTS (GNU/Linux 5.15.0-37-generic x86_64)
```
from here I also did some `ssh-keygen` stuff to allow me to access the NUC without the use of a password each time.



## setting up nginx on the NUC


setting up a webserver on Intel NUC for access on my local network

``` bash
leaver2000@nuc:~$ sudo apt update
leaver2000@nuc:~$ sudo apt install nginx
leaver2000@nuc:~$ sudo ufw enable
leaver2000@nuc:~$ sudo ufw app list
# Output
# Available applications:
#   Nginx Full
#   Nginx HTTP
#   Nginx HTTPS
#   OpenSSH
leaver2000@nuc:~$ sudo ufw allow 'Nginx HTTP'
leaver2000@nuc:~$ sudo ufw status

# Output
# Status: active

# To                         Action      From
# --                         ------      ----
# OpenSSH                    ALLOW       Anywhere                  
# Nginx HTTP                 ALLOW       Anywhere                  
# OpenSSH (v6)               ALLOW       Anywhere (v6)             
# Nginx HTTP (v6)            ALLOW       Anywhere (v6)
```


from the local machine there is no service running on localhost

``` bash
leaver2000@inwin:~$ curl localhost
# curl: (7) Failed to connect to localhost port 80 after 0 ms: Connection refused
```

from the NUC

``` bash
leaver2000@nuc:~$ curl localhost
# <!DOCTYPE html>
# <html>
# <head>
# <title>Welcome to nginx!</title>
# <style>
#     body {
#         width: 35em;
#         margin: 0 auto;
#         font-family: Tahoma, Verdana, Arial, sans-serif;
#     }
# </style>
# </head>
# <body>
# <h1>Welcome to nginx!</h1>
# <p>If you see this page, the nginx web server is successfully installed and
# working. Further configuration is required.</p>

# <p>For online documentation and support please refer to
# <a href="http://nginx.org/">nginx.org</a>.<br/>
# Commercial support is available at
# <a href="http://nginx.com/">nginx.com</a>.</p>

# <p><em>Thank you for using nginx.</em></p>
# </body>
# </html>
```


back to the localmachine


``` bash
leaver2000@inwin:~/nuc-api$ curl 192.xxx.x.xxx 
# <!DOCTYPE html>
# <html>
# <head>
# <title>Welcome to nginx!</title>
# <style>
#     body {
#         width: 35em;
#         margin: 0 auto;
#         font-family: Tahoma, Verdana, Arial, sans-serif;
#     }
# </style>
# </head>
# <body>
# <h1>Welcome to nginx!</h1>
# <p>If you see this page, the nginx web server is successfully installed and
# working. Further configuration is required.</p>

# <p>For online documentation and support please refer to
# <a href="http://nginx.org/">nginx.org</a>.<br/>
# Commercial support is available at
# <a href="http://nginx.com/">nginx.com</a>.</p>

# <p><em>Thank you for using nginx.</em></p>
# </body>
# </html>

```



## nextsteps are to use nginx to reverse proxy http request to a docker container