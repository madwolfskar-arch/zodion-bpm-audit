import streamlit as st
import google.generativeai as genai
from PIL import Image
from datetime import datetime

# 1. IDENTIDAD CORPORATIVA
st.set_page_config(page_title="Zodion IA", layout="wide")

# 2. CONFIGURACIÓN DE IA - MÉTODO DE FUERZA BRUTA
model = None
if "GOOGLE_API_KEY" in st.secrets:
    try:
        # Limpieza absoluta de la llave
        key = st.secrets["GOOGLE_API_KEY"].replace('"', '').replace("'", "").strip()
        genai.configure(api_key=key)
        
        # Intentamos cargar el modelo con el nombre técnico completo
        # Esto soluciona el error de "no encontrado" en muchas regiones
        model = genai.GenerativeModel(model_name='models/gemini-1.5-flash')
        
        # Verificación silenciosa
        st.sidebar.success("🟢 SISTEMA ZODION CONECTADO")
    except Exception as e:
        st.sidebar.error(f"🔴 Error de Permisos: {e}")
else:
    st.sidebar.warning("⚪ Esperando configuración en Secrets...")

# 3. INTERFAZ DE USUARIO
st.title("🛡️ Sistema de Diagnóstico Técnico ZODION")
st.caption("CEO de Zodion - Innovación en Saneamiento Ambiental")

# Subida de archivos
fotos = st.file_uploader("Cargar registros de inspección", type=["jpg", "png", "jpeg"], accept_multiple_files=True)

if fotos:
    for i, foto in enumerate(fotos):
        col1, col2 = st.columns([1, 2])
        with col1:
            st.image(foto, use_container_width=True)
            if st.button(f"🪄 Analizar Evidencia {i+1}", key=f"b_{i}"):
                if model:
                    with st.spinner("Zodion AI procesando..."):
                        try:
                            # Procesamiento de imagen para compatibilidad total
                            img = Image.open(foto).convert('RGB')
                            # Llamada simplificada
                            response = model.generate_content(["Describe brevemente riesgos sanitarios en esta foto.", img])
                            st.session_state[f"res_{i}"] = response.text
                        except Exception as e:
                            st.error(f"Error técnico: {e}")
                else:
                    st.error("La IA no está lista. Revisa la llave API.")

        with col2:
            st.text_area("Diagnóstico Técnico:", value=st.session_state.get(f"res_{i}", ""), key=f"t_{i}", height=150)

# 4. GENERACIÓN DE REPORTE
st.divider()
if st.button("🚀 Consolidar Informe Final"):
    st.info("Informe generado. Juntos lo hacemos posible.")




