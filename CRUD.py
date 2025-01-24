# CRUD con Embeddings
# Instalar dependencias ejecutando el archivo requirements.txt


# Importar librerías necesarias

import random
from sentence_transformers import SentenceTransformer
from qdrant_client import QdrantClient
from qdrant_client.models import VectorParams, Distance


# Crear el modelo de embeddings

modelo = SentenceTransformer('all-MiniLM-L6-v2')

# Inicializamos el cliente de Qdrant

client = QdrantClient(
    url="https://c0ecc735-4daa-4faf-8e47-87ec35ba28bc.europe-west3-0.gcp.cloud.qdrant.io:6333", 
    https=True,
    api_key="zXQmNpc6rGfyeSiibzntmDDph_xegr3cI1DoiK5hvK6Uj2WYGKcTdA",
)
index_name = "embeddings_index"


# Crear un embedding y agregarlo a Qdrant

def generar_id_numerico():
    return random.randint(1000, 9999)


def agregar_embedding(texto):
    embedding = modelo.encode([texto])[0]
    
    # Generar un ID aleatorio
    nuevo_id = generar_id_numerico()

    client.upsert(
        collection_name=index_name,
        points=[{
            'id': nuevo_id,
            'vector': embedding.tolist(),
            'payload': {'texto': texto}
        }]
    )
    return nuevo_id, embedding


# Leer un embedding (consultar todos los embeddings)

def obtener_embeddings():
    embeddings = []
    scroll_response = client.scroll(collection_name=index_name, limit=1000)

    while scroll_response and scroll_response[0]:
        for point in scroll_response[0]:
            embeddings.append({
                "id": point.id, 
                "texto": point.payload["texto"]
            })

        # Continuamos con la siguiente página utilizando el scroll_token
        scroll_token = scroll_response[1]
        if not scroll_token:
            break

        # Continuamos el scroll utilizando el token de paginación
        scroll_response = client.scroll(collection_name=index_name, scroll_token=scroll_token)

    return embeddings


# Consultar los embeddings más similares a una consulta

def consultar_similares(texto_consulta, top_k=5):
    embedding_consulta = modelo.encode([texto_consulta])[0]
    resultados = client.search(
        collection_name=index_name,
        query_vector=embedding_consulta.tolist(),
        limit=top_k
    )
    
    # Extraer los resultados y formatearlos
    return [{
        "id": res.id,
        "texto": res.payload["texto"],
        "score": res.score
    } for res in resultados]
    
    
# Actualizar un embedding por ID

def actualizar_embedding(id, nuevo_texto):
    embedding_nuevo = modelo.encode([nuevo_texto])[0]
    
    client.upsert(
        collection_name=index_name,
        points=[{
            'id': id,
            'vector': embedding_nuevo.tolist(),
            'payload': {'texto': nuevo_texto}
        }]
    )
    return id, nuevo_texto


# Eliminar un embedding por ID

def eliminar_embedding(id):
    client.delete(
        collection_name=index_name,
        points_selector=[id]
    )
    return id