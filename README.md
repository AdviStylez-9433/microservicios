# Microservicios con Docker Compose

Este proyecto implementa dos microservicios (`Estudiante` y `Evaluación`) conectados a una base de datos PostgreSQL, utilizando Docker Compose para la orquestación.

## Requisitos previos
- Docker Engine (v20.10+)
- Docker Compose (v2.0+)
- Postman o cURL para probar los endpoints

## Configuración
1. Clona el repositorio:
   ```bash
   git clone [URL_DEL_REPOSITORIO]
   cd microservicios-docker

2. Configura las variables de entorno (opcional):
    Edita el archivo .env para cambiar las credenciales de la base de datos.

3. Construye y levanta los servicios:
    ```bash
    docker compose up -d --build

## Endpoints disponibles
### Microservicio Estudiante (Puerto 5000)

- **`POST /estudiantes`**  
  Crear nuevo estudiante.

- **`GET /estudiantes`**  
  Listar todos los estudiantes.

- **`GET /estudiantes/{rut}`**  
  Obtener estudiante por RUT.

---

### Microservicio Evaluación (Puerto 5001)

- **`POST /evaluaciones`**  
  Crear nueva evaluación.

- **`GET /evaluaciones`**  
  Listar todas las evaluaciones.

- **`GET /evaluaciones/{id}`**  
  Obtener evaluación por ID.

## Estructura del proyecto

microservicios-docker/
├── estudiante/
│   ├── app.py           # Lógica del servicio
│   ├── requirements.txt # Dependencias
│   └── Dockerfile       # Configuración del contenedor
├── evaluacion/
│   ├── app.py
│   ├── requirements.txt
│   └── Dockerfile
├── docker-compose.yml   # Orquestación de servicios
└── README.md            # Documentación

## Pruebas con Postman

- **`POST /estudiantes`**  
http://localhost:5000/estudiantes
{
    "rut": "12345678-9",
    "nombre": "Ana Pérez",
    "edad": 20,
    "curso": "Matemáticas"
}

- **`GET /estudiantes`**  
http://localhost:5000/estudiantes

- **`GET /estudiantes/{rut}`**  
http://localhost:5000/estudiantes/12345678-9

---

- **`POST /evaluaciones`**  
http://localhost:5001/evaluaciones
{
    "rut_estudiante": "12345678-9",
    "semestre": "2023-2",
    "asignatura": "Cálculo",
    "evaluacion": 6.5
}

- **`GET /evaluaciones`**  
http://localhost:5001/evaluaciones

- **`GET /evaluaciones/{id}`**  
http://localhost:5001/evaluaciones/1

## Comandos útiles

| Comando | Descripción |
|---------|-------------|
| `docker compose up -d` | Inicia los servicios en segundo plano |
| `docker compose down -v` | Detiene los servicios y elimina volúmenes |
| `docker compose logs estudiante` | Muestra los logs del servicio Estudiante |
| `docker exec -it [DB_CONTAINER] psql -U user -d microservicios` | Accede a la base de datos PostgreSQL |

**Nota:** Reemplaza `[DB_CONTAINER]` con el ID o nombre del contenedor de la base de datos.