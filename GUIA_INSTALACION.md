# EcoAndino - Guía de Instalación y Ejecución

## 📋 Requisitos del Sistema

### Requisitos de Software:
- **Python**: 3.8 o superior
- **PostgreSQL**: 12 o superior
- **pip**: Gestor de paquetes de Python
- **Git**: Para clonar el repositorio

### Requisitos de Hardware:
- **RAM**: Mínimo 2GB
- **Almacenamiento**: 500MB disponibles
- **CPU**: Cualquier procesador moderno

---

## 🚀 Instalación Paso a Paso

### 1. **Clonar el Repositorio**
```bash
git clone https://github.com/melqui16rv/ecoAndino.git
cd ecoAndino
```

### 2. **Crear Entorno Virtual (Recomendado)**
```bash
# Crear entorno virtual
python -m venv venv

# Activar entorno virtual
# En Linux/macOS:
source venv/bin/activate
# En Windows:
venv\Scripts\activate
```

### 3. **Instalar Dependencias**
```bash
pip install -r requirements.txt
```

### 4. **Configurar Base de Datos**

#### Crear Base de Datos PostgreSQL:
```sql
-- Conectar a PostgreSQL como superusuario
CREATE DATABASE ecoandino;
CREATE USER ecoandino_user WITH PASSWORD 'tu_password_segura';
GRANT ALL PRIVILEGES ON DATABASE ecoandino TO ecoandino_user;
```

#### Ejecutar Script de Creación de Tablas:
```bash
# Conectar a la base de datos y ejecutar el script
psql -U ecoandino_user -d ecoandino -f base.sql
```

### 5. **Configurar Variables de Entorno**

Crear archivo `.env` en la raíz del proyecto:
```env
# .env
DATABASE_URL=postgresql://ecoandino_user:tu_password_segura@localhost:5432/ecoandino
APP_NAME=EcoAndino API
APP_DESCRIPTION=Sistema de gestión de puntos de reciclaje
VERSION=1.0.0
DEBUG=true
```

---

## ▶️ Ejecución de la Aplicación

### **Método 1: Ejecutión Directa**
```bash
# Desde la raíz del proyecto
python -m app.main
```

### **Método 2: Con Uvicorn (Recomendado)**
```bash
# Ejecución básica
uvicorn app.main:app --reload

# Ejecución con configuración específica
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

### **Método 3: Usando el script principal**
```bash
python app/main.py
```

---

## 🧪 Verificación de la Instalación

### 1. **Verificar que la Aplicación Esté Ejecutándose**
- Abrir navegador en: `http://localhost:8000`
- Debería mostrar mensaje de bienvenida con endpoints disponibles

### 2. **Acceder a la Documentación Automática**
- **Swagger UI**: `http://localhost:8000/docs`
- **ReDoc**: `http://localhost:8000/redoc`

### 3. **Probar Endpoints Básicos**
```bash
# Obtener todas las categorías
curl -X GET "http://localhost:8000/api/v1/categorias"

# Crear una nueva categoría
curl -X POST "http://localhost:8000/api/v1/categorias" \
     -H "Content-Type: application/json" \
     -d '{
       "nombre": "Plásticos",
       "codigo": "PL001",
       "descripcion": "Materiales plásticos reciclables",
       "orden_display": 1
     }'
```

---

## 🗄️ Configuración de Base de Datos Detallada

### **Estructura de Tablas Creadas:**

1. **categorias**: Categorías de materiales reciclables
2. **materiales**: Materiales específicos por categoría  
3. **puntos_reciclaje**: Puntos de recolección georreferenciados
4. **punto_materiales**: Relación many-to-many puntos-materiales

### **Datos de Ejemplo (Opcional):**
```sql
-- Insertar categorías de ejemplo
INSERT INTO categorias (nombre, descripcion, codigo, color_identificacion, orden_display) VALUES
('Plásticos', 'Botellas, envases y recipientes plásticos', 'PL001', '#3498db', 1),
('Papel y Cartón', 'Papel, cartón, periódicos, revistas', 'PC002', '#2ecc71', 2),
('Vidrio', 'Botellas y envases de vidrio', 'VD003', '#e74c3c', 3),
('Metales', 'Latas de aluminio, acero, cobre', 'MT004', '#f39c12', 4);
```

---

## 🔧 Solución de Problemas Comunes

### **Error: "No se puede conectar a la base de datos"**
**Soluciones:**
1. Verificar que PostgreSQL esté ejecutándose:
   ```bash
   sudo systemctl status postgresql
   ```
2. Verificar credenciales en `.env`
3. Verificar que la base de datos existe:
   ```bash
   psql -U postgres -l | grep ecoandino
   ```

### **Error: "Módulo no encontrado"**
**Soluciones:**
1. Activar entorno virtual:
   ```bash
   source venv/bin/activate
   ```
2. Instalar dependencias:
   ```bash
   pip install -r requirements.txt
   ```

### **Error: "Puerto ya en uso"**
**Soluciones:**
1. Cambiar puerto de ejecución:
   ```bash
   uvicorn app.main:app --port 8001
   ```
2. Matar proceso que usa el puerto:
   ```bash
   lsof -ti:8000 | xargs kill -9
   ```

### **Error: "Permiso denegado en PostgreSQL"**
**Soluciones:**
1. Dar permisos al usuario:
   ```sql
   GRANT ALL PRIVILEGES ON DATABASE ecoandino TO ecoandino_user;
   GRANT ALL ON SCHEMA public TO ecoandino_user;
   ```

---

## 📊 Monitoreo y Logs

### **Logs de la Aplicación:**
- Los logs se muestran en la consola donde ejecutas la aplicación
- Nivel de detalle controlado por variable `DEBUG` en `.env`

### **Logs de PostgreSQL:**
```bash
# Ubuntu/Debian
tail -f /var/log/postgresql/postgresql-*.log

# CentOS/RHEL  
tail -f /var/lib/pgsql/data/log/postgresql-*.log
```

---

## 🔒 Configuración de Producción

### **Variables de Entorno para Producción:**
```env
DEBUG=false
DATABASE_URL=postgresql://usuario:password@host_produccion:5432/ecoandino_prod
APP_NAME=EcoAndino API - Producción
```

### **Ejecución en Producción:**
```bash
# Con Gunicorn (recomendado)
pip install gunicorn
gunicorn app.main:app -w 4 -k uvicorn.workers.UvicornWorker

# Con Uvicorn
uvicorn app.main:app --host 0.0.0.0 --port 80 --workers 4
```

### **Configuración de Proxy Reverso (Nginx):**
```nginx
server {
    listen 80;
    server_name tu_dominio.com;
    
    location / {
        proxy_pass http://localhost:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

---

## ✅ Lista de Verificación Pre-Entrega

### **Funcionalidad:**
- [ ] ✅ API responde en `http://localhost:8000`
- [ ] ✅ Documentación accesible en `/docs`
- [ ] ✅ Base de datos conectada correctamente
- [ ] ✅ Operaciones CRUD funcionando
- [ ] ✅ Endpoints de búsqueda georreferenciada

### **Código:**
- [ ] ✅ Todos los archivos `.py` sin errores de sintaxis
- [ ] ✅ Variables de entorno configuradas
- [ ] ✅ Dependencias instaladas correctamente
- [ ] ✅ Comentarios y documentación en código

### **Base de Datos:**
- [ ] ✅ Tablas creadas con `base.sql`
- [ ] ✅ Relaciones entre tablas funcionando
- [ ] ✅ Índices y constraints aplicados
- [ ] ✅ Datos de ejemplo insertados

### **Documentación:**
- [ ] ✅ README.md completo
- [ ] ✅ Documentación técnica detallada
- [ ] ✅ Comentarios en código explicativos
- [ ] ✅ Diagramas arquitectónicos

---

## 📞 Soporte y Contacto

### **Información del Proyecto:**
- **Nombre**: EcoAndino - Sistema de Puntos de Reciclaje
- **Versión**: 1.0.0
- **Lenguaje**: Python 3.8+
- **Framework**: FastAPI
- **Base de Datos**: PostgreSQL

### **Recursos Adicionales:**
- **FastAPI Docs**: https://fastapi.tiangolo.com/
- **PostgreSQL Docs**: https://www.postgresql.org/docs/
- **Pydantic Docs**: https://pydantic-docs.helpmanual.io/

¡Aplicación lista para demostrar el cumplimiento completo de los requisitos académicos!
