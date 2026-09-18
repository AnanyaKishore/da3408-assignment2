# Use of AI

**Tools used:** Claude, ChatGPT


**How they were used:**
1. Generating the template for `Dockerfile.naive` and `Dockerfile.multistage` for question 1 based on the provided examples in the Module 3 Student Handouts. I provided the LLM (Claude) with the files to be copied, how they were organized in my local directory, and instructed it to use python:3.10-slim everywhere instead of python:3.10.
2. To provide an overview of the FastAPI framework to be used in the assignment and to generate the boilerplate code for main.py for question 1. I made the necessary changes based on the assignment requirements (keeping only healthz() and predict() functions as required) and debugged the code with LLM (Claude) assistance.
3. To understand what the Redis cache mechanism is and a brief overview using ChatGPT. Generated the standard boilerplate for docker-compose.yml for question_2 by instructing the LLM to create 2 services, `cache` and `api`, and using the redis image for `cache`, and instructing it to not pull any images for the   `api` service and to instead use the provided Dockerfile.multistage in the compose file.
4. Understanding what nodes, jobs and pods are in the Kubernetes setup. For question 3, I provided the LLM (ChatGPT) with instructions to generate the template for `indexed-job.yaml` such as the parallelism = 4, the backOff limit if a pod fails, and instructed to not pull images from Docker and to instead load into minikube the `shard-validator:v1` image I built.
5. Similarly for question 4, generating the boilerplate deployment.yaml.
6. Assistance with terminal commands:
* Discovering the following command:
`for i in $(kubectl get pods -l job-name=signup-shard-validation -o jsonpath='{.items[*].metadata.name}'); do kubectl logs $i; done`
to print the kubectl logs including the shard index, the pod name, the node which ran the pod and the total and invalid counts per shard csv file

* And, a basic explanation of some `kubectl` and `curl` commands I was unfamiliar with, including:
1. `kubectl get pods -l app=spam-api`: gives information about the pods belonging to the spam-api deployment
2. `time curl -s -X POST http://localhost:5000/predict -H "Content-Type: application/json" -d '{"text":"Congrats! So proud of you!"}'`: lets you time your curl command to fetch data, and prints the time taken


**Impact:**

LLMs greatly reduced the time I would have otherwise spent writing the required Python scripts, allowing me greater freedom to figure out how to work with the terminal commands for the assignment.