import streamlit as st
import google.generativeai as genai
from PIL import Image
from datetime import datetime

# CONFIGURACIÓN DE IDENTIDAD
st.set_page_config(page_title="Zodion IA - Auditoría", page_icon="🛡️", layout="wide")

# CONEXIÓN BLINDADA CON LA IA
model = None
if "GOOGLE_API_KEY" in st.secrets:
    try:
        # Extraemos y limpiamos la llave de cualquier espacio o comilla accidental
        api_key = st.secrets["GOOGLE_API_KEY"].strip().replace('"', '')
        genai.configure(api_key=api_key)
        
        # Inicializamos el modelo probado en AI Studio
        model = genai.GenerativeModel('gemini-1.5-flash')
        st.sidebar.success("🟢 SISTEMA ZODION: CONECTADO")
    except Exception as e:
        st.sidebar.error(f"🔴 Error de Conexión: {e}")
else:
    st.sidebar.warning("⚠️ Configura la API Key en Secrets")

# INTERFAZ CORPORATIVA
st.title("🛡️ Sistema de Diagnóstico Técnico ZODION")
st.caption("Control de Inocuidad y Saneamiento Ambiental - Juntos lo hacemos posible")

# BARRA LATERAL - DATOS DE CAMPO
with st.sidebar:
    st.header("📋 Datos de Inspección")
    cliente = st.text_input("Cliente:", value="JAVERIANO")
    auditor = st.text_input("Auditor:", value="CEO de Zodion")
    if st.button("🔄 Reiniciar Sesión"):
        st.cache_data.clear()
        st.rerun()

# CARGA DE EVIDENCIAS
fotos = st.file_uploader("Subir fotos de auditoría (Pan, Carnes, Equipos, etc.)", 
                         type=["jpg", "png", "jpeg"], accept_multiple_files=True)

if fotos:
    for i, foto in enumerate(fotos):
        col1, col2 = st.columns([1, 2])
        
        with col1:
            st.image(foto, use_container_width=True)
            if st.button(f"🪄 Analizar Hallazgo {i+1}", key=f"btn_{i}"):
                if model:
                    with st.spinner("Zodion AI evaluando evidencia..."):
                        try:
                            img = Image.open(foto).convert('RGB')
                            # Prompt basado en la Resolución 2674 de Colombia
                            prompt = (
                                "Como experto en inocuidad alimentaria (Res. 2674), describe en 3 puntos: "
                                "1. Identificación del objeto/producto. 2. Estado sanitario observado. "
                                "3. Riesgos de plagas o contaminación cruzada. Sé técnico y directo."
                            )
                            response = model.generate_content([prompt, img])
                            st.session_state[f"analisis_{i}"] = response.text
                        except Exception as e:
                            st.error(f"Fallo en análisis: {e}")
                else:
                    st.error("IA no disponible.")

        with col2:
            st.text_area("Diagnóstico Técnico Profesional:", 
                         value=st.session_state.get(f"analisis_{i}", ""), 
                         key=f"txt_{i}", height=180)

# CIERRE Y REPORTE
st.divider()
if st.button("🚀 Consolidar Informe Final"):
    st.success(f"Informe de auditoría para {cliente} listo para previsualización.")



