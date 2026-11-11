# Task 7: Nomad Job Specifications

## Day 1: Understanding and Preparing Nomad Job Specifications

### Objective
Understand Nomad job specifications, prepare the Nomad environment, and create and validate an Nginx job specification.

### Activities Completed

1. Reviewed the purpose of HashiCorp Nomad and its role in workload scheduling and orchestration.
2. Checked the Nomad installation and version.
3. Started a Nomad development agent in Ubuntu WSL2.
4. Confirmed that the Nomad client was ready and eligible.
5. Confirmed that the Docker driver was detected as healthy.
6. Created an Nginx job specification using HCL.
7. Validated the job specification successfully.
8. Ran a scheduling plan to check whether Nomad could allocate the requested task.

### Job Specification

File: `nginx-app.nomad.hcl`

The job defines:
- Job name: nginx-app
- Datacenter: dc1
- Job type: service
- Task group: nginx-group
- Number of instances: 1
- Task name: nginx
- Driver: docker
- Image: nginx:alpine
- Container port: 80
- CPU allocation: 100 MHz
- Memory allocation: 128 MB

### Validation Results

**Command:**

`nomad job validate 07-nomad-job-specifications/nginx-app.nomad.hcl`

**Result:** Job validation successful.

**Command:**

`nomad job plan 07-nomad-job-specifications/nginx-app.nomad.hcl`

**Result:** All tasks successfully allocated in the scheduler dry-run.

### Troubleshooting

The initial Nomad agent running in Windows detected the Docker driver as unhealthy because Docker Desktop was configured to use Linux containers.

Rather than switching Docker Desktop to Windows containers, I started the Nomad development agent inside Ubuntu WSL2, where the Docker driver was detected as healthy.

This allowed Nomad to validate the job and successfully plan the task allocation.

### Day 1 Outcome

Successfully prepared the Nomad environment and created, formatted, validated, and planned an Nginx job specification.

The Nginx job was not submitted or deployed on Day 1.

---

## Day 2: Deploying and Managing the Nomad Job

### Objective

Deploy the Nginx application using Nomad, inspect its allocation, verify application accessibility, and safely stop the job.

### Activities Completed

1. Synchronized the local main branch with GitHub.
2. Created a new feature branch named `feature/nomad-job-specifications-day2`.
3. Verified that the Nomad server and client were running.
4. Confirmed that Docker was using Linux containers.
5. Submitted the Nginx job specification using Nomad.
6. Inspected the job status and allocation details.
7. Identified the dynamically assigned host port.
8. Tested the Nginx application using curl.
9. Verified that Nomad created and managed the Nginx Docker container.
10. Stopped the Nomad job and confirmed that its container was removed.

### 1. Environment Verification

Checked the Nomad server:

`nomad status`

Result: Nomad responded successfully, with no running jobs before deployment.

Checked the Nomad client:

`nomad node status`

Result: The Ubuntu WSL2 Nomad client was ready and eligible.

Checked Docker:

`docker info --format '{{.OSType}}'`

Result: Linux.

Also checked existing Docker containers using:

`docker ps`

The existing Flask, Redis, and Caddy containers were running. These containers were left untouched throughout the exercise.

### 2. Nginx Job Deployment

**Command:**

`nomad job run 07-nomad-job-specifications/nginx-app.nomad.hcl`

**Result:** Deployment successful.

Deployment details:

- Job name: `nginx-app`
- Task group: `nginx-group`
- Desired instances: 1
- Placed instances: 1
- Healthy instances: 1
- Unhealthy instances: 0
- Allocation ID: `8c3581f7`
- Deployment status: successful

### 3. Job Status Inspection

**Command:**

`nomad job status nginx-app`

**Result:**

- Job status: running
- Task group: nginx-group
- Running instances: 1
- Failed instances: 0
- Latest deployment: successful

### 4. Allocation Inspection

**Command:**

`nomad alloc status 8c3581f7`

Results:

- Allocation status: running
- Deployment health: healthy
- Task name: nginx
- CPU allocation: 100 MHz
- Memory allocation: 128 MB
- Actual memory usage at inspection: 2.6 MiB
- Restarts: 0
- Dynamic host port: 23712
- Container port: 80

The allocation showed the following port mapping:

`127.0.0.1:23712 -> 80`

This means Nomad dynamically assigned port 23712 on the host and mapped it to port 80 inside the Nginx container.

### 5. Application Testing

**Command:**

`curl http://127.0.0.1:23712`

**Result:** Successfully returned the default Nginx welcome page.

The response included:

`Welcome to nginx!`

This confirmed that the Nginx web server was running and accessible through the dynamically assigned port.

### 6. Docker Container Verification

**Command:**

`docker ps`

Confirmed that Nomad created the Nginx container.

Container details:

- Image: `nginx:alpine`
- Container ID: `12b1dff1f8ec`
- Container name: `nginx-8c3581f7-3d79-b794-65b5-3878f3e12ea2`
- Status: running
- Port mapping: `127.0.0.1:23712 -> 80`

The existing Flask, Redis, and Caddy containers remained running.

### 7. Job Cleanup

After successful deployment and application testing, the Nginx job was stopped through Nomad.

**Command:**

`nomad job stop nginx-app`

**Result:** Job stopped successfully.

Verified the final job status:

`nomad job status nginx-app`

Results:

- Job status: dead (stopped)
- Allocation status: complete
- Desired allocation status: stop

Finally, checked Docker containers:

`docker ps`

Confirmed that the Nomad-managed Nginx container had been removed, while the existing Flask, Redis, and Caddy containers remained running.

### Day 2 Outcome

Successfully deployed, inspected, tested, and stopped an Nginx application using HashiCorp Nomad.

Verified that the application was accessible through its dynamically assigned port, confirmed the allocation was healthy, and safely cleaned up the Nomad-managed container without affecting other running Docker workloads.

---

## Overall Task 7 Conclusion

Successfully completed the two-day Nomad Job Specifications exercise.

Day 1 focused on preparing the Nomad environment, understanding job specifications, creating the Nginx HCL configuration, formatting it, validating it, and confirming that the scheduler could allocate the task.

Day 2 focused on deploying the Nginx application, inspecting job and allocation status, testing the application, verifying the Docker container, and safely stopping the job.

The exercise provided practical experience with HashiCorp Nomad, HCL job specifications, Docker integration, workload scheduling, allocation management, dynamic port mapping, application verification, and job cleanup.

All Day 1 deliverables were committed, pushed, and merged into the main branch. Day 2 implementation and documentation are prepared on the `feature/nomad-job-specifications-day2` branch for review and submission.
