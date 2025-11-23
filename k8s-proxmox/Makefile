SHELL := /bin/bash
.DEFAULT_GOAL := init

# Variáveis de caminho
HOME=/home/douglas
ROOT_DIR := ${HOME}/Documentos/git/homelab/k8s-proxmox
TF_DIR := $(ROOT_DIR)/terraform/k8s
KUBESPRAY_DIR := $(ROOT_DIR)/kubespray
INVENTORY_NAME := homelab
INVENTORY_DIR := $(KUBESPRAY_DIR)/inventory/$(INVENTORY_NAME)
INVENTORY_FILE := $(TF_DIR)/inventory.ini
GROUP_VARS_FILE := $(INVENTORY_DIR)/group_vars/k8s_cluster/k8s-cluster.yml
ENV_FILE := $(TF_DIR)/.env
TERRAFORM_VERSION=1.9.8
HELMFILE_VERSION=1.2.0
init: pre provisioning kubespray fixInventory createCluster helm

destroy:
	@cd $(TF_DIR) && \
	source $(ENV_FILE) && \
	terraform destroy -auto-approve

pre:
	@if ! command -v helmfile >/dev/null 2>&1; then \
		echo ">>> Helmfile não encontrado. Instalando..."; \
		wget -O /tmp/helmfile.tar.gz https://github.com/helmfile/helmfile/releases/download/v$(HELMFILE_VERSION)/helmfile_$(HELMFILE_VERSION)_linux_amd64.tar.gz; \
		cd /tmp && tar -xvf helmfile.tar.gz; \
		sudo chmod +x /tmp/helmfile; \
		sudo mv /tmp/helmfile /usr/local/bin/helmfile; \
	else \
		echo ">>> Helmfile já está instalado."; \
		helmfile version; \
	fi

	@if ! command -v terraform >/dev/null 2>&1; then \
		echo ">>> Terraform não encontrado. Instalando..."; \
		wget -O /tmp/terraform.zip https://releases.hashicorp.com/terraform/$(TERRAFORM_VERSION)/terraform_$(TERRAFORM_VERSION)_linux_amd64.zip; \
		cd /tmp && unzip -o terraform.zip; \
		sudo chmod +x /tmp/terraform; \
		sudo mv /tmp/terraform /usr/local/bin/terraform; \
	else \
		echo ">>> Terraform já está instalado."; \
		terraform version; \
	fi

provisioning:
	@cd $(TF_DIR) && \
	source $(ENV_FILE) && \
	terraform init && \
	terraform apply -auto-approve


kubespray:
	cd $(ROOT_DIR) && \
	rm -rf $(KUBESPRAY_DIR) && \
	git clone https://github.com/kubernetes-sigs/kubespray.git $(KUBESPRAY_DIR) && \
	cp -r $(KUBESPRAY_DIR)/inventory/sample $(KUBESPRAY_DIR)/inventory/homelab && \
	cp $(INVENTORY_FILE) $(INVENTORY_DIR)/inventory.ini && \
	cd $(KUBESPRAY_DIR)/inventory/homelab/group_vars/k8s_cluster && \
	sed -i 's/kube_network_plugin: calico/kube_network_plugin: flannel/g' k8s-cluster.yml

createCluster:
	docker run --rm -it \
		--mount type=bind,source=$(INVENTORY_DIR),dst=/inventory \
		--mount type=bind,source=${HOME}/.ssh/id_rsa,dst=/root/.ssh/id_rsa \
		quay.io/kubespray/kubespray:v2.29.0 \
		bash -c "ansible-playbook -i /inventory/inventory.ini --private-key /root/.ssh/id_rsa cluster.yml"

helm:
	helm repo add zabbix-community https://zabbix-community.github.io/helm-charts || true
	helm repo add metrics-server https://kubernetes-sigs.github.io/metrics-server/ || true
	helm repo add ingress-nginx https://kubernetes.github.io/ingress-nginx || true
	helm repo update && \
	curl -fsSL -o get_helm.sh https://raw.githubusercontent.com/helm/helm/main/scripts/get-helm-4 && \
    chmod 700 get_helm.sh && \
	./get_helm.sh && \
	helm plugin update diff || helm plugin install https://github.com/databus23/helm-diff --verify=false && \
	helmfile apply && \
	kubectl apply -f values/metallb/pool.yaml

fixInventory:
	sed -i '/^\[all\]/a ansible_user=douglas\\nansible_become=true\\nansible_become_method=sudo\\n' $(INVENTORY_DIR)/inventory.ini