# Task 7: Nomad Job Specifications

## Day 1: Understanding and Preparing Nomad Job Specifications

### Objective
Understand Nomad job specifications, prepare the Nomad environment,
and create and validate an Nginx job specification.

### Activities Completed

1. Reviewed the purpose of HashiCorp Nomad and its role in workload
   scheduling and orchestration.
2. Checked the Nomad installation and version.
3. Started a Nomad development agent in Ubuntu WSL2.
4. Confirmed that the Nomad client was ready and eligible.
5. Confirmed that the Docker driver was detected as healthy.
6. Created an Nginx job specification using HCL.
7. Validated the job specification successfully.
8. Ran a scheduling plan to check whether Nomad could allocate
   the requested task.

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

Command:
`nomad job validate 07-nomad-job-specifications/nginx-app.nomad.hcl`

Result: Job validation successful.

Command:
`nomad job plan 07-nomad-job-specifications/nginx-app.nomad.hcl`

Result: All tasks successfully allocated in the scheduler dry-run.

### Troubleshooting

The initial Nomad agent running in Windows detected the Docker
driver as unhealthy because Docker Desktop was configured to use
Linux containers.

Rather than switching Docker Desktop to Windows containers,
I started the Nomad development agent inside Ubuntu WSL2, where
the Docker driver was detected as healthy.

This allowed Nomad to validate the job and successfully plan
the task allocation.

### Day 1 Outcome

Successfully prepared the Nomad environment and created, validated,
and planned an Nginx job specification.

The Nginx job has not yet been submitted or deployed.
Deployment, allocation inspection, application testing, and job
cleanup are reserved for Day 2.
