# Tutorial: Despliegue de "La Panchoneta" en Django con Docker
Práctico de Mapeo Objeto-Relacional para la materia, Bases de Datos de la carrera `Ingeniería en Sistemas` de la *`Universidad Tecnológica Nacional`* *`Facultad Regional Villa María`*.

![Docker](https://img.shields.io/badge/Docker-2496ED?style=for-the-badge&logo=docker&logoColor=white)
![Django 5.1.11](https://img.shields.io/badge/Django%205.1.11-092E20?style=for-the-badge&logo=django&logoColor=white)
![Alpine Linux](https://img.shields.io/badge/Alpine_Linux-0D597F?style=for-the-badge&logo=alpine-linux&logoColor=white)
![Python 3.13](https://img.shields.io/badge/Python%203.13-3776AB?style=for-the-badge&logo=python&logoColor=white)
![PostgreSQL 17](https://img.shields.io/badge/PostgreSQL%2017-336791?style=for-the-badge&logo=postgresql&logoColor=white)

**Referencia Rápida**

## **Mantenido por Grupo 09**
### **Integrantes:**
- Maggi, Mateo David.
- Pereyra Argüello, Milagros.
- Petry, Victoria.
- Roldán, Lautaro.
- Urzagaste, Karen.
- Zandrino, Felipe.

## **Descargo de Responsabilidad:**
El código proporcionado se ofrece "tal cual", sin garantía de ningún tipo, expresa o implícita. En ningún caso los autores o titulares de derechos de autor serán responsables de cualquier reclamo, daño u otra responsabilidad.

## Introducción
Este proyecto tiene como finalidad aplicar los contenidos vistos en la Cátedra de **Bases de Datos** mediante el desarrollo de un sistema para la gestión de un negocio de venta de panchos y bebidas. A través de este trabajo se busca poner en práctica conceptos fundamentales como el modelado de datos.

---

## Requisitos Previos
- **Docker** y **Docker Compose** instalados en tu sistema. Puedes consultar la [documentación oficial de Docker](https://docs.docker.com/get-docker/) para la instalación.
- Conocimientos básicos de Python y Django (no excluyente, el tutorial es autoexplicativo).

### Recursos Útiles
- [Tutorial oficial de Django](https://docs.djangoproject.com/en/2.0/intro/tutorial01/)
- [Cómo crear un entorno virtual en Python](https://docs.djangoproject.com/en/2.0/intro/contributing/)

---
## **Instrucciones de para levantar el proyecto**

### 1. Clonar el repositorio
> **Puedes copiar todo este bloque y pegarlo directamente en tu terminal.**
```sh
git clone https://github.com/milipereyra/panchoneta-django
```

### 2. Configuración de Variables de Entorno
En el archivo `.env.db` utilizado para almacenar las variables de entorno necesarias para la conexión a la base de datos configurarlo de la siguiente manera:

> **Puedes copiar todo este bloque y pegarlo directamente en tu archivo .env.db.**
```conf
# .env.db
# .env.db
DATABASE_ENGINE=django.db.backends.postgresql
POSTGRES_HOST=db
POSTGRES_PORT=5432
POSTGRES_DB=panchoneta
POSTGRES_USER=postgres
PGUSER=${POSTGRES_USER}
POSTGRES_PASSWORD=postgres
LANG=es_AR.utf8
POSTGRES_INITDB_ARGS="--locale-provider=icu --icu-locale=es-AR --auth-local=trust"
```

### 3. Levantar el proyecto
> [!NOTE]
> Si es la primera vez que se levanta el proyecto, desde la terminal ingresa el siguiente comando:
> 
> **Windows**
>```txt
>./init.ps1
>```
> **Linux**
>```txt
>. init.sh
>```

> [!IMPORTANT]
> En caso de que ya lo hayas levantado previamente, solo levanta el contenedor
> ```txt
>docker compuse up -d backend
>```


### 4. Acceso a La Panchoneta
Accede a la administración de DJango en `http://localhost:8000/admin/panchoneta`

---

## **Servicios Definidos en Docker Compose**
### 1. `db`
> Contenedor de PostgreSQL.
- Imagen: `postgres:alpine`
- Volumen persistente: `postgres-db`
- Variables de entorno: definidas en `.env.db`
- Healthcheck incluido (espera a que el servicio esté listo)

### 2. `backend`
> Servidor de desarrollo Django.
- Comando: `python3 manage.py runserver 0.0.0.0:8000`
- Puerto expuesto: `8000`
- Código montado desde `./src`
- Depende de: `db` (espera a que esté saludable)

### 3. `generate`
> Servicio opcional para crear el proyecto Django si no existe.
- Ejecuta: `django-admin startproject app src`
- Útil al iniciar el proyecto por primera vez
- Usa permisos de root para crear carpetas

### 4. `manage`
> Ejecuta comandos `manage.py` desde Docker.
- Entrypoint: `python3 manage.py`
- Ideal para migraciones, superusuario, etc.



---
## **Estructura del Proyecto: "La Panchoneta"**
```
PANCHONETA/
├── DiagramaClases
│ └── clases.puml # Diagrama de clases realizado en PlantUML
├── src/ # Código fuente de la aplicación
│ └── app/ # Proyecto Django
│ └── panchoneta/ # Aplicación principal
│ ├── fixtures/ # Datos de ejemplo (carga inicial con loaddata)
│ │ └── initial_data.json
│ ├── migrations/ # Migraciones de base de datos
│ ├── init.py
│ ├── admin.py # Registro de modelos en el panel de administración
│ ├── apps.py # Configuración de la app
│ ├── models.py # Definición de modelos (estructura de la BD)
│ ├── signals.py # Señales personalizadas de Django
│ ├── tests.py # Pruebas automáticas
│ ├── views.py # Vistas (lógica del backend)
│ └── manage.py # Herramienta CLI de Django
├── .env.db # Variables de entorno de la base de datos
├── docker-compose.yml # Definición de servicios Docker
├── Dockerfile # Imagen personalizada del backend
├── init.sh # Script de inicio rápido (bash)
├── init.ps1 # Script de inicio rápido (PowerShell)
└── README.md # Documentación del proyecto
```
