## objective:
> deploy to minikube a containeriezed python - fastapi application to run on a headless nuc.
> automate scraping data from the web, extraction, data preperation, and preprocessing

## SETUP

### WSL
- (wsl-install)[https://docs.microsoft.com/en-us/windows/wsl/install]
``` powershell
wsl --install
```




## Setting up the nuc:

### installing minikube and helm

- minikube

``` bash
curl -LO https://storage.googleapis.com/minikube/releases/latest/minikube-linux-amd64
sudo install minikube-linux-amd64 /usr/local/bin/minikube
```

- helm

``` bash
https://get.helm.sh/helm-v3.9.0-linux-amd64.tar.gz
tar -zxvf helm-v3.0.0-linux-amd64.tar.gz
mv linux-amd64/helm /usr/local/bin/helm
```


### connect to the nuc via SSH

Note there is some configuration with ubuntu-server to enable ssh that has to be accomplished

With VS Code you can create a remote connection va SSH `username@target`

each time you connect it will prompt you for a password, which is kind of annoying

on the nuc run `ssh-keygen`

move `public_key` from the nuc into the `local/.ssh/authorized_keys` 

``` bash
# sudo permission to user
sudo usermod -aG sudo username
```

### mount an external drive to ubuntu

``` bash
# I've attached an external 2tb HHD to the nuc that I want to mount
# list the disks on the nuc
sudo fdisk -l
# Disk /dev/sdb: 1.82 TiB, 2000398929920 bytes, 488378645 sectors
# Disk model: Expansion Desk  

# create a directory to mount the drive
sudo mkdir /media/external/data
# change the permissions to the directory
sudo chmod 777 /media/external/data
# mount the drive
sudo mount /dev/sdb /media/external/data
# run a test
touch /media/external/data/test.txt

rm /media/external/data/test.txt
```

### attach the volume to the container

``` bash
docker volume create data
docker volume inspect data
# [
#     {
#         "CreatedAt": "2022-06-11T20:39:25Z",
#         "Driver": "local",
#         "Labels": {},
#         "Mountpoint": "/var/snap/docker/common/var-lib-docker/volumes/data/_data",
#         "Name": "data",
#         "Options": {},
#         "Scope": "local"
#     }
# ]
sudo mount /dev/sdb /var/snap/docker/common/var-lib-docker/volumes/data/_data
docker run -d \
    --name nuc \
    --mount source=data,target=/media/external \
    leaver2000/nuc-api:1.0.0
```

## application

the app should automaticly scrape data from the web 2 sources

this is the predicted data
https://nomads.ncep.noaa.gov/pub/data/
this is the observed condition
https://mrms.ncep.noaa.gov/data/ProbSevere/PROBSEVERE/

### Python

The environment used for this image was built with conda, miniconda specificly.  Because of some of the grib decoding requirements it's for the moment the easier solution. 

environment: numpy pandas fastapi requests xarray[pyino] pyarrow 
environment-dev: environment + black plint pytest  

data scraping flow
> cron.event -> requests.get("nomads.ncep.noaa.gov/pub/data/...grib2") -> xarray.Dataset -> pandas.Dataframe -> parquet -> storage_volume/product-date.parquet

accessing the data
> requests.get("http://localhost:8080/nuc/product?from_valid_time=...&to_valid_time=...")  parquet -> pandas.Dataframe -> machine_learing 



## Code Deployment

### build/run commands
<!-- https://github.com/4OH4/kubernetes-fastapi -->



``` bash
# local
uvicorn app.main:app --reload
# image
docker build -t leaver2000/nuc-api:1.0.0 .
# container
docker run -p 0.0.0.0:8080:8080 --name nuc-api leaver2000/nuc-api:1.0.0
# network
docker network create nuc-net
# bridge
docker create --name nuc \
  --network nuc-net \
  --publish 8080:80 \
  leaver2000/nuc-api:1.0.0


docker network connect nuc-net nuc
# push the image to docker hub
docker login
# Username: ...
# Password: ...
docker push leaver2000/nuc-api:1.0.0
```

### minikube
``` bash
minikube start
minikube kubectl -- apply -f .kube
minikube kubectl -- get deployment -w
# NAME      READY   UP-TO-DATE   AVAILABLE   AGE
# nuc-api   0/1     1            0           31s
# nuc-api   1/1     1            1           33s
minikube kubectl -- port-forward service/nuc-api-svc 8080
```



``` bash
# start minikube
minikube start
# deploy the config files
kubectl apply -f ./.kube/api.yaml
# display the pod config
kubectl get pods -o wide
# expose the deployment
kubectl expose deployment nuc-api --type=NodePort --port=8080
# forward the minikube port
kubectl port-forward service/nuc-api-svc 8080
```


### junk

```
# kubectl create deployment nuc-api --image=nuc/api
# deployment.apps/nuc-api created
kubectl get services nuc-api
# NAME      TYPE       CLUSTER-IP      EXTERNAL-IP   PORT(S)          AGE
# nuc-api   NodePort   10.97.230.113   <none>        8080:31318/TCP   3m5s
minikube service nuc-api
kubectl port-forward service/nuc-api 7080:80
```


### minikube

```
kubectl
kubectl delete deployment nuc-api
kubectl port-forward service/nuc-api-svc 8080
```



## contab

scheudled events 


The cron utility runs based on commands specified in a cron table (crontab). Each user, including root, can have a cron file. These files don't exist by default, but can be created in the /var/spool/cron directory using the crontab -e command that's also used to edit a cron file (see the script below). I strongly recommend that you not use a standard editor (such as Vi, Vim, Emacs, Nano, or any of the many other editors that are available). Using the crontab command not only allows you to edit the command, it also restarts the crond daemon when you save and exit the editor. The crontab command uses Vi as its underlying editor, because Vi is always present (on even the most basic of installations).

New cron files are empty, so commands must be added from scratch. I added the job definition example below to my own cron files, just as a quick reference, so I know what the various parts of a command mean. Feel free to copy it for your own use.


``` bash

# crontab -e
SHELL=/bin/bash
MAILTO=root@example.com
PATH=/bin:/sbin:/usr/bin:/usr/sbin:/usr/local/bin:/usr/local/sbin

# For details see man 4 crontabs

# Example of job definition:
# .---------------- minute (0 - 59)
# |  .------------- hour (0 - 23)
# |  |  .---------- day of month (1 - 31)
# |  |  |  .------- month (1 - 12) OR jan,feb,mar,apr ...
# |  |  |  |  .---- day of week (0 - 6) (Sunday=0 or 7) OR sun,mon,tue,wed,thu,fri,sat
# |  |  |  |  |
# *  *  *  *  * user-name  command to be executed

# backup using the rsbu program to the internal 4TB HDD and then 4TB external
01 01 * * * /usr/local/bin/rsbu -vbd1 ; /usr/local/bin/rsbu -vbd2

# Set the hardware clock to keep it in sync with the more accurate system clock
03 05 * * * /sbin/hwclock --systohc

# Perform monthly updates on the first of the month
# 25 04 1 * * /usr/bin/dnf -y update
```

``` yaml
apiVersion: batch/v1
kind: CronJob
metadata:
  name: hello
spec:
  schedule: "* * * * *"
  jobTemplate:
    spec:
      template:
        spec:
          containers:
          - name: hello
            image: busybox:1.28
            imagePullPolicy: IfNotPresent
            command:
            - /bin/sh
            - -c
            - date; echo Hello from the Kubernetes cluster
          restartPolicy: OnFailure

```