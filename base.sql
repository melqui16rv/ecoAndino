-- ============================================================================
-- SCRIPT DE CREACIÓN DE BASE DE DATOS SIMPLIFICADA PARA ECOANDINO
-- Sistema de Puntos de Reciclaje y Categorías de Materiales
-- ============================================================================

-- Eliminar tablas si existen (para recrear limpiamente)
DROP TABLE IF EXISTS punto_materiales CASCADE;
DROP TABLE IF EXISTS materiales CASCADE;
DROP TABLE IF EXISTS puntos_reciclaje CASCADE;
DROP TABLE IF EXISTS categorias CASCADE;

-- ============================================================================
-- TABLA: categorias
-- Almacena las categorías principales de materiales reciclables
-- ============================================================================
CREATE TABLE categorias (
    id SERIAL PRIMARY KEY,
    nombre VARCHAR(50) NOT NULL UNIQUE,
    descripcion TEXT,
    codigo VARCHAR(10) NOT NULL UNIQUE,
    color_identificacion VARCHAR(7) DEFAULT '#FFFFFF', -- Color hex para UI
    icono VARCHAR(50), -- Nombre del icono para la interfaz
    orden_display INTEGER DEFAULT 1, -- Para ordenar en la UI
    activo BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- ============================================================================
-- TABLA: materiales
-- Almacena los tipos específicos de materiales reciclables
-- ============================================================================
CREATE TABLE materiales (
    id SERIAL PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    categoria_id INTEGER NOT NULL REFERENCES categorias(id) ON DELETE CASCADE,
    codigo VARCHAR(10) NOT NULL UNIQUE,
    descripcion TEXT,
    preparacion_requerida TEXT, -- Instrucciones de preparación
    beneficio_ambiental TEXT,
    es_peligroso BOOLEAN DEFAULT FALSE,
    requiere_manejo_especial BOOLEAN DEFAULT FALSE,
    ejemplos TEXT, -- Ejemplos específicos del material
    materiales_no_aceptados TEXT, -- Qué NO se acepta en esta categoría
    activo BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- ============================================================================
-- TABLA: puntos_reciclaje
-- Almacena información de centros de acopio y puntos de reciclaje
-- ============================================================================
CREATE TABLE puntos_reciclaje (
    id SERIAL PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    descripcion TEXT,
    direccion VARCHAR(200) NOT NULL,
    ciudad VARCHAR(50) NOT NULL,
    provincia VARCHAR(50),
    codigo_postal VARCHAR(10),
    latitud DECIMAL(10, 8) NOT NULL,
    longitud DECIMAL(11, 8) NOT NULL,
    tipo_instalacion ENUM('centro_acopio', 'punto_limpio', 'estacion_reciclaje', 'punto_movil', 'contenedor_publico') 
        DEFAULT 'centro_acopio',
    horario_apertura TIME,
    horario_cierre TIME,
    dias_servicio VARCHAR(100) DEFAULT 'Lunes,Martes,Miércoles,Jueves,Viernes,Sábado',
    telefono VARCHAR(20),
    email VARCHAR(100),
    sitio_web VARCHAR(200),
    capacidad_estimada VARCHAR(50), -- Descripción de capacidad
    instrucciones_acceso TEXT, -- Cómo llegar o instrucciones especiales
    foto_url VARCHAR(500), -- URL de foto del punto
    estado ENUM('activo', 'inactivo', 'mantenimiento', 'temporalmente_cerrado') DEFAULT 'activo',
    fecha_registro TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    fecha_actualizacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- ============================================================================
-- TABLA: punto_materiales (RELACIÓN MUCHOS A MUCHOS)
-- Conecta qué materiales acepta cada punto de reciclaje
-- ============================================================================
CREATE TABLE punto_materiales (
    id SERIAL PRIMARY KEY,
    punto_reciclaje_id INTEGER NOT NULL REFERENCES puntos_reciclaje(id) ON DELETE CASCADE,
    material_id INTEGER NOT NULL REFERENCES materiales(id) ON DELETE CASCADE,
    acepta BOOLEAN DEFAULT TRUE,
    observaciones TEXT, -- Condiciones especiales para este material en este punto
    cantidad_maxima VARCHAR(50), -- Límite de cantidad si aplica
    horario_especial VARCHAR(100), -- Si tiene horario diferente para este material
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    -- Evitar duplicados
    UNIQUE(punto_reciclaje_id, material_id)
);

-- ============================================================================
-- ÍNDICES PARA OPTIMIZACIÓN
-- ============================================================================
CREATE INDEX idx_materiales_categoria ON materiales(categoria_id);
CREATE INDEX idx_materiales_codigo ON materiales(codigo);
CREATE INDEX idx_materiales_activo ON materiales(activo);
CREATE INDEX idx_puntos_ciudad ON puntos_reciclaje(ciudad);
CREATE INDEX idx_puntos_coordenadas ON puntos_reciclaje(latitud, longitud);
CREATE INDEX idx_puntos_tipo ON puntos_reciclaje(tipo_instalacion);
CREATE INDEX idx_puntos_estado ON puntos_reciclaje(estado);
CREATE INDEX idx_punto_materiales_punto ON punto_materiales(punto_reciclaje_id);
CREATE INDEX idx_punto_materiales_material ON punto_materiales(material_id);
CREATE INDEX idx_categorias_activo ON categorias(activo);

-- ============================================================================
-- TRIGGERS PARA ACTUALIZACIÓN AUTOMÁTICA DE TIMESTAMPS
-- ============================================================================
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ language 'plpgsql';

CREATE TRIGGER update_categorias_updated_at 
    BEFORE UPDATE ON categorias 
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_materiales_updated_at 
    BEFORE UPDATE ON materiales 
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_puntos_updated_at 
    BEFORE UPDATE ON puntos_reciclaje 
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

-- ============================================================================
-- DATOS INICIALES: CATEGORÍAS
-- ============================================================================
INSERT INTO categorias (nombre, descripcion, codigo, color_identificacion, icono, orden_display) VALUES
('Plásticos', 'Materiales plásticos reciclables con códigos PET, HDPE, PVC, LDPE, PP, PS', 'PLA', '#FFE135', 'plastic-bottle', 1),
('Vidrio', 'Botellas y envases de vidrio de diferentes colores', 'VID', '#4CAF50', 'glass-bottle', 2),
('Papel y Cartón', 'Papel, cartón y materiales celulósicos reciclables', 'PAP', '#2196F3', 'file-text', 3),
('Metales', 'Aluminio, acero y otros metales reciclables', 'MET', '#9E9E9E', 'metal-can', 4),
('Electrónicos', 'Residuos de aparatos eléctricos y electrónicos (RAEE)', 'ELE', '#FF5722', 'smartphone', 5),
('Textiles', 'Ropa, telas y materiales textiles reutilizables', 'TEX', '#E91E63', 'shirt', 6),
('Orgánicos', 'Residuos orgánicos para compostaje', 'ORG', '#8BC34A', 'leaf', 7),
('Especiales', 'Materiales que requieren manejo específico', 'ESP', '#FF9800', 'alert-triangle', 8),
('Madera', 'Productos de madera reutilizables y reciclables', 'MAD', '#795548', 'tree', 9),
('Peligrosos', 'Residuos que requieren manejo especial por seguridad', 'PEL', '#F44336', 'warning', 10);

-- ============================================================================
-- DATOS INICIALES: MATERIALES
-- ============================================================================
INSERT INTO materiales (nombre, categoria_id, codigo, descripcion, preparacion_requerida, beneficio_ambiental, ejemplos, materiales_no_aceptados, es_peligroso) VALUES
-- PLÁSTICOS
('Botellas PET', 1, 'PET01', 'Botellas de agua y bebidas', 'Lavar, aplastar y mantener tapa', 'Reduce contaminación marina y ahorra petróleo', 'Botellas de agua, bebidas, aceites comestibles', 'Botellas de productos químicos, muy sucias', false),
('Envases HDPE', 1, 'HDP01', 'Envases de detergentes y shampoo', 'Lavar completamente y quitar etiquetas', 'Reduce residuos plásticos domésticos', 'Envases de shampoo, detergente, leche', 'Envases con residuos químicos peligrosos', false),
('Bolsas LDPE', 1, 'LDP01', 'Bolsas plásticas limpias', 'Limpiar y secar completamente', 'Evita contaminación de suelos', 'Bolsas de supermercado, de pan, film transparente', 'Bolsas biodegradables, muy sucias', false),
('Tapas PP', 1, 'PP001', 'Tapas de botellas de polipropileno', 'Separar de botellas y limpiar', 'Facilita reciclaje completo', 'Tapas de botellas, envases de yogurt', 'Tapas de productos químicos', false),

-- VIDRIO
('Botellas transparentes', 2, 'VID01', 'Botellas de vidrio transparente', 'Lavar y quitar tapas metálicas', 'Reciclaje infinito sin pérdida de calidad', 'Botellas de agua, vino, cerveza transparente', 'Vidrio de ventanas, espejos, pyrex', false),
('Botellas verdes', 2, 'VID02', 'Botellas de vidrio verde', 'Lavar y separar por color', 'Reduce extracción de materias primas', 'Botellas de vino, cerveza verde', 'Vidrio plano, cristal de vajilla', false),
('Frascos de conservas', 2, 'VID03', 'Frascos de alimentos y conservas', 'Lavar completamente y quitar etiquetas', 'Ahorra energía en producción', 'Frascos de mermelada, conservas, cosméticos', 'Frascos de medicamentos, químicos', false),

-- PAPEL Y CARTÓN
('Papel blanco', 3, 'PAP01', 'Papel de oficina y documentos', 'Mantener seco y limpio, quitar grapas', 'Salva árboles y reduce deforestación', 'Papel de oficina, cuadernos, libros', 'Papel higiénico, papeles engrasados, carbón', false),
('Cartón corrugado', 3, 'PAP02', 'Cajas de cartón ondulado', 'Aplanar y mantener seco', 'Reduce tala de árboles', 'Cajas de electrodomésticos, paquetería', 'Cartón húmedo, encerado, sucio', false),
('Periódicos y revistas', 3, 'PAP03', 'Papel de prensa y revistas', 'Mantener secos y sin contaminar', 'Reduce residuos y ahorra fibra', 'Periódicos, revistas, folletos', 'Papel plastificado, autoadhesivo', false),

-- METALES
('Latas de aluminio', 4, 'ALU01', 'Latas de bebidas de aluminio', 'Enjuagar y aplastar', 'Ahorra 95% de energía vs producción nueva', 'Latas de bebidas, cervezas', 'Latas de pintura, aerosoles', false),
('Latas de conservas', 4, 'ACE01', 'Latas de acero para alimentos', 'Lavar y quitar etiquetas', 'Reduce extracción minera', 'Latas de atún, conservas, salsas', 'Latas oxidadas, con químicos', false),
('Chatarra de cobre', 4, 'COB01', 'Cable de cobre y tuberías', 'Separar de cubiertas plásticas', 'Alto valor económico y ambiental', 'Cables eléctricos, tuberías', 'Cobre contaminado con plomo', false),

-- ELECTRÓNICOS
('Teléfonos móviles', 5, 'ELE01', 'Smartphones y tablets', 'Borrar datos personales y quitar batería', 'Recupera metales preciosos', 'Celulares, tablets, smartwatches', 'Equipos con baterías dañadas', true),
('Computadoras', 5, 'ELE02', 'PCs y laptops completas', 'Formatear discos y desconectar', 'Evita contaminación por metales pesados', 'Computadoras, laptops, servidores', 'Equipos con CRT (monitores antiguos)', true),
('Pilas y baterías', 5, 'PIL01', 'Pilas domésticas y baterías', 'Depositar en contenedor especial', 'Previene contaminación del suelo', 'Pilas AA, AAA, baterías de teléfono', 'Baterías de auto, industriales', true),

-- TEXTILES
('Ropa usada', 6, 'TEX01', 'Ropa en buen estado para reutilización', 'Lavar y secar completamente', 'Reduce industria textil contaminante', 'Camisas, pantalones, vestidos', 'Ropa muy deteriorada, íntima', false),
('Calzado', 6, 'TEX02', 'Zapatos y calzado reutilizable', 'Limpiar y verificar estado', 'Evita residuos de cuero y sintéticos', 'Zapatos, botas, sandalias', 'Calzado muy dañado, con moho', false),

-- ORGÁNICOS
('Restos vegetales', 7, 'ORG01', 'Frutas, verduras y restos de poda', 'Separar de otros residuos', 'Produce compost nutritivo', 'Cáscaras de fruta, restos de verdura', 'Carne, pescado, lácteos', false),
('Residuos de jardín', 7, 'ORG02', 'Hojas, césped y poda', 'Libre de químicos y plásticos', 'Mejora suelos y reduce metano', 'Hojas secas, césped, ramas pequeñas', 'Plantas tratadas con pesticidas', false),

-- ESPECIALES
('Aceite de cocina', 8, 'ACE01', 'Aceite vegetal usado para cocinar', 'Filtrar sólidos y depositar en botella', 'Evita contaminación de agua', 'Aceite de freír, de cocina vegetal', 'Aceite de motor, industrial', false),
('Medicamentos', 8, 'MED01', 'Medicamentos caducados o no usados', 'Mantener en envase original', 'Evita contaminación farmacéutica', 'Pastillas, jarabes, cremas', 'Medicamentos controlados, oncológicos', true),
('Tetrabriks', 8, 'TET01', 'Envases multicapa de cartón', 'Enjuagar y aplastar', 'Recupera cartón, plástico y aluminio', 'Envases de leche, jugos, sopas', 'Tetrabriks muy sucios, deteriorados', false),

-- MADERA
('Palets de madera', 9, 'MAD01', 'Tarimas y palets de madera', 'Verificar ausencia de clavos y tratamientos', 'Reutilización en construcción', 'Palets EUR, americanos, cajas de fruta', 'Madera tratada con químicos', false),
('Muebles de madera', 9, 'MAD02', 'Muebles de madera reparables', 'Evaluar estado estructural', 'Evita tala y fomenta reutilización', 'Mesas, sillas, estanterías', 'Muebles con termitas, muy deteriorados', false),

-- PELIGROSOS
('Pinturas y disolventes', 10, 'PIN01', 'Pinturas, barnices y disolventes', 'Mantener en envase original hermético', 'Evita contaminación química', 'Pinturas al agua, barnices, thinner', 'Envases vacíos, pinturas secas', true),
('Aerosoles', 10, 'AER01', 'Envases de aerosol con contenido', 'Verificar que NO estén vacíos para tratamiento especial', 'Previene emisiones de gases', 'Desodorantes, insecticidas, pinturas en spray', 'Aerosoles completamente vacíos', true),
('Pesticidas', 10, 'PES01', 'Insecticidas y productos de jardín', 'No abrir envases, llevar completos', 'Protege suelo y agua subterránea', 'Insecticidas, herbicidas, fungicidas', 'Envases vacíos, productos vencidos hace años', true);

-- ============================================================================
-- DATOS INICIALES: PUNTOS DE RECICLAJE
-- ============================================================================
INSERT INTO puntos_reciclaje (nombre, descripcion, direccion, ciudad, provincia, latitud, longitud, tipo_instalacion, horario_apertura, horario_cierre, telefono, email, instrucciones_acceso) VALUES
('EcoPunto Centro Histórico', 'Centro de acopio principal en el centro de Quito', 'Av. García Moreno y Sucre', 'Quito', 'Pichincha', -0.2202, -78.5132, 'centro_acopio', '08:00:00', '18:00:00', '+593-2-123-4567', 'centro@ecoandino.com', 'Entrada por la puerta principal, mostrar cédula'),

('Punto Verde La Carolina', 'Estación de reciclaje en el Parque La Carolina', 'Parque La Carolina, junto al vivarium', 'Quito', 'Pichincha', -0.1807, -78.4840, 'punto_limpio', '06:00:00', '20:00:00', '+593-2-234-5678', 'carolina@ecoandino.com', 'Ubicado cerca de la laguna artificial'),

('EcoEstación Norte', 'Punto de reciclaje en el sector norte de Quito', 'Av. Eloy Alfaro y De los Shyris', 'Quito', 'Pichincha', -0.1500, -78.4700, 'estacion_reciclaje', '07:00:00', '19:00:00', '+593-2-345-6789', 'norte@ecoandino.com', 'Acceso vehicular disponible, estacionamiento gratuito'),

('Punto Móvil Sur', 'Unidad móvil que recorre el sur de Quito', 'Variable según cronograma', 'Quito', 'Pichincha', -0.2800, -78.5200, 'punto_movil', '09:00:00', '17:00:00', '+593-99-123-4567', 'movil@ecoandino.com', 'Consultar cronograma de ubicaciones semanales'),

('Contenedores Plaza Foch', 'Contenedores públicos especializados', 'Plaza Foch, La Mariscal', 'Quito', 'Pichincha', -0.2014, -78.4918, 'contenedor_publico', NULL, NULL, NULL, NULL, 'Contenedores disponibles 24/7, solo materiales específicos');

-- ============================================================================
-- RELACIONES: QUÉ MATERIALES ACEPTA CADA PUNTO
-- ============================================================================

-- EcoPunto Centro Histórico - Acepta la mayoría de materiales básicos
INSERT INTO punto_materiales (punto_reciclaje_id, material_id, acepta, observaciones) VALUES
(1, 1, true, 'Máximo 50 botellas por visita'),
(1, 2, true, 'Lavar completamente antes de entregar'),
(1, 3, true, 'Solo bolsas limpias y secas'),
(1, 5, true, 'Separar por colores'),
(1, 6, true, 'Quitar tapas metálicas'),
(1, 7, true, 'Separar por colores'),
(1, 8, true, 'Limpiar completamente'),
(1, 9, true, 'Sin grapas ni clips'),
(1, 10, true, 'Debe estar seco'),
(1, 11, true, 'Sin páginas plastificadas'),
(1, 12, true, 'Aplastar antes de entregar'),
(1, 13, true, 'Quitar etiquetas de papel'),
(1, 18, true, 'Solo ropa en buen estado'),
(1, 23, true, 'Horario especial: 14:00-16:00');

-- Punto Verde La Carolina - Punto completo con materiales especiales
INSERT INTO punto_materiales (punto_reciclaje_id, material_id, acepta, observaciones) VALUES
(2, 1, true, NULL),
(2, 2, true, NULL),
(2, 3, true, NULL),
(2, 4, true, NULL),
(2, 5, true, NULL),
(2, 6, true, NULL),
(2, 7, true, NULL),
(2, 8, true, NULL),
(2, 9, true, NULL),
(2, 10, true, NULL),
(2, 11, true, NULL),
(2, 12, true, NULL),
(2, 13, true, NULL),
(2, 14, true, 'Verificar pureza del cobre'),
(2, 18, true, NULL),
(2, 19, true, NULL),
(2, 20, true, 'Solo para compostaje comunitario'),
(2, 21, true, 'Mezclar con otros orgánicos'),
(2, 22, true, 'Traer en botellas plásticas'),
(2, 23, true, 'Horario especial: 10:00-12:00 y 15:00-17:00'),
(2, 25, true, 'Coordinar entrega previa'),
(2, 26, true, 'Evaluación previa requerida');

-- EcoEstación Norte - Especializado en electrónicos y metales
INSERT INTO punto_materiales (punto_reciclaje_id, material_id, acepta, observaciones) VALUES
(3, 1, true, NULL),
(3, 2, true, NULL),
(3, 12, true, NULL),
(3, 13, true, NULL),
(3, 14, true, NULL),
(3, 15, true, 'Borrar datos personales obligatorio'),
(3, 16, true, 'Formateo incluido en el servicio'),
(3, 17, true, 'Contenedor especial disponible'),
(3, 22, true, 'Punto de recolección certificado'),
(3, 27, true, 'Solo con cita previa'),
(3, 28, true, 'Verificar que no estén vacíos'),
(3, 29, true, 'Manejo especializado, cita obligatoria');

-- Punto Móvil Sur - Básicos y textiles
INSERT INTO punto_materiales (punto_reciclaje_id, material_id, acepta, observaciones) VALUES
(4, 1, true, 'Según capacidad del vehículo'),
(4, 2, true, 'Según capacidad del vehículo'),
(4, 5, true, 'Según capacidad del vehículo'),
(4, 6, true, 'Según capacidad del vehículo'),
(4, 9, true, 'Según capacidad del vehículo'),
(4, 10, true, 'Según capacidad del vehículo'),
(4, 12, true, 'Según capacidad del vehículo'),
(4, 18, true, 'Recolección especial de textiles'),
(4, 19, true, 'Evaluación in situ');

-- Contenedores Plaza Foch - Solo básicos 24/7
INSERT INTO punto_materiales (punto_reciclaje_id, material_id, acepta, observaciones) VALUES
(5, 1, true, 'Contenedor azul'),
(5, 5, true, 'Contenedor azul'),
(5, 6, true, 'Contenedor verde'),
(5, 7, true, 'Contenedor verde'),
(5, 9, true, 'Contenedor azul'),
(5, 12, true, 'Contenedor gris');

-- ============================================================================
-- VISTAS PARA CONSULTAS ÚTILES
-- ============================================================================

-- Vista completa de materiales con su categoría
CREATE VIEW vista_materiales_completa AS
SELECT 
    m.id,
    m.nombre,
    m.codigo,
    c.nombre as categoria,
    c.codigo as codigo_categoria,
    c.color_identificacion,
    c.icono,
    m.descripcion,
    m.preparacion_requerida,
    m.ejemplos,
    m.materiales_no_aceptados,
    m.es_peligroso,
    m.requiere_manejo_especial,
    m.activo
FROM materiales m
JOIN categorias c ON m.categoria_id = c.id
WHERE m.activo = true
ORDER BY c.orden_display, m.nombre;

-- Vista de puntos con conteo de materiales que aceptan
CREATE VIEW vista_puntos_resumen AS
SELECT 
    p.id,
    p.nombre,
    p.tipo_instalacion,
    p.direccion,
    p.ciudad,
    p.latitud,
    p.longitud,
    p.telefono,
    p.horario_apertura,
    p.horario_cierre,
    p.estado,
    COUNT(pm.material_id) as total_materiales_aceptados
FROM puntos_reciclaje p
LEFT JOIN punto_materiales pm ON p.id = pm.punto_reciclaje_id AND pm.acepta = true
WHERE p.estado = 'activo'
GROUP BY p.id, p.nombre, p.tipo_instalacion, p.direccion, p.ciudad, p.latitud, p.longitud, p.telefono, p.horario_apertura, p.horario_cierre, p.estado
ORDER BY total_materiales_aceptados DESC;

-- Vista para buscar puntos por material específico
CREATE VIEW vista_puntos_por_material AS
SELECT 
    p.id as punto_id,
    p.nombre as punto_nombre,
    p.direccion,
    p.ciudad,
    p.latitud,
    p.longitud,
    p.telefono,
    p.tipo_instalacion,
    p.horario_apertura,
    p.horario_cierre,
    m.id as material_id,
    m.nombre as material_nombre,
    m.codigo as material_codigo,
    c.nombre as categoria_nombre,
    pm.observaciones,
    pm.cantidad_maxima,
    pm.horario_especial
FROM puntos_reciclaje p
JOIN punto_materiales pm ON p.id = pm.punto_reciclaje_id
JOIN materiales m ON pm.material_id = m.id
JOIN categorias c ON m.categoria_id = c.id
WHERE p.estado = 'activo' AND pm.acepta = true AND m.activo = true
ORDER BY p.ciudad, p.nombre, c.orden_display, m.nombre;

-- ============================================================================
-- FUNCIÓN PARA BUSCAR PUNTOS CERCANOS
-- ============================================================================
CREATE OR REPLACE FUNCTION buscar_puntos_cercanos(
    lat_usuario DECIMAL(10,8), 
    lng_usuario DECIMAL(11,8), 
    radio_km DECIMAL DEFAULT 10
)
RETURNS TABLE (
    punto_id INTEGER,
    nombre VARCHAR(100),
    direccion VARCHAR(200),
    distancia_km DECIMAL,
    latitud DECIMAL(10,8),
    longitud DECIMAL(11,8),
    tipo_instalacion VARCHAR(50),
    total_materiales BIGINT
) AS $$
BEGIN
    RETURN QUERY
    SELECT 
        p.id,
        p.nombre,
        p.direccion,
        ROUND(
            CAST(
                6371 * acos(
                    cos(radians(lat_usuario)) * 
                    cos(radians(p.latitud)) * 
                    cos(radians(p.longitud) - radians(lng_usuario)) + 
                    sin(radians(lat_usuario)) * 
                    sin(radians(p.latitud))
                ) AS DECIMAL
            ), 2
        ) as distancia_km,
        p.latitud,
        p.longitud,
        CAST(p.tipo_instalacion AS VARCHAR(50)),
        COUNT(pm.material_id)
    FROM puntos_reciclaje p
    LEFT JOIN punto_materiales pm ON p.id = pm.punto_reciclaje_id AND pm.acepta = true
    WHERE p.estado = 'activo'
    AND (
        6371 * acos(
            cos(radians(lat_usuario)) * 
            cos(radians(p.latitud)) * 
            cos(radians(p.longitud) - radians(lng_usuario)) + 
            sin(radians(lat_usuario)) * 
            sin(radians(p.latitud))
        )
    ) <= radio_km
    GROUP BY p.id, p.nombre, p.direccion, p.latitud, p.longitud, p.tipo_instalacion
    ORDER BY distancia_km;
END;
$$ LANGUAGE plpgsql;

-- ============================================================================
-- COMENTARIOS FINALES
-- ============================================================================
COMMENT ON TABLE categorias IS 'Categorías principales de materiales reciclables con información visual';
COMMENT ON TABLE materiales IS 'Materiales específicos con instrucciones detalladas de preparación';
COMMENT ON TABLE puntos_reciclaje IS 'Ubicaciones físicas donde se pueden llevar materiales reciclables';
COMMENT ON TABLE punto_materiales IS 'Relación que define qué materiales acepta cada punto de reciclaje';

-- ============================================================================
-- FINALIZACIÓN
-- ============================================================================
SELECT 'Base de datos EcoAndino (versión simplificada) creada exitosamente' as mensaje,
       (SELECT COUNT(*) FROM categorias) as total_categorias,
       (SELECT COUNT(*) FROM materiales) as total_materiales,
       (SELECT COUNT(*) FROM puntos_reciclaje) as total_puntos,
       (SELECT COUNT(*) FROM punto_materiales) as total_relaciones;