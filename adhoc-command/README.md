# Ansible Ad-Hoc Commands



> Run one-liner tasks across multiple remote hosts — no playbook needed.

---

## Project Overview

This project demonstrates the use of **Ansible Ad-Hoc commands** to manage and query multiple Ubuntu servers without writing a full playbook. It's a quick-start reference for common sysadmin tasks using Ansible's CLI interface.

---

## Inventory

**File:** `inverntory.ini`

```ini
danish@192.168.100.16
danish@192.168.100.29
danish@192.168.100.30
```

Three Ubuntu 24.04.3 LTS (Noble Numbat) hosts managed over SSH.

---

## Commands Used

### Ping All Hosts
Test connectivity to all hosts in the inventory.

```bash
ansible -i inverntory.ini -m ping all
```

**Output:** All 3 hosts returned `pong` — connectivity confirmed.

---

### Check Disk Usage
Get filesystem disk space usage on all hosts.

```bash
ansible -i inverntory.ini -m shell -a "df -Th" all
```

**Sample Output (per host):**

| Filesystem                          | Type  | Size | Used | Avail | Use% | Mounted on |
|-------------------------------------|-------|------|------|-------|------|------------|
| /dev/mapper/ubuntu--vg-ubuntu--lv   | ext4  | 28G  | ~11G | ~16G  | ~43% | /          |
| /dev/sda2                           | ext4  | 2.0G | 112M | 1.7G  |  7%  | /boot      |

---

### Check OS Release
Retrieve OS information from all managed hosts.

```bash
ansible -i inverntory.ini -m shell -a "cat /etc/os-release" all
```

**Result:** All hosts running **Ubuntu 24.04.3 LTS (Noble Numbat)**

---

## Requirements

- Ansible Core 2.21+
- SSH key-based authentication configured to all hosts
- Python 3.12 on remote hosts (auto-discovered)

---

## Common Ad-Hoc Patterns

```bash
# Run any shell command across all hosts
ansible -i inverntory.ini -m shell -a "<command>" all

# Target a specific host
ansible -i inverntory.ini -m shell -a "<command>" danish@192.168.100.16

# Check uptime
ansible -i inverntory.ini -m shell -a "uptime" all

# Check memory usage
ansible -i inverntory.ini -m shell -a "free -h" all

# Check running processes
ansible -i inverntory.ini -m shell -a "ps aux --sort=-%cpu | head -10" all
```

---

## Notes

- The `pattern` argument (e.g., `all`) must come **after** the module args — forgetting it causes the `error: the following arguments are required: pattern` error.
- Python interpreter warnings are informational and don't affect functionality. To suppress them, set `interpreter_python = auto_silent` in `ansible.cfg`.

---

## Author

**danish-ali** — practicing Ansible automation on a local Ubuntu lab environment.
