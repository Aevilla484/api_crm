Este proyecto es una API desarrollada con Django para gestionar vulnerabilidades. 

La API se puede ejecutar localmente o en un contenedor Docker.

Requisitos

Python 3.9 o superior

Docker y Docker Compose (opcional para ejecución en contenedor)

pip y virtualenv

Instalación y ejecución local

Clonar el repositorio:

git clone https://github.com/Aevilla484/api_crm
cd crm_api

Crear y activar un entorno virtual:

python -m venv venv
source venv/bin/activate  # En Windows: venv\Scripts\activate

Instalar las dependencias:

pip install -r requirements.txt

Aplicar migraciones:

python manage.py migrate

Ejecutar el servidor:

python manage.py runserver

La API estará disponible en http://localhost:8000/

Ejecución con Docker

Construir la imagen del contenedor:

docker build -t mi_api_django .

Ejecutar el contenedor:

docker run -p 8000:8000 mi_api_django

La API estará disponible en http://localhost:8000/

Endpoints principales

## Endpoints

- `GET /api/nist-vulnerabilities/` - Obtener vulnerabilidades desde NIST.
- `GET /api/unfixed-vulnerabilities/` - Listar vulnerabilidades no corregidas.
- `GET /api/vulnerabilities-summary/` - Obtener un resumen de vulnerabilidades por severidad.
- `POST /api/fixed-vulnerabilities/` - Agregar vulnerabilidades corregidas.


