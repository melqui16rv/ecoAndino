# EcoAndino - Demostración CRUD

## 🎯 Propósito

Este script demuestra el funcionamiento completo de las operaciones CRUD (Create, Read, Update, Delete) implementadas en la aplicación EcoAndino, sin necesidad de una interfaz gráfica de usuario.

## ▶️ Ejecución

```bash
# Asegúrate de que la aplicación esté ejecutándose
uvicorn app.main:app --reload

# En otra terminal, ejecuta el script de demostración
python demo_crud.py
```

## 📋 Operaciones Demostradas

### 1. **CREATE** - Crear nuevos registros
- Crear categorías de materiales
- Crear materiales específicos
- Crear puntos de reciclaje

### 2. **READ** - Consultar registros
- Listar todas las categorías
- Obtener categoría por ID
- Buscar materiales por categoría

### 3. **UPDATE** - Actualizar registros
- Modificar información de categorías
- Actualizar datos de materiales
- Cambiar estado de puntos de reciclaje

### 4. **DELETE** - Eliminar registros
- Eliminar categorías
- Remover materiales
- Desactivar puntos de reciclaje

## 🧪 Casos de Prueba

El script incluye casos de prueba para:

### **Casos Exitosos:**
✅ Creación de registros válidos  
✅ Consultas de datos existentes  
✅ Actualización parcial de campos  
✅ Eliminación de registros  

### **Casos de Error:**
❌ Intentar crear registros duplicados  
❌ Buscar registros inexistentes  
❌ Actualizar con datos inválidos  
❌ Eliminar registros con dependencias  

## 📊 Salida Esperada

```
=== DEMOSTRACIÓN CRUD ECOANDINO ===

🔸 INICIANDO PRUEBAS DE CATEGORÍAS...

✅ CREATE - Creando categoría 'Plásticos'...
   ➤ Categoría creada exitosamente con ID: 1
   ➤ Nombre: Plásticos, Código: PL001

✅ READ - Consultando todas las categorías...
   ➤ Encontradas 1 categorías:
   ➤ [1] Plásticos (PL001) - Botellas y envases plásticos

✅ UPDATE - Actualizando descripción...
   ➤ Categoría actualizada exitosamente
   ➤ Nueva descripción: Materiales plásticos reciclables mejorados

✅ DELETE - Eliminando categoría...
   ➤ Categoría eliminada exitosamente

🔸 PRUEBAS COMPLETADAS EXITOSAMENTE ✅

=== RESUMEN DE PATRONES DEMOSTRADOS ===
📋 Repository Pattern: ✅ Acceso a datos encapsulado
🏗️  Service Layer: ✅ Lógica de negocio separada  
📦 DTO Pattern: ✅ Transferencia de datos validada
🎯 CRUD Completo: ✅ Todas las operaciones funcionando
```
