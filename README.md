## objective:
> deploy to minikube a containeriezed python - fastapi application to run on a headless nuc.
> automate scraping data from the web, extraction, data preperation, and preprocessing

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
  --name devtest \
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
# local-container
docker build -t leaver2000/nuc-api:1.0.0 .
docker run -p 8080:8080 --name nuc-api leaver2000/nuc-api:1.0.0
# push the image to docker hub
docker login
# Username: ...
# Password: ...
docker push leaver2000/nuc-api:1.0.0
```

### minikube
``` bash
# start minikube
minikube start
kubectl apply -f api.yaml

```


``` bash
# start minikube
minikube start
# 
kubectl apply -f ./.kube/api.yaml
kubectl get pods -o wide


kubectl create deployment -api --image=nuc/api
# kubectl apply -f ./.kube/deployment.yaml
kubectl get pods -l run=nuc-api -o wide


# kubectl create deployment nuc-api --image=nuc/api


# deployment.apps/nuc-api created
kubectl expose deployment nuc-api --type=NodePort --port=80
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