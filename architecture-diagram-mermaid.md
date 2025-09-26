# Budget Planner Architecture Diagram (Mermaid)

## Complete Microservices Architecture

```mermaid
graph TB
    subgraph "External Access"
        Browser[🌐 Web Browser<br/>User Interface]
    end
    
    subgraph "Kubernetes Cluster - budget-planner namespace"
        subgraph "Load Balancing & External Access"
            NodePort[🔌 NodePort Service<br/>Port 30000]
            HPA1[📈 Budget HPA<br/>2-10 replicas]
            HPA2[📈 Auth HPA<br/>2-10 replicas]
        end
        
        subgraph "Application Layer"
            BudgetService[💼 Budget Service<br/>Flask App + Web UI<br/>Port 5000<br/>Jinja2 + Bootstrap + Chart.js]
            AuthService[🔐 Auth Service<br/>Flask App + JWT<br/>Port 5001<br/>bcrypt + Rate Limiting]
        end
        
        subgraph "Data Layer"
            MongoDB[(🗄️ MongoDB<br/>Port 27017<br/>Document Database)]
            PVC[(💾 PersistentVolumeClaim<br/>1Gi Storage<br/>Data Persistence)]
        end
        
        subgraph "Infrastructure"
            ConfigMap[⚙️ ConfigMap<br/>App Configuration]
            Secret[🔑 Secret<br/>MongoDB Credentials]
            K8sDNS[🌐 Kubernetes DNS<br/>Service Discovery]
        end
    end
    
    %% External Access Flow
    Browser -->|HTTP/HTTPS<br/>Port 30000| NodePort
    NodePort -->|Load Balance| BudgetService
    
    %% Authentication Flow
    BudgetService -->|JWT Verification<br/>Internal API| AuthService
    AuthService -->|User Data<br/>CRUD Operations| MongoDB
    
    %% Data Operations Flow
    BudgetService -->|Budget/Expense Data<br/>CRUD Operations| MongoDB
    
    %% Infrastructure Connections
    BudgetService -.->|Configuration| ConfigMap
    AuthService -.->|Configuration| ConfigMap
    MongoDB -.->|Credentials| Secret
    MongoDB -->|Persistent Storage| PVC
    
    %% Scaling Connections
    HPA1 -.->|Auto Scale| BudgetService
    HPA2 -.->|Auto Scale| AuthService
    
    %% Service Discovery
    BudgetService -.->|DNS Resolution| K8sDNS
    AuthService -.->|DNS Resolution| K8sDNS
    MongoDB -.->|DNS Resolution| K8sDNS
    
    %% Styling
    classDef external fill:#e1f5fe,stroke:#01579b,stroke-width:2px
    classDef app fill:#e8f5e8,stroke:#2e7d32,stroke-width:2px
    classDef data fill:#f3e5f5,stroke:#7b1fa2,stroke-width:2px
    classDef infra fill:#f5f5f5,stroke:#424242,stroke-width:2px
    classDef loadbalancer fill:#fff3e0,stroke:#ef6c00,stroke-width:2px
    
    class Browser external
    class BudgetService,AuthService app
    class MongoDB,PVC data
    class ConfigMap,Secret,K8sDNS infra
    class NodePort,HPA1,HPA2 loadbalancer
```

## Service Communication Flow

```mermaid
sequenceDiagram
    participant Browser
    participant BudgetService
    participant AuthService
    participant MongoDB
    
    Note over Browser,MongoDB: User Registration Flow
    Browser->>BudgetService: POST /register
    BudgetService->>AuthService: POST /register
    AuthService->>MongoDB: Store user data
    MongoDB-->>AuthService: User created
    AuthService-->>BudgetService: JWT tokens
    BudgetService-->>Browser: Registration success
    
    Note over Browser,MongoDB: User Login Flow
    Browser->>BudgetService: POST /login
    BudgetService->>AuthService: POST /login
    AuthService->>MongoDB: Verify credentials
    MongoDB-->>AuthService: User data
    AuthService-->>BudgetService: JWT tokens
    BudgetService-->>Browser: Login success + session
    
    Note over Browser,MongoDB: Budget Management Flow
    Browser->>BudgetService: POST /api/monthly-budgets
    BudgetService->>AuthService: Verify JWT token
    AuthService-->>BudgetService: Token valid
    BudgetService->>MongoDB: Store budget data
    MongoDB-->>BudgetService: Budget created
    BudgetService-->>Browser: Budget added to UI
    
    Note over Browser,MongoDB: Expense Tracking Flow
    Browser->>BudgetService: POST /api/daily-expenses
    BudgetService->>AuthService: Verify JWT token
    AuthService-->>BudgetService: Token valid
    BudgetService->>MongoDB: Store expense data
    MongoDB-->>BudgetService: Expense created
    BudgetService-->>Browser: Expense added + chart update
```

## Data Flow Architecture

```mermaid
flowchart TD
    subgraph "User Interface Layer"
        UI[🌐 Web Interface<br/>HTML + CSS + JavaScript<br/>Bootstrap + Chart.js]
    end
    
    subgraph "API Gateway Layer"
        API[🔌 REST API<br/>Flask Routes<br/>JWT Middleware]
    end
    
    subgraph "Business Logic Layer"
        Auth[🔐 Authentication<br/>JWT + bcrypt<br/>Rate Limiting]
        Budget[💼 Budget Management<br/>CRUD Operations<br/>Data Validation]
    end
    
    subgraph "Data Access Layer"
        DB[(🗄️ MongoDB<br/>Collections:<br/>users, budgets, expenses)]
        Cache[⚡ Session Cache<br/>Flask Sessions<br/>JWT Tokens]
    end
    
    subgraph "Infrastructure Layer"
        K8s[☸️ Kubernetes<br/>Deployments + Services<br/>HPA + PVC]
        Monitor[📊 Monitoring<br/>Health Checks<br/>Logging]
    end
    
    UI -->|HTTP Requests| API
    API -->|Route to| Auth
    API -->|Route to| Budget
    Auth -->|User Data| DB
    Budget -->|Budget/Expense Data| DB
    Auth -->|Session Data| Cache
    Budget -->|Session Data| Cache
    DB -->|Persistent Storage| K8s
    Cache -->|Memory Storage| K8s
    K8s -->|Health Monitoring| Monitor
    
    classDef ui fill:#e3f2fd,stroke:#1976d2,stroke-width:2px
    classDef api fill:#e8f5e8,stroke:#388e3c,stroke-width:2px
    classDef business fill:#fff3e0,stroke:#f57c00,stroke-width:2px
    classDef data fill:#f3e5f5,stroke:#7b1fa2,stroke-width:2px
    classDef infra fill:#f5f5f5,stroke:#616161,stroke-width:2px
    
    class UI ui
    class API api
    class Auth,Budget business
    class DB,Cache data
    class K8s,Monitor infra
```

## Deployment Architecture

```mermaid
graph TB
    subgraph "Development Environment"
        Dev[💻 Local Development<br/>Docker Compose<br/>Port 5000]
    end
    
    subgraph "Production Environment"
        subgraph "Kubernetes Cluster"
            subgraph "budget-planner namespace"
                subgraph "Deployments"
                    AuthDeploy[🔐 auth-deployment<br/>2-10 replicas<br/>HPA enabled]
                    BudgetDeploy[💼 budget-deployment<br/>2-10 replicas<br/>HPA enabled]
                    MongoDeploy[🗄️ mongo-deployment<br/>1 replica<br/>PVC attached]
                end
                
                subgraph "Services"
                    AuthSvc[🔌 auth-service<br/>ClusterIP:5001]
                    BudgetSvc[🔌 budget-service<br/>ClusterIP:5000]
                    BudgetNodePort[🌐 budget-nodeport<br/>NodePort:30000]
                    MongoSvc[🔌 mongo-service<br/>ClusterIP:27017]
                end
                
                subgraph "Storage"
                    PVC[💾 mongodb-pvc<br/>1Gi PersistentVolume]
                end
            end
        end
    end
    
    subgraph "External Access"
        User[👤 User<br/>Web Browser]
        LoadBalancer[⚖️ Load Balancer<br/>Traffic Distribution]
    end
    
    Dev -->|Development Testing| User
    User -->|Production Access| LoadBalancer
    LoadBalancer -->|Port 30000| BudgetNodePort
    BudgetNodePort -->|Load Balance| BudgetDeploy
    BudgetDeploy -->|Internal API| AuthDeploy
    BudgetDeploy -->|Data Operations| MongoDeploy
    AuthDeploy -->|User Data| MongoDeploy
    MongoDeploy -->|Persistent Storage| PVC
    
    classDef dev fill:#e8f5e8,stroke:#4caf50,stroke-width:2px
    classDef prod fill:#e3f2fd,stroke:#2196f3,stroke-width:2px
    classDef external fill:#fff3e0,stroke:#ff9800,stroke-width:2px
    classDef storage fill:#f3e5f5,stroke:#9c27b0,stroke-width:2px
    
    class Dev dev
    class AuthDeploy,BudgetDeploy,MongoDeploy,AuthSvc,BudgetSvc,BudgetNodePort,MongoSvc prod
    class User,LoadBalancer external
    class PVC storage
```

## Security Architecture

```mermaid
graph TB
    subgraph "Security Layers"
        subgraph "Network Security"
            Firewall[🔥 Firewall<br/>Port 30000 only]
            TLS[🔒 TLS/SSL<br/>HTTPS Encryption]
        end
        
        subgraph "Application Security"
            JWT[🎫 JWT Tokens<br/>Stateless Authentication]
            Bcrypt[🔐 bcrypt Hashing<br/>Password Security]
            RateLimit[⏱️ Rate Limiting<br/>API Protection]
        end
        
        subgraph "Session Security"
            HttpOnly[🍪 HttpOnly Cookies<br/>XSS Protection]
            SameSite[🛡️ SameSite Policy<br/>CSRF Protection]
            Secure[🔒 Secure Cookies<br/>HTTPS Only]
        end
        
        subgraph "Data Security"
            Encryption[🔐 Data Encryption<br/>At Rest & In Transit]
            Access[👤 Access Control<br/>User Isolation]
            Backup[💾 Data Backup<br/>PVC Persistence]
        end
    end
    
    subgraph "Security Monitoring"
        Logs[📝 Security Logs<br/>Authentication Events]
        Alerts[🚨 Security Alerts<br/>Failed Attempts]
        Audit[🔍 Audit Trail<br/>User Actions]
    end
    
    Firewall -->|Traffic Filtering| TLS
    TLS -->|Encrypted Communication| JWT
    JWT -->|Token Validation| Bcrypt
    Bcrypt -->|Password Verification| RateLimit
    RateLimit -->|API Protection| HttpOnly
    HttpOnly -->|Cookie Security| SameSite
    SameSite -->|CSRF Protection| Secure
    Secure -->|Session Security| Encryption
    Encryption -->|Data Protection| Access
    Access -->|User Isolation| Backup
    
    JWT -->|Security Events| Logs
    RateLimit -->|Failed Attempts| Alerts
    Access -->|User Actions| Audit
    
    classDef network fill:#ffebee,stroke:#d32f2f,stroke-width:2px
    classDef app fill:#e8f5e8,stroke:#388e3c,stroke-width:2px
    classDef session fill:#fff3e0,stroke:#f57c00,stroke-width:2px
    classDef data fill:#e3f2fd,stroke:#1976d2,stroke-width:2px
    classDef monitor fill:#f3e5f5,stroke:#7b1fa2,stroke-width:2px
    
    class Firewall,TLS network
    class JWT,Bcrypt,RateLimit app
    class HttpOnly,SameSite,Secure session
    class Encryption,Access,Backup data
    class Logs,Alerts,Audit monitor
```
