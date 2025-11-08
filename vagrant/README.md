# 🚀 Kubernetes com Vagrant e Kubespray

## 🧩 Descrição do Projeto

Este projeto tem como objetivo criar um **cluster Kubernetes local** de forma totalmente automatizada, utilizando:  

- 🧱 **Vagrant** — para provisionar as máquinas virtuais;  
- ⚙️ **Kubespray** — para instalar e configurar o ambiente Kubernetes dentro dessas VMs.  

Essa abordagem permite construir um cluster **consistente, reproduzível e isolado**, ideal para **testes, estudos ou desenvolvimento local**, sem depender de infraestrutura externa.

---

## ⚙️ Automação com Makefile

O projeto inclui um **Makefile** que simplifica todo o processo de criação e gerenciamento do ambiente.  
Abaixo estão os principais alvos e suas funções:

| Alvo | Descrição |
|------|------------|
| `make init` | Executa o fluxo completo: inicia as VMs, clona e prepara o Kubespray, e cria o cluster Kubernetes. |
| `make start` | Sobe as máquinas virtuais definidas no diretório `k8s` via Vagrant. |
| `make stop` | Pausa todas as VMs em execução. |
| `make destroy` | Remove todas as VMs criadas pelo Vagrant. |
| `make kubespray` | Clona o repositório oficial do Kubespray, copia o inventário e ajusta o plugin de rede para **Flannel**. |
| `make createCluster` | Executa a criação do cluster Kubernetes utilizando o **Docker Compose** definido no projeto. |

🔹 O comportamento padrão (`make` sem argumentos) executa **`make init`**, realizando todas as etapas automaticamente.

---

## 🧰 Pré-requisitos

Antes de executar o projeto, verifique se os seguintes pacotes estão instalados no seu sistema:

| Ferramenta | Descrição | Comando de instalação (exemplo para Ubuntu/Debian) |
|-------------|------------|----------------------------------------------------|
| **Vagrant** | Criação e gerenciamento de VMs. | `sudo apt install vagrant` |
| **VirtualBox** | Provider utilizado pelo Vagrant. | `sudo apt install virtualbox` |
| **Git** | Necessário para clonar o Kubespray. | `sudo apt install git` |
| **Docker** | Utilizado pelo Kubespray via Docker Compose. | [Instruções oficiais](https://docs.docker.com/engine/install/) |
| **Make** | Para executar as tarefas definidas no Makefile. | `sudo apt install make` |
| **Ansible** | Utilizado internamente pelo Kubespray. | `sudo apt install ansible` |

---

## ▶️ Como Executar

Siga os passos abaixo para subir o ambiente:

```bash
# Clone este repositório
git clone git@github.com:douglasportugal/homelab.git
cd homelab

# Inicialize o ambiente (cria as VMs, prepara o Kubespray e sobe o cluster)
make init
```

Após a conclusão, você terá um cluster Kubernetes funcional.  
Para confirmar o status:

```bash
kubectl get nodes
```

---

## 🧹 Comandos Úteis

```bash
make stop      # Pausa as VMs
make start     # Reinicia as VMs
make destroy   # Remove todas as VMs criadas
```

---

## 📁 Estrutura do Projeto (exemplo)

```
.
├── k8s/
│   ├── Vagrantfile
│   └── (outros arquivos relacionados às VMs)
├── kubespray/
│   └── (gerado automaticamente pelo Makefile)
├── inventory.ini
├── docker-compose.yml
├── Makefile
└── README.md
```