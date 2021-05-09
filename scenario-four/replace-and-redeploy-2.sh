#!/bin/bash
rm -f /home/elcpt/Documents/train-ticket/deployment/kubernetes-manifests/k8s-no-resource-limits/scrambled-yaml.yaml
cp scrambled-yaml.yaml /home/elcpt/Documents/train-ticket/deployment/kubernetes-manifests/k8s-no-resource-limits/
cd /home/elcpt/Documents/train-ticket/deployment/kubernetes-manifests/k8s-no-resource-limits/
kubectl delete -f quickstart-ts-deployment-part2.yml
kubectl apply -f scrambled-yaml.yaml