
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
# docker0: flags=4099<UP,BROADCAST,MULTICAST>  mtu 1500
#         inet 172.17.0.1  netmask 255.255.0.0  broadcast 172.17.255.255
#         ether 02:42:27:07:f0:83  txqueuelen 0  (Ethernet)
#         RX packets 0  bytes 0 (0.0 B)
#         RX errors 0  dropped 0  overruns 0  frame 0
#         TX packets 0  bytes 0 (0.0 B)
#         TX errors 0  dropped 0 overruns 0  carrier 0  collisions 0

# eno1: flags=4099<UP,BROADCAST,MULTICAST>  mtu 1500
#         ether d4:5d:df:13:72:04  txqueuelen 1000  (Ethernet)
#         RX packets 0  bytes 0 (0.0 B)
#         RX errors 0  dropped 0  overruns 0  frame 0
#         TX packets 0  bytes 0 (0.0 B)
#         TX errors 0  dropped 0 overruns 0  carrier 0  collisions 0
#         device interrupt 16  memory 0xdf100000-df120000  

# lo: flags=73<UP,LOOPBACK,RUNNING>  mtu 65536
#         inet 127.0.0.1  netmask 255.0.0.0
#         inet6 ::1  prefixlen 128  scopeid 0x10<host>
#         loop  txqueuelen 1000  (Local Loopback)
#         RX packets 1425  bytes 1191386 (1.1 MB)
#         RX errors 0  dropped 0  overruns 0  frame 0
#         TX packets 1425  bytes 1191386 (1.1 MB)
#         TX errors 0  dropped 0 overruns 0  carrier 0  collisions 0

# wlp1s0: flags=4163<UP,BROADCAST,RUNNING,MULTICAST>  mtu 1500
# ------> inet 192.168.1.157  netmask 255.255.255.0  broadcast 192.168.1.255
#         inet6 2600:1700:a7d4:5810:d66d:6dff:feb0:d60f  prefixlen 64  scopeid 0x0<global>
#         inet6 2600:1700:a7d4:5810::36  prefixlen 128  scopeid 0x0<global>
#         inet6 fe80::d66d:6dff:feb0:d60f  prefixlen 64  scopeid 0x20<link>
#         ether d4:6d:6d:b0:d6:0f  txqueuelen 1000  (Ethernet)
#         RX packets 53003  bytes 63495486 (63.4 MB)
#         RX errors 0  dropped 3330  overruns 0  frame 0
#         TX packets 4165  bytes 1167992 (1.1 MB)
#         TX errors 0  dropped 0 overruns 0  carrier 0  collisions 0

```
from the localmachine


``` bash
leaver2000@inwin:~$ ssh leaver2000@192.168.1.157
# Welcome to Ubuntu 22.04 LTS (GNU/Linux 5.15.0-37-generic x86_64)

#  * Documentation:  https://help.ubuntu.com
#  * Management:     https://landscape.canonical.com
#  * Support:        https://ubuntu.com/advantage

#   System information as of Wed Jun 15 01:20:46 AM UTC 2022

#   System load:              0.0
#   Usage of /:               20.6% of 53.21GB
#   Memory usage:             1%
#   Swap usage:               0%
#   Temperature:              52.0 C
#   Processes:                154
#   Users logged in:          1
#   IPv4 address for docker0: 172.17.0.1
#   IPv4 address for wlp1s0:  192.168.1.157
#   IPv6 address for wlp1s0:  2600:1700:a7d4:5810::36
#   IPv6 address for wlp1s0:  2600:1700:a7d4:5810:d66d:6dff:feb0:d60f


# 0 updates can be applied immediately.
leaver2000@nuc:~$ 
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
leaver2000@inwin:~/nuc-api$ curl 192.168.1.157
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