SHELL := /bin/bash
.DEFAULT_GOAL := init

# Variáveis de caminho
ROOT_DIR := /home/douglas/Documentos/git/homelab/k8s-proxmox
TF_DIR := $(ROOT_DIR)/terraform/k8s
KUBESPRAY_DIR := $(ROOT_DIR)/kubespray
INVENTORY_NAME := homelab
INVENTORY_DIR := $(KUBESPRAY_DIR)/inventory/$(INVENTORY_NAME)
INVENTORY_FILE := $(TF_DIR)/inventory.ini
GROUP_VARS_FILE := $(INVENTORY_DIR)/group_vars/k8s_cluster/k8s-cluster.yml
ENV_FILE := $(TF_DIR)/.env
TERRAFORM_VERSION=1.9.8
HELMFILE_VERSION=1.2.0
init: pre provisioning k8s

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

k8s:
	@cd $(ROOT_DIR) && \
	rm -rf $(KUBESPRAY_DIR) && \
	git clone https://github.com/kubernetes-sigs/kubespray.git && \
	python3 -m venv .venv && \
	source .venv/bin/activate && \
	pip install -r $(KUBESPRAY_DIR)/requirements.txt && \
	cd $(KUBESPRAY_DIR) && \
	cp -r $(KUBESPRAY_DIR)/inventory/sample $(INVENTORY_DIR) && \
	sed -i 's#kube_network_plugin: calico#kube_network_plugin: flannel#g' $(GROUP_VARS_FILE) && \
	cp $(INVENTORY_FILE) $(INVENTORY_DIR)/inventory.ini && \
	ANSIBLE_HOST_KEY_CHECKING=False ansible-playbook -vv -i $(INVENTORY_DIR)/inventory.ini -b cluster.yml

helm:
	@helm plugin update diff || helm plugin install https://github.com/databus23/helm-diff && \
	helmfile apply && \
	kubectl apply -f values/metallb/pool.yaml