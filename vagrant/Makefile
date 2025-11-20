SHELL := /bin/bash
.DEFAULT_GOAL := init

# Variáveis de caminho
ROOT_DIR := ./
KUBESPRAY_DIR := $(ROOT_DIR)/kubespray
K8S_DIR := $(ROOT_DIR)/k8s

init:
	$(MAKE) start
	$(MAKE) kubespray
	$(MAKE) createCluster

up: start

down: stop

kubespray:
	git clone https://github.com/kubernetes-sigs/kubespray.git $(KUBESPRAY_DIR); \
	cp $(ROOT_DIR)/inventory.ini $(KUBESPRAY_DIR)/inventory/sample/; \
	cd $(KUBESPRAY_DIR)/inventory/sample/group_vars/k8s_cluster/; \
	sed -i s/kube_network_plugin\:\ calico/kube_network_plugin\:\ flannel/g k8s-cluster.yml

createCluster:
	cd $(KUBESPRAY_DIR) && docker compose -f $(ROOT_DIR)/docker-compose.yml up

start:
	cd $(K8S_DIR) && vagrant up

stop:
	cd $(K8S_DIR) && vagrant halt

destroy:
	cd $(K8S_DIR) && vagrant destroy -f