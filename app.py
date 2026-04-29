import streamlit as st
import google.generativeai as genai
from PIL import Image
from datetime import datetime

# 1. IDENTIDAD ZODION
st.set_page_config(page_title="Zodion IA - Auditoría", layout="wide")

# 2. CONEXIÓN DINÁMICA (EVITA EL ERROR 404)
model = None
if "GOOGLE_API_KEY" in st.secrets:
    try:
        api_key = st.secrets["GOOGLE_API_KEY"].strip().replace('"', '')
        genai.configure(api_key=api_key)
        
        # Buscamos qué modelos tienes activos realmente
        modelos_disponibles = [m.name for m in genai.list_models() if 'generateContent' in m.supported_generation_methods]
        
        # Seleccionamos el mejor disponible (Flash es la prioridad)
        if 'models/gemini-1.5-flash' in modelos_disponibles:
            nombre_modelo = 'models/gemini-1.5-flash'
        elif 'models/gemini-pro-vision' in modelos_disponibles:
            nombre_modelo = 'models/gemini-pro-vision'
        else:
            # Si no encuentra los anteriores, toma el primero que permita visión
            nombre_modelo = modelos_disponibles[0] if modelos_disponibles else None

        if nombre_modelo:
            model = genai.GenerativeModel(nombre_modelo)
            st.sidebar.success(f"🟢 ZODION ACTIVO: {nombre_modelo.split('/')[-1]}")
        else:
            st.sidebar.error("🔴 No hay modelos de visión activos en esta llave.")
            
    except Exception as e:
        st.sidebar.error(f"🔴 Error de Configuración: {e}")
else:
    st.sidebar.warning("⚠️ Configura la API Key en Secrets")

# 3. INTERFAZ TÉCNICA
st.title("🛡️ Sistema de Diagnóstico Técnico ZODION")
st.caption("CEO de Zodion - Saneamiento Ecológico Profesional")

fotos = st.file_uploader("Subir evidencias", type=["jpg", "png", "jpeg"], accept_multiple_files=True)

if fotos:
    for i, foto in enumerate(fotos):
        col1, col2 = st.columns([1, 2])
        with col1:
            st.image(foto, use_container_width=True)
            if st.button(f"🪄 Analizar Evidencia {i+1}", key=f"btn_{i}"):
                if model:
                    with st.spinner("Analizando..."):
                        try:
                            img = Image.open(foto).convert('RGB')
                            # Usamos un llamado simplificado para máxima compatibilidad
                            response = model.generate_content(["Describe hallazgos sanitarios y riesgos de plagas.", img])
                            st.session_state[f"analisis_{i}"] = response.text
                        except Exception as e:
                            st.error(f"Fallo en análisis: {e}")
                else:
                    st.error("El modelo no se pudo inicializar.")

        with col2:
            st.text_area("Diagnóstico Técnico:", value=st.session_state.get(f"analisis_{i}", ""), key=f"txt_{i}", height=150)




