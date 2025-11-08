# users-api


API REST (Django + DRF) para **alta** y **listado** de usuarios.  
Al crear un usuario, se envía **notificación por email**.

## Requisitos
- WSL/Ubuntu o Linux (Python 3.10+)
- PostgreSQL (corriendo en Windows u host accesible)
- Cuenta SMTP (p. ej., TurboSMTP)

## Configuración rápida (WSL)
1. **Clonar** y crear **venv**:
   ```bash
   cd ~/proyectos
   git clone <URL-DEL-REPO> users-api
   cd users-api
   python3 -m venv .venv
   source .venv/bin/activate
   python -m pip install --upgrade pip wheel
   pip install -r requirements.txt
