# DA3408 - Assignment 2

## Structure
```text
da3408-assignment2/
├── question_1/
│   ├── Dockerfile.multistage
│   ├── Dockerfile.naive
│   ├── generate_dataset.py
│   ├── main.py
│   ├── requirements-serve.txt
│   ├── requirements-train.txt
│   └── train.py
├── question_2/
│   ├── docker-compose.yml
│   ├── Dockerfile.multistage
│   ├── evidence_script.py
│   ├── generate_dataset.py
│   ├── main.py
│   ├── requirements-serve.txt
│   ├── requirements-train.txt
│   └── train.py
├── question_3/
│   ├── shards/
│   ├── Dockerfile
│   ├── generate_shards.py
│   ├── indexed-job.yaml
│   └── validate.py
├── question_4/
│   ├── deployment.yaml
│   └── service.yaml
├── .gitignore
├── AI_DISCLOSURE.md
├── README.md
└── Report_DA3408_Assignment2.pdf
```
The final report is **Report_DA3408_Assignment2.pdf**. All the required evidence and explanations can be found here.

## To run the experiments:

```bash
git clone https://github.com/AnanyaKishore/da3408-assignment2.git
cd da3408-assignment2
```
---

# Question 1

Please note that both **Dockerfile.naive** and **Dockerfile.multistage** use **python:3.10-slim** to build their images. Using python:3.10 to build the naive image and python:3.10-slim to build the multi-stage image would unnecessarily inflate disk usage for the naive image **(2.09 GB)**, instead showing an artificially large **71.57%** reduction when packaged as a multi-stage image.

Commands to rerun the experiment on your terminal:

```bash
cd question_1
docker build -t spam-naive -f Dockerfile.naive .
docker images spam-naive
docker build -t spam-multistage -f Dockerfile.multistage .
docker images spam-multistage:latest
docker run -d --name spam-naive-classifier -p 5000:5000 spam-naive
curl http://localhost:5000/healthz
curl -X POST http://localhost:5000/predict -H "Content-Type: application/json" -d '{"text":"Hey, are we still meeting today about the laptop?"}'
curl -X POST http://localhost:5000/predict -H "Content-Type: application/json" -d '{"text":"WIN a FREE iPhone now! Click here: bit.ly/xyz123"}'
docker stop spam-naive-classifier
docker rm spam-naive-classifier
docker run -d --name spam-multi-classifier -p 5000:5000 spam-multistage
curl http://localhost:5000/healthz
curl -X POST http://localhost:5000/predict -H "Content-Type: application/json" -d '{"text":"Hey, are we still meeting today about the laptop?"}'
curl -X POST http://localhost:5000/predict -H "Content-Type: application/json" -d '{"text":"WIN a FREE iPhone now! Click here: bit.ly/xyz123"}'
docker stop spam-multi-classifier
docker rm spam-multi-classifier
docker ps
```
---

# Question 2

```bash
cd question_2
docker compose build
docker compose up -d
docker compose ps
docker compose logs -f api
curl http://localhost:5000/healthz
python3 evidence_script.py # script to show cache hit, cache miss and time differences
# we can also directly check from the terminal instead of running the script:
time curl -s -X POST http://localhost:5000/predict -H "Content-Type: application/json" -d '{"text":"WIN a FREE iPhone now! Click here: bit.ly/xyz123"}'
time curl -s -X POST http://localhost:5000/predict -H "Content-Type: application/json" -d '{"text":"WIN a FREE iPhone now! Click here: bit.ly/xyz123"}'
time curl -s -X POST http://localhost:5000/predict -H "Content-Type: application/json" -d '{"text":"Congrats! So proud of you!"}'
time curl -s -X POST http://localhost:5000/predict -H "Content-Type: application/json" -d '{"text":"WIN a FREE iPhone now! Click here: bit.ly/xyz123"}'
time curl -s -X POST http://localhost:5000/predict -H "Content-Type: application/json" -d '{"text":"Congrats! So proud of you!"}'
docker compose down
```
---

# Question 3

```bash
cd question_3
python3 generate_shards.py
minikube start --nodes=2 --cpus=2 --memory=4000
kubectl get nodes -o wide
docker build -t shard-validator:v1 .
minikube image load shard-validator:v1
minikube image ls | grep shard-validator
kubectl apply -f indexed-job.yaml
kubectl get pods -o wide -w
for i in $(kubectl get pods -l job-name=signup-shard-validation -o jsonpath='{.items[*].metadata.name}'); do
  kubectl logs $i
done
kubectl delete -f indexed-job.yaml
```
---

# Question 4

```bash
cd question_4
docker build -t spam-multistage:v1 -f ../question_1/Dockerfile.multistage ../question_1
minikube image load spam-multistage:v1
kubectl get nodes -o wide
kubectl apply -f deployment.yaml
kubectl apply -f service.yaml
kubectl get svc spam-api-svc
kubectl get pods -l app=spam-api
kubectl delete pod spam-api-b7cddf48d-nqnlc # the pod I chose to delete
kubectl get pods -l app=spam-api
# add "version" :"v2" to the JSON response at question_1/main.py under the healthz() function
docker build -t spam-multistage:v2 -f ../question_1/Dockerfile.multistage ../question_1
minikube image load spam-multistage:v2
kubectl set image deployment/spam-api spam-api=spam-multistage:v2
kubectl rollout status deployment/spam-api
kubectl rollout history deployment/spam-api
kubectl delete -f .
```
---

Author: Ananya Kishore (DA24B035)