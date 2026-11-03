
# Task 2: Linux Log Inspection

## 1. Introduction

Linux log inspection is the process of examining system records to understand system activities, monitor services, identify errors and warnings, and troubleshoot problems.

During this task, I used Ubuntu Linux running on Windows Subsystem for Linux (WSL 2) to explore Linux log files and practise different log inspection commands.

## 2. Environment Setup

- Operating System: Windows
- Linux Distribution: Ubuntu
- Linux Environment: Windows Subsystem for Linux (WSL 2)
- Terminal: VS Code integrated terminal
- Project Repository: devops-intern-tasks

I verified the WSL installation using:

```bash
wsl --status
wsl -l -v
```

Ubuntu was installed and configured to use WSL 2.

### Ubuntu Password Recovery

I had forgotten my Ubuntu password. I opened Ubuntu as the root user from PowerShell and reset the password for my normal account.

```powershell
wsl -d Ubuntu -u root
```

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
| syslog | Records general system activities and messages. |
| auth.log | Records authentication and security-related events. |
| kern.log | Contains Linux kernel messages. |
| dmesg | Displays kernel messages, including hardware and startup information. |
| boot.log | Contains system boot messages. |
| dpkg.log | Records package installation and removal activities. |
| journal/ | Stores systemd journal data. |
| lastlog | Contains information about users' most recent logins. |
| wtmp | Records login and logout activity. |
| btmp | Records failed login attempts. |

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

I used grep to search for important messages:

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

- `dxgki_query_adapter_info: ioctl failed`
- `WaitForBootProcess`
- `system.journal corrupted or uncleanly shut down`

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

I used journalctl to inspect system journal records:

```bash
sudo journalctl -n 20 --no-pager
```

This displayed the latest 20 journal entries.

I also filtered the journal for error-priority messages:

```bash
sudo journalctl -p err -n 10 --no-pager
```

The output revealed errors involving:

- WSL graphics adapter operations.
- WSL boot process timeout.
- Ubuntu Insights collection service.
- Ubuntu Insights upload service.
- Missing files or directories during service startup.

These errors were observed and documented. They were not repaired as part of this exercise.

## 9. Troubleshooting and Challenges

### Challenge 1: Forgotten Ubuntu Password

I could not remember my existing Ubuntu password when attempting to inspect system logs with sudo.

**Solution:** I opened Ubuntu as the root user through PowerShell and used the passwd command to reset the password for my normal Ubuntu account.

### Challenge 2: WSL Systemd User Session Warning

When starting Ubuntu, I encountered a warning indicating that the systemd user session could not start.

**Observation:** Ubuntu still opened successfully, allowing me to continue with the practical exercises.

### Challenge 3: Windows Agent Connection Warnings

The system logs repeatedly displayed warnings about the Windows agent connection and a missing agent port file.

**Observation:** These messages were related to WSL integration. They did not prevent me from accessing the Linux log files.

### Challenge 4: WSL and Ubuntu Insights Errors

Kernel and system journal inspection revealed WSL startup timeout messages, graphics-related errors, and Ubuntu Insights service failures.

**Observation:** I identified and documented these errors using grep, dmesg and journalctl. They were not treated as confirmed application failures.

## 10. Key Linux Commands Practised

| Command | Purpose |
|---|---|
| `cd /var/log` | Navigate to the Linux log directory. |
| `pwd` | Display the current working directory. |
| `ls -lah` | List files with detailed information. |
| `tail -n 20` | Display the last 20 lines of a file. |
| `grep` | Search for specific text in files. |
| `grep -i` | Search without case sensitivity. |
| `dmesg -T` | Display kernel messages with readable timestamps. |
| `tail -f` | Monitor new log entries in real time. |
| `journalctl` | Inspect systemd journal records. |
| `journalctl -p err` | Filter journal entries by error priority. |
| `sudo` | Execute commands with administrator privileges. |
| `passwd` | Change a Linux user password. |

## 11. Skills and Knowledge Gained

By completing this task, I gained practical experience in:

1. Locating and understanding Linux log files.
2. Inspecting general system activity.
3. Examining authentication records.
4. Searching for errors and warnings using grep.
5. Reading kernel messages using dmesg.
6. Monitoring logs in real time.
7. Using journalctl to inspect system events.
8. Interpreting system errors and warnings.
9. Troubleshooting basic Linux environment issues.
10. Understanding the importance of logs in system administration and DevOps operations.

## 12. Conclusion

This task improved my understanding of Linux system logging and troubleshooting. I gained hands-on experience using Ubuntu on WSL 2 to inspect system, authentication, and kernel logs.

I also learned how to identify errors and warnings, monitor system activity in real time, and use different Linux commands to investigate system behaviour.

These skills are important for DevOps engineers because logs provide valuable information for monitoring infrastructure, diagnosing service problems, and maintaining reliable systems.

**Task:** Linux Log Inspection  
**Status:** Practical exercises completed; documentation prepared.
