# Linux Server Hardening Guide

Securing a Linux server is critical to maintaining confidentiality, integrity, and availability. Below are standard practices for hardening a Linux machine.

## 1. Secure SSH Access
- **Disable Root Login:** Set `PermitRootLogin no` in `/etc/ssh/sshd_config`.
- **Use Key-Based Authentication:** Disable password authentication by setting `PasswordAuthentication no`.
- **Change Default Port:** Consider changing the default SSH port (22) to a non-standard port to avoid automated script kiddie scans.
- **Implement Fail2Ban:** Install and configure Fail2Ban to block IPs after multiple failed login attempts.

## 2. Firewall Configuration (UFW/iptables)
- Install UFW (Uncomplicated Firewall) on Ubuntu/Debian.
- Deny all incoming traffic by default: `ufw default deny incoming`
- Allow only necessary ports (e.g., SSH, HTTP, HTTPS):
  - `ufw allow 22/tcp`
  - `ufw allow 80/tcp`
  - `ufw allow 443/tcp`
- Enable the firewall: `ufw enable`

## 3. User and Privilege Management
- **Sudo Access:** Only grant `sudo` privileges to users who absolutely need it.
- **Remove Unused Accounts:** Regularly audit `/etc/passwd` and remove default or inactive accounts.
- **Strong Passwords:** Enforce strong password policies using `libpam-pwquality`.

## 4. System Updates and Patching
- Regularly update all system packages using the package manager (`apt update && apt upgrade` or `dnf update`).
- Configure Unattended-Upgrades for automatic security patch installation.

## 5. Disable Unused Services
- Identify running services using `systemctl list-units --type=service --state=running`.
- Disable and stop services that are not required for the server's function: `systemctl disable <service>`

## 6. Audit and Logging
- Ensure `syslog` is running and capturing logs to `/var/log/`.
- Install `auditd` to monitor file changes and execute strict system auditing.
