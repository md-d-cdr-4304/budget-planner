# Budget Planner Assignment - Video Demonstration Script
## Duration: 5-10 minutes | Format: Screen Recording + Voiceover

---

## **INTRODUCTION (45 seconds)**

**[Screen: Show GitHub repository homepage]**

"Hello! I'm presenting my Budget Planner microservices application for the cloud computing assignment. This project demonstrates a complete microservices architecture deployed on Kubernetes, featuring three distinct microservices as required by the assignment."

**[Screen: Show microservices architecture diagram]**

"The application implements three microservices: **Budget Service** (Flask) for main application logic and web interface, **Auth Service** (Flask) for JWT authentication and user management, and **MongoDB Database Service** for persistent data storage. All services can be scaled independently and communicate securely within the Kubernetes cluster."

**[Screen: Show project structure in file explorer]**

"The application allows users to manage their personal finances by creating monthly budgets and tracking daily expenses, with features like data visualization, search functionality, and secure authentication. It fully satisfies all assignment requirements including Kubernetes deployment, REST API implementation, horizontal scaling, and persistent storage."

---

## **DETAILED ARCHITECTURE EXPLANATION (2 minutes)**

**[Screen: Display the Architecture Diagram prominently]**

"Let me walk you through our comprehensive architecture diagram. This visual representation shows how our microservices interact within a Kubernetes environment, following cloud architecture patterns."

**[Point to EXTERNAL section]**

"Starting from the **EXTERNAL** layer, users interact through a **Web Browser (UI)** on Port 30000. This is our entry point where users access the Budget Planner interface."

**[Point to ACCESS section]**

"The **ACCESS** layer features a **NodePort Service** that acts as our gateway, routing external HTTP/HTTPS traffic on Port 30000 into our Kubernetes cluster. This ensures secure external access while keeping internal services private."

**[Point to INFRASTRUCTURE section]**

"The **INFRASTRUCTURE** layer is the heart of our orchestration. Our **Kubernetes Cluster** runs in the `budget-planner` namespace, managing all components. The **Horizontal Pod Autoscaler (HPA)** automatically scales our microservices between 2-10 replicas based on demand, demonstrating independent horizontal scalability. **ConfigMaps** manage application configuration, while **Secrets** securely handle MongoDB credentials."

**[Point to APPLICATION section]**

"The **APPLICATION** layer contains our two core microservices:

**Budget Service** runs on Port 5000, built with Flask, Jinja2, and Chart.js. It handles the web UI, budget management logic, and data visualization. It performs CRUD operations on budgets and expenses, communicating with MongoDB for data persistence.

**Auth Service** runs on Port 5001, also built with Flask. It implements JWT authentication, bcrypt password hashing, and rate limiting for security. It validates tokens for the Budget Service and manages user authentication data.

The Budget Service communicates with the Auth Service for JWT verification, demonstrating microservices interaction."

**[Point to DATA section]**

"The **DATA** layer features **MongoDB** running on Port 27017 as a separate microservice. Both services interact with MongoDB - the Budget Service for budget/expense CRUD operations, and the Auth Service for user authentication data. **PersistentVolumeClaim** ensures data survival across pod restarts and infrastructure changes, meeting the persistent storage requirement."

"This architecture follows the microservices pattern with clear separation of concerns, independent scalability, and secure inter-service communication."

---

## **ASSIGNMENT REQUIREMENTS COMPLIANCE (1 minute)**

**[Screen: Show README.md requirements section]**

"Our application satisfies all assignment requirements:"

**[Read from README]**

"✅ **Kubernetes Deployment**: Fully deployable using Kubernetes with complete manifests
✅ **Multiple Microservices**: Two distinct microservices (Budget Service, Auth Service) plus MongoDB database  
✅ **REST API Implementation**: Each microservice implements comprehensive REST APIs
✅ **External Access**: Accessible via web browser through NodePort services
✅ **Independent Scaling**: Each microservice can be scaled horizontally using HPA
✅ **Docker Hub Images**: All images published to Docker Hub under dilshaan namespace
✅ **Database Microservice**: MongoDB running as separate microservice with persistent storage
✅ **Persistent Storage**: PVC ensures data survival across infrastructure restarts"

---

## **KUBERNETES DEPLOYMENT DEMONSTRATION (2 minutes)**

**[Screen: Open terminal/command prompt]**

"Now let me demonstrate the deployment process. I'll show you how to deploy this application on Kubernetes."

**[Type commands while explaining]**

```bash
# Show current directory and files
ls -la
```

"First, let me show you our project structure. We have complete Kubernetes manifests in the k8s folder."

```bash
# Show Kubernetes manifests
cat k8s/budget-planner-complete.yaml | head -20
```

"This is our complete Kubernetes deployment file containing all services, deployments, services, and configurations."

```bash
# Deploy the application
kubectl apply -f k8s/budget-planner-complete.yaml
```

"Now I'm deploying the entire application with a single command. This creates the namespace, MongoDB with persistent storage, both microservices, and all necessary configurations."

```bash
# Check deployment status
kubectl get pods -n budget-planner
kubectl get services -n budget-planner
```

"Let me check the deployment status. You can see all pods are running and services are active."

```bash
# Show HPA status
kubectl get hpa -n budget-planner
```

"Here's our Horizontal Pod Autoscaler configuration, demonstrating independent scaling capabilities."

---

## **WEB INTERFACE DEMONSTRATION (2.5 minutes)**

**[Screen: Open web browser and navigate to the dashboard]**

"Now let me access the application through the web interface."

```bash
# Get the application URL
minikube service budget-nodeport -n budget-planner --url
```

**[Open the URL in browser - Show the dashboard image you uploaded]**

"This is our Budget Planner dashboard - a comprehensive financial management interface. Let me walk you through its key components and functionality:"

**[Point to different sections of the dashboard]**

"**Top Navigation Bar**: Features the application title, a search bar for finding budgets and expenses, user welcome message, and logout functionality."

**[Point to Filters section]**

"**Filter Controls**: Users can filter by month and year, with a bulk select mode for managing multiple items simultaneously."

**[Point to Monthly Budgets section]**

"**Monthly Budgets Section**: 
- Input form for creating new budgets with category, amount, and month fields
- List showing existing budgets with categories like Food ($300), Transportation ($300), Entertainment ($300), Bills ($500), Shopping ($200), and Others ($1000)
- Each budget item has edit and delete buttons for full CRUD functionality"

**[Point to Daily Expenses section]**

"**Daily Expenses Section**:
- Input form for adding daily expenses with description, amount, category, and date
- List displaying expenses like Monthly rent ($500), H&M Hoodies ($100), Groceries ($125), CPH to Karlskrona ($50), Birthday Surprise ($50), and OTT Subscription ($60)
- Each expense shows category, date, and action buttons for editing and deletion"

**[Point to Budget Summary]**

"**Budget Summary**: Shows total monthly budget ($2850), total expenses ($885), and remaining amount ($1965) with color-coded indicators."

**[Point to Expense Categories pie chart]**

"**Expense Categories Visualization**: Interactive pie chart showing expense distribution across categories - Bills (pink), Shopping (purple), Food (yellow), Transportation (teal), and Entertainment (orange). This demonstrates data visualization capabilities."

**[Demonstrate functionality]**

"Let me add a new budget and expense to show real-time updates. Notice how the pie chart and summary automatically refresh, demonstrating the dynamic nature of our application."

---

## **REST API TESTING WITH POSTMAN (2 minutes)**

**[Screen: Show Postman interface with collection ready]**

"Now let me demonstrate that our REST APIs are fully functional using Postman. This proves our microservices implement proper REST API endpoints as required by the assignment."

**[Show Postman environment setup]**

"I've set up Postman with our service URLs:
- Budget Service: http://127.0.0.1:3209
- Auth Service: http://127.0.0.1:3044"

**[Execute User Registration]**

"First, I'll register a new user. The Auth Service returns JWT tokens for authentication, demonstrating our REST API implementation."

**[Execute User Login]**

"Here's the login endpoint. Notice how the system validates credentials using bcrypt and returns fresh JWT tokens, proving our security implementation."

**[Execute Create Budget]**

"Now I'll create a monthly budget. The Budget Service validates the JWT token with the Auth Service before processing, demonstrating microservices communication."

**[Execute Get Budgets]**

"This retrieves all budgets for the authenticated user, showing data persistence in MongoDB through our REST API."

**[Execute Create Expense]**

"Let me add a daily expense. Again, the JWT token is validated before processing, proving our authentication flow."

**[Execute Get Expenses]**

"This shows all expenses, demonstrating our complete CRUD operations through REST APIs."

**[Execute Invalid Token Test]**

"Finally, here's our security in action - invalid tokens are properly rejected with 401 Unauthorized, proving our API security measures."

"This demonstrates that our microservices architecture has fully functional REST APIs with proper authentication, data persistence, and security measures."

---

## **LOG OUTPUT AND MONITORING (1 minute)**

**[Screen: Show terminal with logs]**

"Let me show you the application logs to demonstrate the microservices communication:"

```bash
# Show Budget Service logs
kubectl logs -f deployment/budget-deployment -n budget-planner
```

**[Scroll through logs]**

"Here you can see the Budget Service handling requests, including JWT token verification and database operations."

```bash
# Show Auth Service logs  
kubectl logs -f deployment/auth-deployment -n budget-planner
```

"The Auth Service logs show user authentication, password hashing with bcrypt, and JWT token generation."

```bash
# Show MongoDB logs
kubectl logs -f deployment/mongo-deployment -n budget-planner
```

"MongoDB logs demonstrate data persistence and CRUD operations."

---

## **KUBERNETES YAML WALKTHROUGH (1.5 minutes)**

**[Screen: Open YAML file in editor]**

"Let me walk through our secure Kubernetes configuration to show the microservices architecture:"

**[Navigate through the YAML file]**

"Here's our complete deployment manifest with security enhancements. You can see:

- **Namespace**: budget-planner for resource isolation
- **Kubernetes Secrets**: Secure credential storage with base64 encoding
- **MongoDB Deployment**: With PersistentVolumeClaim for data persistence
- **Auth Service**: JWT authentication with bcrypt password hashing
- **Budget Service**: Web UI and API with NodePort exposure
- **Services**: Internal ClusterIP for secure communication
- **HPA**: Horizontal Pod Autoscaler for independent scaling
- **ConfigMaps**: Non-sensitive application configuration"

**[Highlight security sections]**

"**Security Features:**
- **Strong Passwords**: MongoDB2024!SecurePass, BudgetPlanner2024!SecureKey
- **Environment Variables**: Runtime credential injection from secrets
- **Network Isolation**: Internal services use ClusterIP, external via NodePort
- **Kubernetes Secret Encryption**: All credentials encrypted at rest in etcd"

**[Highlight key sections]**

"The NodePort service exposes our application on port 30000, while internal services communicate securely within the cluster. The PVC ensures data persistence across pod restarts."

---

## **SCALING DEMONSTRATION (30 seconds)**

**[Screen: Show terminal]**

"Let me demonstrate independent scaling capabilities:"

```bash
# Scale Budget Service
kubectl scale deployment budget-deployment --replicas=3 -n budget-planner
kubectl get pods -l app=budget-service -n budget-planner
```

"Here I'm scaling the Budget Service to 3 replicas independently, demonstrating how each microservice can be scaled based on demand."

---

## **ASSIGNMENT REQUIREMENTS SUMMARY (1 minute)**

**[Screen: Show requirements checklist]**

"This Budget Planner application fully satisfies all assignment requirements:

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
✅ **Secure Architecture**: Environment variable injection, network isolation, credential management"

---

## **CONCLUSION (30 seconds)**

**[Screen: Show GitHub repository]**

"In conclusion, this Budget Planner application successfully demonstrates:

- **Three distinct microservices** as required by the assignment: Budget Service, Auth Service, and MongoDB Database Service
- **Complete microservices architecture** with clear separation of concerns
- **Kubernetes deployment** with persistent storage and independent scaling  
- **Enhanced security practices** including JWT authentication, bcrypt password hashing, and Kubernetes Secrets
- **Professional web interface** with real-time data visualization and interactive charts
- **Production-ready infrastructure** with monitoring, logging, and comprehensive REST APIs
- **Secure credential management** with environment variable injection and network isolation
- **Full assignment compliance** meeting all specified requirements

The application is fully functional, accessible via web browser, and demonstrates all required assignment components with enhanced security. The complete source code and consolidated deployment manifests are available in the GitHub repository.

Thank you for watching this demonstration of the Budget Planner microservices application!"

---

## **TECHNICAL NOTES FOR RECORDING:**

### **Screen Setup:**
- **Primary Screen**: Terminal/Command Prompt (50% of screen)
- **Secondary Screen**: Web Browser (30% of screen)  
- **Tertiary Screen**: Code Editor/YAML files (20% of screen)

### **Recording Tips:**
1. **Speak clearly** and at moderate pace
2. **Pause briefly** between sections for clarity
3. **Highlight important elements** with cursor movements
4. **Show actual functionality** rather than just static screens
5. **Demonstrate real user interactions** with the application

### **Timing Breakdown:**
- Introduction: 30 seconds
- Architecture: 1 minute  
- Requirements: 1 minute
- Deployment: 2 minutes
- Web Interface: 2 minutes
- Logs: 1 minute
- YAML Walkthrough: 1 minute
- Scaling: 30 seconds
- Conclusion: 30 seconds
- **Total: 8-9 minutes**

### **Key Points to Emphasize:**
- ✅ All assignment requirements met
- ✅ Real microservices communication
- ✅ Kubernetes orchestration
- ✅ Persistent data storage
- ✅ Independent scaling
- ✅ Modern security practices
- ✅ Professional user interface
