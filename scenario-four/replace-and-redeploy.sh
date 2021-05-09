#!/bin/bash
minikube delete
minikube start --memory=24g --cpus=7 --driver=docker
cp scrambled-yaml.yaml /home/elcpt/Documents/train-ticket/deployment/kubernetes-manifests/quickstart-k8s/
cd /home/elcpt/Documents/train-ticket/deployment/kubernetes-manifests/quickstart-k8s/
kubectl apply -f quickstart-ts-deployment-part1.yml
kubectl apply -f scrambled-yaml.yaml
kubectl apply -f quickstart-ts-deployment-part3.yml
