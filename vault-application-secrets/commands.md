# HashiCorp Vault – Commands and Explanations

## 1. Docker and Vault Environment

### Check Docker version

```powershell
docker --version
```

**Meaning:** Displays the installed Docker version.

**Purpose:** Confirms that Docker is installed and available.

### Check running containers

```powershell
docker ps
```

**Meaning:** Lists currently running Docker containers.

**Purpose:** Confirms whether the Vault container is running.

### Inspect Vault secrets engines

```powershell
docker exec -e VAULT_ADDR=http://127.0.0.1:8200 -e VAULT_TOKEN=dev-only-token vault-dev vault secrets list -detailed
```

**Meaning:** Executes the Vault CLI inside the running `vault-dev` container and displays the enabled secrets engines.

**Purpose:** Checks which secrets engines are available and their configurations.

---

## 2. Enable KV v1

```powershell
docker exec -e VAULT_ADDR=http://127.0.0.1:8200 -e VAULT_TOKEN=dev-only-token vault-dev vault secrets enable -path=kv-v1 kv
```

**Meaning:** Enables a Key-Value version 1 secrets engine at the mount path `kv-v1`.

**Purpose:** Allows Vault to store and retrieve basic key-value secrets.

**Important:** KV v1 does not provide built-in secret version history.

## 3. Enable KV v2

```powershell
docker exec -e VAULT_ADDR=http://127.0.0.1:8200 -e VAULT_TOKEN=dev-only-token vault-dev vault secrets enable -path=kv-v2 kv-v2
```

**Meaning:** Enables a Key-Value version 2 secrets engine at the mount path `kv-v2`.

**Purpose:** Allows Vault to store secrets and maintain version history.

---

## 4. Store Secrets in KV v1

```powershell
docker exec -e VAULT_ADDR=http://127.0.0.1:8200 -e VAULT_TOKEN=dev-only-token vault-dev vault kv put kv-v1/devops-app username="demo-user" password="<DEMO_PASSWORD>"
```

**Meaning:** Stores a username and demonstration password in the KV v1 secrets engine.

**Purpose:** Demonstrates how application credentials can be stored in Vault rather than directly in application source code.

## 5. Retrieve Secrets from KV v1

```powershell
docker exec -e VAULT_ADDR=http://127.0.0.1:8200 -e VAULT_TOKEN=dev-only-token vault-dev vault kv get kv-v1/devops-app
```

**Meaning:** Retrieves the stored credentials from the specified secret path.

**Purpose:** Confirms that the secret was successfully stored and can be retrieved.

---

## 6. Store Secrets in KV v2

```powershell
docker exec -e VAULT_ADDR=http://127.0.0.1:8200 -e VAULT_TOKEN=dev-only-token vault-dev vault kv put kv-v2/devops-app username="demo-user-v2" password="<DEMO_PASSWORD>"
```

**Meaning:** Creates the first version of a secret in the KV v2 secrets engine.

**Purpose:** Demonstrates secure secret storage with versioning enabled.

## 7. Update a KV v2 Secret

```powershell
docker exec -e VAULT_ADDR=http://127.0.0.1:8200 -e VAULT_TOKEN=dev-only-token vault-dev vault kv put kv-v2/devops-app username="demo-user-v2" password="<UPDATED_DEMO_PASSWORD>"
```

**Meaning:** Writes updated secret data to the same KV v2 path.

**Purpose:** Demonstrates how Vault creates a new version when a secret is updated.

**Expected result:** The secret version increases from Version 1 to Version 2.

---

## 8. Retrieve the Latest Secret Version

```powershell
docker exec -e VAULT_ADDR=http://127.0.0.1:8200 -e VAULT_TOKEN=dev-only-token vault-dev vault kv get kv-v2/devops-app
```

**Meaning:** Retrieves the latest version of the secret.

**Purpose:** Confirms that the updated secret is available.

## 9. Retrieve a Previous Secret Version

```powershell
docker exec -e VAULT_ADDR=http://127.0.0.1:8200 -e VAULT_TOKEN=dev-only-token vault-dev vault kv get -version=1 kv-v2/devops-app
```

**Meaning:** Retrieves Version 1 of the stored secret.

**Purpose:** Demonstrates one of the main benefits of KV v2: the ability to access previous secret versions.

---

## 10. Inspect Secret Metadata

```powershell
docker exec -e VAULT_ADDR=http://127.0.0.1:8200 -e VAULT_TOKEN=dev-only-token vault-dev vault kv metadata get kv-v2/devops-app
```

**Meaning:** Displays metadata associated with the secret.

**Purpose:** Helps inspect secret version information, creation and update timestamps, and other metadata.

---

## 11. Git Protection

### Display the `.gitignore` file

```powershell
Get-Content .gitignore
```

**Meaning:** Displays the contents of the `.gitignore` file.

**Purpose:** Verifies that sensitive local files and environment files are included in the ignore rules.

### Check whether `.gitignore` exists

```powershell
Test-Path .gitignore
```

**Meaning:** Checks whether the specified file exists.

**Purpose:** Confirms that the `.gitignore` file is present in the project directory.

---

## 12. Important Vault Concepts

| Term | Meaning |
|---|---|
| Vault | A secrets management tool |
| Secret | Sensitive information such as a password or API key |
| Secrets engine | A Vault component that stores or manages secrets |
| KV | Key-Value secrets engine |
| KV v1 | Basic key-value secret storage |
| KV v2 | Key-value storage with versioning and metadata |
| Mount path | The path where a secrets engine is enabled |
| Secret path | The location of a particular secret |
| Metadata | Information describing a secret and its versions |
| Versioning | Keeping previous versions of secret data |
| Token | A credential used to authenticate with Vault |

## 13. Important Security Note

The commands above use a development token and demonstration credentials from a local learning environment.

The development token must not be used in production.

Real passwords, API keys, access tokens, and database credentials should never be committed to GitHub. Production environments require secure authentication, appropriate policies, and proper Vault configuration.

## 14. Practical Outcome

The following activities were demonstrated successfully:

- Enabled KV v1 and KV v2.
- Stored sample application credentials.
- Retrieved stored secrets.
- Updated a KV v2 secret.
- Retrieved an earlier secret version.
- Inspected secret metadata.
- Added Git ignore rules to help protect sensitive files.
