# Linux Privilege Escalation Techniques

Privilege escalation occurs when a user gains elevated access (usually root) on a Linux system. This guide covers common misconfigurations that lead to privesc.

## 1. Sudo Misconfigurations
If a user is allowed to run certain commands via `sudo` without a password, those commands can sometimes be exploited to spawn a root shell.
- Check allowed sudo commands: `sudo -l`
- Reference **GTFOBins** for commands that can break out of their intended environment (e.g., `find`, `vim`, `awk`, `less`).

## 2. SUID/SGID Binaries
Files with the SUID bit set run with the permissions of the file owner. If a vulnerable or abusable binary is owned by root and has SUID set, it can be exploited.
- Find SUID files: `find / -perm -u=s -type f 2>/dev/null`

## 3. Cron Jobs
Cron jobs that run as root can be exploited if they interact with files or directories that are writable by a low-privileged user.
- Check for weak permissions on scripts executed by cron.
- Check `/etc/crontab` and `/var/spool/cron/`.

## 4. Kernel Exploits
Old or unpatched kernels often have known privilege escalation vulnerabilities (e.g., Dirty COW, Dirty Pipe).
- Check kernel version: `uname -a`
- Search for known CVEs for that specific kernel version.

## 5. Weak File Permissions
Sensitive files might be readable or writable by unprivileged users.
- `/etc/shadow`: If readable, password hashes can be cracked. If writable, passwords can be changed.
- `/etc/passwd`: If writable, a new root user can be added.
