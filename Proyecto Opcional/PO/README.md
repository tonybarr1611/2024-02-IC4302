# Optional Project

## Requirements

* Create an user in [DockerHub](https://hub.docker.com/)
* Install [Docker Desktop](https://docs.docker.com/desktop/install/windows-install/), if you are using MacOS, please make sure you select the right installer for your CPU architecture.
* Open Docker Desktop, go to **Settings > Kubernetes** and enable Kubernetes.
![K8s](./images/docker-desktop-k8s.png "K8s Docker Desktop")
* Install [Kubectl](https://kubernetes.io/docs/tasks/tools/install-kubectl-macos/)
* Install [Helm](https://helm.sh/docs/intro/install/)
* Install [Visual Studio Code](https://code.visualstudio.com/)
* Install [Lens](https://k8slens.dev/)


## AWS Access Information

**Bucket:** 2024-02-ic4302-gr1

**Access Key:** AKIAQ2VOGXQDTWAX4PUY

**Secret Key:** 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


## Building the docker images

There is a script to build the docker images, to execute it in a bash shell execute:

```bash
cd ./PO/docker
./build.sh nereo08
```

Change **nereo08** by your DockerHub username

Please take a look on the script contents to make sure you understand what is done under the hood.


## Helm Charts

### Configure

* Open the file **PO/charts/application/values.yaml**
* Replace **nereo08** by your DockerHub username

```yaml
config:
  docker_registry: nereo08
```

### Install

Execute:

```bash
cd ./PO/charts
./install.sh
```


### Uninstall

Execute:

```bash
cd ./PO/charts
./uninstall.sh
```

## Access Debug Pod

```bash
# copy the name that says debug from the following command
kubectl get pods
# then replace debug-844bb45d6f-9jt45 by that name
kubectl exec --stdin --tty debug-844bb45d6f-9jt45 -- /bin/bash
```

### Execute Spark

```bash
cd /opt/spark/
bin/spark-shell
```

Now that Spark Shell is up and running, you can execute the contents of the file **PO/charts/application/scala/app.scala**
