# Ansible Learning & Automation Lab

![Ansible](https://img.shields.io/badge/Ansible-EE0000?style=for-the-badge&logo=ansible&logoColor=white)
![Linux](https://img.shields.io/badge/Linux-FCC624?style=for-the-badge&logo=linux&logoColor=black)
![Ubuntu](https://img.shields.io/badge/Ubuntu_24.04-E95420?style=for-the-badge&logo=ubuntu&logoColor=white)
![Python](https://img.shields.io/badge/Python_3.12-3776AB?style=for-the-badge&logo=python&logoColor=white)
![YAML](https://img.shields.io/badge/YAML-CB171E?style=for-the-badge&logo=yaml&logoColor=white)
![SSH](https://img.shields.io/badge/SSH_Auth-4D4D4D?style=for-the-badge&logo=openssh&logoColor=white)

![Topics](https://img.shields.io/badge/Topics-11_Covered-brightgreen?style=flat-square)
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
- [Getting Started](#getting-started)
- [Requirements](#requirements)


---

## About

This repository documents a complete Ansible learning journey — covering core concepts, real automation scripts, and hands-on lab exercises. Each topic is backed by a reference PDF and practical implementations in dedicated project folders.

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
├── adhoc-command/                  # Ad-hoc command demos
│   ├── inverntory.ini              # Inventory file (3 Ubuntu hosts)
│   └── README.md                  # Ad-hoc command reference
│
├── user-automation/                # User management automation (WIP)
│
├── Ansible_Architecture_and_Inventory.pdf
├── Ansible_Conditionals_and_Loops.pdf
├── Ansible_Dynamic_Inventory_and_Performance.pdf
├── Ansible_Essential_Core_Modules.pdf
├── Ansible_Handlers_and_Templates.pdf
├── Ansible_Playbook.pdf
├── Ansible_Roles.pdf
├── Ansible_Testing_CI_CD_and_Enterprise.pdf
├── Ansible_Variables_and_Facts.pdf
├── Ansible_Vault_and_Error_Handling.pdf
└── adhoc-command.pdf
```

---

## Topics Covered
| No. | Module / Topic |
| :--- | :--- |
| **1** | Architecture & Inventory |
| **2** | Ad-Hoc Commands |
| **3** | Playbooks |
| **4** | Variables & Facts |
| **5** | Conditionals & Loops |
| **6** | Handlers & Templates |
| **7** | Core Modules |
| **8** | Roles |
| **9** | Vault & Error Handling |
| **10** | Dynamic Inventory & Performance |
| **11** | Testing, CI/CD & Enterprise |

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

### Ad-Hoc Commands



**Folder:** `adhoc-command/`

Hands-on demos using Ansible's CLI to run one-liner tasks against 3 Ubuntu hosts — no playbooks required.

```bash
# Ping all hosts
ansible -i adhoc-command/inverntory.ini -m ping all

# Check disk usage
ansible -i adhoc-command/inverntory.ini -m shell -a "df -Th" all

# Check OS release
ansible -i adhoc-command/inverntory.ini -m shell -a "cat /etc/os-release" all
```

See [`adhoc-command/README.md`](adhoc-command/README.md) for full details.

---

### User Automation



**Folder:** `user-automation/`

Automating user creation, SSH key distribution, and privilege management across managed hosts.

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

---

