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
TERRAFORM_VERSION=1.14.0
HELMFILE_VERSION=1.2.1
init: pre provisioning kubespray setKubeVersion fixInventory createCluster helm

destroy:
	@cd $(TF_DIR) && \
	source $(ENV_FILE) && \
	terraform destroy -auto-approve

pre:
	@echo ">>> Verificando Terraform..."
	@if ! command -v terraform >/dev/null 2>&1; then \
		echo ">>> Terraform não encontrado. Instalando..."; \
		curl -fsSL https://releases.hashicorp.com/terraform/1.9.8/terraform_1.9.8_linux_amd64.zip -o terraform.zip; \
		unzip -o terraform.zip >/dev/null; \
		mv terraform /usr/local/bin/terraform; \
		chmod +x /usr/local/bin/terraform; \
		rm -f terraform.zip; \
	else \
		echo ">>> Terraform já está instalado:"; \
		terraform version; \
	fi

	@echo ">>> Verificando Helm..."
	@if ! command -v helm >/dev/null 2>&1; then \
		echo ">>> Helm não encontrado. Instalando Helm v3.15.4..."; \
		curl -fsSL -o get_helm.sh https://raw.githubusercontent.com/helm/helm/v3.15.4/scripts/get-helm-3; \
		chmod 700 get_helm.sh; \
		HELM_INSTALL_DIR=/usr/local/bin DESIRED_VERSION=v3.15.4 ./get_helm.sh; \
	else \
		echo ">>> Helm já está instalado:"; \
		helm version; \
	fi

	@echo ">>> Verificando Helmfile..."
	@if ! command -v helmfile >/dev/null 2>&1; then \
		echo ">>> Helmfile não encontrado. Instalando..."; \
		LATEST=$$(curl -fsSL https://api.github.com/repos/helmfile/helmfile/releases/latest | grep tag_name | cut -d '"' -f 4); \
		echo ">> Baixando Helmfile $$LATEST..."; \
		curl -fsSL -o helmfile.tar.gz https://github.com/helmfile/helmfile/releases/download/$$LATEST/helmfile_$${LATEST#v}_linux_amd64.tar.gz; \
		tar -xzf helmfile.tar.gz; \
		sudo mv helmfile /usr/local/bin/helmfile; \
		sudo chmod +x /usr/local/bin/helmfile; \
		rm -f helmfile.tar.gz; \
	else \
		echo ">>> Helmfile já está instalado:"; \
		helmfile version; \
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

upgradeCluster:
	docker run --rm -it \
		--mount type=bind,source=$(INVENTORY_DIR),dst=/inventory \
		--mount type=bind,source=${HOME}/.ssh/id_rsa,dst=/root/.ssh/id_rsa \
		quay.io/kubespray/kubespray:v2.29.0 \
		bash -c "ansible-playbook -i /inventory/inventory.ini --private-key /root/.ssh/id_rsa upgrade-cluster.yml"

# By chatgpt
helm:
	@helm repo add zabbix-community https://zabbix-community.github.io/helm-charts || true
	@helm repo add metrics-server https://kubernetes-sigs.github.io/metrics-server/ || true
	@helm repo add ingress-nginx https://kubernetes.github.io/ingress-nginx || true
	@helm repo add metallb https://metallb.github.io/metallb || true
	@helm repo update

	@echo ">> Verificando plugin diff..."
	@if ! helm plugin list | grep -q diff; then \
		echo ">> Plugin diff não encontrado. Instalando..."; \
		helm plugin install https://github.com/databus23/helm-diff --version v3.9.5 --verify=false; \
	else \
		echo ">> Plugin diff já instalado. Atualizando..."; \
		helm plugin update diff || true; \
	fi

	@echo ">> Aplicando helmfile..."
	@helmfile apply

	@echo ">> Aguardando MetalLB subir antes de aplicar o pool..."
	@kubectl -n metallb-system wait --for=condition=Ready pod -l app.kubernetes.io/component=controller --timeout=120s
	@kubectl -n metallb-system wait --for=condition=Ready pod -l app.kubernetes.io/component=speaker --timeout=120s

	@echo ">> Aplicando pool do MetalLB..."
	@kubectl apply -f values/metallb/pool.yaml

	@echo ">> Finalizado!"

fixInventory:
	sed -i '/^\[all\]/a ansible_user=douglas\\nansible_become=true\\nansible_become_method=sudo\\n' $(INVENTORY_DIR)/inventory.ini

setKubeVersion:
	@echo ">> Ajustando kube_version e kube_version_min_required"

	@if grep -q '^kube_version:' $(KUBESPRAY_DIR)/inventory/homelab/group_vars/k8s_cluster/k8s-cluster.yml; then \
		sed -i 's/^kube_version:.*/kube_version: "v1.29.3"/' $(KUBESPRAY_DIR)/inventory/homelab/group_vars/k8s_cluster/k8s-cluster.yml; \
	else \
		echo 'kube_version: "v1.29.3"' >> $(KUBESPRAY_DIR)/inventory/homelab/group_vars/k8s_cluster/k8s-cluster.yml; \
	fi

	@if grep -q '^kube_version_min_required:' $(KUBESPRAY_DIR)/inventory/homelab/group_vars/k8s_cluster/k8s-cluster.yml; then \
		sed -i 's/^kube_version_min_required:.*/kube_version_min_required: "v1.24.0"/' $(KUBESPRAY_DIR)/inventory/homelab/group_vars/k8s_cluster/k8s-cluster.yml; \
	else \
		echo 'kube_version_min_required: "v1.24.0"' >> $(KUBESPRAY_DIR)/inventory/homelab/group_vars/k8s_cluster/k8s-cluster.yml; \
	fi
