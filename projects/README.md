# Ansible Projects

<p align="center">
  <img src="https://img.shields.io/badge/Ansible-EE0000?style=for-the-badge&logo=ansible&logoColor=white" />
  <img src="https://img.shields.io/badge/YAML-CB171E?style=for-the-badge&logo=yaml&logoColor=white" />
  <img src="https://img.shields.io/badge/Linux-FCC624?style=for-the-badge&logo=linux&logoColor=black" />
  <img src="https://img.shields.io/badge/Ubuntu-E95420?style=for-the-badge&logo=ubuntu&logoColor=white" />
  <img src="https://img.shields.io/badge/License-MIT-blue?style=for-the-badge" />
  <img src="https://img.shields.io/badge/Status-Active-brightgreen?style=for-the-badge" />
</p>

<p align="center">
  A collection of production-ready Ansible playbooks and roles covering web server deployment, database installation, monitoring setup, dynamic configuration templating, and Linux user automation.
</p>

---

## Projects

| Project | Description | Tech Stack |
|---|---|---|
| [web-server](#-web-server) | Apache web server install, configure & deploy | Apache, Ubuntu, apt |
| [dynamic-configs-with-templates](#-dynamic-configs-with-templates) | Nginx deployment with Jinja2 config templates | Nginx, Jinja2, Ubuntu |
| [install-configure-monitoring](#-install-configure-monitoring) | Prometheus Node Exporter cross-platform setup | Prometheus, systemd, Ubuntu/AlmaLinux |
| [install-postgress](#-install-postgress) | PostgreSQL install, DB + user creation with Vault | PostgreSQL, Ansible Vault, Ubuntu |
| [user-automation](#-user-automation) | Bulk user creation with sudo + passwordless SSH | SSH, authorized_keys, Linux |

---

## Web Server

Automates the full lifecycle of an Apache web server on a remote Ubuntu host — installs the latest version, ensures the service is started and enabled on boot, and deploys a custom `index.html` to the document root.

**Location:** [`web-server/`](./web-server)

**Playbook:** `web-playbook.yaml` → targets `[webserver]` group

### Tasks

| # | Task | Module |
|---|---|---|
| 1 | Install / upgrade Apache2 to latest | `ansible.builtin.apt` |
| 2 | Start Apache2 service and enable on boot | `ansible.builtin.service` |
| 3 | Copy `index.html` → `/var/www/html/` | `ansible.builtin.copy` |

### Quick Start

```bash
cd web-server
ansible-playbook -i inventory.ini web-playbook.yaml
```

**Inventory:**
```ini
[webserver]
192.168.100.16 ansible_user=danish
```

---

## Dynamic Configs with Templates



Deploys a personal portfolio website on a remote Ubuntu host using Nginx. Stops Apache to free port 80, installs Nginx, deploys a Jinja2-based server block config, and serves a static HTML portfolio page — all driven by the `web-role` Ansible role.

**Location:** [`dynamic-configs-with-templates/`](./dynamic-configs-with-templates)

**Playbook:** `main-playbook.yaml` → targets `[danish]` group → uses `web-role`

### Role Structure

```
web-role/
├── defaults/main.yml       # ansible_user default
├── files/index.html        # Static portfolio HTML
├── handlers/main.yml       # nginx-service restart handler
├── tasks/main.yml          # 4 deployment tasks
├── templates/nginx.conf.j2 # Nginx server block (Jinja2)
└── vars/main.yml           # Role-level vars
```

### Tasks

| # | Task | Module | Action |
|---|---|---|---|
| 1 | Stop & disable Apache2 | `ansible.builtin.service` | Prevents port 80 conflict |
| 2 | Install / upgrade Nginx | `ansible.builtin.apt` | `state: latest` |
| 3 | Deploy Nginx config | `ansible.builtin.copy` | → `/etc/nginx/conf.d/website.conf` |
| 4 | Deploy index.html | `ansible.builtin.copy` | → `/var/www/html/` |

### Nginx Template

```nginx
server {
    listen 80;
    server_name _;
    root  /var/www/html;
    index index.html;

    location / {
        try_files $uri $uri/ =404;
    }
}
```

### Quick Start

```bash
cd dynamic-configs-with-templates
ansible-playbook -i inventory.ini main-playbook.yaml
```

**Inventory:**
```ini
[danish]
192.168.100.16
```

---

## Install & Configure Monitoring



Automates the full installation and configuration of **Prometheus Node Exporter** on remote Linux hosts. Handles cross-platform package installation (apt / dnf), binary download from GitHub, dedicated system user/group creation, and systemd service deployment via a Jinja2 unit template.

**Location:** [`install-configure-monitoring/`](./install-configure-monitoring)

**Playbook:** `main.yaml` → targets `[server]` group → uses `node_exporter` role

**Metrics endpoint after deployment:** `http://<host>:9100/metrics`

### Variables (`group_vars/all.yml`)

| Variable | Default | Description |
|---|---|---|
| `node_exporter_version` | `1.8.1` | Node Exporter release version |
| `node_exporter_system_user` | `node_exporter` | Dedicated service user |
| `node_exporter_system_group` | `node_exporter` | Dedicated service group |

### Task Flow

| # | Task | Description |
|---|---|---|
| 1 | Create system group | Adds `node_exporter` system group |
| 2 | Create system user | No-login, no-home system user |
| 3 | Install deps (Ubuntu) | `wget`, `tar` via apt |
| 4 | Install deps (RHEL/AlmaLinux) | `wget`, `tar` via dnf |
| 5 | Download binary | Fetches tarball from GitHub releases |
| 6 | Extract binary | Unpacks to `/tmp/` |
| 7 | Copy binary | Places at `/usr/local/bin/node_exporter` |
| 8 | Deploy systemd unit | Renders `.service` from Jinja2 template |
| 9 | Enable & start service | `systemd` daemon reload + start |

### Supported Platforms



### Quick Start

```bash
cd install-configure-monitoring
ansible-playbook -i inventory.ini main.yaml
```

**Verify after run:**
```bash
curl http://192.168.100.16:9100/metrics
```

---

## Install PostgreSQL


Automates the full installation and configuration of PostgreSQL on a remote Ubuntu server. Installs required packages, starts the service, creates a database (`mydb`), and provisions a PostgreSQL user — with all credentials stored securely in **Ansible Vault (AES256)**.

**Location:** [`install-postgress/`](./install-postgress)

**Playbook:** `main.yaml` → targets `[db]` group → uses `postgress` role

### Variables (Vault-encrypted in `group_vars/all/main.yml`)

| Variable | Description |
|---|---|
| `db_host` | PostgreSQL host address |
| `db_port` | PostgreSQL port (default: `5432`) |
| `db_user` | PostgreSQL login username |
| `db_password` | PostgreSQL login password — **encrypted** |

### Task Flow

| # | Task | Description |
|---|---|---|
| 1 | Install packages | `postgresql`, `postgresql-contrib`, `libpq-dev`, `python3-psycopg2` |
| 2 | Start & enable service | systemd: `postgresql` started + enabled on boot |
| 3 | Create database | Creates `mydb` (runs as `postgres` user) |
| 4 | Create user | Configures PostgreSQL user on `mydb` with vault credentials |

### Vault Commands

```bash
# Edit vault-encrypted variables
ansible-vault edit group_vars/all/main.yml --vault-password-file pass.vault

# View encrypted content
ansible-vault view group_vars/all/main.yml --vault-password-file pass.vault

# Generate a strong password
openssl rand -hex 16
```

### Quick Start

```bash
cd install-postgress
ansible-playbook main.yaml -i inventory.ini --vault-password-file pass.vault
```

**Inventory:**
```ini
[db]
192.168.100.16 ansible_user=danish
```

---

## User Automation


Automates bulk Linux user account creation on a remote host. Creates users, adds them to the `sudo` group for administrative privileges, and configures **passwordless SSH login** by copying the controller's public key into each user's `authorized_keys`.

**Location:** [`user-automation/`](./user-automation)

**Playbook:** `user-playbook.yaml` → targets `[danish]` group

**Users created:** `ahmad`, `ali`, `shahid`

### Tasks

| Task | Module | Description |
|---|---|---|
| Create users | `ansible.builtin.user` | Creates users with `/bin/bash` shell, adds to `sudo` group (`append: yes`) |
| Set up authorized keys | `ansible.posix.authorized_key` | Copies `~/.ssh/id_rsa.pub` → each user's `authorized_keys` |

### Quick Start

```bash
cd user-automation

# Install required collection
ansible-galaxy collection install ansible.posix

# Run the playbook
ansible-playbook -i inventory.ini user-playbook.yaml
```

**Inventory:**
```ini
[danish]
danish@192.168.100.16
```

---

## Prerequisites



| Requirement | Details |
|---|---|
| Ansible | >= 2.2 |
| Control node OS | Linux / macOS |
| Managed node OS | Ubuntu (tested); AlmaLinux/RHEL for monitoring role |
| SSH access | Key-based or password-based to the target host |
| Sudo privileges | `become: yes` required on managed nodes |
| `ansible.posix` collection | Required for `user-automation` — `ansible-galaxy collection install ansible.posix` |

---

## Repository Structure

```
projects/
├── web-server/                        # Apache web server deployment
│   ├── web-playbook.yaml
│   ├── inventory.ini
│   └── index.html
├── dynamic-configs-with-templates/    # Nginx + Jinja2 template deployment
│   ├── main-playbook.yaml
│   ├── inventory.ini
│   └── web-role/
├── install-configure-monitoring/      # Prometheus Node Exporter
│   ├── main.yaml
│   ├── inventory.ini
│   ├── group_vars/all.yml
│   └── node_exporter/
├── install-postgress/                 # PostgreSQL with Ansible Vault
│   ├── main.yaml
│   ├── inventory.ini
│   ├── group_vars/all/main.yml
│   └── postgress/
└── user-automation/                   # Bulk user + SSH key setup
    ├── user-playbook.yaml
    └── inventory.ini
```

---

