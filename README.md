# 🌱 EcoAndino - Sistema de Gestión de Reciclaje

API REST desarrollada con FastAPI para la gestión de puntos de reciclaje y categorización de materiales reciclables en Ecuador.

## 📋 Descripción del Proyecto

EcoAndino es una API que permite gestionar información sobre:

- **Categorías de materiales** reciclables (plásticos, vidrio, papel, metales, etc.)
- **Materiales específicos** con instrucciones de preparación y beneficios ambientales
- **Puntos de reciclaje** geolocalizados con información de contacto y horarios
- **Relaciones** entre puntos y materiales aceptados

## 🗂️ Estructura del Proyecto

```
ecoAndino/
├── main.py              # Aplicación principal FastAPI
├── base.sql             # Script de creación de base de datos PostgreSQL
├── .env                 # Variables de entorno (DATABASE_URL)
├── requirements.txt     # Dependencias Python
├── .venv/              # Entorno virtual (ya configurado)
├── app/                # Módulos adicionales
└── README.md           # Este archivo
```

## 🛠️ Tecnologías Utilizadas

- **FastAPI** - Framework web moderno para Python
- **PostgreSQL** - Base de datos (hosted en Neon.tech)
- **SQLAlchemy** - ORM para Python
- **Uvicorn** - Servidor ASGI
- **psycopg2** - Adaptador PostgreSQL
- **python-dotenv** - Gestión de variables de entorno

## 🚀 Configuración y Ejecución Local

### Prerrequisitos

- Python 3.8+ instalado
- Git instalado

### 📥 1. Clonar el Repositorio

```bash
git clone https://github.com/melqui16rv/ecoAndino.git
cd ecoAndino
```

### 🐍 2. Activar el Entorno Virtual (ya configurado)

El proyecto ya tiene un entorno virtual configurado. Solo necesitas activarlo:

**En Windows:**

```bash
.venv\Scripts\activate
```

**En macOS/Linux:**

```bash
source .venv/bin/activate
```

### 🔧 3. Verificar Variables de Entorno

El archivo `.env` ya está configurado con la conexión a la base de datos. Si necesitas modificarlo:

```bash
# .env
DATABASE_URL=postgresql://neondb_owner:npg_I1OHcMDa2GwA@ep-red-rice-adioq7pe-pooler.c-2.us-east-1.aws.neon.tech/ecoAndino?sslmode=require&channel_binding=require
```

### ▶️ 4. Ejecutar la Aplicación

```bash
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

La aplicación estará disponible en:

- **API**: <http://localhost:8000>
- **Documentación Swagger**: <http://localhost:8000/docs>
- **Documentación ReDoc**: <http://localhost:8000/redoc>

## 📡 Endpoints Disponibles

### 📊 Información General

- `GET /` - Información de la API y endpoints disponibles
- `GET /test-db` - Probar conexión a base de datos y estadísticas

### 🏷️ Categorías y Materiales

- `GET /categorias` - Obtener todas las categorías de materiales
- `GET /materiales` - Obtener todos los materiales
- `GET /materiales?categoria_id={id}` - Materiales filtrados por categoría

### 📍 Puntos de Reciclaje

- `GET /puntos-reciclaje` - Obtener todos los puntos de reciclaje
- `GET /puntos-reciclaje?ciudad={nombre}` - Filtrar por ciudad
- `GET /puntos-cercanos?lat={lat}&lng={lng}&radio={km}` - Buscar puntos cercanos

### 🔗 Relaciones

- `GET /material/{material_id}/puntos` - Puntos que aceptan un material específico
- `GET /punto/{punto_id}/materiales` - Materiales aceptados por un punto

## 🧪 Ejemplos de Uso

### Obtener categorías de materiales

```bash
curl http://localhost:8000/categorias
```

### Buscar puntos de reciclaje en Quito

```bash
curl "http://localhost:8000/puntos-reciclaje?ciudad=Quito"
```

### Encontrar puntos cercanos a una ubicación

```bash
curl "http://localhost:8000/puntos-cercanos?lat=-0.1807&lng=-78.4678&radio=10"
```

### Ver qué puntos aceptan botellas PET

```bash
curl http://localhost:8000/material/1/puntos
```

## 🗄️ Base de Datos

### Estructura de Tablas

- **categorias** - Categorías principales (Plásticos, Vidrio, Papel, etc.)
- **materiales** - Materiales específicos con instrucciones de preparación
- **puntos_reciclaje** - Ubicaciones físicas con coordenadas GPS
- **punto_materiales** - Relación muchos-a-muchos entre puntos y materiales

### Recrear Base de Datos

Si necesitas recrear la base de datos, ejecuta el script SQL en Neon.tech:

```bash
# El archivo base.sql contiene toda la estructura y datos iniciales
```

## 🔧 Desarrollo

### Ejecutar en modo desarrollo

```bash
python -m uvicorn main:app --reload
```

### Agregar nuevas dependencias

```bash
pip install nueva-dependencia
pip freeze > requirements.txt
```

### Estructura de respuestas JSON

Todas las respuestas siguen el formato:

```json
{
  "data": [...],
  "total": 0,
  "message": "success"
}
```

## 🌐 Despliegue

La aplicación está configurada para desplegarse fácilmente en plataformas como:

- **Heroku**
- **Railway**
- **Render**
- **DigitalOcean**

## 👥 Equipo de Desarrollo

- **melqui16rv** - Desarrollador Principal

## 📞 Soporte

Si encuentras algún problema:

1. Verifica que el entorno virtual esté activado
2. Confirma que la base de datos esté accesible
3. Revisa los logs de la aplicación
4. Consulta la documentación en `/docs`

## 📄 Licencia

Este proyecto está bajo la Licencia MIT.

---

**¡Listo para reciclar! 🌱♻️**
