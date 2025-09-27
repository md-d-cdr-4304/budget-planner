# Budget Planner — Kubernetes Microservices

A comprehensive, production-ready microservices application for personal budget management. Deploy on Kubernetes with persistent storage, JWT authentication, and a modern web interface.

## 🏗️ Microservices Architecture

This application implements **three distinct microservices** as required by the assignment:

### **1. Budget Service (Flask)**
- **Purpose**: Main application logic and web interface
- **Technology**: Python Flask with Jinja2 templates
- **Features**: REST API, web UI, data visualization with Chart.js
- **Port**: 5000 (internal), 30000 (external NodePort)
- **Responsibilities**: Budget/expense CRUD operations, user interface rendering

### **2. Auth Service (Flask)**
- **Purpose**: User authentication and authorization
- **Technology**: Python Flask with JWT and bcrypt
- **Features**: User registration/login, JWT token management, rate limiting
- **Port**: 5001 (internal), 30001 (external NodePort)
- **Responsibilities**: Password hashing, token generation/validation, user management

### **3. MongoDB Database Service**
- **Purpose**: Persistent data storage
- **Technology**: MongoDB 7.0 with PersistentVolumeClaim
- **Features**: User data, budget/expense storage, data persistence
- **Port**: 27017 (internal ClusterIP only)
- **Responsibilities**: Data persistence, user authentication data, budget/expense storage

**All microservices communicate internally via Kubernetes ClusterIP services and can be scaled independently using Horizontal Pod Autoscaler (HPA).**

## Repository Layout

```
budget-planner/
├── auth_service/                 # Authentication microservice
│   ├── app.py                   # Flask application with JWT
│   ├── requirements.txt         # Python dependencies
│   └── Dockerfile              # Container configuration
├── budget_service/              # Budget management microservice
│   ├── app.py                  # Flask application with web UI
│   ├── templates/              # Jinja2 templates
│   ├── static/                 # CSS, JS, assets
│   ├── requirements.txt        # Python dependencies
│   └── Dockerfile             # Container configuration
├── k8s/                        # Kubernetes deployment
│   └── budget-planner-complete.yaml  # Complete secure deployment
├── docker-compose.yml          # Local development setup
└── README.md                  # This file
```

**Note:** All Kubernetes manifests are consolidated into a single secure YAML file for simplified deployment and maintenance.

## 🔄 Service Communication Flow

1. **User Access**: Web browser → NodePort (30000) → Budget Service
2. **Authentication**: Budget Service → Auth Service (5001) → JWT validation
3. **Data Operations**: Budget Service → MongoDB (27017) → CRUD operations
4. **User Management**: Auth Service → MongoDB (27017) → User authentication data
5. **Scaling**: HPA monitors CPU/Memory → Scales services independently (2-10 replicas)

## Architecture

```
                +---------------------------+
  Browser  ---> |  budget-service (UI+API)  |   (NodePort :30000)
                +-----------+---------------+
                            |
                            v
                  +---------+---------+             +------------------+
                  |  auth-service     |  <---->     | MongoDB (mongo:7)|
                  |  (Flask + JWT)    |   Auth      |  (PVC Storage)   |
                  +-------------------+             +------------------+
```

## 🚀 Quick Start

### **Prerequisites**
- **Docker Desktop** with Kubernetes enabled (Windows/macOS) OR **Minikube** (Linux)
- **kubectl** CLI tool
- **Git** for cloning the repository

### **Deployment Steps**

1. **Clone the repository:**
   ```bash
   git clone https://github.com/md-d-cdr-4304/budget-planner.git
   cd budget-planner
   ```
   **Why this step?** Downloads the complete source code including all microservices, Kubernetes manifests, and documentation to your local machine.

2. **Deploy to Kubernetes (Single Command):**
   ```bash
   kubectl apply -f k8s/budget-planner-complete.yaml
   ```
   **Why this step?** This single command deploys the complete microservices stack with security enhancements:
   - **MongoDB** with persistent storage and secure credentials
   - **Auth Service** with JWT authentication and bcrypt password hashing
   - **Budget Service** with web UI and REST API
   - **Services** for inter-service communication (ClusterIP and NodePort)
   - **HPA** for automatic scaling (2-10 replicas)
   - **Secrets** for secure credential management

3. **Wait for deployment:**
   ```bash
   kubectl get pods -n budget-planner
   ```
   **Why this step?** Ensures all pods are running and healthy before accessing the application. This command shows the status of all microservices and confirms they're ready to handle requests.

4. **Access the application:**
   ```bash
   minikube service budget-nodeport -n budget-planner --url
   ```
   **Why this step?** Provides the external URL to access the Budget Planner web interface. The NodePort service exposes the Budget Service externally while keeping other services internal for security.

## 🌐 **Current Service URLs**

After deployment, get your live URLs with these commands:

```bash
# Get Budget Service URL (Web Interface)
minikube service budget-nodeport -n budget-planner --url

# Get Auth Service URL (API Testing)
minikube service auth-nodeport -n budget-planner --url
```

**Example Output:**
- **Base URL (Budget Service):** `http://127.0.0.1:47027`
- **Auth URL (Auth Service):** `http://127.0.0.1:47036`

**Note:** NodePort URLs change each time you restart minikube. Run the commands above to get current URLs.

### **Security Features**
- **Kubernetes Secrets:** All credentials stored securely with base64 encoding
- **Strong Passwords:** MongoDB and JWT secrets use complex passwords
- **Environment Variables:** Runtime credential injection from secrets
- **Network Isolation:** Internal services use ClusterIP, external via NodePort

## 📊 Assignment Requirements Compliance

This application fully satisfies all assignment requirements:

✅ **Kubernetes Deployment**: Complete deployment using Kubernetes with consolidated secure manifests  
✅ **Multiple Microservices**: Two distinct microservices (Budget Service, Auth Service) plus MongoDB database  
✅ **REST API Implementation**: Each microservice implements comprehensive REST APIs with full CRUD operations  
✅ **External Access**: Accessible via web browser through NodePort services  
✅ **Independent Scaling**: Each microservice can be scaled horizontally using HPA (2-10 replicas)  
✅ **Docker Hub Images**: All images published to Docker Hub under dilshaan namespace  
✅ **Database Microservice**: MongoDB running as separate microservice with persistent storage  
✅ **Persistent Storage**: PVC ensures data survival across infrastructure restarts  
✅ **Security Implementation**: JWT authentication, bcrypt password hashing, Kubernetes Secrets, strong passwords  
✅ **Professional Interface**: Modern web UI with data visualization and real-time updates  
✅ **Secure Architecture**: Environment variable injection, network isolation, credential management

## 🔧 API Endpoints

### **Budget Service (Port 5000)**
- `GET /` - Web interface
- `POST /api/monthly-budgets` - Create budget
- `GET /api/monthly-budgets` - Get all budgets
- `PUT /api/monthly-budgets/{id}` - Update budget
- `DELETE /api/monthly-budgets/{id}` - Delete budget
- `POST /api/daily-expenses` - Create expense
- `GET /api/daily-expenses` - Get all expenses
- `PUT /api/daily-expenses/{id}` - Update expense
- `DELETE /api/daily-expenses/{id}` - Delete expense

### **Auth Service (Port 5001)**
- `POST /register` - User registration
- `POST /login` - User login
- `POST /verify` - JWT token verification
- `POST /refresh` - Token refresh
- `POST /logout` - User logout

## 🐳 Docker Compose (Alternative - Local Testing Only)

**Note:** This is for local development/testing only. The main deployment method is Kubernetes.

### **Windows Users (Convenient Script):**
```bash
# Run the provided batch script
start-app.bat
```
**Why this script?** Automatically pulls latest images, starts all services, and displays access URLs. Convenient for Windows users who want to test locally without Kubernetes.

### **Manual Docker Compose:**
```bash
# Start all services locally
docker-compose up -d
```
**Why this command?** Starts all microservices locally using Docker Compose for quick testing without Kubernetes setup. Useful for development and debugging.

```bash
# Access the application
open http://localhost:5000
```
**Why this command?** Opens the Budget Planner web interface in your default browser for local testing and development.

**Important:** Docker Compose uses demo credentials for local testing only. For production-like deployment, use the secure Kubernetes deployment method above.

## 🔍 Monitoring and Logs

```bash
# View all pods
kubectl get pods -n budget-planner
```
**Why this command?** Shows the status of all microservices pods, confirming they're running and healthy.

```bash
# View services
kubectl get services -n budget-planner
```
**Why this command?** Displays all services including ClusterIP (internal) and NodePort (external) services, showing how microservices communicate.

```bash
# View HPA status
kubectl get hpa -n budget-planner
```
**Why this command?** Shows the Horizontal Pod Autoscaler status, demonstrating independent scaling capabilities as required by the assignment.

```bash
# View logs
kubectl logs -f deployment/budget-deployment -n budget-planner
kubectl logs -f deployment/auth-deployment -n budget-planner
kubectl logs -f deployment/mongo-deployment -n budget-planner
```
**Why these commands?** Monitor real-time logs from each microservice to demonstrate inter-service communication, authentication flows, and database operations.

## 🛡️ Security Implementation

### **Kubernetes Secrets**
- All credentials stored in encrypted Kubernetes Secrets
- Base64 encoding for secure storage
- Environment variable injection at runtime

### **Strong Authentication**
- JWT tokens with expiration
- bcrypt password hashing
- Rate limiting on auth endpoints

### **Network Security**
- Internal services use ClusterIP (no external access)
- External access only via NodePort services
- MongoDB accessible only within cluster

## 📈 Scaling

The application supports independent horizontal scaling:

```bash
# Scale Budget Service
kubectl scale deployment budget-deployment --replicas=5 -n budget-planner
```
**Why this command?** Manually scales the Budget Service to 5 replicas, demonstrating independent scaling as required by the assignment.

```bash
# Scale Auth Service
kubectl scale deployment auth-deployment --replicas=3 -n budget-planner
```
**Why this command?** Manually scales the Auth Service to 3 replicas, showing how each microservice can be scaled independently based on demand.

```bash
# View HPA status
kubectl get hpa -n budget-planner
```
**Why this command?** Shows the Horizontal Pod Autoscaler status, demonstrating automatic scaling based on CPU and memory utilization.

## 🎯 Features

- **Modern Web Interface**: Responsive design with dark mode
- **Real-time Data Visualization**: Interactive charts with Chart.js
- **Search and Filtering**: Advanced filtering by date and category
- **Bulk Operations**: Select and delete multiple items
- **User Authentication**: Secure JWT-based authentication
- **Data Persistence**: MongoDB with PersistentVolumeClaim
- **Auto-scaling**: Horizontal Pod Autoscaler for performance

## 📝 License

This project is created for educational purposes as part of a cloud computing assignment.

## 🙏 Acknowledgments

This README file and project documentation were generated with the assistance of Generative AI tools to ensure comprehensive coverage of all technical aspects, security implementations, and assignment requirements. The AI assistance helped in structuring the documentation, explaining complex microservices architecture, and ensuring all assignment criteria are clearly addressed.

---

**Repository**: [https://github.com/md-d-cdr-4304/budget-planner](https://github.com/md-d-cdr-4304/budget-planner)  
**Docker Hub**: [dilshaan/budget-planner-auth](https://hub.docker.com/r/dilshaan/budget-planner-auth), [dilshaan/budget-planner-budget](https://hub.docker.com/r/dilshaan/budget-planner-budget)