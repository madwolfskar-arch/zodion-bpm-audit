import streamlit as st
import pandas as pd
from datetime import datetime
import google.generativeai as genai
from PIL import Image
import io

# 1. CONFIGURACIÓN DE IDENTIDAD ZODION
st.set_page_config(page_title="Zodion - Auditoría Técnica IA", page_icon="🛡️", layout="wide")

# Inicialización con Autodetección de Modelos
model = None
status_ia = "🔴 No configurada"

if "GOOGLE_API_KEY" in st.secrets:
    try:
        genai.configure(api_key=st.secrets["GOOGLE_API_KEY"].strip())
        
        # BUSCADOR DE MODELOS DISPONIBLES (Evita el error 404)
        available_models = [m.name for m in genai.list_models() if 'generateContent' in m.supported_generation_methods]
        
        # Prioridad de selección
        target_model = None
        for name in ["models/gemini-1.5-flash", "models/gemini-1.5-pro", "models/gemini-pro-vision"]:
            if name in available_models:
                target_model = name
                break
        
        if target_model:
            model = genai.GenerativeModel(target_model)
            status_ia = f"🟢 Conectado a {target_model.split('/')[-1]}"
        else:
            status_ia = "⚠️ No se hallaron modelos compatibles."
            
    except Exception as e:
        status_ia = f"❌ Error de Conexión: {str(e)}"
else:
    status_ia = "⚠️ Falta GOOGLE_API_KEY en Secrets"

# Estética Corporativa
st.markdown("""
    <style>
    .main { background-color: #f8f9fa; }
    .stDownloadButton button {
        background-color: #003366 !important;
        color: white !important;
        width: 100% !important;
        font-weight: bold !important;
        border-radius: 8px !important;
    }
    .report-preview {
        background-color: #ffffff;
        padding: 30px;
        border: 2px solid #003366;
        border-radius: 10px;
        font-family: 'Courier New', Courier, monospace;
        color: #000;
        white-space: pre-wrap;
    }
    </style>
    """, unsafe_allow_html=True)

st.title("🛡️ Sistema de Diagnóstico Técnico ZODION")
st.caption("Innovación en Saneamiento Ecológico Profesional - Pasto, Nariño")

if 'analisis_cache' not in st.session_state:
    st.session_state.analisis_cache = {}

# 2. BARRA LATERAL
with st.sidebar:
    st.header("📋 Estado del Sistema")
    st.info(f"IA: {status_ia}")
    st.divider()
    cliente = st.text_input("Establecimiento / Cliente", value="JAVERIANO")
    fecha_auditoria = st.date_input("Fecha", datetime.now())
    auditor = st.text_input("Auditor", value="CEO Zodion")
    st.divider()
    if st.button("🔄 Reiniciar Auditoría"):
        st.session_state.analisis_cache = {}
        st.rerun()

# 3. MÓDULOS DE INSPECCIÓN
tab1, tab2, tab3 = st.tabs(["📸 IA Vision", "🔍 Evaluación Técnica", "📝 Reporte Final"])

with tab1:
    st.subheader("1. Análisis de Evidencias")
    fotos = st.file_uploader("Cargar imágenes de inspección", type=["jpg", "png", "jpeg"], accept_multiple_files=True)
    
    if fotos:
        for i, foto in enumerate(fotos):
            col_img, col_txt = st.columns([1, 2])
            with col_img:
                st.image(foto, use_container_width=True)
                if st.button(f"🪄 Analizar Foto {i+1}", key=f"btn_{i}"):
                    if model:
                        with st.spinner("Zodion AI procesando..."):
                            try:
                                img = Image.open(foto).convert('RGB')
                                response = model.generate_content(["Describe hallazgos sanitarios (Res. 2674) en esta imagen.", img])
                                st.session_state.analisis_cache[f"f_{i}"] = response.text
                            except Exception as e:
                                st.error(f"Error en el análisis: {e}")
                    else:
                        st.error("IA no lista. Verifique la barra lateral.")

            with col_txt:
                titulo = st.text_input(f"Título {i+1}:", value=f"Evidencia {i+1}", key=f"tit_{i}")
                analisis_ia = st.text_area(f"Resultado IA:", value=st.session_state.analisis_cache.get(f"f_{i}", ""), key=f"txt_{i}", height=150)

# Módulos de texto simple
with tab2:
    st.subheader("2. Evaluación Técnica")
    diag_seg = st.selectbox("Segregación:", ["CONFORME", "CUMPLE PARCIALMENTE", "NO CONFORME"])
    riesgo_mip = st.select_slider("Riesgo MIP:", options=["BAJO", "MODERADO", "ALTO", "CRÍTICO"])

with tab3:
    st.subheader("3. Recomendaciones")
    plan = st.text_area("Plan de Acción:", value="- Reorganización de frío.\n- Higiene de superficies.")

# 4. GENERACIÓN DE INFORME
st.divider()
if st.button("🚀 GENERAR INFORME"):
    txt_evidencias = ""
    for i in range(len(fotos) if fotos else 0):
        t = st.session_state.get(f"tit_{i}", f"Evidencia {i+1}")
        d = st.session_state.analisis_cache.get(f"f_{i}", "Sin datos.")
        txt_evidencias += f"{t.upper()}:\n{d}\n\n"

    informe = f"INFORME ZODION - {cliente.upper()}\nAUDITOR: {auditor}\nFECHA: {fecha_auditoria}\n\n1. EVIDENCIAS:\n{txt_evidencias}\n2. EVALUACIÓN:\nSegregación: {diag_seg}\nRiesgo: {riesgo_mip}\n\n3. PLAN:\n{plan}"
    st.text_area("Vista Previa:", informe, height=200)
    st.download_button("📥 DESCARGAR INFORME (.DOC)", informe, file_name=f"Zodion_{cliente}.doc")




