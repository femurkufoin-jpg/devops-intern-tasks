# Task 2: Linux Log Inspection

## 1. Introduction

Linux log inspection is the process of examining system records to understand system activities, monitor services, identify errors and warnings, and troubleshoot problems.

During this task, I used Ubuntu Linux running on Windows Subsystem for Linux (WSL 2) to explore Linux log files and practise different log inspection commands.

The objective was to understand how Linux administrators and DevOps engineers use logs to monitor systems, investigate issues, and maintain reliable infrastructure.

## 2. Environment Setup

**Operating System:** Windows  
**Linux Distribution:** Ubuntu  
**Linux Environment:** Windows Subsystem for Linux (WSL 2)  
**Terminal:** VS Code integrated terminal  
**Project Repository:** `devops-intern-tasks`

I verified the WSL installation using:

```bash
wsl --status
wsl -l -v
```

Ubuntu was installed and configured to use WSL 2.

### Ubuntu Password Recovery

I had forgotten my Ubuntu password. I opened Ubuntu as the root user from PowerShell and reset the password for my normal account.

From PowerShell:

```powershell
wsl -d Ubuntu -u root
```

Then, inside Ubuntu:

```bash
passwd synthia_k
```

The password was successfully updated, and I returned to my normal Ubuntu account.

## 3. Understanding Linux Log Files

I navigated to the Linux log directory:

```bash
cd /var/log
pwd
ls -lah
```

I identified the following important files and directories:

| Log file | Purpose |
|---|---|
| `syslog` | Records general system activities and messages. |
| `auth.log` | Records authentication and security-related events. |
| `kern.log` | Contains Linux kernel messages. |
| `dmesg` | Displays kernel messages, including hardware and startup information. |
| `boot.log` | Contains system boot messages. |
| `dpkg.log` | Records package installation and removal activities. |
| `journal/` | Stores systemd journal data. |
| `lastlog` | Contains information about users' most recent logins. |
| `wtmp` | Records login and logout activity. |
| `btmp` | Records failed login attempts. |

I also observed compressed log files ending in `.gz`, which generally contain older rotated logs.

## 4. Inspecting System Logs

I inspected the latest system log entries using:

```bash
sudo tail -n 20 /var/log/syslog
```

This command displayed the last 20 entries in the system log.

I observed:

- System service startup messages.
- SSH agent and GPG agent socket activity.
- Systemd session activity.
- Time synchronization messages.
- WSL-related warnings.

### Searching for Errors and Warnings

I used `grep` to search for important messages:

```bash
sudo grep -iE 'error|fail|warning' /var/log/syslog | tail -n 20
```

This helped identify warnings and errors without reading the entire log file.

Some messages indicated that WSL could not communicate with a Windows agent because an expected agent port file was unavailable.

## 5. Inspecting Authentication Logs

I inspected authentication records using:

```bash
sudo tail -n 20 /var/log/auth.log
```

I observed:

- User session opening and closing events.
- Root account login activity.
- Password reset activity.
- Sudo command execution records.
- Normal user session activity.

I searched for failed authentication-related messages:

```bash
sudo grep -i "failed" /var/log/auth.log
```

The output included PAM system-bus connection failures. These were system-session errors, not confirmed incorrect-password attempts.

I also searched for successful authentication messages:

```bash
sudo grep -i "accepted" /var/log/auth.log
```

No actual successful SSH authentication entry was identified in the output.

## 6. Inspecting Kernel Logs

I inspected kernel messages using:

```bash
sudo dmesg -T | tail -n 20
```

I observed messages relating to:

- System termination signals.
- System-bus connection failures.
- WSL graphics adapter operations.
- System journal activity.
- WSL startup delays.

The output included messages such as:

```text
dxgkio_query_adapter_info: ioctl failed
WaitForBootProcess
system.journal corrupted or uncleanly shut down
```

These messages provided examples of kernel-level and WSL startup issues.

## 7. Real-Time Log Monitoring

I practised monitoring system logs as new entries were generated:

```bash
sudo tail -f /var/log/syslog
```

The command displayed new log entries in real time.

I stopped the monitoring process using:

```text
Ctrl + C
```

This exercise demonstrated how administrators can monitor system activity and observe new errors or warnings as they occur.

## 8. Inspecting Systemd Journal Logs

I used `journalctl` to inspect system journal records:

```bash
sudo journalctl -n 20 --no-pager
```

This displayed the latest 20 journal entries.

I also filtered the journal for error-priority messages:

```bash
sudo journalctl -p err -n 10 --no-pager
```

The command displayed recent error-level journal entries.

I observed:

- WSL graphics adapter errors.
- System initialization messages.
- Ubuntu Insights service failures.
- Mount namespace errors.
- Missing file or directory messages.

Some entries included:

```text
dxgkio_query_adapter_info: ioctl failed
```

Other entries showed failures involving Ubuntu Insights services and missing files.

These were WSL and Ubuntu Insights environment-related messages. They were not evidence of an application failure.

This exercise helped me identify system-level errors and distinguish environmental warnings from application-related problems.

## 9. Important Linux Log Inspection Commands

The following commands were practised during the assignment:

| Command | Purpose |
|---|---|
| `cd /var/log` | Navigate to the Linux log directory. |
| `pwd` | Display the current directory. |
| `ls -lah` | List files, including hidden files, with details. |
| `sudo tail -n 20 /var/log/syslog` | Display the latest 20 system log entries. |
| `sudo grep -iE 'error|fail|warning' /var/log/syslog` | Search system logs for errors, failures, and warnings. |
| `sudo tail -n 20 /var/log/auth.log` | Display recent authentication records. |
| `sudo grep -i "failed" /var/log/auth.log` | Search authentication logs for failed messages. |
| `sudo grep -i "accepted" /var/log/auth.log` | Search for successful authentication messages. |
| `sudo dmesg -T` | Display kernel messages with readable timestamps. |
| `sudo tail -f /var/log/syslog` | Monitor system logs in real time. |
| `sudo journalctl -n 20 --no-pager` | Display recent systemd journal entries. |
| `sudo journalctl -p err -n 10 --no-pager` | Display recent error-priority journal entries. |

## 10. Challenges Faced and Troubleshooting

During the assignment, I encountered a few challenges:

**1. Forgotten Ubuntu password**

I could not initially access my normal Ubuntu account because I had forgotten its password.

**Solution:** I opened the Ubuntu distribution as the root user from PowerShell and reset the password using the `passwd` command.

**2. WSL system and service warnings**

While inspecting system logs, I encountered WSL-related warnings, graphics adapter errors, and Ubuntu Insights service failures.

**Solution:** I used `grep`, `dmesg`, and `journalctl` to investigate the messages and understand that they were related to the WSL environment and Ubuntu Insights services.

**3. Understanding log output**

Some log entries contained technical messages that were difficult to interpret.

**Solution:** I used targeted commands such as `tail`, `grep`, and `journalctl` to filter the output and focus on relevant messages.

## 11. Skills and Knowledge Gained

Through this assignment, I gained practical experience in:

- Navigating the Linux filesystem.
- Locating and understanding important Linux log files.
- Inspecting system and authentication logs.
- Searching for errors and warnings using `grep`.
- Reading kernel messages using `dmesg`.
- Monitoring logs in real time.
- Inspecting systemd journal entries using `journalctl`.
- Identifying and interpreting WSL-related system messages.
- Using Linux commands to support troubleshooting and system monitoring.

These skills are important for DevOps engineers because logs provide valuable information for monitoring infrastructure, diagnosing service problems, and maintaining reliable systems.

## 12. Task Summary

**Task:** Linux Log Inspection

**Status:** Practical exercises completed; documentation prepared.

**Environment:** Ubuntu Linux on WSL 2.

**Main Tools:** Linux terminal, `grep`, `tail`, `dmesg`, and `journalctl`.

**Outcome:** Successfully explored Linux log files, inspected system and authentication activity, investigated kernel messages, practised real-time log monitoring, and identified error-level journal entries.

