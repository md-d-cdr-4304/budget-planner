# Budget Planner — Kubernetes Microservices

A comprehensive, production-ready microservices application for personal budget management. Deploy on Kubernetes with persistent storage, JWT authentication, and a modern web interface.

It includes a responsive web UI, two backend services, an auth service backed by MongoDB, and persistent storage for data reliability.

## Repository Layout

```
budget-planner/
├── auth_service/                 # Authentication microservice
│   ├── app.py                   # Flask application with JWT
│   ├── requirements.txt         # Python dependencies
│   ├── Dockerfile              # Container configuration
│   └── k8s/                    # Kubernetes manifests
├── budget_service/              # Budget management microservice
│   ├── app.py                  # Flask application with web UI
│   ├── templates/              # Jinja2 templates
│   ├── static/                 # CSS, JS, assets
│   ├── requirements.txt        # Python dependencies
│   ├── Dockerfile             # Container configuration
│   └── k8s/                   # Kubernetes manifests
├── k8s/                        # Shared Kubernetes resources
│   ├── budget-planner-complete.yaml  # Complete deployment
│   └── mongo-deployment.yaml   # MongoDB configuration
├── docker-compose.yml          # Local development setup
└── README.md                  # This file
```

## Microservices

**budget-service** — Python Flask; web UI + REST API for budget/expense management. Exposed via NodePort for browser access.

**auth-service** — Python Flask; JWT-based authentication with bcrypt password hashing.

**mongodb** — MongoDB 6; user data and budget storage with PersistentVolumeClaim (PVC).

All services communicate in-cluster; budget-service is exposed to your machine for the web interface.

## Architecture

```
                +---------------------------+
  Browser  ---> |  budget-service (UI+API)  |   (NodePort :30000)
                +-----------+---------------+
                            |
                            v
                  +---------+---------+             +------------------+
                  |  auth-service     |  <---->     | MongoDB (mongo:6)|
                  |  (Flask + JWT)    |   Auth      |  (PVC Storage)   |
                  +-------------------+             +------------------+
```

## Patterns Used

- **Stateless microservices** (easy to scale independently with HPA)
- **Database-per-service** (auth owns MongoDB, budget service manages its data)
- **Persistent storage** (PVC) for MongoDB across pod restarts
- **External access** via NodePort (no ingress required)
- **JWT authentication** with refresh tokens and rate limiting
- **Modern web UI** with dark mode, search, filtering, and data visualization

## Public Images

- `dilshaan/budget-planner-auth:latest`
- `dilshaan/budget-planner-budget:latest`
- `mongo:latest`

## Prerequisites

**Windows (preferred for grading):**
- Docker Desktop with Kubernetes enabled (Settings ▸ Kubernetes ▸ Enable Kubernetes)
- kubectl in PATH (Docker Desktop provides one)
- PowerShell or CMD

**macOS (alternative):**
- Docker Desktop (or any Docker daemon)
- minikube + kubectl

**Linux:**
- Docker + minikube/k3s
- kubectl

> **Tip:** Do not run `kubectl apply -f .` from the repository root. Apply only the files in the `k8s/` folder.

## Quick Start — Windows (Docker Desktop Kubernetes)

From the project root where the `k8s` folder is:

```powershell
# 1) Select Docker Desktop's cluster
kubectl config use-context docker-desktop
kubectl get nodes

# 2) Apply complete deployment
kubectl apply -f .\k8s\budget-planner-complete.yaml

# 3) Wait for pods to be Ready
kubectl -n budget-planner wait --for=condition=available deploy --all --timeout=300s
kubectl -n budget-planner get pods -o wide

# 4) Get the application URL
kubectl -n budget-planner get svc budget-nodeport -o jsonpath="{.spec.ports[0].nodePort}{'\n'}"

# 5) Open the app
start http://127.0.0.1:30000
```

## Quick Start — macOS (minikube)

```bash
# 1) Start minikube (Docker driver)
minikube start

# 2) Apply complete deployment
kubectl apply -f k8s/budget-planner-complete.yaml

# 3) Wait for deployment
kubectl -n budget-planner wait --for=condition=available deploy --all --timeout=300s

# 4) Get application URL
minikube service budget-nodeport -n budget-planner --url
# (or use port-forward)
kubectl -n budget-planner port-forward svc/budget-nodeport 5000:5000
open http://127.0.0.1:5000
```

## Quick Start — Local Development (Docker Compose)

```bash
# Start all services locally
docker-compose up -d

# Access the application
open http://localhost:5000
```

## Verify & Demo Commands

**Health checks:**
```bash
# Budget service health
curl -i http://127.0.0.1:30000/health

# Auth service health  
curl -i http://127.0.0.1:30001/health
```

**User registration and login:**
```bash
# Register new user
curl -X POST http://127.0.0.1:30001/register \
  -H "Content-Type: application/json" \
  -d '{"username": "demo", "password": "demo123"}'

# Login user
curl -X POST http://127.0.0.1:30001/login \
  -H "Content-Type: application/json" \
  -d '{"username": "demo", "password": "demo123"}'
```

**Budget operations:**
```bash
# Create monthly budget (requires auth token)
curl -X POST http://127.0.0.1:30000/api/monthly-budgets \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_JWT_TOKEN" \
  -d '{"category": "Food", "amount": 500, "month": "2024-01"}'

# Get budgets
curl -X GET http://127.0.0.1:30000/api/monthly-budgets \
  -H "Authorization: Bearer YOUR_JWT_TOKEN"
```

## Scale Out (Horizontal Scalability)

```bash
# Scale auth service
kubectl -n budget-planner scale deploy/auth-deployment --replicas=3

# Scale budget service  
kubectl -n budget-planner scale deploy/budget-deployment --replicas=5

# Check scaled pods
kubectl -n budget-planner get pods -l app=auth-service -o wide
kubectl -n budget-planner get pods -l app=budget-service -o wide
```

Each microservice can be scaled independently. HPA is configured for automatic scaling based on CPU usage.

## Persistence Check (Mongo PVC)

```bash
# Check PVC status
kubectl -n budget-planner get pvc

# Verify MongoDB data persistence
kubectl -n budget-planner exec -it deployment/mongo-deployment -- mongosh --eval "db.adminCommand('listCollections')"
```

You should see `mongodb-pvc` in `Bound` state (e.g., 1Gi, hostpath).

## Application Features

- **🔐 Secure Authentication**: JWT tokens with bcrypt password hashing
- **📊 Budget Management**: Create, edit, delete monthly budgets
- **💰 Expense Tracking**: Add daily expenses with categories
- **📈 Data Visualization**: Interactive pie charts for expense breakdown
- **🔍 Search & Filter**: Find budgets/expenses by date, category, amount
- **🌙 Dark Mode**: Toggle between light and dark themes
- **📱 Responsive Design**: Works on desktop, tablet, and mobile
- **⚡ Bulk Operations**: Select and delete multiple items
- **🔄 Real-time Updates**: Live data synchronization

## Troubleshooting

**NodePort 30000 already allocated:**
```bash
# Check available ports
kubectl -n budget-planner get svc

# Use port-forward as alternative
kubectl -n budget-planner port-forward svc/budget-nodeport 5000:5000
```

**Pods stuck in ImagePullBackOff:**
```bash
# Check pod status
kubectl -n budget-planner get pods

# Verify image availability
docker pull dilshaan/budget-planner-auth:latest
docker pull dilshaan/budget-planner-budget:latest
```

**MongoDB connection issues:**
```bash
# Check MongoDB logs
kubectl -n budget-planner logs deployment/mongo-deployment

# Restart MongoDB if needed
kubectl -n budget-planner rollout restart deployment/mongo-deployment
```

**Namespace stuck in Terminating:**
```bash
# Delete all resources first
kubectl delete -f k8s/budget-planner-complete.yaml

# Then reapply
kubectl apply -f k8s/budget-planner-complete.yaml
```

## Development Scenarios

### Scenario 1: Local Development
```bash
# Start MongoDB locally
docker run -d -p 27017:27017 --name mongodb mongo:latest

# Run services locally
cd auth_service && python app.py
cd budget_service && python app.py
```

### Scenario 2: Docker Compose Testing
```bash
# Test full stack locally
docker-compose up -d
docker-compose logs -f
```

### Scenario 3: Kubernetes Production
```bash
# Deploy to production cluster
kubectl apply -f k8s/budget-planner-complete.yaml

# Monitor deployment
kubectl -n budget-planner get all
kubectl -n budget-planner logs -f deployment/budget-deployment
```

### Scenario 4: Scaling and Load Testing
```bash
# Scale services
kubectl -n budget-planner scale deploy/budget-deployment --replicas=10

# Check HPA status
kubectl -n budget-planner get hpa

# Monitor resource usage
kubectl -n budget-planner top pods
```

## Cleanup

```bash
# Remove all resources
kubectl delete -f k8s/budget-planner-complete.yaml

# Or remove namespace (removes everything)
kubectl delete namespace budget-planner

# Local cleanup
docker-compose down
docker stop mongodb && docker rm mongodb
```

---

**Built with ❤️ using Python Flask, Docker, Kubernetes, and modern web technologies**