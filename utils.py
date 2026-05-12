"""
Utilidades para procesamiento de PDFs y conexión a MongoDB
"""
import os
import fitz  # PyMuPDF
import pytesseract
from PIL import Image
import io
from typing import List, Dict, Tuple
from datetime import datetime
from pymongo import MongoClient
from openai import OpenAI


def get_mongo_client():
    """Conectar a MongoDB Atlas"""
    from dotenv import load_dotenv
    load_dotenv()
    
    uri = os.getenv("MONGODB_URI")
    client = MongoClient(uri)
    
    # Verificar conexión
    try:
        client.admin.command('ping')
        print("✓ Conexión exitosa a MongoDB Atlas")
    except Exception as e:
        print(f"✗ Error conectando a MongoDB: {e}")
        raise
    
    return client


def get_database():
    """Obtener la base de datos configurada"""
    from dotenv import load_dotenv
    load_dotenv()
    
    client = get_mongo_client()
    db_name = os.getenv("MONGODB_DATABASE", "lopsrm_rag")
    return client[db_name]


def detectar_pdf_escaneado(pdf_path: str) -> bool:
    """
    Detecta si un PDF está escaneado (imagen) o tiene texto extraíble
    """
    doc = fitz.open(pdf_path)
    
    # Revisar primeras 3 páginas
    num_paginas_check = min(3, len(doc))
    
    for page_num in range(num_paginas_check):
        page = doc[page_num]
        text = page.get_text()
        
        # Si tiene más de 50 caracteres, asumimos que tiene texto
        if len(text.strip()) > 50:
            doc.close()
            return False
    
    doc.close()
    return True


def extraer_texto_con_ocr(pdf_path: str) -> str:
    """
    Extrae texto de PDF escaneado usando OCR
    """
    doc = fitz.open(pdf_path)
    texto_completo = []
    
    for page_num in range(len(doc)):
        page = doc[page_num]
        
        # Convertir página a imagen
        pix = page.get_pixmap(dpi=300)
        img_data = pix.tobytes("png")
        img = Image.open(io.BytesIO(img_data))
        
        # Aplicar OCR
        texto = pytesseract.image_to_string(img, lang='spa')
        texto_completo.append(texto)
    
    doc.close()
    return "\n\n".join(texto_completo)


def extraer_texto_nativo(pdf_path: str) -> str:
    """
    Extrae texto de PDF nativo (no escaneado)
    """
    doc = fitz.open(pdf_path)
    texto_completo = []
    
    for page in doc:
        texto_completo.append(page.get_text())
    
    doc.close()
    return "\n\n".join(texto_completo)


def procesar_pdf(pdf_path: str) -> Tuple[str, bool]:
    """
    Procesa un PDF y devuelve el texto extraído
    Returns: (texto, fue_ocr)
    """
    es_escaneado = detectar_pdf_escaneado(pdf_path)
    
    if es_escaneado:
        print(f"📄 PDF escaneado detectado. Aplicando OCR...")
        texto = extraer_texto_con_ocr(pdf_path)
        return texto, True
    else:
        print(f"📄 PDF con texto nativo. Extrayendo...")
        texto = extraer_texto_nativo(pdf_path)
        return texto, False


def crear_chunks(texto: str, chunk_size: int = 1000, chunk_overlap: int = 200) -> List[str]:
    """
    Divide el texto en chunks con overlap
    Para documentos legales, idealmente deberías dividir por artículos/cláusulas
    Esta es una versión simple basada en caracteres
    """
    chunks = []
    inicio = 0
    
    while inicio < len(texto):
        fin = inicio + chunk_size
        chunk = texto[inicio:fin]
        
        # Intentar cortar en punto final si es posible
        if fin < len(texto):
            ultimo_punto = chunk.rfind('.')
            if ultimo_punto > chunk_size * 0.7:  # Si está en los últimos 30%
                fin = inicio + ultimo_punto + 1
                chunk = texto[inicio:fin]
        
        chunks.append(chunk.strip())
        inicio = fin - chunk_overlap
    
    return chunks


def generar_embedding(texto: str, modelo: str = "text-embedding-3-small") -> List[float]:
    """
    Genera embedding usando OpenAI
    """
    from dotenv import load_dotenv
    load_dotenv()
    
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    
    response = client.embeddings.create(
        input=texto,
        model=modelo
    )
    
    return response.data[0].embedding


def guardar_en_mongodb(chunks: List[str], metadata: Dict, db) -> int:
    """
    Guarda chunks con embeddings en MongoDB
    """
    from dotenv import load_dotenv
    load_dotenv()
    
    collection_name = os.getenv("MONGODB_COLLECTION", "documentos_legales")
    collection = db[collection_name]
    
    documentos = []
    
    for idx, chunk in enumerate(chunks):
        # Generar embedding
        embedding = generar_embedding(chunk)
        
        # Crear documento
        doc = {
            "texto": chunk,
            "embedding": embedding,
            "metadata": {
                **metadata,
                "chunk_index": idx,
                "fecha_ingestion": datetime.utcnow().isoformat()
            }
        }
        
        documentos.append(doc)
    
    # Insertar en batch
    result = collection.insert_many(documentos)
    return len(result.inserted_ids)
