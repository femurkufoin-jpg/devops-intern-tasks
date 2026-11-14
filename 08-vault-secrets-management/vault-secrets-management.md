\# Task 8: Vault Secrets Management



\## Day 1 – Vault Setup, Secret Storage and Access Control



\### 1. Objective



The objective of this task was to understand HashiCorp Vault and practise managing application secrets securely. The exercise covered Vault setup, secret storage, retrieval, versioning, policies and access control.



\### 2. Environment and Tools



\- Operating System: Windows 11

\- Terminal: Windows PowerShell

\- Container Runtime: Docker Desktop

\- Vault Image: `hashicorp/vault:latest`

\- Vault Version: 2.2.2 (as reported by the running container)

\- Vault Address: `http://127.0.0.1:8200`

\- Secret Engine: KV (Key-Value) version 2

\- Repository: `devops-intern-tasks`



\### 3. Starting Vault with Docker



Started Vault in development mode using Docker:



```powershell

docker run -d --name vault-dev --cap-add=IPC\_LOCK -p 127.0.0.1:8200:8200 -e VAULT\_DEV\_ROOT\_TOKEN\_ID=dev-only-token hashicorp/vault:latest

```



Verified that the container was running:



```powershell

docker ps --filter name=vault-dev

```



Checked the Vault status:



```powershell

docker exec vault-dev sh -c "VAULT\_ADDR=http://127.0.0.1:8200 vault status"

```



\*\*Verified result:\*\*

\- Vault was initialized.

\- Vault was unsealed.

\- Storage type was in-memory.

\- HA was disabled.

\- Vault version reported as 2.2.2.



The Vault server was successfully started and made accessible locally.



\### 4. Inspecting Secret Engines and Authentication



Listed the enabled secret engines:



```powershell

docker exec vault-dev sh -c "VAULT\_ADDR=http://127.0.0.1:8200 vault secrets list"

```



Identified the KV secret engine mounted at `secret/`.



Listed enabled authentication methods:



```powershell

docker exec vault-dev sh -c "VAULT\_ADDR=http://127.0.0.1:8200 vault auth list"

```



The token authentication method was enabled.



\### 5. Storing and Retrieving Secrets



Stored a practice application username and password:



```powershell

docker exec vault-dev sh -c "VAULT\_ADDR=http://127.0.0.1:8200 vault kv put secret/devops-app username=devops-user password=<practice-password>"

```



Vault successfully created Version 1.



Retrieved the stored secret:



```powershell

docker exec vault-dev sh -c "VAULT\_ADDR=http://127.0.0.1:8200 vault kv get secret/devops-app"

```



\*\*Verified result:\*\* The stored username and password were successfully retrieved.



\### 6. Updating Secrets and Versioning



Updated the application credentials:



```powershell

docker exec vault-dev sh -c "VAULT\_ADDR=http://127.0.0.1:8200 vault kv put secret/devops-app username=devops-admin password=<updated-practice-password>"

```



\*\*Verified result:\*\* Vault created Version 2.



Retrieved the original Version 1:



```powershell

docker exec vault-dev sh -c "VAULT\_ADDR=http://127.0.0.1:8200 vault kv get -version=1 secret/devops-app"

```



The original credentials were successfully retrieved.



Inspected the secret metadata and version history:



```powershell

docker exec vault-dev sh -c "VAULT\_ADDR=http://127.0.0.1:8200 vault kv metadata get secret/devops-app"

```



\*\*Verified result:\*\*

\- Current version: 2

\- Version 1: Created successfully and not destroyed.

\- Version 2: Updated successfully and not destroyed.

\- Both versions were visible in the metadata output.



\### 7. Creating a Read-Only Vault Policy



Created a local policy directory and policy file:



```powershell

New-Item -ItemType Directory -Force vault-policies

notepad vault-policies\\devops-readonly.hcl

```



Policy configuration:



```hcl

path "secret/data/devops-app" {

&#x20; capabilities = \["read"]

}

```



Uploaded the policy to Vault using a PowerShell-compatible command:



```powershell

Get-Content .\\vault-policies\\devops-readonly.hcl -Raw | docker exec -i vault-dev sh -c "VAULT\_ADDR=http://127.0.0.1:8200 vault policy write devops-readonly -"

```



\*\*Verified result:\*\* Vault successfully uploaded the `devops-readonly` policy.



Read the policy back:



```powershell

docker exec vault-dev sh -c "VAULT\_ADDR=http://127.0.0.1:8200 vault policy read devops-readonly"

```



The returned policy matched the local HCL configuration.



\### 8. Creating and Testing a Restricted Token



Created a token associated with the read-only policy:



```powershell

docker exec vault-dev sh -c "VAULT\_ADDR=http://127.0.0.1:8200 vault token create -policy=devops-readonly"

```



Used the generated token to retrieve the application secret:



```powershell

docker exec vault-dev sh -c "VAULT\_ADDR=http://127.0.0.1:8200 VAULT\_TOKEN=<restricted-token> vault kv get secret/devops-app"

```



\*\*Verified result:\*\* The restricted token successfully retrieved the secret.



Tested whether the same token could update the secret:



```powershell

docker exec vault-dev sh -c "VAULT\_ADDR=http://127.0.0.1:8200 VAULT\_TOKEN=<restricted-token> vault kv put secret/devops-app username=test-user password=<test-password>"

```



\*\*Verified result:\*\* Vault rejected the update request with HTTP 403 – permission denied.



This confirmed that the policy allowed reading but prevented updating the secret.



\### 9. Listing Vault Policies



Listed the policies registered in Vault:



```powershell

docker exec vault-dev sh -c "VAULT\_ADDR=http://127.0.0.1:8200 vault policy list"

```



\*\*Verified output included:\*\*

\- `default`

\- `default-ceiling`

\- `devops-readonly`

\- `root`



\### 10. Challenges and Troubleshooting



\*\*Challenge 1: Vault CLI connection protocol\*\*



The initial status command attempted an HTTPS connection while the development server was using HTTP.



\*\*Resolution:\*\* Explicitly set `VAULT\_ADDR=http://127.0.0.1:8200` when running Vault CLI commands inside the container.



\*\*Challenge 2: PowerShell input redirection\*\*



The initial policy upload command used `<` input redirection, which PowerShell does not support in that form.



\*\*Resolution:\*\* Used `Get-Content -Raw` and piped the policy contents into `docker exec -i`.



\*\*Challenge 3: Understanding Vault permissions\*\*



A restricted token needed to be tested to confirm that the policy actually enforced read-only access.



\*\*Resolution:\*\* Successfully tested secret retrieval and confirmed that an update attempt returned HTTP 403.



\### 11. Security Considerations



\- The exercise used Vault development mode and in-memory storage.

\- Development mode is intended for learning and testing, not production use.

\- Practice credentials and development tokens must not be reused as real application credentials.

\- Sensitive tokens, passwords and unseal keys must never be committed to GitHub.

\- Production Vault deployments require appropriate storage, TLS, authentication, access policies and secure key management.



\### 12. Day 1 Outcome



Successfully deployed Vault locally using Docker and practised secret management operations. Stored, retrieved and updated application credentials, inspected secret version history, created a read-only policy, generated a restricted token and verified that Vault allowed read access while denying unauthorized updates.



\*\*Day 1 status: Completed.\*\*



\### 13. Day 2 – Planned Activities



\- Continue practising Vault secret management.

\- Explore policy-based access control further.

\- Practise token management and authentication.

\- Perform additional access-control tests.

\- Document verified results and troubleshooting.

\- Commit and push the completed assignment to GitHub.
---

# Day 2 – Vault Token Lifecycle and Secret Lifecycle Management

## 1. Objective

The objective of Day 2 was to practise Vault token lifecycle management and understand how to manage secret versions securely. The exercises covered token inspection, renewal, revocation, access verification, soft deletion, recovery and permanent destruction.

## 2. Environment

- Operating System: Windows 11
- Terminal: Windows PowerShell
- Container Runtime: Docker Desktop
- Vault Container: `vault-dev`
- Vault Address: `http://127.0.0.1:8200`
- Secret Engine: KV Version 2

Verified that the Vault container was still running:

```powershell
docker ps --filter name=vault-dev
```

The container was running successfully, and the Day 1 Vault configuration remained available.

## 3. Inspecting the Root Token

Inspected the token currently used by the Vault CLI inside the container:

```powershell
docker exec vault-dev sh -c "VAULT_ADDR=http://127.0.0.1:8200 vault token lookup"
```

**Verified results:**
- Policy: `root`
- Token type: `service`
- Renewable: `false`
- TTL: `0s`
- Orphan: `true`

This demonstrated that the development root token has administrative permissions and is not renewable.

## 4. Inspecting the Restricted Token

Inspected the restricted token created during Day 1:

```powershell
docker exec vault-dev sh -c "VAULT_ADDR=http://127.0.0.1:8200 VAULT_TOKEN=<restricted-token> vault token lookup"
```

**Verified results:**
- Policies: `default` and `devops-readonly`
- Token type: `service`
- Renewable: `true`
- Creation TTL: `768h`
- Token had a valid expiration time.

This confirmed that the token inherited the intended read-only policy.

## 5. Token Renewal

Renewed the restricted token:

```powershell
docker exec vault-dev sh -c "VAULT_ADDR=http://127.0.0.1:8200 VAULT_TOKEN=<restricted-token> vault token renew"
```

**Verified result:**

Vault successfully renewed the token.

Vault returned a TTL warning because the requested duration of 768 hours exceeded the effective maximum TTL at the time of renewal. The duration was automatically capped.

Inspected the token again:

```powershell
docker exec vault-dev sh -c "VAULT_ADDR=http://127.0.0.1:8200 VAULT_TOKEN=<restricted-token> vault token lookup"
```

The output contained a `last_renewal` timestamp and confirmed that the token remained renewable.

## 6. Token Revocation

Revoked the restricted token:

```powershell
docker exec vault-dev sh -c "VAULT_ADDR=http://127.0.0.1:8200 VAULT_TOKEN=<restricted-token> vault token revoke -self"
```

**Verified result:**

```text
Success! Revoked token (if it existed)
```

Attempted to retrieve the secret using the revoked token:

```powershell
docker exec vault-dev sh -c "VAULT_ADDR=http://127.0.0.1:8200 VAULT_TOKEN=<revoked-token> vault kv get secret/devops-app"
```

Vault returned HTTP 403 with `permission denied` and `invalid token`.

This confirmed that the revoked token could no longer authenticate.

## 7. Creating and Testing a Replacement Token

Created a fresh restricted token:

```powershell
docker exec vault-dev sh -c "VAULT_ADDR=http://127.0.0.1:8200 vault token create -policy=devops-readonly"
```

Inspected the new token:

```powershell
docker exec vault-dev sh -c "VAULT_ADDR=http://127.0.0.1:8200 VAULT_TOKEN=<new-restricted-token> vault token lookup"
```

**Verified results:**
- Policies: `default` and `devops-readonly`
- Renewable: `true`
- Token type: `service`
- Token had a valid TTL.

Tested secret retrieval:

```powershell
docker exec vault-dev sh -c "VAULT_ADDR=http://127.0.0.1:8200 VAULT_TOKEN=<new-restricted-token> vault kv get secret/devops-app"
```

**Verified result:** The replacement restricted token successfully retrieved Version 2 of the application secret.

## 8. Soft-Deleting a Secret Version

Inspected the secret metadata:

```powershell
docker exec vault-dev sh -c "VAULT_ADDR=http://127.0.0.1:8200 vault kv metadata get secret/devops-app"
```

Confirmed that Versions 1 and 2 were available and neither was destroyed.

Soft-deleted Version 2:

```powershell
docker exec vault-dev sh -c "VAULT_ADDR=http://127.0.0.1:8200 vault kv delete -versions=2 secret/devops-app"
```

**Verified result:** Vault successfully processed the deletion request.

Inspected the metadata again and confirmed:
- Version 2 had a deletion timestamp.
- `destroyed` remained `false`.
- Version 1 remained untouched.

## 9. Recovering a Soft-Deleted Version

Recovered Version 2:

```powershell
docker exec vault-dev sh -c "VAULT_ADDR=http://127.0.0.1:8200 vault kv undelete -versions=2 secret/devops-app"
```

**Verified result:** Vault successfully processed the undelete operation.

Retrieved Version 2:

```powershell
docker exec vault-dev sh -c "VAULT_ADDR=http://127.0.0.1:8200 vault kv get -version=2 secret/devops-app"
```

The original Version 2 data was successfully retrieved. Its deletion time returned to `n/a`, confirming recovery.

## 10. Permanently Destroying a Secret Version

Permanently destroyed Version 1:

```powershell
docker exec vault-dev sh -c "VAULT_ADDR=http://127.0.0.1:8200 vault kv destroy -versions=1 secret/devops-app"
```

**Verified result:** Vault successfully processed the permanent destruction request.

Inspected the metadata:

```powershell
docker exec vault-dev sh -c "VAULT_ADDR=http://127.0.0.1:8200 vault kv metadata get secret/devops-app"
```

The output confirmed:
- Version 1: `destroyed: true`
- Version 2: `destroyed: false`

Version 1 was permanently destroyed and could no longer be recovered.

## 11. Final Secret Verification

Retrieved the current secret:

```powershell
docker exec vault-dev sh -c "VAULT_ADDR=http://127.0.0.1:8200 vault kv get secret/devops-app"
```

**Verified result:**
- Current version: 2
- Destroyed: `false`
- Deletion time: `n/a`
- Secret retrieval: successful.

This confirmed that permanently destroying Version 1 did not affect Version 2.

## 12. Day 2 Challenges and Troubleshooting

- Understanding the difference between the root token and a restricted token.
- Interpreting Vault's TTL warning during token renewal.
- Verifying that token revocation prevents further access.
- Understanding the differences between soft deletion, recovery and permanent destruction.
- Confirming that permanent destruction of one version does not affect another version.

These exercises were completed successfully through Vault CLI commands and metadata inspection.

## 13. Security Considerations

- Root tokens should be reserved for administrative operations.
- Application tokens should follow the principle of least privilege.
- Tokens should be revoked when they are no longer needed or are compromised.
- Soft deletion and permanent destruction have different recovery implications.
- Real passwords, tokens and other sensitive credentials must not be committed to GitHub.
- Vault development mode and in-memory storage are suitable for learning, not production deployments.

## 14. Day 2 Outcome

Successfully practised Vault token lifecycle management, including inspection, renewal and revocation. Created a replacement restricted token and verified its access permissions.

Also demonstrated KV Version 2 secret lifecycle management by soft-deleting Version 2, recovering it, permanently destroying Version 1 and verifying that Version 2 remained accessible.

**Day 2 practical exercises: Completed.**

## 15. Overall Task 8 Status

The two-day Vault Secrets Management assignment covered:

- Vault deployment using Docker.
- Secret storage and retrieval.
- KV Version 2 secret versioning.
- Vault policies and restricted tokens.
- Token inspection, renewal and revocation.
- Soft deletion, recovery and permanent destruction.
- Access-control verification.
- Documentation of commands, results and troubleshooting.

**Practical work: Completed.**

**Documentation: Day 2 update recorded; final GitHub submission pending.**

