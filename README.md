# Ansible

![Ansible](https://img.shields.io/badge/Ansible-EE0000?style=for-the-badge&logo=ansible&logoColor=white)
![Linux](https://img.shields.io/badge/Linux-FCC624?style=for-the-badge&logo=linux&logoColor=black)
![Ubuntu](https://img.shields.io/badge/Ubuntu_24.04-E95420?style=for-the-badge&logo=ubuntu&logoColor=white)
![Python](https://img.shields.io/badge/Python_3.12-3776AB?style=for-the-badge&logo=python&logoColor=white)
![YAML](https://img.shields.io/badge/YAML-CB171E?style=for-the-badge&logo=yaml&logoColor=white)
![SSH](https://img.shields.io/badge/SSH_Auth-4D4D4D?style=for-the-badge&logo=openssh&logoColor=white)

![Topics](https://img.shields.io/badge/Topics-11_Covered-brightgreen?style=flat-square)
![Projects](https://img.shields.io/badge/Projects-5_Completed-blue?style=flat-square)
![Managed Hosts](https://img.shields.io/badge/Managed_Hosts-3_Ubuntu_VMs-blue?style=flat-square)
![Status](https://img.shields.io/badge/Status-Active-success?style=flat-square)
![License](https://img.shields.io/badge/License-MIT-yellow?style=flat-square)

> A structured hands-on Ansible learning repository — from ad-hoc commands to roles, vault, CI/CD, and enterprise patterns.

---

## Table of Contents

- [About](#about)
- [Lab Environment](#lab-environment)
- [Repository Structure](#repository-structure)
- [Topics Covered](#topics-covered)
- [Projects](#projects)
  - [Ad-Hoc Commands](#1-ad-hoc-commands)
  - [Web Server — Apache Deployment](#2-web-server--apache-deployment)
  - [Dynamic Configs with Templates — Nginx](#3-dynamic-configs-with-templates--nginx)
  - [Install & Configure Monitoring — Node Exporter](#4-install--configure-monitoring--node-exporter)
  - [Install PostgreSQL](#5-install-postgresql)
  - [User Automation](#6-user-automation)
- [Getting Started](#getting-started)
- [Requirements](#requirements)

---

## About

This repository documents a complete Ansible learning journey — covering core concepts, real automation scripts, and hands-on lab exercises. Each topic is backed by a reference PDF and a practical implementation in a dedicated project folder.

---

## Lab Environment

| Detail        | Value                              |
|---------------|------------------------------------|
| Control Node  | Local machine (Ansible Core 2.21+) |
| Managed Hosts | 3 × Ubuntu 24.04.3 LTS VMs         |
| Auth Method   | SSH key-based authentication       |
| Python        | 3.12 (auto-discovered)             |
| Network       | Local LAN (192.168.100.x)          |

---

## Repository Structure

```
Ansible/
├── adhoc-command/                          # Ad-hoc command demos
│   ├── inverntory.ini                      # Inventory (3 Ubuntu hosts)
│   └── README.md
│
├── projects/
│   ├── web-server/                         # Apache web server deployment
│   │   ├── web-playbook.yaml
│   │   ├── inventory.ini
│   │   ├── index.html
│   │   └── README.md
│   │
│   ├── dynamic-configs-with-templates/     # Nginx + Jinja2 template deployment
│   │   ├── main-playbook.yaml
│   │   ├── inventory.ini
│   │   ├── web-role/                       # Ansible role
│   │   │   ├── defaults/main.yml
│   │   │   ├── files/index.html
│   │   │   ├── handlers/main.yml
│   │   │   ├── tasks/main.yml
│   │   │   ├── templates/nginx.conf.j2
│   │   │   └── vars/main.yml
│   │   └── README.md
│   │
│   ├── install-configure-monitoring/       # Prometheus Node Exporter
│   │   ├── main.yaml
│   │   ├── inventory.ini
│   │   ├── group_vars/all.yml
│   │   ├── node_exporter/                  # Ansible role
│   │   │   ├── defaults/main.yml
│   │   │   ├── handlers/main.yml
│   │   │   ├── tasks/main.yml
│   │   │   ├── templates/node_exporter.service.j2
│   │   │   └── vars/main.yml
│   │   └── README.md
│   │
│   ├── install-postgress/                  # PostgreSQL with Ansible Vault
│   │   ├── main.yaml
│   │   ├── inventory.ini
│   │   ├── pass.vault
│   │   ├── group_vars/all/main.yml         # Vault-encrypted credentials
│   │   ├── postgress/                      # Ansible role
│   │   │   ├── defaults/main.yml
│   │   │   ├── handlers/main.yml
│   │   │   ├── tasks/main.yml
│   │   │   └── vars/main.yml
│   │   └── README.md
│   │
│   └── user-automation/                    # Bulk user + SSH key setup
│       ├── user-playbook.yaml
│       ├── inventory.ini
│       └── README.md
│
├── Ansible_Architecture_and_Inventory.pdf
├── Ansible_Conditionals_and_Loops.pdf
├── Ansible_Dynamic_Inventory_and_Performance.pdf
├── Ansible_Essential_Core_Modules.pdf
├── Ansible_Handlers_and_Templates.pdf
├── Ansible_Passwordless_Authentication_EC2.pdf
├── Ansible_Playbook.pdf
├── Ansible_Roles.pdf
├── Ansible_Testing_CI_CD_and_Enterprise.pdf
├── Ansible_Variables_and_Facts.pdf
├── Ansible_Vault_and_Error_Handling.pdf
├── Passwordless_Authentication_Guide.pdf
└── adhoc-command.pdf
```

---

## Topics Covered

| # | Topic | Reference PDF | Status |
|---|-------|--------------|--------|
| 1 | Architecture & Inventory | `Ansible_Architecture_and_Inventory.pdf` | ✅ Done |
| 2 | Ad-Hoc Commands | `adhoc-command.pdf` | ✅ Done |
| 3 | Playbooks | `Ansible_Playbook.pdf` | ✅ Done |
| 4 | Variables & Facts | `Ansible_Variables_and_Facts.pdf` | ✅ Done |
| 5 | Conditionals & Loops | `Ansible_Conditionals_and_Loops.pdf` | ✅ Done |
| 6 | Handlers & Templates | `Ansible_Handlers_and_Templates.pdf` | ✅ Done |
| 7 | Essential Core Modules | `Ansible_Essential_Core_Modules.pdf` | ✅ Done |
| 8 | Roles | `Ansible_Roles.pdf` | ✅ Done |
| 9 | Vault & Error Handling | `Ansible_Vault_and_Error_Handling.pdf` | ✅ Done |
| 10 | Dynamic Inventory & Performance | `Ansible_Dynamic_Inventory_and_Performance.pdf` | ✅ Done |
| 11 | Testing, CI/CD & Enterprise | `Ansible_Testing_CI_CD_and_Enterprise.pdf` | ✅ Done |

---

## Projects

### 1. Ad-Hoc Commands

**Folder:** [`adhoc-command/`](adhoc-command/)

Hands-on demos using Ansible's CLI to run one-liner tasks against 3 Ubuntu hosts — no playbooks needed.

**Inventory:** 3 × Ubuntu 24.04.3 LTS hosts over SSH

```bash
# Ping all hosts
ansible -i adhoc-command/inverntory.ini -m ping all

# Check disk usage
ansible -i adhoc-command/inverntory.ini -m shell -a "df -Th" all

# Check OS release
ansible -i adhoc-command/inverntory.ini -m shell -a "cat /etc/os-release" all

# Check memory
ansible -i adhoc-command/inverntory.ini -m shell -a "free -h" all
```

See [`adhoc-command/README.md`](adhoc-command/README.md) for the full command reference.

---

### 2. Web Server — Apache Deployment

**Folder:** [`projects/web-server/`](projects/web-server/)  
**Playbook:** `web-playbook.yaml` → targets `[webserver]` group

Automates the full lifecycle of an Apache web server — installs the latest version, ensures the service is running and enabled on boot, and deploys a custom `index.html` to the document root.

**Inventory:**
```ini
[webserver]
192.168.100.16 ansible_user=danish
```

**Tasks:**

| # | Task | Module |
|---|------|--------|
| 1 | Install / upgrade Apache2 to latest | `ansible.builtin.apt` |
| 2 | Start Apache2 and enable on boot | `ansible.builtin.service` |
| 3 | Copy `index.html` → `/var/www/html/` | `ansible.builtin.copy` |

```bash
cd projects/web-server
ansible-playbook -i inventory.ini web-playbook.yaml
```

See [`projects/web-server/README.md`](projects/web-server/README.md) for details.

---

### 3. Dynamic Configs with Templates — Nginx

**Folder:** [`projects/dynamic-configs-with-templates/`](projects/dynamic-configs-with-templates/)  
**Playbook:** `main-playbook.yaml` → targets `[danish]` group → uses `web-role`

Deploys a personal portfolio website on a remote Ubuntu host using Nginx. Stops Apache to free port 80, installs Nginx, deploys a Jinja2-rendered server block config, and serves a static HTML page.

**Role structure:**
```
web-role/
├── defaults/main.yml       # ansible_user default
├── files/index.html        # Static portfolio HTML
├── handlers/main.yml       # nginx-service restart handler
├── tasks/main.yml          # 4 deployment tasks
├── templates/nginx.conf.j2 # Nginx server block (Jinja2)
└── vars/main.yml
```

**Tasks:**

| # | Task | Module | Action |
|---|------|--------|--------|
| 1 | Stop & disable Apache2 | `ansible.builtin.service` | Prevents port 80 conflict |
| 2 | Install / upgrade Nginx | `ansible.builtin.apt` | `state: latest` |
| 3 | Deploy Nginx config | `ansible.builtin.copy` | → `/etc/nginx/conf.d/website.conf` |
| 4 | Deploy index.html | `ansible.builtin.copy` | → `/var/www/html/` |

```bash
cd projects/dynamic-configs-with-templates
ansible-playbook -i inventory.ini main-playbook.yaml
```

Site available at `http://192.168.100.16/` after a successful run.

See [`projects/dynamic-configs-with-templates/README.md`](projects/dynamic-configs-with-templates/README.md) for details.

---

### 4. Install & Configure Monitoring — Node Exporter

**Folder:** [`projects/install-configure-monitoring/`](projects/install-configure-monitoring/)  
**Playbook:** `main.yaml` → targets `[server]` group → uses `node_exporter` role

Automates the full installation and configuration of **Prometheus Node Exporter** on remote Linux hosts. Handles cross-platform package installation (apt / dnf), binary download from GitHub, dedicated system user/group creation, and systemd service deployment via a Jinja2 unit template.

**Variables (`group_vars/all.yml`):**

| Variable | Default | Description |
|---|---|---|
| `node_exporter_version` | `1.8.1` | Node Exporter release |
| `node_exporter_system_user` | `node_exporter` | Dedicated service user |
| `node_exporter_system_group` | `node_exporter` | Dedicated service group |

**Task flow:**

| # | Task | Description |
|---|------|-------------|
| 1 | Create system group | Adds `node_exporter` group |
| 2 | Create system user | No-login, no-home system user |
| 3 | Install deps (Ubuntu) | `wget`, `tar` via apt |
| 4 | Install deps (RHEL/AlmaLinux) | `wget`, `tar` via dnf |
| 5 | Download binary | Fetches tarball from GitHub releases |
| 6 | Extract binary | Unpacks to `/tmp/` |
| 7 | Copy binary | Places at `/usr/local/bin/node_exporter` |
| 8 | Deploy systemd unit | Renders `.service` from Jinja2 template |
| 9 | Enable & start service | systemd daemon reload + start |

**Supported platforms:** Ubuntu / Debian (apt) · AlmaLinux / RHEL / CentOS (dnf)

```bash
cd projects/install-configure-monitoring
ansible-playbook -i inventory.ini main.yaml

# Verify deployment
curl http://192.168.100.16:9100/metrics
```

Metrics available at `http://<host>:9100/metrics` after deployment.

See [`projects/install-configure-monitoring/README.md`](projects/install-configure-monitoring/README.md) for details.

---

### 5. Install PostgreSQL

**Folder:** [`projects/install-postgress/`](projects/install-postgress/)  
**Playbook:** `main.yaml` → targets `[db]` group → uses `postgress` role

Automates the full installation and configuration of PostgreSQL on a remote Ubuntu server. Installs required packages, starts the service, creates a database (`mydb`), and provisions a PostgreSQL user — with all credentials stored securely in **Ansible Vault (AES256)**.

**Variables (Vault-encrypted in `group_vars/all/main.yml`):**

| Variable | Description |
|---|---|
| `db_host` | PostgreSQL host address |
| `db_port` | PostgreSQL port (default: `5432`) |
| `db_user` | PostgreSQL login username |
| `db_password` | PostgreSQL login password — encrypted |

**Task flow:**

| # | Task | Description |
|---|------|-------------|
| 1 | Install packages | `postgresql`, `postgresql-contrib`, `libpq-dev`, `python3-psycopg2` |
| 2 | Start & enable service | systemd: started + enabled on boot |
| 3 | Create database | Creates `mydb` (runs as `postgres` user) |
| 4 | Create user | Configures PostgreSQL user with vault credentials |

**Vault commands:**
```bash
# Edit encrypted variables
ansible-vault edit group_vars/all/main.yml --vault-password-file pass.vault

# View encrypted content
ansible-vault view group_vars/all/main.yml --vault-password-file pass.vault

# Generate a strong password
openssl rand -hex 16
```

```bash
cd projects/install-postgress
ansible-playbook main.yaml -i inventory.ini --vault-password-file pass.vault
```

See [`projects/install-postgress/README.md`](projects/install-postgress/README.md) for details.

---

### 6. User Automation

**Folder:** [`projects/user-automation/`](projects/user-automation/)  
**Playbook:** `user-playbook.yaml` → targets `[danish]` group

Automates bulk Linux user account creation on a remote host. Creates users (`ahmad`, `ali`, `shahid`), adds them to the `sudo` group for administrative privileges, and configures **passwordless SSH login** by copying the controller's public key into each user's `authorized_keys`.

**Tasks:**

| Task | Module | Description |
|------|--------|-------------|
| Create users | `ansible.builtin.user` | Creates users with `/bin/bash` shell, adds to `sudo` group |
| Set up authorized keys | `ansible.posix.authorized_key` | Copies `~/.ssh/id_rsa.pub` → each user's `authorized_keys` |

```bash
cd projects/user-automation

# Install required collection
ansible-galaxy collection install ansible.posix

# Run the playbook
ansible-playbook -i inventory.ini user-playbook.yaml
```

See [`projects/user-automation/README.md`](projects/user-automation/README.md) for details.

---

## Getting Started

**1. Clone the repository**

```bash
git clone https://github.com/danish-ali/Ansible.git
cd Ansible
```

**2. Install Ansible**

```bash
pip install ansible
# or
sudo apt install ansible
```

**3. Configure SSH key access to your managed hosts**

```bash
ssh-copy-id danish@192.168.100.16
ssh-copy-id danish@192.168.100.29
ssh-copy-id danish@192.168.100.30
```

**4. Test connectivity**

```bash
ansible -i adhoc-command/inverntory.ini -m ping all
```

---

## Requirements

- Ansible Core `2.17+`
- Python `3.10+` on both control node and managed hosts
- SSH key-based authentication to all managed hosts
- Ubuntu 20.04+ on managed hosts (or any Linux distro)
- `ansible.posix` collection for user automation: `ansible-galaxy collection install ansible.posix`
