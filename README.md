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

### **Windows (Recommended for Grading)**
- **Docker Desktop** with Kubernetes enabled (Settings ▸ Kubernetes ▸ Enable Kubernetes)
- **kubectl** in PATH (Docker Desktop provides one automatically)
- **PowerShell** or **CMD** (PowerShell recommended)
- **Git** for cloning the repository

### **macOS (Alternative)**
- **Docker Desktop** (or any Docker daemon)
- **minikube** + **kubectl** (install via Homebrew: `brew install minikube kubectl`)
- **Git** for cloning the repository

### **Linux (Ubuntu/Debian)**
- **Docker** + **minikube** + **kubectl**
- **Git** for cloning the repository
- Install commands:
  ```bash
  # Install Docker
  sudo apt update && sudo apt install docker.io
  sudo systemctl start docker && sudo systemctl enable docker
  
  # Install kubectl
  curl -LO "https://dl.k8s.io/release/$(curl -L -s https://dl.k8s.io/release/stable.txt)/bin/linux/amd64/kubectl"
  sudo install -o root -g root -m 0755 kubectl /usr/local/bin/kubectl
  
  # Install minikube
  curl -LO https://storage.googleapis.com/minikube/releases/latest/minikube-linux-amd64
  sudo install minikube-linux-amd64 /usr/local/bin/minikube
  ```

> **Important:** Do not run `kubectl apply -f .` from the repository root. Apply only the files in the `k8s/` folder to avoid conflicts.

## 🚀 Getting Started - Complete Setup Guide

### **Step 1: Clone the Repository**

```bash
# Clone the repository to your local machine
git clone https://github.com/md-d-cdr-4304/budget-planner.git

# Navigate to the project directory
cd budget-planner
```

**Why this step?** This downloads the complete source code, including all microservices, Kubernetes manifests, and documentation to your local machine.

### **Step 2: Verify Prerequisites**

```bash
# Check if Docker is running
docker --version
docker ps

# Check if kubectl is available
kubectl version --client

# Check if Kubernetes cluster is accessible
kubectl get nodes
```

**Why this step?** Ensures all required tools are installed and working before deployment. Docker is needed for containerization, kubectl for Kubernetes management.

### **Step 3: Choose Your Deployment Method**

You have three options:

1. **Kubernetes Deployment** (Recommended for production-like environment)
2. **Docker Compose** (Quick local testing)
3. **Local Development** (For code modifications)

---

## 🖥️ Quick Start — Windows (Docker Desktop Kubernetes)

**Why Windows?** Docker Desktop on Windows provides the most stable Kubernetes environment for grading and testing.

### **Step 1: Enable Docker Desktop Kubernetes**

1. Open **Docker Desktop**
2. Go to **Settings** → **Kubernetes**
3. Check **"Enable Kubernetes"**
4. Click **"Apply & Restart"**
5. Wait for Kubernetes to start (green indicator)

**Why this step?** Docker Desktop's built-in Kubernetes provides a production-like environment without additional setup.

### **Step 2: Deploy the Application**

From the project root where the `k8s` folder is:

```powershell
# 1) Verify Docker Desktop's Kubernetes cluster is active
kubectl config use-context docker-desktop
kubectl get nodes
```

**Why this step?** Ensures we're using the correct Kubernetes cluster and it's accessible.

```powershell
# 2) Deploy all microservices and infrastructure
kubectl apply -f .\k8s\budget-planner-complete.yaml
```

**Why this step?** This single command deploys:
- **MongoDB** with persistent storage
- **Auth Service** with JWT authentication
- **Budget Service** with web UI
- **Services** for inter-service communication
- **NodePort** for external access
- **HPA** for automatic scaling

```powershell
# 3) Wait for all services to be ready
kubectl -n budget-planner wait --for=condition=available deploy --all --timeout=300s
kubectl -n budget-planner get pods -o wide
```

**Why this step?** Ensures all containers are running and healthy before accessing the application.

```powershell
# 4) Get the application URL
kubectl -n budget-planner get svc budget-nodeport -o jsonpath="{.spec.ports[0].nodePort}{'\n'}"
```

**Why this step?** NodePort exposes the application on a specific port (usually 30000) for external access.

```powershell
# 5) Open the application in your browser
start http://127.0.0.1:30000
```

**Why this step?** Opens the Budget Planner web interface where you can register, login, and manage budgets.

## 🍎 Quick Start — macOS (minikube)

**Why macOS?** minikube provides a lightweight Kubernetes environment perfect for development and testing on Mac systems.

### **Step 1: Start minikube**

```bash
# 1) Start minikube with Docker driver
minikube start
```

**Why this step?** minikube creates a local Kubernetes cluster using Docker as the container runtime, providing a complete K8s environment.

```bash
# 2) Verify minikube is running
minikube status
kubectl get nodes
```

**Why this step?** Confirms the Kubernetes cluster is healthy and accessible.

### **Step 2: Deploy the Application**

```bash
# 3) Deploy all microservices
kubectl apply -f k8s/budget-planner-complete.yaml
```

**Why this step?** Deploys the complete microservices stack including MongoDB, Auth Service, Budget Service, and all supporting infrastructure.

```bash
# 4) Wait for all deployments to be ready
kubectl -n budget-planner wait --for=condition=available deploy --all --timeout=300s
```

**Why this step?** Ensures all pods are running and healthy before accessing the application.

### **Step 3: Access the Application**

**Option A: Using minikube service (Recommended)**
```bash
# 5) Get the application URL
minikube service budget-nodeport -n budget-planner --url
```

**Why this option?** minikube automatically handles port forwarding and provides the correct URL for external access.

**Option B: Using port-forward**
```bash
# 5) Alternative: Use port-forward
kubectl -n budget-planner port-forward svc/budget-nodeport 5000:5000
open http://127.0.0.1:5000
```

**Why this option?** Direct port forwarding provides more control over the connection and is useful for debugging.

## 🐧 Quick Start — Linux (minikube)

**Why Linux?** Native Linux provides the most efficient Kubernetes environment with direct access to system resources.

### **Step 1: Start minikube**

```bash
# 1) Start minikube with Docker driver
minikube start
```

**Why this step?** minikube creates a local Kubernetes cluster optimized for Linux systems.

```bash
# 2) Verify minikube is running
minikube status
kubectl get nodes
```

**Why this step?** Confirms the Kubernetes cluster is healthy and accessible.

### **Step 2: Deploy the Application**

```bash
# 3) Deploy all microservices
kubectl apply -f k8s/budget-planner-complete.yaml
```

**Why this step?** Deploys the complete microservices stack with all necessary components.

```bash
# 4) Wait for all deployments to be ready
kubectl -n budget-planner wait --for=condition=available deploy --all --timeout=300s
```

**Why this step?** Ensures all pods are running and healthy before accessing the application.

### **Step 3: Access the Application**

```bash
# 5) Get the application URL
minikube service budget-nodeport -n budget-planner --url
```

**Why this step?** minikube provides the correct URL for accessing the application from your browser.

---

## 🐳 Quick Start — Local Development (Docker Compose)

**Why Docker Compose?** Perfect for quick local testing without Kubernetes complexity. All services run in containers but without orchestration.

### **Step 1: Start All Services**

```bash
# 1) Start all services locally
docker-compose up -d
```

**Why this step?** Docker Compose starts all microservices (MongoDB, Auth Service, Budget Service) in separate containers with proper networking.

```bash
# 2) Verify all containers are running
docker-compose ps
```

**Why this step?** Confirms all services are healthy and accessible.

### **Step 2: Access the Application**

```bash
# 3) Access the application
# Windows
start http://localhost:5000

# macOS
open http://localhost:5000

# Linux
xdg-open http://localhost:5000
```

**Why this step?** Opens the Budget Planner web interface running locally on port 5000.

### **Step 3: View Logs (Optional)**

```bash
# 4) View service logs
docker-compose logs -f budget-service
docker-compose logs -f auth-service
docker-compose logs -f mongodb
```

**Why this step?** Useful for debugging and monitoring service behavior during development.

---

## 🔧 What Happens During Deployment

### **Kubernetes Deployment Process**

When you run `kubectl apply -f k8s/budget-planner-complete.yaml`, here's what happens:

1. **Namespace Creation**: Creates `budget-planner` namespace for resource isolation
2. **MongoDB Deployment**: 
   - Creates PersistentVolumeClaim for data persistence
   - Deploys MongoDB container with health checks
   - Creates internal service for database access
3. **Auth Service Deployment**:
   - Deploys Flask application with JWT authentication
   - Connects to MongoDB for user data storage
   - Creates internal service for authentication
4. **Budget Service Deployment**:
   - Deploys Flask application with web UI
   - Connects to Auth Service for user verification
   - Connects to MongoDB for budget/expense data
   - Creates NodePort service for external access
5. **Horizontal Pod Autoscaler**: Configures automatic scaling based on CPU usage
6. **Service Discovery**: Sets up internal DNS for service communication

### **Why This Architecture?**

- **Microservices**: Each service has a single responsibility (auth, budget management, data storage)
- **Containerization**: Ensures consistent deployment across different environments
- **Orchestration**: Kubernetes manages service lifecycle, scaling, and health monitoring
- **Persistence**: MongoDB data survives pod restarts and deployments
- **Security**: JWT tokens provide stateless authentication
- **Scalability**: Services can be scaled independently based on demand

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

## 🛠️ Troubleshooting

### **Common Issues and Solutions**

#### **NodePort 30000 Already Allocated**

**Problem**: Port 30000 is already in use by another service.

**Solution**:
```bash
# Check available ports
kubectl -n budget-planner get svc

# Use port-forward as alternative
kubectl -n budget-planner port-forward svc/budget-nodeport 5000:5000
```

**Why this happens**: Other applications or services might be using the same port.

#### **Pods Stuck in ImagePullBackOff**

**Problem**: Kubernetes cannot pull the Docker images.

**Solution**:
```bash
# Check pod status
kubectl -n budget-planner get pods

# Verify image availability
docker pull dilshaan/budget-planner-auth:latest
docker pull dilshaan/budget-planner-budget:latest

# Check image pull secrets
kubectl -n budget-planner get secrets
```

**Why this happens**: Network issues, incorrect image names, or Docker Hub access problems.

#### **MongoDB Connection Issues**

**Problem**: Auth Service cannot connect to MongoDB.

**Solution**:
```bash
# Check MongoDB logs
kubectl -n budget-planner logs deployment/mongo-deployment

# Check MongoDB pod status
kubectl -n budget-planner get pods -l app=mongodb

# Restart MongoDB if needed
kubectl -n budget-planner rollout restart deployment/mongo-deployment
```

**Why this happens**: MongoDB pod might be starting slowly or having configuration issues.

#### **Namespace Stuck in Terminating**

**Problem**: Cannot delete the budget-planner namespace.

**Solution**:
```bash
# Delete all resources first
kubectl delete -f k8s/budget-planner-complete.yaml

# Force delete namespace if needed
kubectl delete namespace budget-planner --force --grace-period=0

# Then reapply
kubectl apply -f k8s/budget-planner-complete.yaml
```

**Why this happens**: Resources with finalizers or persistent volumes preventing deletion.

### **Platform-Specific Issues**

#### **Windows (Docker Desktop)**

**Issue**: Kubernetes not starting
```bash
# Restart Docker Desktop
# Go to Settings → Kubernetes → Enable Kubernetes
# Wait for green indicator
```

**Issue**: PowerShell execution policy
```powershell
# Set execution policy
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

#### **macOS (minikube)**

**Issue**: minikube start fails
```bash
# Delete and recreate minikube
minikube delete
minikube start --driver=docker
```

**Issue**: Port conflicts
```bash
# Use different port
kubectl -n budget-planner patch svc/budget-nodeport \
  -p '{"spec":{"ports":[{"port":5000,"targetPort":5000,"nodePort":31000}],"type":"NodePort"}}'
```

#### **Linux (minikube)**

**Issue**: Permission denied for Docker
```bash
# Add user to docker group
sudo usermod -aG docker $USER
# Log out and log back in
```

**Issue**: minikube driver issues
```bash
# Use virtualbox driver
minikube start --driver=virtualbox
```

### **Debugging Commands**

```bash
# Check all resources
kubectl -n budget-planner get all

# Check pod logs
kubectl -n budget-planner logs -f deployment/budget-deployment
kubectl -n budget-planner logs -f deployment/auth-deployment
kubectl -n budget-planner logs -f deployment/mongo-deployment

# Check service endpoints
kubectl -n budget-planner get endpoints

# Check persistent volumes
kubectl -n budget-planner get pvc
kubectl -n budget-planner get pv

# Check horizontal pod autoscaler
kubectl -n budget-planner get hpa
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

**Built using Python Flask, Docker, Kubernetes, and modern web technologies** 