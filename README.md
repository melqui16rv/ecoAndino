# EcoAndino - README Principal

![EcoAndino Logo](https://img.shields.io/badge/EcoAndino-Sistema%20de%20Reciclaje-green?style=for-the-badge)
![Python](https://img.shields.io/badge/Python-3.8+-blue?style=for-the-badge&logo=python)
![FastAPI](https://img.shields.io/badge/FastAPI-0.104.1-009688?style=for-the-badge&logo=fastapi)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-12+-336791?style=for-the-badge&logo=postgresql)

## 📖 Descripción del Proyecto

**EcoAndino** es un sistema de gestión de puntos de reciclaje desarrollado en Python que implementa múltiples **patrones de diseño arquitectónicos** para demostrar las mejores prácticas en desarrollo de software. 

El sistema permite gestionar categorías de materiales reciclables, materiales específicos y puntos de reciclaje georreferenciados, proporcionando una API REST completa con operaciones CRUD para todas las entidades.

---

## 🎯 Objetivos Académicos Cumplidos

✅ **Patrones de Diseño Implementados**:
- Repository Pattern (DAO)
- Service Layer Pattern  
- DTO (Data Transfer Object)
- MVC (Model-View-Controller)
- Dependency Injection
- Factory Pattern

✅ **Conexión a Base de Datos**: PostgreSQL con manejo profesional de conexiones

✅ **Programación Orientada a Objetos**: Encapsulación, herencia, polimorfismo y abstracción

✅ **Operaciones CRUD Completas**: Create, Read, Update, Delete para todas las entidades

✅ **Lenguaje Python**: Framework moderno FastAPI con mejores prácticas

---

## 🏗️ Arquitectura del Sistema

### Estructura en Capas

```
┌─────────────────────────────────────────────┐
│                API Layer                    │ ← Endpoints REST (FastAPI)
├─────────────────────────────────────────────┤
│              Service Layer                  │ ← Lógica de Negocio
├─────────────────────────────────────────────┤
│             Repository Layer                │ ← Acceso a Datos (DAO)
├─────────────────────────────────────────────┤
│              Schema Layer                   │ ← DTOs (Pydantic)
├─────────────────────────────────────────────┤
│           Configuration Layer               │ ← Settings & DB Config
└─────────────────────────────────────────────┘
                       ↓
                ┌─────────────┐
                │ PostgreSQL  │
                │  Database   │
                └─────────────┘
```

### Componentes Principales

- **API Endpoints** (`app/api/v1/endpoints/`): Controladores REST
- **Services** (`app/services/`): Lógica de negocio
- **Repositories** (`app/repositories/`): Acceso a datos
- **Schemas** (`app/schemas/`): Objetos de transferencia de datos
- **Config** (`app/config/`): Configuración y conexiones

---

## 📁 Structure del Proyecto

```
ecoAndino/
├── app/                              # Código fuente principal
│   ├── api/v1/endpoints/            # Controllers (MVC)
│   │   ├── categorias.py           # CRUD Categorías
│   │   ├── materiales.py           # CRUD Materiales
│   │   └── puntos_reciclaje.py     # CRUD Puntos + GeoSearch
│   ├── services/                    # Service Layer Pattern
│   │   ├── categoria_service.py
│   │   ├── material_service.py
│   │   └── punto_reciclaje_service.py
│   ├── repositories/                # Repository Pattern (DAO)
│   │   ├── categoria_repository.py
│   │   ├── material_repository.py
│   │   └── punto_reciclaje_repository.py
│   ├── schemas/                     # DTO Pattern
│   │   ├── categoria.py
│   │   ├── material.py
│   │   └── punto_reciclaje.py
│   ├── config/                      # Configuration Layer
│   │   ├── database.py             # DB Connection Factory
│   │   └── settings.py             # App Settings
│   └── main.py                      # Application Factory
├── base.sql                         # Database Schema
├── demo_crud.py                     # Demostración sin Frontend
├── requirements.txt                 # Dependencias Python
├── DOCUMENTACION_TECNICA.md         # Documentación detallada
├── GUIA_INSTALACION.md              # Guía paso a paso
├── DIAGRAMAS_ARQUITECTURA.md        # Diagramas técnicos
└── README.md                        # Este archivo
```

---

## 🚀 Instalación Rápida

### 1. **Clonar Repositorio**
```bash
git clone https://github.com/melqui16rv/ecoAndino.git
cd ecoAndino
```

### 2. **Configurar Entorno Virtual**
```bash
python -m venv venv
source venv/bin/activate  # Linux/macOS
# venv\Scripts\activate   # Windows
```

### 3. **Instalar Dependencias**
```bash
pip install -r requirements.txt
```

### 4. **Configurar Base de Datos**
```sql
-- PostgreSQL
CREATE DATABASE ecoandino;
CREATE USER ecoandino_user WITH PASSWORD 'password123';
GRANT ALL PRIVILEGES ON DATABASE ecoandino TO ecoandino_user;
```

```bash
# Ejecutar schema
psql -U ecoandino_user -d ecoandino -f base.sql
```

### 5. **Variables de Entorno**
```bash
# Crear archivo .env
echo "DATABASE_URL=postgresql://ecoandino_user:password123@localhost:5432/ecoandino" > .env
echo "DEBUG=true" >> .env
```

### 6. **Ejecutar Aplicación**
```bash
uvicorn app.main:app --reload
```

### 7. **Verificar Instalación**
- API: http://localhost:8000
- Documentación: http://localhost:8000/docs

---

## 🧪 Demostración CRUD (Sin Frontend)

### Ejecutar Demo Automática
```bash
# Asegúrate de que la API esté ejecutándose
python demo_crud.py
```

### Pruebas Manuales con curl
```bash
# Crear categoría
curl -X POST "http://localhost:8000/api/v1/categorias" \
  -H "Content-Type: application/json" \
  -d '{"nombre": "Plásticos", "codigo": "PL001", "orden_display": 1}'

# Listar categorías  
curl -X GET "http://localhost:8000/api/v1/categorias"

# Actualizar categoría
curl -X PUT "http://localhost:8000/api/v1/categorias/1" \
  -H "Content-Type: application/json" \
  -d '{"descripcion": "Materiales plásticos actualizados"}'

# Eliminar categoría
curl -X DELETE "http://localhost:8000/api/v1/categorias/1"
```

---

## 🌐 API REST Endpoints

### **Categorías**
```http
GET    /api/v1/categorias           # Listar todas
POST   /api/v1/categorias           # Crear nueva
GET    /api/v1/categorias/{id}      # Obtener por ID
PUT    /api/v1/categorias/{id}      # Actualizar
DELETE /api/v1/categorias/{id}      # Eliminar
```

### **Materiales**
```http
GET    /api/v1/materiales           # Listar todos
POST   /api/v1/materiales           # Crear nuevo
GET    /api/v1/materiales/{id}      # Obtener por ID
PUT    /api/v1/materiales/{id}      # Actualizar
DELETE /api/v1/materiales/{id}      # Eliminar
```

### **Puntos de Reciclaje**
```http
GET    /api/v1/puntos-reciclaje     # Listar todos
POST   /api/v1/puntos-reciclaje     # Crear nuevo
GET    /api/v1/puntos-reciclaje/{id} # Obtener por ID
PUT    /api/v1/puntos-reciclaje/{id} # Actualizar
DELETE /api/v1/puntos-reciclaje/{id} # Eliminar

# Búsqueda georreferenciada
GET    /api/v1/puntos-reciclaje/cercanos?lat=4.6&lng=-74.08&radio=10
```

---

## 🎨 Patrones de Diseño Demostrados

### **1. Repository Pattern (DAO)**
```python
class CategoriaRepository:
    def get_all_categorias(self) -> List[CategoriaResponse]:
        # Encapsula acceso a datos
        with get_db_connection() as conn:
            # ... SQL queries
```

### **2. Service Layer Pattern**
```python
class CategoriaService:
    def __init__(self):
        self.categoria_repo = CategoriaRepository()
    
    def get_all_categorias(self):
        # Lógica de negocio
        return self.categoria_repo.get_all_categorias()
```

### **3. DTO Pattern**
```python
class CategoriaResponse(BaseModel):
    id: int
    nombre: str
    codigo: str
    # Validación automática con Pydantic
```

### **4. MVC Pattern (Adaptado)**
```python
@router.post("/", response_model=CategoriaResponse)
async def create_categoria(categoria: CategoriaBase):  # Controller
    service = CategoriaService()                       # Model
    return service.create_categoria(categoria.dict())  # View (JSON)
```

---

## 🗄️ Base de Datos

### **Entidades Principales**
- **categorias**: Categorías de materiales reciclables
- **materiales**: Materiales específicos por categoría
- **puntos_reciclaje**: Puntos georreferenciados de recolección
- **punto_materiales**: Relación many-to-many

### **Características**
- ✅ Esquema normalizado con relaciones FK
- ✅ Índices para optimización de consultas
- ✅ Triggers para timestamps automáticos
- ✅ Constraints para integridad de datos
- ✅ Tipos ENUM para validación a nivel DB

---

## 📊 Tecnologías Utilizadas

### **Backend**
- **Python 3.8+**: Lenguaje principal
- **FastAPI**: Framework web moderno
- **Pydantic**: Validación y serialización de datos
- **psycopg2**: Driver PostgreSQL
- **Uvicorn**: Servidor ASGI

### **Base de Datos**
- **PostgreSQL**: Base de datos relacional
- **SQL**: Consultas optimizadas raw
- **PostGIS**: Capacidades geoespaciales

### **Herramientas**
- **Git**: Control de versiones
- **Swagger/OpenAPI**: Documentación automática
- **Docker**: Containerización (opcional)

---

## 📚 Documentación Completa

### **Archivos de Documentación**
1. **[DOCUMENTACION_TECNICA.md](./DOCUMENTACION_TECNICA.md)**: Análisis técnico detallado
2. **[GUIA_INSTALACION.md](./GUIA_INSTALACION.md)**: Instalación paso a paso
3. **[DIAGRAMAS_ARQUITECTURA.md](./DIAGRAMAS_ARQUITECTURA.md)**: Diagramas técnicos
4. **[DEMO_CRUD_README.md](./DEMO_CRUD_README.md)**: Guía de demostración

### **Scripts Utilitarios**
- **`demo_crud.py`**: Demostración completa CRUD sin frontend
- **`base.sql`**: Schema completo de base de datos

---

## ✅ Cumplimiento de Requisitos

### **Requisitos Técnicos**
- ✅ **Múltiples patrones de diseño**: Repository, Service Layer, DTO, MVC, DI, Factory
- ✅ **Conexión a base de datos**: PostgreSQL con conexiones robustas
- ✅ **Programación Orientada a Objetos**: Clases, herencia, encapsulación, polimorfismo
- ✅ **Operaciones CRUD completas**: Create, Read, Update, Delete para todas las entidades
- ✅ **Lenguaje Python**: Framework moderno con mejores prácticas

### **Requisitos de Documentación**
- ✅ **Documentación técnica completa**: Patrones, arquitectura, diagramas
- ✅ **Guía de instalación**: Paso a paso detallada
- ✅ **Demostración funcional**: Script que prueba todas las operaciones
- ✅ **Diagramas arquitectónicos**: UML, ERD, flujos de datos
- ✅ **Código comentado**: Explicaciones claras en cada componente

---

## 🏆 Características Destacadas

### **Arquitectura Profesional**
- ✅ Separación clara de responsabilidades en capas
- ✅ Bajo acoplamiento entre componentes
- ✅ Alta cohesión en cada módulo
- ✅ Principios SOLID aplicados

### **Calidad del Código**
- ✅ Type hints para mejor desarrollo
- ✅ Validación automática de datos
- ✅ Manejo robusto de errores
- ✅ Logging y debugging estructurado

### **API REST Completa**
- ✅ Documentación automática con OpenAPI
- ✅ Validación de entrada y salida
- ✅ Códigos de estado HTTP correctos
- ✅ Respuestas JSON consistentes

### **Base de Datos Robusta**
- ✅ Modelo normalizado y optimizado
- ✅ Integridad referencial garantizada
- ✅ Consultas SQL optimizadas
- ✅ Capacidades geoespaciales

---

## 👥 Equipo de Desarrollo

**Proyecto Académico - Arquitectura de Software**
- Universidad: [Nombre de la Universidad]
- Materia: Arquitectura de Software
- Fecha: Agosto 2025

---

## 📞 Soporte

### **Recursos**
- **API Docs**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc
- **Repository**: https://github.com/melqui16rv/ecoAndino

### **Comandos Útiles**
```bash
# Ejecutar aplicación
uvicorn app.main:app --reload

# Ejecutar demostración
python demo_crud.py

# Ver logs de PostgreSQL
tail -f /var/log/postgresql/postgresql-*.log
```

---

## 🎯 Conclusión

El proyecto **EcoAndino** demuestra exitosamente la implementación de múltiples patrones de diseño arquitectónicos en una aplicación real, cumpliendo completamente con todos los requisitos académicos establecidos.

La aplicación representa una solución profesional y escalable que combina:
- **Arquitectura sólida** con separación de responsabilidades
- **Patrones de diseño** implementados correctamente
- **Base de datos robusta** con integridad garantizada
- **API REST completa** con documentación automática
- **Código limpio** siguiendo mejores prácticas

**¡Proyecto listo para evaluación académica! 🚀**
