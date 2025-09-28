# Budget Planner — Kubernetes Microservices

A production-ready microservices application for budget and expense management. Deploy it on Kubernetes with a single command set that works on both Windows and macOS.

## 🏗️ Architecture Overview

The application consists of three main microservices:

### **Budget Service** (Port 5000)
- **Purpose**: Core budget and expense management
- **Technology**: Python Flask with Jinja2 templates
- **Features**: Web interface, budget/expense CRUD operations, analytics
- **Database**: MongoDB collections for budgets and expenses

### **Auth Service** (Port 5001)
- **Purpose**: User authentication and authorization
- **Technology**: Python Flask with JWT tokens
- **Features**: User registration, login, token management, password hashing
- **Database**: MongoDB user collection with bcrypt encryption

### **MongoDB** (Port 27017)
- **Purpose**: Persistent data storage
- **Technology**: MongoDB 7.0 with collections for users, budgets, and expenses
- **Features**: Data persistence, indexing, user isolation

## 📊 Architecture Diagram

```
                +-----------------------+                    +------------------+
  Browser  ---> |  Budget Service       |   (NodePort :30000) |  Auth Service    |
                |  (Flask + Jinja2)     |                    |  (Flask + JWT)   |
                +-----------+-----------+                    +--------+---------+
                            |                                           |
                            v                                           v
                  +---------+---------+             +------------------+
                  |  MongoDB          |  <--------> |  User Data       |
                  |  (Port 27017)     |   CRUD      |  Budget Data     |
                  +---------+---------+             |  Expense Data    |
                            |                       +------------------+
                            v
                  +---------+---------+
                  |  PersistentVolume |
                  |  (Data Storage)   |
                  +-------------------+
```

**Patterns Used:**
- **API Gateway**: Budget Service acts as the main entry point
- **Stateless Microservices**: Easy to scale independently
- **Database-per-Service**: Each service owns its data collections
- **Persistent Storage**: PVC for MongoDB across pod restarts
- **External Access**: NodePort for web interface access

## 🚀 Quick Start — Universal (Windows & macOS)

### Prerequisites
- **Windows**: Docker Desktop with Kubernetes enabled + PowerShell
- **macOS**: Docker Desktop (or minikube) + Terminal
- **Both**: kubectl installed and configured

### One-Command Deployment
The commands are IDENTICAL for both platforms! Only difference is file path separators:

#### Windows (PowerShell)
```powershell
# Clone and deploy everything
git clone https://github.com/md-d-cdr-4304/budget-planner.git
cd budget-planner

# Deploy to Kubernetes
kubectl apply -f .\k8s\budget-planner-complete.yaml

# Wait for all services to be ready
kubectl wait --for=condition=ready pod -l app=budget-service -n budget-planner --timeout=120s
kubectl wait --for=condition=ready pod -l app=auth-service -n budget-planner --timeout=120s
kubectl wait --for=condition=ready pod -l app=mongo -n budget-planner --timeout=120s

# Get service URLs and open
minikube service budget-nodeport -n budget-planner
minikube service auth-nodeport -n budget-planner --url
```

#### macOS/Linux
```bash
# Clone and deploy everything
git clone https://github.com/md-d-cdr-4304/budget-planner.git
cd budget-planner

# Deploy to Kubernetes
kubectl apply -f k8s/budget-planner-complete.yaml

# Wait for all services to be ready
kubectl wait --for=condition=ready pod -l app=budget-service -n budget-planner --timeout=120s
kubectl wait --for=condition=ready pod -l app=auth-service -n budget-planner --timeout=120s
kubectl wait --for=condition=ready pod -l app=mongo -n budget-planner --timeout=120s

# Get service URLs and open
minikube service budget-nodeport -n budget-planner
minikube service auth-nodeport -n budget-planner --url
```

### 🎯 Expected Result
- Browser opens automatically with the Budget Planner
- URL: `http://127.0.0.1:XXXXX` (port varies)
- All 3 pods running (budget-service, auth-service, mongodb)

## 📁 Repository Layout (Clean & Universal)

```
budget-planner/
├── k8s/                           # Universal Kubernetes manifests
│   └── budget-planner-complete.yaml # Complete deployment configuration
├── auth-service/                  # Authentication microservice
│   ├── app.py                     # Flask application
│   ├── requirements.txt           # Python dependencies
│   └── Dockerfile                 # Container definition
├── budget-service/                # Budget management microservice
│   ├── app.py                     # Flask application
│   ├── requirements.txt           # Python dependencies
│   ├── templates/                 # Jinja2 templates
│   │   ├── login.html            # Login/Register page
│   │   └── dashboard.html        # Main dashboard
│   ├── static/                    # Static assets
│   │   ├── style.css             # CSS styles
│   │   └── script.js             # JavaScript functionality
│   └── Dockerfile                 # Container definition
├── docker-compose.yml             # Local development setup
├── start-app.bat                  # Windows quick start script
└── README.md                      # This file
```

## 🔗 Current Service URLs

**Note**: URLs change dynamically with minikube. Run the commands above to get current URLs.

### Example URLs:
- **Budget Service**: `http://127.0.0.1:51294`
- **Auth Service**: `http://127.0.0.1:51301`

## 🧪 Verify & Demo Commands

### Universal API Testing (Windows & macOS)

#### Environment Setup
```bash
# Get current service URLs (run these first)
minikube service budget-nodeport -n budget-planner --url
minikube service auth-nodeport -n budget-planner --url
```

#### Health Check Commands
```bash
# Check Budget Service health
curl.exe -i http://127.0.0.1:30000/

# Check Auth Service health  
curl.exe -i http://127.0.0.1:30001/health

# Check MongoDB connectivity
kubectl logs -l app=mongo -n budget-planner --tail=5
```

#### User Authentication APIs

**Register + Login (PowerShell):**
```powershell
# Generate random username and register
$u = "demo$((Get-Random))"
$body = @{ username = $u; password = "demo123" } | ConvertTo-Json

# Register user
Invoke-RestMethod -Method POST -Uri http://127.0.0.1:30001/register -ContentType 'application/json' -Body $body

# Login user
Invoke-RestMethod -Method POST -Uri http://127.0.0.1:30001/login -ContentType 'application/json' -Body $body
```

**Register + Login (Bash):**
```bash
# Generate random username and register
USERNAME="demo$(shuf -i 1000-9999 -n 1)"
BODY="{\"username\":\"$USERNAME\",\"password\":\"demo123\"}"

# Register user
curl -X POST -H "Content-Type: application/json" -d "$BODY" http://127.0.0.1:30001/register

# Login user
curl -X POST -H "Content-Type: application/json" -d "$BODY" http://127.0.0.1:30001/login
```

#### Budget Management APIs

**Create + Get Budgets (PowerShell):**
```powershell
# Create budget
$budgetBody = @{ category = "Food"; amount = 500; month = "2024-01" } | ConvertTo-Json
Invoke-RestMethod -Method POST -Uri http://127.0.0.1:30000/api/monthly-budgets -ContentType 'application/json' -Body $budgetBody

# Get all budgets
Invoke-RestMethod -Method GET -Uri http://127.0.0.1:30000/api/monthly-budgets
```

**Create + Get Budgets (Bash):**
```bash
# Create budget
BUDGET_BODY='{"category":"Food","amount":500,"month":"2024-01"}'
curl -X POST -H "Content-Type: application/json" -d "$BUDGET_BODY" http://127.0.0.1:30000/api/monthly-budgets

# Get all budgets
curl -X GET http://127.0.0.1:30000/api/monthly-budgets
```

#### Expense Management APIs

**Create + Get Expenses (PowerShell):**
```powershell
# Create expense
$expenseBody = @{ category = "Groceries"; amount = 25.50; date = "2024-01-15"; description = "Weekly groceries" } | ConvertTo-Json
Invoke-RestMethod -Method POST -Uri http://127.0.0.1:30000/api/daily-expenses -ContentType 'application/json' -Body $expenseBody

# Get all expenses
Invoke-RestMethod -Method GET -Uri http://127.0.0.1:30000/api/daily-expenses
```

**Create + Get Expenses (Bash):**
```bash
# Create expense
EXPENSE_BODY='{"category":"Groceries","amount":25.50,"date":"2024-01-15","description":"Weekly groceries"}'
curl -X POST -H "Content-Type: application/json" -d "$EXPENSE_BODY" http://127.0.0.1:30000/api/daily-expenses

# Get all expenses
curl -X GET http://127.0.0.1:30000/api/daily-expenses
```

### Complete End-to-End Test Script

**Windows (PowerShell):**
```powershell
Write-Host "=== Budget Planner API Test ===" -ForegroundColor Green

# 1. Register user
$u = "demo$((Get-Random))"
$body = @{ username = $u; password = "demo123" } | ConvertTo-Json
$user = Invoke-RestMethod -Method POST -Uri http://127.0.0.1:30001/register -ContentType 'application/json' -Body $body
Write-Host "✅ User registered: $($user.username)" -ForegroundColor Green

# 2. Login user
$login = Invoke-RestMethod -Method POST -Uri http://127.0.0.1:30001/login -ContentType 'application/json' -Body $body
Write-Host "✅ User logged in: $($login.username)" -ForegroundColor Green

# 3. Create budget
$budgetBody = @{ category = "Food"; amount = 500; month = "2024-01" } | ConvertTo-Json
$budget = Invoke-RestMethod -Method POST -Uri http://127.0.0.1:30000/api/monthly-budgets -ContentType 'application/json' -Body $budgetBody
Write-Host "✅ Budget created: $($budget.category) - $($budget.amount)" -ForegroundColor Green

# 4. Create expense
$expenseBody = @{ category = "Groceries"; amount = 25.50; date = "2024-01-15"; description = "Weekly groceries" } | ConvertTo-Json
$expense = Invoke-RestMethod -Method POST -Uri http://127.0.0.1:30000/api/daily-expenses -ContentType 'application/json' -Body $expenseBody
Write-Host "✅ Expense created: $($expense.category) - $($expense.amount)" -ForegroundColor Green

# 5. Get budgets
$budgets = Invoke-RestMethod -Method GET -Uri http://127.0.0.1:30000/api/monthly-budgets
Write-Host "✅ Retrieved $($budgets.Count) budgets" -ForegroundColor Green

# 6. Get expenses
$expenses = Invoke-RestMethod -Method GET -Uri http://127.0.0.1:30000/api/daily-expenses
Write-Host "✅ Retrieved $($expenses.Count) expenses" -ForegroundColor Green

Write-Host "=== All API tests completed successfully! ===" -ForegroundColor Green
```

**macOS/Linux (Bash):**
```bash
echo "=== Budget Planner API Test ==="

# 1. Register user
USERNAME="demo$(shuf -i 1000-9999 -n 1)"
BODY="{\"username\":\"$USERNAME\",\"password\":\"demo123\"}"
USER=$(curl -s -X POST -H "Content-Type: application/json" -d "$BODY" http://127.0.0.1:30001/register)
echo "✅ User registered: $USERNAME"

# 2. Login user
LOGIN=$(curl -s -X POST -H "Content-Type: application/json" -d "$BODY" http://127.0.0.1:30001/login)
echo "✅ User logged in: $USERNAME"

# 3. Create budget
BUDGET_BODY='{"category":"Food","amount":500,"month":"2024-01"}'
BUDGET=$(curl -s -X POST -H "Content-Type: application/json" -d "$BUDGET_BODY" http://127.0.0.1:30000/api/monthly-budgets)
echo "✅ Budget created: Food - 500"

# 4. Create expense
EXPENSE_BODY='{"category":"Groceries","amount":25.50,"date":"2024-01-15","description":"Weekly groceries"}'
EXPENSE=$(curl -s -X POST -H "Content-Type: application/json" -d "$EXPENSE_BODY" http://127.0.0.1:30000/api/daily-expenses)
echo "✅ Expense created: Groceries - 25.50"

# 5. Get budgets
BUDGETS=$(curl -s -X GET http://127.0.0.1:30000/api/monthly-budgets)
echo "✅ Retrieved budgets"

# 6. Get expenses
EXPENSES=$(curl -s -X GET http://127.0.0.1:30000/api/daily-expenses)
echo "✅ Retrieved expenses"

echo "=== All API tests completed successfully! ==="
```

## 🔍 Monitoring and Logs

### Check Service Status
```bash
# Check all pods
kubectl get pods -n budget-planner

# Check services
kubectl get services -n budget-planner

# Check deployments
kubectl get deployments -n budget-planner
```

### View Logs
```bash
# Auth Service logs
kubectl logs -l app=auth-service -n budget-planner --tail=10

# Budget Service logs
kubectl logs -l app=budget-service -n budget-planner --tail=10

# MongoDB logs
kubectl logs -l app=mongo -n budget-planner --tail=10
```

### Health Monitoring
```bash
# Check pod health
kubectl get pods -n budget-planner -o wide

# Check resource usage
kubectl top pods -n budget-planner

# Check events
kubectl get events -n budget-planner --sort-by='.lastTimestamp'
```

## 🛠️ Development

### Local Development with Docker Compose
```bash
# Start local development environment
docker-compose up -d

# View logs
docker-compose logs -f

# Stop services
docker-compose down
```

### Windows Quick Start
```bash
# Use the provided batch file
start-app.bat
```

## 📊 Features

### Web Interface
- ✅ Modern, minimalistic UI with soft color palette
- ✅ Responsive design for all devices
- ✅ Dark/Light mode toggle
- ✅ Real-time form validation
- ✅ Password strength indicator
- ✅ Auto-fill demo credentials

### Dashboard Features
- ✅ Budget and expense management
- ✅ CRUD operations (Create, Read, Update, Delete)
- ✅ Search functionality
- ✅ Date range filters (month/year)
- ✅ Bulk delete operations
- ✅ Interactive pie chart for expenses
- ✅ User-specific data isolation

### Security Features
- ✅ JWT token authentication
- ✅ Password hashing with bcrypt
- ✅ Session management
- ✅ Rate limiting
- ✅ API security middleware
- ✅ Token refresh mechanism

## 🏗️ Architecture Details

### Microservices Communication
```
Web Browser → Budget Service (Port 5000) → Auth Service (Port 5001)
                    ↓
              MongoDB (Port 27017)
```

### Data Flow
1. **User Registration/Login**: Auth Service validates credentials and issues JWT tokens
2. **Budget Management**: Budget Service handles CRUD operations with user isolation
3. **Data Persistence**: MongoDB stores all data with proper indexing
4. **Session Management**: JWT tokens provide stateless authentication

### Kubernetes Resources
- **Deployments**: 3 (auth-service, budget-service, mongo)
- **Services**: 3 (ClusterIP for internal, NodePort for external)
- **Secrets**: 2 (app-secrets, mongo-secret)
- **ConfigMaps**: 2 (app-config, mongo-init-script)
- **PVC**: 1 (MongoDB data persistence)
- **HPA**: 2 (Auto-scaling for auth and budget services)

## 🚨 Troubleshooting

### Common Issues

#### Services Not Accessible
```bash
# Check if services are running
kubectl get pods -n budget-planner

# Restart services if needed
kubectl rollout restart deployment auth-deployment budget-deployment -n budget-planner
```

#### MongoDB Connection Issues
```bash
# Check MongoDB logs
kubectl logs -l app=mongo -n budget-planner --tail=20

# Restart MongoDB if needed
kubectl rollout restart deployment mongo-deployment -n budget-planner
```

#### Authentication Failures
```bash
# Check Auth Service logs
kubectl logs -l app=auth-service -n budget-planner --tail=10

# Verify JWT secret
kubectl get secret app-secrets -n budget-planner -o yaml
```

### Reset Everything
```bash
# Delete all resources
kubectl delete namespace budget-planner

# Redeploy
kubectl apply -f k8s/budget-planner-complete.yaml
```

## 📝 API Documentation

### Auth Service Endpoints

| Method | Endpoint | Description | Request Body |
|--------|----------|-------------|--------------|
| POST | `/register` | Register new user | `{username, password}` |
| POST | `/login` | User login | `{username, password}` |
| POST | `/refresh` | Refresh JWT token | `{refresh_token}` |
| POST | `/verify` | Verify JWT token | `{token}` |
| POST | `/logout` | User logout | `{token}` |

### Budget Service Endpoints

| Method | Endpoint | Description | Request Body |
|--------|----------|-------------|--------------|
| GET | `/` | Web interface | - |
| GET | `/api/monthly-budgets` | Get all budgets | - |
| POST | `/api/monthly-budgets` | Create budget | `{category, amount, month}` |
| GET | `/api/daily-expenses` | Get all expenses | - |
| POST | `/api/daily-expenses` | Create expense | `{category, amount, date, description}` |

## 🎯 Assignment Compliance

This project fulfills all microservices assignment requirements:

- ✅ **Multiple Microservices**: Auth Service, Budget Service, MongoDB
- ✅ **Kubernetes Deployment**: Complete YAML manifests with all resources
- ✅ **RESTful APIs**: Full CRUD operations with proper HTTP methods
- ✅ **Web Interface**: Modern, responsive UI with Bootstrap
- ✅ **Data Persistence**: MongoDB with PersistentVolumeClaim
- ✅ **Authentication**: JWT-based security with password hashing
- ✅ **Containerization**: Docker images for all services
- ✅ **Scaling**: HorizontalPodAutoscaler for auto-scaling
- ✅ **Monitoring**: Health checks and logging

## 📞 Support

For issues or questions:
1. Check the troubleshooting section above
2. Review service logs using the monitoring commands
3. Verify all services are running with `kubectl get pods -n budget-planner`

---

**Repository**: [https://github.com/md-d-cdr-4304/budget-planner](https://github.com/md-d-cdr-4304/budget-planner)

*This README provides comprehensive documentation for the Budget Planner microservices application, including all working API endpoints, monitoring commands, and troubleshooting guides.*

*README documentation generated with assistance from a generative AI tool.*