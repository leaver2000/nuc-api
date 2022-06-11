# NUC:
- connect to nuc via ssh:DONE
    NOTES:
        leaver2000@nuc
        ssh-keygen
        move public key to authorized_keys
``` bash

```

``` bash
# sudo permission to user
sudo usermod -aG sudo leaver2000
```

### mount an external drive

``` bash
sudo fdisk -l
# Disk /dev/sdb: 1.82 TiB, 2000398929920 bytes, 488378645 sectors
# Disk model: Expansion Desk  

# create a directory
sudo mkdir /media/external/data
# change the permissions
sudo chmod 777 /media/external/data
# mount the drive
sudo mount /dev/sdb /media/external/data
# run a test
touch /media/external/data/test.txt
```



- installing minikube

``` bash
curl -LO https://storage.googleapis.com/minikube/releases/latest/minikube-linux-amd64
sudo install minikube-linux-amd64 /usr/local/bin/minikube
minikube start
```

- installing helm

``` bash
https://get.helm.sh/helm-v3.9.0-linux-amd64.tar.gz
tar -zxvf helm-v3.0.0-linux-amd64.tar.gz
mv linux-amd64/helm /usr/local/bin/helm
```

- deploy python code to nuc
    - fastapi
    - parquet
- containerize code
- put data on network container


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


kubectl create deployment nuc-api --image=nuc/api
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