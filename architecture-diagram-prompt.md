# Master Prompt for Budget Planner Architecture Diagram

## 🎯 **Objective**
Generate a comprehensive, detailed architecture diagram for a Budget Planner microservices application deployed on Kubernetes, showing all service communications, data flows, and infrastructure components.

## 📋 **Project Overview**
Create a microservices-based Budget Planner application with the following characteristics:
- **Purpose**: Personal budget management with monthly budgets and daily expense tracking
- **Architecture**: Microservices with containerization and orchestration
- **Deployment**: Kubernetes cluster with persistent storage
- **Access**: Web browser interface with external NodePort access

## 🏗️ **Detailed Architecture Requirements**

### **1. External Access Layer**
- **Web Browser** (User Interface)
- **NodePort Service** (Port 30000) for external access
- **Load Balancer** (Kubernetes Service)

### **2. Frontend Layer**
- **Budget Service** (Flask Application)
  - **Web UI**: Jinja2 templates with Bootstrap, Chart.js
  - **REST API**: Budget and expense management endpoints
  - **Session Management**: Flask sessions with JWT tokens
  - **Features**: Dark mode, search, filtering, data visualization

### **3. Authentication Layer**
- **Auth Service** (Flask Application)
  - **JWT Token Management**: Access tokens and refresh tokens
  - **Password Security**: bcrypt hashing with salt
  - **Rate Limiting**: API protection
  - **User Management**: Registration, login, verification

### **4. Data Layer**
- **MongoDB** (Database Service)
  - **User Collection**: Authentication data
  - **Budget Collection**: Monthly budget data
  - **Expense Collection**: Daily expense data
  - **Persistent Storage**: PVC (PersistentVolumeClaim)

### **5. Infrastructure Layer**
- **Kubernetes Cluster**
  - **Namespace**: budget-planner
  - **Deployments**: Auth Service, Budget Service, MongoDB
  - **Services**: Internal communication and external access
  - **HPA**: Horizontal Pod Autoscaler for scaling
  - **ConfigMaps**: Configuration management
  - **Secrets**: Sensitive data management

## 🔄 **Service Communication Flows**

### **Flow 1: User Registration/Login**
1. **Browser** → **Budget Service** (NodePort 30000)
2. **Budget Service** → **Auth Service** (Internal API call)
3. **Auth Service** → **MongoDB** (User data storage)
4. **Auth Service** → **Budget Service** (JWT token response)
5. **Budget Service** → **Browser** (Session establishment)

### **Flow 2: Budget Management**
1. **Browser** → **Budget Service** (Budget CRUD operations)
2. **Budget Service** → **Auth Service** (Token verification)
3. **Budget Service** → **MongoDB** (Budget data operations)
4. **Budget Service** → **Browser** (Updated UI with data)

### **Flow 3: Expense Tracking**
1. **Browser** → **Budget Service** (Expense CRUD operations)
2. **Budget Service** → **Auth Service** (Token verification)
3. **Budget Service** → **MongoDB** (Expense data operations)
4. **Budget Service** → **Browser** (Updated UI with charts)

### **Flow 4: Data Visualization**
1. **Browser** → **Budget Service** (Chart data requests)
2. **Budget Service** → **MongoDB** (Aggregated data queries)
3. **Budget Service** → **Browser** (Chart.js rendering)

## 🛠️ **Technical Components**

### **Container Images**
- **dilshaan/budget-planner-auth:latest** (Auth Service)
- **dilshaan/budget-planner-budget:latest** (Budget Service)
- **mongo:latest** (MongoDB)

### **Kubernetes Resources**
- **Deployments**: 3 (auth-deployment, budget-deployment, mongo-deployment)
- **Services**: 4 (auth-service, budget-service, budget-nodeport, mongo-service)
- **HPA**: 2 (auth-hpa, budget-hpa)
- **PVC**: 1 (mongodb-pvc)
- **ConfigMap**: 1 (app-config)
- **Secret**: 1 (mongo-secret)

### **Ports and Protocols**
- **External Access**: NodePort 30000 → Budget Service 5000
- **Internal Auth**: Auth Service 5001
- **Internal DB**: MongoDB 27017
- **Protocols**: HTTP/HTTPS, TCP, MongoDB Wire Protocol

## 📊 **Data Flow Patterns**

### **Authentication Flow**
- **JWT Token**: Stateless authentication
- **Session Management**: Flask sessions with cookies
- **Password Security**: bcrypt hashing
- **Rate Limiting**: API protection

### **Data Persistence**
- **User Data**: MongoDB user collection
- **Budget Data**: MongoDB budget collection
- **Expense Data**: MongoDB expense collection
- **Persistent Storage**: PVC for data survival

### **Scaling Patterns**
- **Horizontal Scaling**: HPA based on CPU usage
- **Independent Scaling**: Each service scales separately
- **Load Distribution**: Kubernetes service load balancing

## 🎨 **Visual Design Requirements**

### **Color Scheme**
- **External Access**: Blue (#007bff)
- **Frontend Layer**: Green (#28a745)
- **Authentication**: Orange (#fd7e14)
- **Data Layer**: Purple (#6f42c1)
- **Infrastructure**: Gray (#6c757d)

### **Component Shapes**
- **Browser**: Rectangle with rounded corners
- **Services**: Cylinders (containers)
- **Database**: Cylinder with data lines
- **Kubernetes**: Hexagons
- **Network**: Arrows with labels

### **Layout Structure**
- **Top**: External access and browser
- **Middle**: Application services (Budget, Auth)
- **Bottom**: Data layer (MongoDB, PVC)
- **Sides**: Infrastructure components (K8s, HPA)

## 🔍 **Detailed Annotations**

### **Service Details**
- **Budget Service**: Flask app, Jinja2 templates, Chart.js, Bootstrap
- **Auth Service**: Flask app, JWT, bcrypt, rate limiting
- **MongoDB**: Document database, persistent storage, health checks

### **Communication Details**
- **HTTP/HTTPS**: REST API calls
- **JWT Tokens**: Authentication headers
- **MongoDB Protocol**: Database queries
- **Kubernetes DNS**: Service discovery

### **Security Features**
- **JWT Authentication**: Stateless tokens
- **Password Hashing**: bcrypt with salt
- **Rate Limiting**: API protection
- **Session Security**: HttpOnly cookies

## 📝 **Additional Context**

### **Deployment Scenarios**
- **Production**: Kubernetes cluster
- **Development**: Docker Compose
- **Local**: Individual services

### **Monitoring and Health**
- **Health Checks**: Kubernetes probes
- **Logging**: Container logs
- **Metrics**: HPA monitoring
- **Scaling**: Automatic based on load

### **Data Flow Examples**
- **User Registration**: Browser → Budget Service → Auth Service → MongoDB
- **Budget Creation**: Browser → Budget Service → Auth Service (verify) → MongoDB
- **Expense Tracking**: Browser → Budget Service → MongoDB → Chart.js
- **Token Refresh**: Browser → Budget Service → Auth Service → New JWT

## 🎯 **Final Output Requirements**

Generate a comprehensive architecture diagram that:
1. **Shows all service interactions** with labeled arrows
2. **Includes data flow directions** and protocols
3. **Displays infrastructure components** clearly
4. **Highlights security features** and authentication flows
5. **Shows scaling and load balancing** mechanisms
6. **Includes port numbers** and service names
7. **Demonstrates persistent storage** connections
8. **Shows external access** through NodePort
9. **Includes technology stack** annotations
10. **Provides clear visual hierarchy** from user to data

The diagram should be professional, detailed, and suitable for technical documentation and assignment submission.
