# HashiCorp Vault for Application Secrets

## 1. Project Overview

This project demonstrates how HashiCorp Vault can be used to securely store, retrieve, update, and manage application secrets.

The practical exercise uses Docker to run Vault in development mode. It explores two versions of the Key-Value (KV) secrets engine: KV v1 and KV v2.

The project uses demonstration credentials only. No real application passwords or production credentials are used.

## 2. Project Objectives

The objectives of this exercise are to:

- Understand the purpose of HashiCorp Vault.
- Set up a Vault development environment using Docker.
- Explore the KV v1 and KV v2 secrets engines.
- Store and retrieve sample application credentials.
- Update secrets and retrieve previous versions.
- Inspect secret metadata.
- Understand why secrets should not be committed to GitHub.
- Document the commands and practical results.

## 3. Technologies Used

- Windows
- Visual Studio Code
- Docker Desktop
- HashiCorp Vault
- PowerShell
- Git and GitHub

## 4. What Is HashiCorp Vault?

HashiCorp Vault is a secrets management tool used to protect sensitive information such as passwords, API keys, database credentials, and application tokens.

Instead of storing sensitive credentials directly in application code or configuration files, applications can retrieve them securely from Vault.

### Why Vault is important

- Protects sensitive credentials.
- Centralizes secrets management.
- Controls access to stored secrets.
- Supports secret versioning with KV v2.
- Helps prevent accidental exposure of credentials.

## 5. Vault Development Environment

Vault was deployed using Docker Desktop in development mode.

The development environment was used for learning and testing purposes only.

**Important:** Vault development mode is not suitable for production because it uses an automatically initialized, in-memory environment and development credentials.

The Vault web interface is accessible locally at:

`http://localhost:8200`

## 6. Understanding KV v1 and KV v2

The Key-Value secrets engine stores information as key-value pairs.

### KV v1

KV v1 stores secrets but does not provide built-in secret version history.

In this exercise, the following sample credentials were stored:

- Username: demo-user
- Password: demonstration password

The secret was stored at:

`kv-v1/devops-app`

### KV v2

KV v2 supports secret versioning. When a secret is updated, Vault retains previous versions according to its configuration.

In this exercise:

- Version 1 was created.
- The password was updated.
- Version 2 was created.
- Version 1 was retrieved again.
- Metadata was inspected.

The secret was stored at:

`kv-v2/devops-app`

### Main difference

KV v1 provides basic key-value secret storage, while KV v2 adds version management and metadata capabilities.

## 7. Practical Work and Results

The following activities were completed:

1. Enabled the KV v1 secrets engine.
2. Enabled the KV v2 secrets engine.
3. Stored sample application credentials in KV v1.
4. Retrieved the stored KV v1 credentials.
5. Stored sample credentials in KV v2.
6. Updated the KV v2 password.
7. Retrieved the previous version of the KV v2 secret.
8. Inspected secret metadata and version history.
9. Created a `.gitignore` file to help prevent accidental exposure of sensitive local files.

The terminal outputs confirmed successful secret storage and retrieval, including the creation of two KV v2 secret versions.

## 8. Security Best Practices

Secrets should never be committed directly to a public GitHub repository.

Exposing credentials can allow unauthorized users to access applications, databases, and infrastructure.

Security practices followed in this exercise include:

- Using demonstration credentials rather than real passwords.
- Keeping local environment files out of Git.
- Adding secret-related files to `.gitignore`.
- Using Vault as a centralized secrets management system.
- Avoiding the use of development-mode credentials in production.

The `.gitignore` file includes rules for environment files, Vault-related local files, and credential files.

**Note:** `.gitignore` helps prevent accidental commits but does not remove files that have already been tracked by Git.

## 9. Conclusion

This practical exercise provided hands-on experience with HashiCorp Vault and application secrets management.

I successfully explored KV v1 and KV v2, stored and retrieved sample credentials, updated secrets, retrieved previous secret versions, and inspected metadata.

The exercise demonstrated the importance of separating sensitive credentials from application source code and using appropriate secrets management tools in DevOps environments.

## 10. Project Status

Practical Vault setup: Completed.

KV v1 demonstration: Completed.

KV v2 demonstration: Completed.

Secret versioning demonstration: Completed.

Metadata inspection: Completed.

Git protection rules: Added.

Documentation: In progress.
