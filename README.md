# 🧠 Homelabs & Projetos

## 🧩 Descrição

Este repositório tem como objetivo centralizar **homelabs e projetos pessoais** relacionados a **infraestrutura, automação e observabilidade**.  
Aqui são desenvolvidos e documentados diversos ambientes e provas de conceito utilizando tecnologias modernas como **Kubernetes, Ansible, Terraform, Docker e Zabbix**.

O foco principal é o aprendizado contínuo, a prática de boas práticas DevOps e a criação de ambientes **reproduzíveis, automatizados e altamente configuráveis**.

---

## ⚙️ Estrutura do Repositório

Abaixo está a estrutura geral do repositório e o propósito de cada diretório:

```
homelab/
├── vagrant/
│   ├── k8s/                 # Cluster Kubernetes local com Vagrant e Kubespray
│   └── ...                  # Outros labs baseados em Vagrant
│
├── databases-docker/
│   ├── mariadb/             # Ambiente Docker para MariaDB com replicação
│   ├── postgres/            # Ambiente PostgreSQL em containers
│   └── ...                  
│
├── zabbix/                  # Ambientes de monitoramento Zabbix (HA, proxy, agentes)
├── ansible/                 # Playbooks e roles para automação de infraestrutura
├── terraform/               # Provisionamento de VMs e containers (Proxmox, OCI, etc.)
└── README.md
```

Cada projeto possui seu próprio `README.md` com instruções detalhadas de uso, requisitos e fluxo de automação.

---

## 🧰 Tecnologias Utilizadas

As principais ferramentas e tecnologias utilizadas nos projetos incluem:

| Categoria | Tecnologias |
|------------|--------------|
| **Automação & Provisionamento** | Ansible, Terraform, Kubespray |
| **Orquestração & Containers** | Kubernetes, Docker, Docker Compose |
| **Infraestrutura & Virtualização** | Proxmox, Vagrant, VirtualBox, LXC |
| **Monitoramento & Observabilidade** | Zabbix, Prometheus, Grafana |
| **Bancos de Dados** | PostgreSQL, MariaDB, Oracle, DB2 |
| **Sistemas Operacionais** | Linux (Rocky, Ubuntu, openSUSE, AlmaLinux) |

---

## 🚀 Objetivos

- Criar ambientes **homelab** realistas para estudo e validação de conceitos.  
- Aprimorar fluxos de **provisionamento automatizado e infraestrutura como código (IaC)**.  
- Facilitar a **reprodução e o aprendizado de ambientes complexos**.

---

## 💡 Exemplos de Projetos

- **Kubernetes com Vagrant e Kubespray** — cluster local automatizado.  
- **Zabbix HA + Proxy + Grafana** — arquitetura completa de observabilidade.  
- **PostgreSQL com replicação streaming** — ambiente resiliente e automatizado via Ansible.  
- **MariaDB em containers** — cluster de testes com replicação.  
- **Terraform + Proxmox + LXC** — provisionamento automatizado de laboratórios.  

---