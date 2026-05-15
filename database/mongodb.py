import os

from dotenv import load_dotenv
from pymongo import MongoClient
from datetime import datetime

from rag.embeddings import generar_embedding

# =====================================================
# LOAD ENV
# =====================================================

load_dotenv()

# =====================================================
# SINGLETON MONGODB
# =====================================================

class MongoManager:

    _client = None
    _db = None

    @classmethod
    def get_client(cls):

        if cls._client is None:

            cls._client = MongoClient(
                os.getenv("MONGODB_URI"),
                serverSelectionTimeoutMS=5000
            )

            try:

                cls._client.admin.command("ping")

                print("✅ Conexión exitosa a MongoDB")

            except Exception as e:

                print(f"❌ Error MongoDB: {e}")

                raise

        return cls._client

    @classmethod
    def get_database(cls):

        if cls._db is None:

            client = cls.get_client()

            database_name = os.getenv(
                "MONGODB_DATABASE",
                "rag_ai"
            )

            cls._db = client[database_name]

            print(f"✅ Base de datos: {database_name}")

        return cls._db


# =====================================================
# GET DATABASE
# =====================================================

def get_database():

    return MongoManager.get_database()


# =====================================================
# GUARDAR CHUNKS
# =====================================================

def guardar_chunks(
    chunks,
    metadata
):

    db = get_database()

    collection = db["documentos"]

    documentos = []

    for i, chunk in enumerate(chunks):

        try:

            embedding = generar_embedding(chunk)

            documento = {

                "texto": chunk,

                "embedding": embedding,

                "chunk_index": i,

                "longitud_chunk": len(chunk),

                "created_at": datetime.utcnow(),

                "metadata": metadata
            }

            documentos.append(documento)

        except Exception as e:

            print(f"❌ Error generando embedding: {e}")

    if documentos:

        collection.insert_many(documentos)

    return len(documentos)


# =====================================================
# GUARDAR DOCUMENTO VECTORIAL
# =====================================================

def guardar_documento_vectorial(documento):

    db = get_database()

    collection = db["documentos"]

    result = collection.insert_one(documento)

    return result.inserted_id


# =====================================================
# OBTENER DOCUMENTOS
# =====================================================

def obtener_documentos():

    db = get_database()

    collection = db["documentos"]

    documentos = collection.find(
        {},
        {
            "metadata.nombre_archivo": 1,
            "metadata.tipo_documento": 1,
            "metadata.fecha_documento": 1,
            "chunk_index": 1
        }
    ).limit(100)

    return list(documentos)


# =====================================================
# ELIMINAR DOCUMENTO
# =====================================================

def eliminar_documento(nombre_archivo):

    db = get_database()

    collection = db["documentos"]

    result = collection.delete_many({
        "metadata.nombre_archivo": nombre_archivo
    })

    return result.deleted_count


# =====================================================
# CONTAR DOCUMENTOS
# =====================================================

def contar_documentos():

    db = get_database()

    collection = db["documentos"]

    return collection.count_documents({})


# =====================================================
# BUSCAR DOCUMENTOS
# =====================================================

def buscar_documentos_por_tipo(tipo_documento):

    db = get_database()

    collection = db["documentos"]

    documentos = collection.find({

        "metadata.tipo_documento": tipo_documento

    })

    return list(documentos)


# =====================================================
# OBTENER DOCUMENTOS ÚNICOS
# =====================================================

def obtener_nombres_documentos():

    db = get_database()

    collection = db["documentos"]

    nombres = collection.distinct(
        "metadata.nombre_archivo"
    )

    return nombres