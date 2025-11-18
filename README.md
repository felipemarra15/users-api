# Users API - Backend de Registro de Usuarios

API REST para registro y consulta de usuarios. Desarrollada con Django + Django REST Framework como parte de una arquitectura de microservicios desplegada en AWS EKS.

## 📋 Descripción del Proyecto

Este servicio implementa el **backend principal** de la aplicación de registro de usuarios. Forma parte del **Ejercicio 2 y 3** del trabajo práctico de Administración de Infraestructuras, implementando un modelo de microservicios en la nube.

### Funcionalidades Principales

- ✅ **Crear usuarios**: Registra un nuevo usuario (Nombre, Email, Teléfono) en AWS RDS PostgreSQL
- ✅ **Listar usuarios**: Consulta todos los usuarios registrados en formato JSON
- ✅ **Notificaciones automáticas**: Al crear un usuario, invoca el `notification-service` vía HTTP interno
- ✅ **Health check**: Endpoint `/healthz` para verificación del estado del servicio
- ✅ **Integración con RDS**: Almacenamiento persistente en base de datos gestionada de AWS
- ✅ **Comunicación entre microservicios**: Comunicación ClusterIP con notification-service

## 🏗️ Arquitectura de Microservicios

```
Internet → ALB (HTTPS) → users-api-service (NodePort) → users-api-deployment
                                    ↓
                          AWS RDS PostgreSQL
                                    ↓
                          notification-service (ClusterIP)
```

### Componentes del Sistema

| Componente               | Función                                                      |
| ------------------------ | ------------------------------------------------------------ |
| **users-api**            | Microservicio principal con lógica de negocio               |
| **AWS RDS PostgreSQL**   | Base de datos gestionada (no pública)                       |
| **notification-service** | Microservicio de notificaciones (comunicación interna)      |
| **frontend**             | Interfaz web que consume esta API                            |

## 🔧 Tecnologías y Dependencias

### Framework y Librerías

| Paquete                   | Versión   | Descripción                                                    |
| ------------------------- | --------- | -------------------------------------------------------------- |
| **Django**                | 4.2.7     | Framework web principal para Python                            |
| **djangorestframework**   | 3.14.0    | Extensión para crear APIs RESTful                              |
| **psycopg2-binary**       | 2.9.9     | Driver para conexión con PostgreSQL (AWS RDS)                  |
| **django-cors-headers**   | 4.3.1     | Permite solicitudes CORS desde el frontend                     |
| **requests**              | 2.31.0    | Cliente HTTP para comunicación con notification-service        |

### Instalación de Dependencias

```bash
pip install -r requirements.txt
```

**Contenido de `requirements.txt`:**
```
Django==4.2.7
djangorestframework==3.14.0
psycopg2-binary==2.9.9
django-cors-headers==4.3.1
requests==2.31.0
```

## 🌐 Endpoints de la API

### 1. Crear Usuario
```http
POST /api/usuarios/
Content-Type: application/json

{
  "nombre": "Juan Pérez",
  "email": "juan@example.com",
  "telefono": "+59899123456"
}
```

**Respuesta exitosa:**
```json
{
  "id": 1,
  "nombre": "Juan Pérez",
  "email": "juan@example.com",
  "telefono": "+59899123456",
  "created_at": "2025-11-18T10:30:00Z"
}
```

### 2. Listar Usuarios
```http
GET /api/usuarios/
```

**Respuesta:**
```json
[
  {
    "id": 1,
    "nombre": "Juan Pérez",
    "email": "juan@example.com",
    "telefono": "+59899123456",
    "created_at": "2025-11-18T10:30:00Z"
  }
]
```

### 3. Health Check
```http
GET /healthz
```

**Respuesta:**
```json
{
  "status": "healthy",
  "database": "connected",
  "notification_service": "available"
}
```

## ⚙️ Configuración

### Variables de Entorno

El servicio utiliza las siguientes variables de entorno:

#### Configuración de Base de Datos (desde Kubernetes Secret)
```bash
DB_NAME=usuarios_db          # Nombre de la base de datos
DB_USER=postgres             # Usuario de PostgreSQL
DB_PASSWORD=<SECRET>         # Contraseña (almacenada en Secret)
DB_HOST=<RDS_ENDPOINT>       # Endpoint de AWS RDS
DB_PORT=5432                 # Puerto de PostgreSQL
```

#### Configuración General (desde ConfigMap)
```bash
DEBUG=False                           # Modo debug
ALLOWED_HOSTS=*                       # Hosts permitidos
NOTIFY_URL=http://notification-service.app.svc.cluster.local:9000/notify
```

### Archivos de Configuración Kubernetes

**`k8s/db-secret.yaml`** - Credenciales de base de datos:
```yaml
apiVersion: v1
kind: Secret
metadata:
  name: users-db-secret
  namespace: app
type: Opaque
stringData:
  DB_HOST: database-1.c9x8y7z6w5v4.us-east-1.rds.amazonaws.com
  DB_PORT: "5432"
  DB_NAME: usuarios_db
  DB_USER: postgres
  DB_PASS: MySecurePassword123
```

**`k8s/users-api-configmap.yaml`** - Configuración general:
```yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: users-api-config
  namespace: app
data:
  DEBUG: "False"
  ALLOWED_HOSTS: "*"
```

## 🐳 Containerización

### Dockerfile

```dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
EXPOSE 8000
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
```

### Construcción y Push a ECR

```bash
# 1. Autenticarse en ECR
aws ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin 757054385635.dkr.ecr.us-east-1.amazonaws.com

# 2. Construir imagen
docker build -t users-api .

# 3. Etiquetar
docker tag users-api:latest 757054385635.dkr.ecr.us-east-1.amazonaws.com/users-api:latest

# 4. Subir a ECR
docker push 757054385635.dkr.ecr.us-east-1.amazonaws.com/users-api:latest
```

## ☸️ Despliegue en AWS EKS

### Arquitectura de Despliegue

- **Cluster**: cluster-eks (AWS EKS)
- **Namespace**: app
- **Replicas**: 2 pods
- **Service Type**: NodePort (puerto 30930)
- **Exposición pública**: Application Load Balancer (ALB)
- **Dominio**: https://api.labinfrafinal2025.cloud-ip.cc
- **Certificado SSL**: AWS Certificate Manager
- **Base de datos**: AWS RDS PostgreSQL (no pública)

### Deployment

**`k8s/users-api-deployment.yaml`:**
```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: users-api-deployment
  namespace: app
spec:
  replicas: 2
  selector:
    matchLabels:
      app: users-api
  template:
    metadata:
      labels:
        app: users-api
    spec:
      containers:
      - name: users-api
        image: 757054385635.dkr.ecr.us-east-1.amazonaws.com/users-api:latest
        ports:
        - containerPort: 8000
        env:
        - name: DB_HOST
          valueFrom:
            secretKeyRef:
              name: users-db-secret
              key: DB_HOST
        - name: NOTIFY_URL
          value: "http://notification-service.app.svc.cluster.local:9000/notify"
        resources:
          requests:
            cpu: "200m"
            memory: "256Mi"
          limits:
            cpu: "500m"
            memory: "512Mi"
---
apiVersion: v1
kind: Service
metadata:
  name: users-api-service
  namespace: app
spec:
  type: NodePort
  selector:
    app: users-api
  ports:
  - port: 8000
    targetPort: 8000
    protocol: TCP
```

### Aplicar Manifiestos

```bash
# 1. Crear namespace
kubectl apply -f ../k8s/00-namespace.yaml

# 2. Aplicar secrets y configmaps
kubectl apply -f k8s/db-secret.yaml
kubectl apply -f k8s/users-api-configmap.yaml

# 3. Desplegar aplicación
kubectl apply -f k8s/users-api-deployment.yaml

# 4. Verificar estado
kubectl get pods -n app
kubectl get svc -n app
kubectl logs -n app -l app=users-api
```

## 🗄️ Base de Datos AWS RDS

### Configuración de RDS

- **Engine**: PostgreSQL 14.x
- **Instance Class**: db.t3.micro
- **Storage**: 20 GB SSD
- **Multi-AZ**: No (para reducir costos)
- **Public Access**: No (solo acceso desde EKS)
- **VPC**: Misma VPC que EKS
- **Security Group**: Permite puerto 5432 desde worker nodes de EKS

### Migrar Base de Datos

```bash
# Conectarse al pod de users-api
kubectl exec -it -n app deployment/users-api-deployment -- bash

# Ejecutar migraciones
python manage.py migrate

# Verificar tablas
python manage.py dbshell
\dt
```

## 🔐 Seguridad (SSDLC)

### Análisis Estático de Código (SAST)

**Herramienta**: SonarQube / SonarLint

```bash
# Análisis con SonarQube
sonar-scanner \
  -Dsonar.projectKey=users-api \
  -Dsonar.sources=. \
  -Dsonar.host.url=http://localhost:9000 \
  -Dsonar.login=<TOKEN>
```

**Configuración**: `sonar-project.properties`

### Escaneo de Vulnerabilidades en Imágenes

**Herramientas**: AWS Inspector, Trivy, Grype

```bash
# Escaneo con Grype
grype 757054385635.dkr.ecr.us-east-1.amazonaws.com/users-api:latest

# Escaneo con Trivy
trivy image 757054385635.dkr.ecr.us-east-1.amazonaws.com/users-api:latest
```

### Buenas Prácticas Implementadas

- ✅ Credenciales en Kubernetes Secrets (no en código)
- ✅ Validación de entrada en serializers de Django
- ✅ CORS configurado correctamente
- ✅ HTTPS obligatorio en producción
- ✅ Resource limits en pods
- ✅ Health checks configurados
- ✅ Logs estructurados

## 📊 Monitoreo y Logs

### Ver Logs en Tiempo Real

```bash
# Logs de todos los pods
kubectl logs -n app -l app=users-api --tail=100 -f

# Logs de un pod específico
kubectl logs -n app users-api-deployment-<POD_ID>
```

### Verificar Estado de Pods

```bash
kubectl get pods -n app
kubectl describe pod -n app users-api-deployment-<POD_ID>
```

## 🧪 Desarrollo Local

### Requisitos Previos

- Python 3.11+
- PostgreSQL 14+
- Git

### Configuración Local

1. **Clonar repositorio**:
```bash
git clone https://github.com/felipemarra15/users-api.git
cd users-api
```

2. **Crear entorno virtual**:
```bash
python3 -m venv .venv
source .venv/bin/activate  # En Windows: .venv\Scripts\activate
```

3. **Instalar dependencias**:
```bash
pip install --upgrade pip
pip install -r requirements.txt
```

4. **Configurar variables de entorno**:
```bash
export DB_NAME=usuarios_db
export DB_USER=postgres
export DB_PASSWORD=postgres
export DB_HOST=localhost
export DB_PORT=5432
export DEBUG=True
export ALLOWED_HOSTS=localhost,127.0.0.1
export NOTIFY_URL=http://localhost:9000/notify
```

5. **Ejecutar migraciones**:
```bash
python manage.py migrate
```

6. **Ejecutar servidor**:
```bash
python manage.py runserver 0.0.0.0:8000
```

7. **Probar API**:
```bash
curl http://localhost:8000/api/usuarios/
```

## 🧩 Integración con Notification Service

### Flujo de Notificación

1. Frontend envía POST a `/api/usuarios/`
2. users-api crea el usuario en PostgreSQL
3. users-api invoca `notification-service` vía HTTP interno:
   ```python
   import requests
   
   notify_url = os.getenv('NOTIFY_URL')
   payload = {
       "event": "user_created",
       "user_name": user.nombre,
       "user_email": user.email
   }
   requests.post(notify_url, json=payload)
   ```
4. notification-service envía email al administrador

### DNS Interno de Kubernetes

```
notification-service.app.svc.cluster.local:9000
```

## 📁 Estructura del Proyecto

```
users-api/
├── proyecto/                # Configuración de Django
│   ├── settings.py         # Configuración principal
│   ├── urls.py             # Rutas principales
│   └── wsgi.py
├── usuarios/               # App de usuarios
│   ├── models.py          # Modelo Usuario
│   ├── serializers.py     # Serializadores DRF
│   ├── views.py           # ViewSets de la API
│   └── urls.py            # Rutas de la API
├── k8s/                   # Manifiestos Kubernetes
│   ├── db-secret.yaml
│   ├── users-api-configmap.yaml
│   └── users-api-deployment.yaml
├── Dockerfile
├── requirements.txt
├── manage.py
└── README.md
```

## 🔗 URLs de Acceso

- **Producción (AWS)**: https://api.labinfrafinal2025.cloud-ip.cc
- **ALB DNS**: users-api-alb-1939749462.us-east-1.elb.amazonaws.com
- **Repositorio Git**: https://github.com/felipemarra15/users-api
- **Imagen ECR**: `757054385635.dkr.ecr.us-east-1.amazonaws.com/users-api:latest`
