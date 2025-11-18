# Users API

API REST para registro y consulta de usuarios. Desarrollada con Django + Django REST Framework.

## Descripción

Este servicio implementa el backend de la aplicación de registro de usuarios. Proporciona endpoints REST para:

- **Crear usuarios**: Registra un nuevo usuario en la base de datos y envía notificación por email
- **Listar usuarios**: Consulta todos los usuarios registrados
- **Health check**: Verificación del estado del servicio

Al crear un usuario, la API invoca automáticamente el `notification-service` para enviar un email de notificación.

## Tecnologías

| Paquete                   | Descripción                                                    |
| ------------------------- | -------------------------------------------------------------- |
| **Django**                | Framework web principal para Python                            |
| **djangorestframework**   | Extensión para crear APIs RESTful                              |
| **psycopg2-binary**       | Driver para conexión con PostgreSQL                            |
| **django-cors-headers**   | Permite solicitudes CORS desde el frontend                     |
| **requests**              | Cliente HTTP para comunicación con notification-service        |

## Configuración

El servicio utiliza las siguientes variables de entorno:

- `DB_NAME`: Nombre de la base de datos PostgreSQL
- `DB_USER`: Usuario de la base de datos
- `DB_PASSWORD`: Contraseña de la base de datos
- `DB_HOST`: Host de la base de datos (RDS en AWS)
- `DB_PORT`: Puerto de la base de datos (5432)
- `DEBUG`: Modo debug (True/False)
- `ALLOWED_HOSTS`: Hosts permitidos
- `NOTIFY_URL`: URL del notification-service

Las credenciales de la base de datos se almacenan en un Secret de Kubernetes, mientras que otras configuraciones están en un ConfigMap.

## Despliegue

La aplicación se despliega en AWS EKS con:
- **Base de datos**: AWS RDS PostgreSQL
- **Servicio**: NodePort
- **Ingress**: AWS Network Load Balancer (NLB)
- **HTTPS**: Certificado SSL/TLS mediante AWS Certificate Manager
- **Dominio**: api.labinfrafinal2025.cloud-ip.cc
- **Namespace**: app

## Desarrollo Local (WSL)

1. **Clonar y crear entorno virtual**:
   ```bash
   cd ~/proyectos
   git clone <URL-DEL-REPO> users-api
   cd users-api
   python3 -m venv .venv
   source .venv/bin/activate
   python -m pip install --upgrade pip wheel
   pip install -r requirements.txt
