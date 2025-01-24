import streamlit as st
from CRUD import agregar_embedding, obtener_embeddings, consultar_similares, actualizar_embedding, eliminar_embedding

# Configuración de la página
st.set_page_config(page_title="Embeddings CRUD con Qdrant", layout="wide")


st.title("Embeddings CRUD con Qdrant")


menu = ["Crear", "Consultar", "Consultar similares", "Actualizar", "Eliminar"]
opcion = st.sidebar.selectbox("Selecciona una operación", menu)

if opcion == "Crear":
    st.header("Crear un nuevo embedding")
    texto_nuevo = st.text_area("Escribe el texto para el nuevo embedding:")
    
    if st.button("Crear Embedding"):
        if texto_nuevo:
            id_nuevo, embedding = agregar_embedding(texto_nuevo)
            st.success(f"Embedding creado con ID: {id_nuevo}")
        else:
            st.error("Por favor ingresa un texto.")
            
elif opcion == "Consultar":
    st.header("Obtener todos los embeddings")
    embeddings = obtener_embeddings()
    
    if embeddings:
        st.write("Embeddings en la base de datos:")
        for emb in embeddings:
            st.write(f"ID: {emb['id']} - Texto: {emb['texto']}")
            
elif opcion == "Consultar similares":
    st.header("Consultar similares")
    texto_consulta = st.text_area("Escribe el texto de consulta:")
    
    if st.button("Consultar similares"):
        if texto_consulta:
            resultados = consultar_similares(texto_consulta, top_k=5)
            if resultados:
                st.write("Embeddings más similares encontrados:")
                for res in resultados:
                    st.write(f"ID: {res['id']} - Texto: {res['texto']} - Score: {res['score']}")
            else:
                st.write("No se encontraron resultados similares.")
        else:
            st.error("Por favor ingresa un texto para consultar.")

elif opcion == "Actualizar":
    st.header("Actualizar un embedding existente")
    id_actualizar = st.number_input("ID del embedding a actualizar:", min_value=1)
    nuevo_texto = st.text_area("Escribe el nuevo texto:")
    
    if st.button("Actualizar Embedding"):
        if id_actualizar and nuevo_texto:
            id_actualizado, texto_actualizado = actualizar_embedding(id_actualizar, nuevo_texto)
            st.success(f"Embedding actualizado. ID: {id_actualizado}, Nuevo texto: {texto_actualizado}")
        else:
            st.error("Por favor ingresa el ID y el nuevo texto.")

elif opcion == "Eliminar":
    st.header("Eliminar un embedding")
    id_eliminar = st.number_input("ID del embedding a eliminar:", min_value=1)
    
    if st.button("Eliminar Embedding"):
        if id_eliminar:
            id_eliminado = eliminar_embedding(id_eliminar)
            st.success(f"Embedding eliminado. ID: {id_eliminado}")
        else:
            st.error("Por favor ingresa el ID del embedding a eliminar.")
