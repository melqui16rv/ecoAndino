# EcoAndino - Diagramas Arquitectónicos

## 🏗️ Arquitectura General del Sistema

### Diagrama de Arquitectura en Capas

```mermaid
graph TB
    subgraph "Cliente"
        C1[Swagger UI/Docs]
        C2[Cliente HTTP]
        C3[Postman/curl]
    end
    
    subgraph "Aplicación EcoAndino"
        subgraph "API Layer"
            E1[categorias.py]
            E2[materiales.py] 
            E3[puntos_reciclaje.py]
        end
        
        subgraph "Service Layer"
            S1[CategoriaService]
            S2[MaterialService]
            S3[PuntoReciclajeService]
        end
        
        subgraph "Repository Layer"
            R1[CategoriaRepository]
            R2[MaterialRepository]
            R3[PuntoReciclajeRepository]
        end
        
        subgraph "Schema Layer"
            SC1[CategoriaSchema]
            SC2[MaterialSchema]
            SC3[PuntoReciclajeSchema]
        end
        
        subgraph "Config Layer"
            CF1[Database Config]
            CF2[Settings]
        end
    end
    
    subgraph "Base de Datos"
        DB[(PostgreSQL)]
    end
    
    C1 --> E1
    C2 --> E2
    C3 --> E3
    
    E1 --> S1
    E2 --> S2
    E3 --> S3
    
    S1 --> R1
    S2 --> R2
    S3 --> R3
    
    R1 --> DB
    R2 --> DB
    R3 --> DB
    
    E1 -.-> SC1
    E2 -.-> SC2
    E3 -.-> SC3
    
    R1 -.-> CF1
    R2 -.-> CF1
    R3 -.-> CF1
    
    S1 -.-> CF2
    S2 -.-> CF2
    S3 -.-> CF2
```

## 📊 Diagrama de Patrones de Diseño

### Repository Pattern

```mermaid
classDiagram
    class CategoriaRepository {
        +get_all_categorias() List[CategoriaResponse]
        +get_categoria_by_id(id: int) CategoriaResponse
        +create_categoria(data: Dict) CategoriaResponse
        +update_categoria(id: int, data: Dict) CategoriaResponse
        +delete_categoria(id: int) Dict
        -_build_update_query(campos: Dict)
    }
    
    class MaterialRepository {
        +get_all_materiales() List[MaterialResponse]
        +get_material_by_id(id: int) MaterialResponse
        +create_material(data: Dict) MaterialResponse
        +update_material(id: int, data: Dict) MaterialResponse
        +delete_material(id: int) Dict
    }
    
    class PuntoReciclajeRepository {
        +get_all_puntos() List[PuntoResponse]
        +get_punto_by_id(id: int) PuntoResponse
        +get_puntos_cercanos(lat: float, lng: float, radio: float)
        +create_punto(data: Dict) PuntoResponse
        +update_punto(id: int, data: Dict) PuntoResponse
        +delete_punto(id: int) Dict
    }
    
    class DatabaseConnection {
        +get_db_connection() Connection
    }
    
    CategoriaRepository --> DatabaseConnection
    MaterialRepository --> DatabaseConnection
    PuntoReciclajeRepository --> DatabaseConnection
```

### Service Layer Pattern

```mermaid
classDiagram
    class CategoriaService {
        -categoria_repo: CategoriaRepository
        +get_all_categorias() List[CategoriaResponse]
        +get_categoria_by_id(id: int) CategoriaResponse
        +create_categoria(data: dict) CategoriaResponse
        +update_categoria(id: int, data: dict) CategoriaResponse
        +delete_categoria(id: int) Dict
    }
    
    class MaterialService {
        -material_repo: MaterialRepository
        +get_all_materiales() List[MaterialResponse]
        +get_material_by_id(id: int) MaterialResponse
        +create_material(data: dict) MaterialResponse
        +update_material(id: int, data: dict) MaterialResponse
        +delete_material(id: int) Dict
    }
    
    class PuntoReciclajeService {
        -punto_repo: PuntoReciclajeRepository
        +get_all_puntos() List[PuntoResponse]
        +get_punto_by_id(id: int) PuntoResponse
        +get_puntos_cercanos(lat, lng, radio) List[PuntoResponse]
        +create_punto(data: dict) PuntoResponse
        +update_punto(id: int, data: dict) PuntoResponse
        +delete_punto(id: int) Dict
    }
    
    CategoriaService --> CategoriaRepository
    MaterialService --> MaterialRepository
    PuntoReciclajeService --> PuntoReciclajeRepository
```

### DTO Pattern (Data Transfer Objects)

```mermaid
classDiagram
    class BaseModel {
        <<Pydantic>>
    }
    
    class CategoriaBase {
        +nombre: str
        +descripcion: Optional[str]
        +codigo: str
        +color_identificacion: Optional[str]
        +icono: Optional[str]
        +orden_display: int
        +activo: bool
    }
    
    class CategoriaResponse {
        +id: int
    }
    
    class MaterialBase {
        +nombre: str
        +descripcion: Optional[str]
        +categoria_id: int
        +precio_kg: Optional[float]
        +unidad_medida: str
        +activo: bool
    }
    
    class MaterialResponse {
        +id: int
    }
    
    class PuntoReciclajeBase {
        +nombre: str
        +direccion: str
        +latitud: float
        +longitud: float
        +telefono: Optional[str]
        +email: Optional[str]
        +horario_atencion: Optional[str]
        +tipo_instalacion: str
        +estado: str
        +capacidad_maxima: Optional[float]
        +activo: bool
    }
    
    class PuntoReciclajeResponse {
        +id: int
    }
    
    BaseModel <|-- CategoriaBase
    BaseModel <|-- MaterialBase
    BaseModel <|-- PuntoReciclajeBase
    CategoriaBase <|-- CategoriaResponse
    MaterialBase <|-- MaterialResponse
    PuntoReciclajeBase <|-- PuntoReciclajeResponse
```

## 🗄️ Diagrama de Base de Datos

### Modelo Entidad-Relación

```mermaid
erDiagram
    CATEGORIAS {
        int id PK
        varchar nombre
        text descripcion
        varchar codigo
        varchar color_identificacion
        varchar icono
        int orden_display
        boolean activo
        timestamp created_at
        timestamp updated_at
    }
    
    MATERIALES {
        int id PK
        varchar nombre
        text descripcion
        int categoria_id FK
        decimal precio_kg
        varchar unidad_medida
        boolean activo
        timestamp created_at
        timestamp updated_at
    }
    
    PUNTOS_RECICLAJE {
        int id PK
        varchar nombre
        text direccion
        decimal latitud
        decimal longitud
        varchar telefono
        varchar email
        text horario_atencion
        enum tipo_instalacion
        enum estado
        decimal capacidad_maxima
        boolean activo
        timestamp created_at
        timestamp updated_at
    }
    
    PUNTO_MATERIALES {
        int id PK
        int punto_reciclaje_id FK
        int material_id FK
        decimal precio_compra
        boolean acepta_material
        text observaciones
        timestamp created_at
        timestamp updated_at
    }
    
    CATEGORIAS ||--o{ MATERIALES : "tiene"
    PUNTOS_RECICLAJE ||--o{ PUNTO_MATERIALES : "acepta"
    MATERIALES ||--o{ PUNTO_MATERIALES : "se_recicla_en"
```

## 🔄 Diagrama de Flujo CRUD

### Flujo de Operaciones CRUD

```mermaid
flowchart TD
    A[Cliente HTTP] --> B{Tipo de Operación}
    
    B -->|POST| C[CREATE]
    B -->|GET| D[READ]
    B -->|PUT| E[UPDATE]
    B -->|DELETE| F[DELETE]
    
    C --> C1[Validar Datos<br/>Pydantic Schema]
    D --> D1[Procesar Consulta<br/>Service Layer]
    E --> E1[Validar Cambios<br/>Service Layer]
    F --> F1[Verificar Dependencias<br/>Service Layer]
    
    C1 --> C2{¿Válidos?}
    C2 -->|No| C3[HTTP 422<br/>Error Validación]
    C2 -->|Sí| C4[Service Layer<br/>Lógica Negocio]
    
    D1 --> D2[Repository Layer<br/>Consulta BD]
    E1 --> E2[Repository Layer<br/>Actualización BD]
    F1 --> F2[Repository Layer<br/>Eliminación BD]
    
    C4 --> C5[Repository Layer<br/>Inserción BD]
    
    C5 --> C6{¿Éxito?}
    D2 --> D3{¿Encontrado?}
    E2 --> E3{¿Actualizado?}
    F2 --> F3{¿Eliminado?}
    
    C6 -->|No| C7[HTTP 500<br/>Error Servidor]
    C6 -->|Sí| C8[HTTP 201<br/>Recurso Creado]
    
    D3 -->|No| D4[HTTP 404<br/>No Encontrado]
    D3 -->|Sí| D5[HTTP 200<br/>Datos JSON]
    
    E3 -->|No| E4[HTTP 404<br/>No Encontrado]
    E3 -->|Sí| E5[HTTP 200<br/>Datos Actualizados]
    
    F3 -->|No| F4[HTTP 404<br/>No Encontrado]
    F3 -->|Sí| F5[HTTP 200<br/>Confirmación]
    
    C8 --> G[Respuesta Cliente]
    D5 --> G
    E5 --> G
    F5 --> G
    C3 --> G
    C7 --> G
    D4 --> G
    E4 --> G
    F4 --> G
```

## 🌐 Diagrama de API REST

### Endpoints y Métodos HTTP

```mermaid
graph LR
    subgraph "API REST EcoAndino"
        subgraph "Categorías"
            CAT1[GET /categorias<br/>Listar todas]
            CAT2[POST /categorias<br/>Crear nueva]
            CAT3[GET /categorias/{id}<br/>Obtener por ID]
            CAT4[PUT /categorias/{id}<br/>Actualizar]
            CAT5[DELETE /categorias/{id}<br/>Eliminar]
        end
        
        subgraph "Materiales"
            MAT1[GET /materiales<br/>Listar todos]
            MAT2[POST /materiales<br/>Crear nuevo]
            MAT3[GET /materiales/{id}<br/>Obtener por ID]
            MAT4[PUT /materiales/{id}<br/>Actualizar]
            MAT5[DELETE /materiales/{id}<br/>Eliminar]
        end
        
        subgraph "Puntos de Reciclaje"
            PTO1[GET /puntos-reciclaje<br/>Listar todos]
            PTO2[POST /puntos-reciclaje<br/>Crear nuevo]
            PTO3[GET /puntos-reciclaje/{id}<br/>Obtener por ID]
            PTO4[PUT /puntos-reciclaje/{id}<br/>Actualizar]
            PTO5[DELETE /puntos-reciclaje/{id}<br/>Eliminar]
            PTO6[GET /puntos-reciclaje/cercanos<br/>Búsqueda geoespacial]
        end
    end
    
    subgraph "Códigos de Respuesta HTTP"
        HTTP1[200 - OK]
        HTTP2[201 - Created]
        HTTP3[404 - Not Found]
        HTTP4[422 - Validation Error]
        HTTP5[500 - Server Error]
    end
    
    CAT1 --> HTTP1
    CAT2 --> HTTP2
    CAT3 --> HTTP1
    CAT3 --> HTTP3
    MAT1 --> HTTP1
    PTO6 --> HTTP1
```

## 🔧 Diagrama de Configuración y Deployment

### Componentes del Sistema

```mermaid
graph TB
    subgraph "Desarrollo"
        DEV1[Python 3.8+]
        DEV2[FastAPI]
        DEV3[Pydantic]
        DEV4[psycopg2]
        DEV5[Uvicorn]
    end
    
    subgraph "Base de Datos"
        DB1[(PostgreSQL 12+)]
        DB2[Tablas Relacionales]
        DB3[Índices Optimizados]
        DB4[Constraints FK]
        DB5[Triggers Timestamp]
    end
    
    subgraph "Configuración"
        CONF1[.env Variables]
        CONF2[Settings Class]
        CONF3[Database Config]
        CONF4[CORS Middleware]
    end
    
    subgraph "Deployment"
        DEPLOY1[Uvicorn Server]
        DEPLOY2[Gunicorn + Workers]
        DEPLOY3[Nginx Reverse Proxy]
        DEPLOY4[Docker Container]
    end
    
    DEV1 --> DEV2
    DEV2 --> DEV3
    DEV2 --> DEV4
    DEV2 --> DEV5
    
    DEV4 --> DB1
    DB1 --> DB2
    DB2 --> DB3
    DB2 --> DB4
    DB2 --> DB5
    
    DEV2 --> CONF1
    CONF1 --> CONF2
    CONF2 --> CONF3
    DEV2 --> CONF4
    
    DEV5 --> DEPLOY1
    DEPLOY1 --> DEPLOY2
    DEPLOY2 --> DEPLOY3
    DEPLOY3 --> DEPLOY4
```

---

## 📋 Resumen de Diagramas

### **1. Arquitectura en Capas**
- ✅ Separación clara de responsabilidades
- ✅ API → Service → Repository → Database
- ✅ Schemas transversales para validación

### **2. Patrones de Diseño**
- ✅ Repository Pattern: Acceso a datos encapsulado
- ✅ Service Layer: Lógica de negocio centralizada
- ✅ DTO Pattern: Transferencia de datos tipada

### **3. Base de Datos Relacional**
- ✅ Modelo normalizado con relaciones FK
- ✅ Integridad referencial garantizada
- ✅ Optimización con índices

### **4. API REST Completa**
- ✅ Operaciones CRUD para todas las entidades
- ✅ Códigos HTTP estándar
- ✅ Documentación automática

### **5. Flujo de Datos**
- ✅ Validación automática con Pydantic
- ✅ Manejo estructurado de errores
- ✅ Respuestas JSON consistentes

Estos diagramas demuestran la implementación profesional de una arquitectura sólida que cumple completamente con los requisitos académicos del proyecto.
