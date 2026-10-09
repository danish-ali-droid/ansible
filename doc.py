#!/usr/bin/env python3
"""
generate_passwordless_auth_doc.py

Generates a professional black-and-white PDF covering:
  1. Passwordless authentication concepts and security rationale
  2. PEM file-based authentication to EC2 instances
  3. Password-based SSH authentication (enabling/disabling)
  4. Passwordless authentication through Ansible playbooks

Requirements:
    pip install reportlab

Output:
    Ansible_Passwordless_Authentication_EC2.pdf
"""

from reportlab.lib.pagesizes import LETTER
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY, TA_LEFT
from reportlab.platypus import (SimpleDocTemplate, Paragraph, Spacer, Table,
                                TableStyle, PageBreak, Preformatted, HRFlowable)


# ============================================================ PALETTE
BLACK  = colors.black
WHITE  = colors.white
GRAY_1 = colors.HexColor('#F2F2F2')
GRAY_2 = colors.HexColor('#D9D9D9')
GRAY_3 = colors.HexColor('#666666')

PAGE_W, PAGE_H = LETTER
MARGIN    = 0.85 * inch
CONTENT_W = PAGE_W - 2 * MARGIN


# ============================================================ STYLES
def S(name, **kw):
    base = dict(fontName='Helvetica', fontSize=10, leading=14,
                textColor=BLACK, alignment=TA_JUSTIFY, spaceAfter=8)
    base.update(kw)
    return ParagraphStyle(name, **base)


st_title    = S('title', fontName='Helvetica-Bold', fontSize=24, leading=29,
                alignment=TA_CENTER, spaceAfter=8)
st_subtitle = S('subtitle', fontName='Helvetica', fontSize=13, leading=18,
                alignment=TA_CENTER, textColor=GRAY_3, spaceAfter=6)
st_h1       = S('h1', fontName='Helvetica-Bold', fontSize=15, leading=19,
                alignment=TA_LEFT, spaceBefore=18, spaceAfter=8)
st_h2       = S('h2', fontName='Helvetica-Bold', fontSize=12, leading=16,
                alignment=TA_LEFT, spaceBefore=12, spaceAfter=6)
st_h3       = S('h3', fontName='Helvetica-BoldOblique', fontSize=10.5, leading=14,
                alignment=TA_LEFT, spaceBefore=8, spaceAfter=4)
st_body     = S('body')
st_bullet   = S('bullet', leftIndent=16, bulletIndent=4, spaceAfter=4,
                alignment=TA_LEFT)
st_code     = ParagraphStyle('code', fontName='Courier', fontSize=8.2, leading=10.6,
                             textColor=BLACK)
st_caption  = S('caption', fontName='Helvetica-Oblique', fontSize=8.5, leading=11,
                alignment=TA_CENTER, textColor=GRAY_3, spaceBefore=2, spaceAfter=10)
st_toc      = S('toc', fontSize=10, leading=16, alignment=TA_LEFT, spaceAfter=0)
st_toc_sub  = S('tocsub', fontSize=9.5, leading=14, alignment=TA_LEFT,
                leftIndent=20, textColor=GRAY_3, spaceAfter=0)

st_cell     = ParagraphStyle('cell', fontName='Helvetica', fontSize=8, leading=10.5,
                             textColor=BLACK, alignment=TA_LEFT)
st_cellh    = ParagraphStyle('cellh', fontName='Helvetica-Bold', fontSize=8, leading=10.5,
                             textColor=BLACK, alignment=TA_LEFT)
st_cellc    = ParagraphStyle('cellc', fontName='Courier', fontSize=7.6, leading=10,
                             textColor=BLACK, alignment=TA_LEFT)


# ============================================================ HELPERS
def P(text, style=st_body):
    return Paragraph(text, style)


def B(text):
    return Paragraph(text, st_bullet, bulletText='\u2022')


def code(text, chunk_lines=35):
    """Return a list of flowables, splitting long code across pages."""
    lines = text.split('\n')
    flowables = []
    for i in range(0, len(lines), chunk_lines):
        chunk = '\n'.join(lines[i:i + chunk_lines])
        pre = Preformatted(chunk, st_code)
        t = Table([[pre]], colWidths=[CONTENT_W])
        t.setStyle(TableStyle([
            ('BACKGROUND',    (0, 0), (-1, -1), GRAY_1),
            ('BOX',           (0, 0), (-1, -1), 0.6, GRAY_3),
            ('LEFTPADDING',   (0, 0), (-1, -1), 9),
            ('RIGHTPADDING',  (0, 0), (-1, -1), 9),
            ('TOPPADDING',    (0, 0), (-1, -1), 7),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 7),
        ]))
        flowables.append(t)
        if i + chunk_lines < len(lines):
            flowables.append(Spacer(1, 2))
    return flowables


def datatable(rows, widths, header=True):
    t = Table(rows, colWidths=widths, repeatRows=1 if header else 0)
    style = [
        ('FONTNAME',     (0, 0), (-1, -1), 'Helvetica'),
        ('FONTSIZE',     (0, 0), (-1, -1), 8),
        ('VALIGN',       (0, 0), (-1, -1), 'TOP'),
        ('GRID',         (0, 0), (-1, -1), 0.4, GRAY_3),
        ('LEFTPADDING',  (0, 0), (-1, -1), 6),
        ('RIGHTPADDING', (0, 0), (-1, -1), 6),
        ('TOPPADDING',   (0, 0), (-1, -1), 4),
        ('BOTTOMPADDING',(0, 0), (-1, -1), 4),
    ]
    if header:
        style += [
            ('BACKGROUND', (0, 0), (-1, 0), GRAY_2),
            ('FONTNAME',   (0, 0), (-1, 0), 'Helvetica-Bold'),
        ]
    t.setStyle(TableStyle(style))
    return t


def cell(txt, style=st_cell):
    return Paragraph(txt, style)


def rule(space_before=4, space_after=10):
    return HRFlowable(width='100%', thickness=0.8, color=BLACK,
                      spaceBefore=space_before, spaceAfter=space_after)


# ============================================================ PAGE DECORATION
def draw_footer(canvas, doc):
    canvas.saveState()
    canvas.setStrokeColor(GRAY_3)
    canvas.setLineWidth(0.5)
    canvas.line(MARGIN, 0.68 * inch, PAGE_W - MARGIN, 0.68 * inch)
    canvas.setFont('Helvetica', 7.5)
    canvas.setFillColor(GRAY_3)
    canvas.drawCentredString(PAGE_W / 2, 0.52 * inch, 'Page %d' % doc.page)
    canvas.restoreState()


def on_first_page(canvas, doc):
    draw_footer(canvas, doc)


def on_later_pages(canvas, doc):
    canvas.saveState()
    canvas.setStrokeColor(GRAY_3)
    canvas.setLineWidth(0.5)
    canvas.line(MARGIN, PAGE_H - 0.62 * inch, PAGE_W - MARGIN, PAGE_H - 0.62 * inch)
    canvas.setFont('Helvetica', 7.5)
    canvas.setFillColor(GRAY_3)
    canvas.drawString(MARGIN, PAGE_H - 0.56 * inch,
                      'Passwordless Authentication for AWS EC2')
    canvas.drawRightString(PAGE_W - MARGIN, PAGE_H - 0.56 * inch,
                           'Professional Reference')
    canvas.restoreState()
    draw_footer(canvas, doc)


# ============================================================ STORY
story = []

# ---------------------------------------------------------- TITLE PAGE
story.append(Spacer(1, 1.7 * inch))
story.append(P('PASSWORDLESS AUTHENTICATION', st_title))
story.append(Spacer(1, 0.10 * inch))
story.append(HRFlowable(width='45%', thickness=1.4, color=BLACK, hAlign='CENTER'))
story.append(Spacer(1, 0.14 * inch))
story.append(P('PEM Key Access, Password Configuration,<br/>'
               'and Ansible Playbook Automation<br/>'
               'for AWS EC2 Instances', st_subtitle))
story.append(Spacer(1, 0.9 * inch))
story.append(P('Professional Reference Documentation', st_caption))
story.append(P('Version 1.0', st_caption))
story.append(PageBreak())

# ---------------------------------------------------------- TABLE OF CONTENTS
story.append(P('Table of Contents', st_h1))
story.append(rule())

toc = [
    ('1.  Introduction to Passwordless Authentication', None),
    ('2.  Authentication Methods: A Security Comparison', None),
    ('     2.1  Password Authentication', None),
    ('     2.2  Public Key Authentication', None),
    ('     2.3  PEM Files in AWS', None),
    ('3.  Connecting to EC2 with a PEM File', None),
    ('     3.1  Obtaining the PEM File', None),
    ('     3.2  Setting File Permissions', None),
    ('     3.3  Connecting via SSH', None),
    ('     3.4  Common Errors', None),
    ('4.  Password-Based Authentication on EC2', None),
    ('     4.1  Default AWS Configuration', None),
    ('     4.2  Enabling Password Authentication', None),
    ('     4.3  Setting User Passwords', None),
    ('     4.4  Security Warnings', None),
    ('5.  Passwordless Authentication via Ansible Playbook', None),
    ('     5.1  Architecture Overview', None),
    ('     5.2  Generating the Control Node SSH Key', None),
    ('     5.3  The Ansible Inventory', None),
    ('     5.4  The Playbook', None),
    ('     5.5  Running the Playbook', None),
    ('     5.6  Verification', None),
    ('6.  Hardening: Disabling Password Authentication', None),
    ('7.  Best Practices', None),
    ('8.  Quick Reference', None),
]
for title, _ in toc:
    if title.startswith('     '):
        story.append(P(title.strip(), st_toc_sub))
    else:
        story.append(P(title, st_toc))

story.append(PageBreak())

# ============================================================ 1. INTRO
story.append(P('1.  Introduction to Passwordless Authentication', st_h1))
story.append(rule())

story.append(P(
    'Passwordless authentication is an access model in which a user or automated '
    'system proves its identity using a cryptographic key pair rather than a '
    'shared secret (password). The user holds a private key; the server holds the '
    'corresponding public key. When a connection is attempted, the server issues a '
    'challenge that can only be answered correctly by the holder of the private '
    'key. No password ever crosses the network.'))

story.append(P(
    'In the context of AWS EC2, passwordless authentication takes three practical '
    'forms:'))

story.append(B('<b>PEM file authentication</b> — the standard AWS mechanism, where '
               'the private key downloaded at instance launch is used with '
               '<font face="Courier" size="9">ssh -i</font> to connect.'))
story.append(B('<b>Password-based authentication</b> — the traditional Unix SSH '
               'model, disabled by default on EC2 but sometimes required for '
               'legacy tooling or third-party clients.'))
story.append(B('<b>Ansible-managed key deployment</b> — an automation pattern in '
               'which a playbook distributes a control node\'s public key to '
               'managed instances, establishing passwordless access for all future '
               'automation.'))

story.append(P(
    'This document covers all three, with a strong emphasis on the Ansible '
    'workflow, which is the standard approach in production environments.'))

story.append(P('Why passwordless matters:', st_body))
story.append(B('<b>Eliminates brute-force attacks.</b> A private key cannot be '
               'guessed; an attacker would need to steal the key file.'))
story.append(B('<b>Enables automation.</b> Scripts, CI/CD pipelines, and '
               'configuration management tools cannot type a password interactively.'))
story.append(B('<b>Scales cleanly.</b> A single public key can be distributed to '
               'hundreds of instances by an Ansible playbook.'))
story.append(B('<b>Supports auditing.</b> Key issuance and revocation are '
               'explicit events, unlike password changes that are often invisible.'))

# ============================================================ 2. COMPARISON
story.append(P('2.  Authentication Methods: A Security Comparison', st_h1))
story.append(rule())

story.append(P('2.1  Password Authentication', st_h2))
story.append(P(
    'Password authentication requires the user to transmit a shared secret over '
    'the encrypted SSH channel. The server compares the received password against '
    'a stored hash. While SSH encrypts the transmission, passwords remain '
    'vulnerable to:'))
story.append(B('Brute-force and dictionary attacks against the SSH daemon.'))
story.append(B('Reuse across systems, where one breach compromises many hosts.'))
story.append(B('Weak or default credentials left in place.'))
story.append(B('Interception if the server is compromised or misconfigured.'))

story.append(P(
    'Because of these risks, password authentication is disabled by default on '
    'Amazon EC2 Linux instances.[reference:0]'))

story.append(P('2.2  Public Key Authentication', st_h2))
story.append(P(
    'Public key authentication uses asymmetric cryptography. The private key '
    'never leaves the client; only a challenge response is sent. The server '
    'validates the response using the public key stored in the user\'s '
    '<font face="Courier" size="9">~/.ssh/authorized_keys</font> file.'))

story.append(P('Security advantages over passwords:', st_body))
story.append(B('<b>Nothing secret travels over the wire.</b> Even if the session '
               'were somehow decrypted, no reusable credential is exposed.'))
story.append(B('<b>Immune to guessing.</b> The key space is astronomically large; '
               'brute-forcing a 4096-bit key is computationally infeasible.'))
story.append(B('<b>No password reuse.</b> Each key is unique to its owner and can '
               'be revoked independently.'))
story.append(B('<b>Supports passphrases.</b> A passphrase-protected private key '
               'adds a second factor without weakening the first.'))

story.append(P(
    'Public key authentication is the recommended method by OpenSSH and by AWS '
    'itself.[reference:1]'))

story.append(P('2.3  PEM Files in AWS', st_h2))
story.append(P(
    'When an EC2 instance is launched, AWS offers to create a key pair or to use '
    'an existing one. The private key is downloaded once, in PEM format (Privacy '
    'Enhanced Mail). This file is the only copy; AWS does not retain it. The '
    'corresponding public key is injected into the instance\'s '
    '<font face="Courier" size="9">~/.ssh/authorized_keys</font> file at boot.'))

story.append(P('Key facts about PEM files:', st_body))
story.append(B('<b>Format.</b> PEM is a base64-encoded container. PuTTY on Windows '
               'requires conversion to PPK format.'))
story.append(B('<b>Permissions.</b> OpenSSH refuses to use a private key that is '
               'readable by anyone other than the owner. Set mode '
               '<font face="Courier" size="9">400</font>.'))
story.append(B('<b>Single download.</b> If the PEM file is lost, it cannot be '
               're-downloaded. A new key pair must be created.'))
story.append(B('<b>Scope.</b> The key pair is bound to the region in which it was '
               'created; it cannot be used in another region without re-importing '
               'the public key.'))

# ============================================================ 3. PEM CONNECTION
story.append(PageBreak())
story.append(P('3.  Connecting to EC2 with a PEM File', st_h1))
story.append(rule())

story.append(P('3.1  Obtaining the PEM File', st_h2))
story.append(P(
    'The PEM file is downloaded when the instance is launched. Its default name '
    'matches the key pair name, with a '
    '<font face="Courier" size="9">.pem</font> extension. Store it in a secure '
    'location, ideally outside the repository tree.'))

story.extend(code(
"""# Recommended location on Linux / macOS
mv ~/Downloads/my-key-pair.pem ~/.ssh/my-key-pair.pem

# Recommended location on Windows
# Place in a dedicated folder, e.g. C:\\Keys\\my-key-pair.pem"""))

story.append(P('3.2  Setting File Permissions', st_h2))
story.append(P(
    'OpenSSH will reject a private key that is group- or world-readable. On Linux '
    'and macOS, use '
    '<font face="Courier" size="9">chmod 400</font>; on Windows, use the file '
    'properties dialog to remove inherited permissions.[reference:2]'))

story.extend(code(
"""# Linux / macOS
chmod 400 ~/.ssh/my-key-pair.pem

# Verify permissions (should show -r--------)
ls -l ~/.ssh/my-key-pair.pem

# Windows PowerShell (alternative to GUI)
icacls C:\\Keys\\my-key-pair.pem /inheritance:r
icacls C:\\Keys\\my-key-pair.pem /grant:r "$($env:USERNAME):(R)\""""))

story.append(P('3.3  Connecting via SSH', st_h2))

story.extend(code(
"""# Amazon Linux
ssh -i ~/.ssh/my-key-pair.pem ec2-user@<public-ip>

# Ubuntu
ssh -i ~/.ssh/my-key-pair.pem ubuntu@<public-ip>

# Debian
ssh -i ~/.ssh/my-key-pair.pem admin@<public-ip>

# Rocky Linux
ssh -i ~/.ssh/my-key-pair.pem rocky@<public-ip>

# RHEL
ssh -i ~/.ssh/my-key-pair.pem ec2-user@<public-ip>"""))

story.append(P(
    'The default username depends on the AMI. The following table lists common '
    'distributions.[reference:3]'))

user_rows = [
    [cell('Distribution', st_cellh), cell('Default user', st_cellh)],
    [cell('Amazon Linux'), cell('ec2-user', st_cellc)],
    [cell('Ubuntu'), cell('ubuntu', st_cellc)],
    [cell('Debian'), cell('admin', st_cellc)],
    [cell('RHEL'), cell('ec2-user', st_cellc)],
    [cell('CentOS'), cell('centos', st_cellc)],
    [cell('Fedora'), cell('fedora', st_cellc)],
    [cell('Rocky Linux'), cell('rocky', st_cellc)],
    [cell('SUSE'), cell('ec2-user', st_cellc)],
]
story.append(datatable(user_rows, [200, 289]))
story.append(P('Table 1 — Default SSH user by distribution.', st_caption))

story.append(P('3.4  Common Errors', st_h2))

story.append(B('<b>"Permissions are too open."</b> The PEM file has incorrect '
               'permissions. Run '
               '<font face="Courier" size="9">chmod 400</font>.'))
story.append(B('<b>"Connection timed out."</b> The security group does not allow '
               'inbound SSH (port 22) from your IP address.'))
story.append(B('<b>"Permission denied (publickey)."</b> The wrong user name or the '
               'wrong PEM file. Verify both.'))
story.append(B('<b>"No such file or directory."</b> The path to the PEM file is '
               'incorrect. Use an absolute path.'))

# ============================================================ 4. PASSWORD AUTH
story.append(P('4.  Password-Based Authentication on EC2', st_h1))
story.append(rule())

story.append(P('4.1  Default AWS Configuration', st_h2))
story.append(P(
    'On all Amazon EC2 Linux instances, password authentication and direct root '
    'login are disabled by default. The SSH daemon is configured with '
    '<font face="Courier" size="9">PasswordAuthentication no</font> and '
    '<font face="Courier" size="9">PermitRootLogin no</font>. Only key-based '
    'authentication is accepted.[reference:4]'))

story.append(P(
    'This default exists for sound security reasons. Enabling password '
    'authentication reintroduces the brute-force and password-reuse risks that '
    'key-based authentication eliminates. It should be done only when a specific '
    'requirement demands it, and never on internet-facing instances without '
    'additional safeguards.'))

story.append(P('4.2  Enabling Password Authentication', st_h2))
story.append(P(
    'To enable password authentication, edit '
    '<font face="Courier" size="9">/etc/ssh/sshd_config</font> on the instance. '
    'Keep an existing SSH session open in case the change prevents reconnection, '
    'and always back up the file first.[reference:5]'))

story.extend(code(
"""# Back up the original configuration
sudo cp /etc/ssh/sshd_config /etc/ssh/sshd_config.bak

# Edit the file
sudo vi /etc/ssh/sshd_config

# Locate the PasswordAuthentication line and set it to yes
# PasswordAuthentication yes

# Optionally, disable key-based authentication (not recommended)
# PubkeyAuthentication no

# Save the file, then restart the SSH daemon
sudo systemctl restart sshd

# Verify the SSH daemon accepted the configuration
sudo sshd -t"""))

story.append(P(
    'On Ubuntu, the service is called '
    '<font face="Courier" size="9">ssh</font> rather than '
    '<font face="Courier" size="9">sshd</font>: '
    '<font face="Courier" size="9">sudo service ssh restart</font>.[reference:6]'))

story.append(P(
    'On AMIs that use cloud-init, the setting can also be controlled through '
    '<font face="Courier" size="9">ssh_pwauth</font> in '
    '<font face="Courier" size="9">/etc/cloud/cloud.cfg</font>. Setting it to '
    '<font face="Courier" size="9">1</font> causes cloud-init to configure '
    '<font face="Courier" size="9">PasswordAuthentication yes</font> at boot.'))

story.append(P('4.3  Setting User Passwords', st_h2))
story.append(P(
    'Once password authentication is enabled, each user must have a password set. '
    'New users created with '
    '<font face="Courier" size="9">useradd</font> have no password by default and '
    'cannot log in until one is set with '
    '<font face="Courier" size="9">passwd</font>.'))

story.extend(code(
"""# Set a password for an existing user
sudo passwd ec2-user

# Create a new user and set a password
sudo adduser deploy
sudo passwd deploy

# Verify the account is not locked
sudo passwd -S deploy"""))

story.append(P('4.4  Security Warnings', st_h2))

story.append(B('<b>Never enable password authentication on an internet-facing '
               'instance without fail2ban or an equivalent rate limiter.</b> '
               'Exposed SSH daemons with password authentication are scanned and '
               'attacked within minutes of becoming reachable.'))
story.append(B('<b>Prefer key-based authentication even when passwords are '
               'enabled.</b> The two can coexist; leave '
               '<font face="Courier" size="9">PubkeyAuthentication yes</font> and '
               'use passwords only as a fallback for specific accounts.'))
story.append(B('<b>Restrict source IPs in the security group.</b> Limit inbound '
               'port 22 to known networks rather than '
               '<font face="Courier" size="9">0.0.0.0/0</font>.'))
story.append(B('<b>Enforce strong password policies.</b> Use PAM modules such as '
               '<font face="Courier" size="9">pam_pwquality</font> to reject weak '
               'passwords.'))
story.append(B('<b>Audit authentication attempts.</b> Monitor '
               '<font face="Courier" size="9">/var/log/auth.log</font> or '
               '<font face="Courier" size="9">/var/log/secure</font> for failed '
               'login attempts.'))

# ============================================================ 5. ANSIBLE
story.append(PageBreak())
story.append(P('5.  Passwordless Authentication via Ansible Playbook', st_h1))
story.append(rule())

story.append(P(
    'The most scalable way to establish passwordless authentication across many '
    'EC2 instances is an Ansible playbook. The playbook uses the initial PEM key '
    'to connect once, then distributes the control node\'s public SSH key to each '
    'instance. From that point forward, the PEM file is no longer needed for '
    'routine automation.[reference:7]'))

story.append(P('5.1  Architecture Overview', st_h2))

story.extend(code(
"""   +-----------------------------+          +-------------------------------+
   |      ANSIBLE CONTROL NODE   |          |        EC2 INSTANCES          |
   |-----------------------------|          |-------------------------------|
   |  ~/.ssh/id_ed25519          |          |  ~/.ssh/authorized_keys       |
   |  ~/.ssh/id_ed25519.pub      |  SSH     |    (control node public key)  |
   |                             | -------> |                               |
   |  inventory/hosts.ini        |          |  ec2-user account             |
   |  playbook: ssh-setup.yml    |          |                               |
   +-----------------------------+          +-------------------------------+
              |                                          ^
              |                                          |
              +---- initial connection using PEM file ----+"""))
story.append(P('Figure 1 — Control node distributes its public key to EC2 instances.',
               st_caption))

story.append(P('5.2  Generating the Control Node SSH Key', st_h2))
story.append(P(
    'If the control node does not already have an SSH key pair, generate one. '
    'Ed25519 is preferred for its strong security and short key length.'))

story.extend(code(
"""# Generate an Ed25519 key pair (recommended)
ssh-keygen -t ed25519 -f ~/.ssh/id_ed25519 -C "ansible-control"

# Or RSA 4096 if Ed25519 is not supported by a legacy target
ssh-keygen -t rsa -b 4096 -f ~/.ssh/id_rsa -C "ansible-control"

# Verify the key pair
ls -l ~/.ssh/id_ed25519*
cat ~/.ssh/id_ed25519.pub"""))

story.append(P('5.3  The Ansible Inventory', st_h2))

story.extend(code(
"""# inventory/hosts.ini
[ec2_instances]
web01 ansible_host=192.0.2.10
web02 ansible_host=192.0.2.11
db01  ansible_host=192.0.2.20

[ec2_instances:vars]
ansible_user=ec2-user
ansible_ssh_private_key_file=~/.ssh/my-key-pair.pem
ansible_python_interpreter=/usr/bin/python3"""))

story.append(P('The inventory references the original PEM file so the playbook can '
               'connect for the first time.'))

story.append(P('5.4  The Playbook', st_h2))

story.extend(code(
"""---
# ssh-setup.yml
- name: Establish passwordless SSH access
  hosts: ec2_instances
  gather_facts: false
  become: false

  tasks:
    - name: Ensure the .ssh directory exists
      ansible.builtin.file:
        path: "~/.ssh"
        state: directory
        mode: '0700'

    - name: Install the control node public key
      ansible.posix.authorized_key:
        user: "{{ ansible_user }}"
        state: present
        key: "{{ lookup('file', '~/.ssh/id_ed25519.pub') }}"
        manage_dir: false

    - name: Verify the authorized_keys file
      ansible.builtin.stat:
        path: "~/.ssh/authorized_keys"
      register: auth_keys

    - name: Report the result
      ansible.builtin.debug:
        msg: "Public key installed on {{ inventory_hostname }}"
      when: auth_keys.stat.exists"""))

story.append(P(
    'The <font face="Courier" size="9">ansible.posix.authorized_key</font> module '
    'is the correct tool for this task. It is idempotent: if the key is already '
    'present, no change is reported. The '
    '<font face="Courier" size="9">manage_dir: false</font> option prevents the '
    'module from altering the permissions of the home directory itself, which can '
    'cause problems on some AMIs.[reference:8]'))

story.append(P('5.5  Running the Playbook', st_h2))

story.extend(code(
"""# First run -- uses the PEM file from the inventory
ansible-playbook -i inventory/hosts.ini ssh-setup.yml

# Expected output:
# PLAY [Establish passwordless SSH access] **************************************
# TASK [Ensure the .ssh directory exists] ***************************************
# ok: [web01]
# ok: [web02]
# ok: [db01]
# TASK [Install the control node public key] *************************************
# changed: [web01]
# changed: [web02]
# changed: [db01]
# ..."""))

story.append(P('5.6  Verification', st_h2))
story.append(P(
    'After the playbook runs, the PEM file is no longer required. Test the new '
    'key by connecting directly:'))

story.extend(code(
"""# Connect using the control node key instead of the PEM file
ssh -i ~/.ssh/id_ed25519 ec2-user@192.0.2.10

# Run an Ansible ad-hoc command without specifying the PEM file
ansible -i inventory/hosts.ini ec2_instances -m ping \\
  --private-key ~/.ssh/id_ed25519"""))

story.append(P(
    'Once the control node key is installed on every instance, remove the '
    '<font face="Courier" size="9">ansible_ssh_private_key_file</font> line from '
    'the inventory (or leave it pointing to the control node key) so that all '
    'subsequent playbooks use passwordless authentication.'))

# ============================================================ 6. HARDENING
story.append(P('6.  Hardening: Disabling Password Authentication', st_h1))
story.append(rule())

story.append(P(
    'After passwordless access is established and verified, harden the '
    'configuration by disabling password authentication entirely. This eliminates '
    'the brute-force attack surface while preserving key-based access.'))

story.extend(code(
"""---
# harden-ssh.yml
- name: Harden SSH configuration
  hosts: ec2_instances
  become: true

  tasks:
    - name: Disable password authentication
      ansible.builtin.lineinfile:
        path: /etc/ssh/sshd_config
        regexp: '^#?PasswordAuthentication'
        line: 'PasswordAuthentication no'
        validate: '/usr/sbin/sshd -t -f %s'
      notify: Restart sshd

    - name: Disable direct root login
      ansible.builtin.lineinfile:
        path: /etc/ssh/sshd_config
        regexp: '^#?PermitRootLogin'
        line: 'PermitRootLogin no'
        validate: '/usr/sbin/sshd -t -f %s'
      notify: Restart sshd

    - name: Ensure key-based authentication is enabled
      ansible.builtin.lineinfile:
        path: /etc/ssh/sshd_config
        regexp: '^#?PubkeyAuthentication'
        line: 'PubkeyAuthentication yes'
        validate: '/usr/sbin/sshd -t -f %s'
      notify: Restart sshd

  handlers:
    - name: Restart sshd
      ansible.builtin.service:
        name: sshd
        state: restarted"""))

story.append(P(
    'The <font face="Courier" size="9">validate</font> parameter runs '
    '<font face="Courier" size="9">sshd -t</font> against the temporary file '
    'before the change is committed. If the syntax is invalid, the original file '
    'is left untouched — a critical safety net when editing SSH configuration.'))

# ============================================================ 7. BEST PRACTICES
story.append(P('7.  Best Practices', st_h1))
story.append(rule())

story.append(B('<b>Prefer key-based authentication over passwords.</b> It is '
               'stronger, scalable, and immune to brute-force attacks.'))
story.append(B('<b>Use Ed25519 keys.</b> They offer strong security with short '
               'key length and are supported by all modern OpenSSH versions.'))
story.append(B('<b>Protect private keys with a passphrase.</b> Use '
               '<font face="Courier" size="9">ssh-agent</font> to avoid typing it '
               'repeatedly.'))
story.append(B('<b>Set PEM file permissions to 400.</b> OpenSSH will refuse to use '
               'a key that is readable by others.'))
story.append(B('<b>Never store PEM files in the repository.</b> Keep them in '
               '<font face="Courier" size="9">~/.ssh</font> with restricted '
               'permissions.'))
story.append(B('<b>Distribute a single control node key with Ansible.</b> This '
               'eliminates the need to manage individual PEM files per engineer.'))
story.append(B('<b>Disable password authentication after key deployment.</b> Remove '
               'the fallback once passwordless access is verified.'))
story.append(B('<b>Restrict SSH access by source IP.</b> Configure security groups '
               'to allow port 22 only from known networks.'))
story.append(B('<b>Rotate keys periodically.</b> Generate new control node keys '
               'every 12 to 18 months and redistribute them.'))
story.append(B('<b>Audit authorized_keys files.</b> Remove keys belonging to '
               'departed team members or decommissioned systems.'))
story.append(B('<b>Use AWS Systems Manager Session Manager where possible.</b> It '
               'eliminates inbound SSH entirely and provides full audit logging.'))
story.append(B('<b>Store secrets in Ansible Vault.</b> If a playbook must handle '
               'a private key, encrypt it rather than committing plain text.'))

# ============================================================ 8. QUICK REF
story.append(PageBreak())
story.append(P('8.  Quick Reference', st_h1))
story.append(rule())

story.append(P('PEM File Connection', st_h2))

pem_rows = [
    [cell('Task', st_cellh), cell('Command', st_cellh)],
    [cell('Set permissions'),
     cell('chmod 400 ~/.ssh/my-key.pem', st_cellc)],
    [cell('Connect (Amazon Linux)'),
     cell('ssh -i key.pem ec2-user@<ip>', st_cellc)],
    [cell('Connect (Ubuntu)'),
     cell('ssh -i key.pem ubuntu@<ip>', st_cellc)],
    [cell('Connect (Debian)'),
     cell('ssh -i key.pem admin@<ip>', st_cellc)],
    [cell('Convert to PPK (PuTTY)'),
     cell('puttygen key.pem -o key.ppk', st_cellc)],
    [cell('Verify key format'),
     cell('head -1 key.pem', st_cellc)],
]
story.append(datatable(pem_rows, [180, 309]))
story.append(P('Table 2 — PEM file quick reference.', st_caption))

story.append(P('Password Authentication', st_h2))

pwd_rows = [
    [cell('Task', st_cellh), cell('Command / File', st_cellh)],
    [cell('Enable password authentication'),
     cell('PasswordAuthentication yes in /etc/ssh/sshd_config', st_cellc)],
    [cell('Disable password authentication'),
     cell('PasswordAuthentication no in /etc/ssh/sshd_config', st_cellc)],
    [cell('Set a user password'),
     cell('sudo passwd <username>', st_cellc)],
    [cell('Restart SSH daemon (RHEL)'),
     cell('sudo systemctl restart sshd', st_cellc)],
    [cell('Restart SSH daemon (Ubuntu)'),
     cell('sudo service ssh restart', st_cellc)],
    [cell('Cloud-init setting'),
     cell('ssh_pwauth: 1 in /etc/cloud/cloud.cfg', st_cellc)],
]
story.append(datatable(pwd_rows, [180, 309]))
story.append(P('Table 3 — Password authentication quick reference.', st_caption))

story.append(P('Ansible Passwordless Setup', st_h2))

ans_rows = [
    [cell('Task', st_cellh), cell('Command / Module', st_cellh)],
    [cell('Generate control node key'),
     cell('ssh-keygen -t ed25519 -f ~/.ssh/id_ed25519', st_cellc)],
    [cell('Install public key'),
     cell('ansible.posix.authorized_key', st_cellc)],
    [cell('Verify key file'),
     cell('ansible.builtin.stat', st_cellc)],
    [cell('Run the playbook'),
     cell('ansible-playbook -i inventory ssh-setup.yml', st_cellc)],
    [cell('Test without PEM'),
     cell('ssh -i ~/.ssh/id_ed25519 ec2-user@<ip>', st_cellc)],
    [cell('Disable password auth'),
     cell('ansible.builtin.lineinfile + validate', st_cellc)],
    [cell('Validate sshd config'),
     cell('validate: /usr/sbin/sshd -t -f %s', st_cellc)],
]
story.append(datatable(ans_rows, [180, 309]))
story.append(P('Table 4 — Ansible passwordless setup quick reference.', st_caption))

story.append(Spacer(1, 0.15 * inch))
story.append(rule(space_before=6, space_after=8))
story.append(P(
    '<i>This document describes AWS EC2 and Ansible Core behaviour as of version '
    '2.14 and later. Default usernames, service names, and security practices may '
    'evolve; always consult the official AWS and Ansible documentation for the '
    'version in use.</i>',
    st_caption))


# ============================================================ BUILD
def main():
    doc = SimpleDocTemplate(
        'Ansible_Passwordless_Authentication_EC2.pdf',
        pagesize=LETTER,
        leftMargin=MARGIN,
        rightMargin=MARGIN,
        topMargin=0.95 * inch,
        bottomMargin=0.85 * inch,
        title='Passwordless Authentication for AWS EC2 Instances',
        author='Professional Reference Documentation',
        subject='Passwordless authentication, PEM files, Ansible playbooks, AWS EC2',
    )
    doc.build(story, onFirstPage=on_first_page, onLaterPages=on_later_pages)
    print('Generated: Ansible_Passwordless_Authentication_EC2.pdf')


if __name__ == '__main__':
    main()
