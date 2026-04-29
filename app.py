import streamlit as st
import google.generativeai as genai
from PIL import Image
from datetime import datetime

# CONFIGURACIÓN BÁSICA
st.set_page_config(page_title="Zodion Auditoría IA", layout="wide")

# CONEXIÓN DIRECTA Y ESTABLE
# Eliminamos las menciones a v1beta y forzamos la versión estable
if "GOOGLE_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
    # Intentamos con el nombre de modelo más universal
    model = genai.GenerativeModel('gemini-1.5-flash-latest') 
else:
    st.error("Falta la API Key en los Secrets de Streamlit.")
    st.stop()

st.title("🛡️ Sistema de Diagnóstico Técnico ZODION")

# Lógica simplificada de análisis
fotos = st.file_uploader("Subir evidencias", type=["jpg", "png", "jpeg"], accept_multiple_files=True)

if fotos:
    for i, foto in enumerate(fotos):
        col1, col2 = st.columns([1, 2])
        with col1:
            st.image(foto)
            if st.button(f"Analizar Foto {i+1}", key=f"b_{i}"):
                try:
                    img = Image.open(foto).convert('RGB')
                    # Prompt ultra-directo
                    response = model.generate_content(["Describe hallazgos sanitarios en esta imagen de alimentos.", img])
                    st.session_state[f"res_{i}"] = response.text
                except Exception as e:
                    st.error(f"Error: {e}")
        
        with col2:
            analisis = st.text_area("Resultado del análisis:", value=st.session_state.get(f"res_{i}", ""), key=f"t_{i}", height=150)

# Botón de informe
if st.button("🚀 Generar Informe"):
    st.success("Informe listo para descarga (Simulación)")





