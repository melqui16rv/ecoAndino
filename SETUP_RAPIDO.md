# 🚀 Setup Rápido - EcoAndino

## Para Compañeros de Equipo

### ⚡ Pasos Rápidos (2 minutos)

1. **Clonar el repo:**
   ```bash
   git clone https://github.com/melqui16rv/ecoAndino.git
   cd ecoAndino
   ```

2. **Activar entorno virtual:**
   ```bash
   # Windows
   .venv\Scripts\activate
   
   # macOS/Linux
   source .venv/bin/activate
   ```

3. **Ejecutar la API:**
   ```bash
   python -m uvicorn main:app --reload
   ```

4. **¡Listo!** Abre: http://localhost:8000/docs

### 🔧 URLs para Probar

- **API Principal**: http://localhost:8000
- **Documentación**: http://localhost:8000/docs
- **Test DB**: http://localhost:8000/test-db
- **Categorías**: http://localhost:8000/categorias
- **Materiales**: http://localhost:8000/materiales
- **Puntos**: http://localhost:8000/puntos-reciclaje

### ⚠️ Si algo no funciona:

1. Verifica que Python 3.8+ esté instalado
2. Asegúrate de activar el entorno virtual
3. Si hay error de DB, verifica el archivo `.env`
4. Revisa que el puerto 8000 esté libre

### 📱 Endpoints Más Útiles para Testing:

```bash
# Ver todas las categorías
curl http://localhost:8000/categorias

# Ver materiales de plásticos (categoría 1)
curl http://localhost:8000/materiales?categoria_id=1

# Buscar puntos en Quito
curl "http://localhost:8000/puntos-reciclaje?ciudad=Quito"

# Puntos cercanos al centro de Quito
curl "http://localhost:8000/puntos-cercanos?lat=-0.2202&lng=-78.5132&radio=5"
```

---
**💡 Tip**: Usa la documentación automática en `/docs` para probar todos los endpoints desde el navegador.
