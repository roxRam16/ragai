# Sistema RAG para detección de incumplimientos de contratos

Sistema de gestión de documentos legales con base de datos vectorial para detectar incumplimientos en contratos de obra pública.

## 📋 Fase 1: Ingestión de PDFs a MongoDB Atlas

Esta primera fase permite:
- Subir documentos PDF (normales o escaneados con OCR)
- Procesarlos automáticamente en chunks
- Generar embeddings vectoriales
- Almacenarlos en MongoDB Atlas

---

## 🚀 Instalación

### 1. Clonar o crear el proyecto

```bash
mkdir rag-lopsrm
cd rag-lopsrm
```

### 2. Instalar dependencias

```bash
pip install -r requirements.txt
```

### 3. Instalar Tesseract OCR (para PDFs escaneados)

**En Ubuntu/Debian:**
```bash
sudo apt-get install tesseract-ocr tesseract-ocr-spa
```

**En macOS:**
```bash
brew install tesseract tesseract-lang
```

**En Windows:**
Descarga el instalador desde: https://github.com/UB-Mannheim/tesseract/wiki

### 4. Configurar variables de entorno

Copia el archivo `.env.example` a `.env`:

```bash
cp .env.example .env
```

Edita `.env` con tus credenciales:

```env
# MongoDB Atlas
MONGODB_URI=XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
MONGODB_DATABASE=XXX
MONGODB_COLLECTION=XXXXXXXXXXXXXXXXXXXXXXXXXX

# OpenAI (para embeddings)
OPENAI_API_KEY=sk-tu-api-key-aqui

# Credenciales de login
ADMIN_USERNAME=admin
ADMIN_PASSWORD=lopsrm2024

# Modelo de embeddings
EMBEDDING_MODEL=text-embedding-3-small
EMBEDDING_DIMENSION=1536
```

---

## 🎯 Configuración de MongoDB Atlas

### Paso 1: Crear cluster (YA LO TIENES)
✅ Ya creaste tu cluster y base de datos

### Paso 2: Obtener URI de conexión

1. Ve a tu cluster en MongoDB Atlas
2. Click en "Connect" → "Connect your application"
3. Copia la URI (formato: `mongodb+srv://...`)
4. Reemplaza `<password>` con tu contraseña
5. Pégala en el archivo `.env`

### Paso 3: Subir documentos (usando la app)

**¡NO NECESITAS crear el índice vectorial todavía!**

Primero sube documentos, luego crearás el índice.

### Paso 4: Crear Vector Search Index (DESPUÉS de subir docs)

Una vez que hayas subido al menos un documento:

1. Ve a tu cluster en MongoDB Atlas
2. Click en la pestaña **"Search"**
3. Click en **"Create Search Index"**
4. Selecciona **"JSON Editor"**
5. Pega esta configuración:

```json
{
  "fields": [
    {
      "type": "vector",
      "path": "embedding",
      "numDimensions": 1536,
      "similarity": "cosine"
    },
    {
      "type": "filter",
      "path": "metadata.tipo_documento"
    },
    {
      "type": "filter",
      "path": "metadata.tags"
    }
  ]
}
```

6. **Nombra el índice como:** `vector_index`
7. Selecciona tu base de datos: `lopsrm_rag`
8. Selecciona tu colección: `documentos_legales`
9. Click en "Create Search Index"

⏱️ El índice tardará unos minutos en crearse.

---

## ▶️ Ejecutar la aplicación

```bash
streamlit run app.py
```

La aplicación se abrirá en: http://localhost:8501

### Credenciales de login (por defecto):
- **Usuario:** admin
- **Contraseña:** lopsrm2024

---

## 📖 Uso de la aplicación

### 1. Cargar documentos

1. Inicia sesión
2. Ve a la pestaña **"Cargar documentos"**
3. Selecciona un PDF
4. Elige el tipo de documento (Contrato, LOPSRM, etc.)
5. (Opcional) Añade metadatos adicionales
6. Ajusta el tamaño de chunks si lo deseas
7. Click en **"Procesar y subir a MongoDB"**

El sistema:
- ✅ Detecta automáticamente si es PDF escaneado
- ✅ Aplica OCR si es necesario
- ✅ Divide en chunks inteligentes
- ✅ Genera embeddings vectoriales
- ✅ Guarda en MongoDB Atlas

### 2. Ver estadísticas

En el sidebar verás:
- Total de chunks almacenados
- Distribución por tipo de documento

### 3. Configuración

En la pestaña "Configuración" puedes:
- Verificar que todas las variables estén configuradas
- Ver instrucciones para crear el índice vectorial

---

## 📁 Estructura de documentos en MongoDB

Cada chunk se guarda con esta estructura:

```json
{
  "_id": ObjectId("..."),
  "texto": "Contenido del fragmento del documento...",
  "embedding": [0.123, -0.456, ...],  // Vector de 1536 dimensiones
  "metadata": {
    "tipo_documento": "Contrato",
    "nombre_archivo": "contrato_001.pdf",
    "dependencia": "SEDENA",
    "numero_contrato": "ABC-123-2024",
    "fecha_documento": "2024-01-15",
    "tags": ["obra pública", "construcción"],
    "fue_ocr": false,
    "chunk_index": 0,
    "chunk_size": 1000,
    "chunk_overlap": 200,
    "fecha_ingestion": "2024-05-12T10:30:00"
  }
}
```

---

## 🔍 Siguientes pasos (Fase 2)

Una vez que tengas documentos en MongoDB:

1. ✅ Crear el Vector Search Index
2. 🚧 Implementar búsqueda semántica
3. 🚧 Motor de detección de incumplimientos
4. 🚧 Sistema de alertas

---

## ⚠️ Troubleshooting

### Error: "No module named 'pytesseract'"
```bash
pip install pytesseract
```

### Error: "TesseractNotFoundError"
Necesitas instalar Tesseract OCR en tu sistema (ver sección de instalación)

### Error de conexión a MongoDB
- Verifica que tu IP esté en la whitelist de MongoDB Atlas
- Ve a "Network Access" en Atlas y añade tu IP o permite acceso desde cualquier IP (0.0.0.0/0)

### Error de OpenAI API
- Verifica que tu API key sea válida
- Revisa que tengas saldo en tu cuenta de OpenAI

---

## 💰 Costos estimados

### OpenAI Embeddings (text-embedding-3-small)
- **Precio:** $0.020 / 1M tokens
- **Estimado:** ~1000 páginas = ~$0.50

### MongoDB Atlas
- **Tier gratuito:** M0 (512 MB) - GRATIS
- **Recomendado:** M10 ($0.08/hora = ~$57/mes) si subes muchos documentos

---

## 📞 Soporte

Para dudas o problemas, verifica:
1. Los logs en la terminal donde corre Streamlit
2. La consola de MongoDB Atlas (ver logs de conexiones)
3. El archivo `.env` tiene todas las variables correctas

---

## 🔐 Seguridad

**IMPORTANTE:**
- Cambia las credenciales por defecto en `.env`
- NO subas el archivo `.env` a GitHub
- Usa variables de entorno o secrets en producción
