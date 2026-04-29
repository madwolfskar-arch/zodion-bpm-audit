import streamlit as st
import pandas as pd
from datetime import datetime
import google.generativeai as genai
from PIL import Image
import io

# 1. CONFIGURACIÓN DE IDENTIDAD ZODION
st.set_page_config(page_title="Zodion - Auditoría Técnica IA", page_icon="🛡️", layout="wide")

# Configuración de IA con forzado de versión estable
model = None
if "GOOGLE_API_KEY" in st.secrets:
    try:
        genai.configure(api_key=st.secrets["GOOGLE_API_KEY"].strip())
        # Usamos el nombre del modelo sin prefijos de versión para evitar el 404
        model = genai.GenerativeModel(model_name='gemini-1.5-flash')
    except Exception as e:
        st.error(f"Error al configurar Google AI: {e}")
else:
    st.warning("⚠️ Agrega 'GOOGLE_API_KEY' en los Secrets de Streamlit.")

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
st.caption("CEO de Zodion - Saneamiento Ecológico Profesional - Pasto, Nariño")

if 'analisis_dict' not in st.session_state:
    st.session_state.analisis_dict = {}

# 2. BARRA LATERAL
with st.sidebar:
    st.header("📋 Datos de Auditoría")
    cliente = st.text_input("Establecimiento / Cliente", value="JAVERIANO")
    fecha_auditoria = st.date_input("Fecha", datetime.now())
    auditor = st.text_input("Auditor", value="CEO Zodion")
    st.divider()
    if st.button("🔄 Reiniciar Aplicación"):
        st.session_state.analisis_dict = {}
        st.rerun()

# 3. MÓDULOS DE INSPECCIÓN
tab1, tab2, tab3 = st.tabs(["📸 IA Vision", "🔍 Evaluación", "📝 Reporte"])

with tab1:
    st.subheader("1. Análisis con IA")
    fotos = st.file_uploader("Subir fotos", type=["jpg", "png", "jpeg"], accept_multiple_files=True)
    
    if fotos:
        for i, foto in enumerate(fotos):
            col_img, col_txt = st.columns([1, 2])
            with col_img:
                st.image(foto, use_container_width=True)
                if st.button(f"🪄 Analizar Foto {i+1}", key=f"btn_{i}"):
                    if model:
                        with st.spinner("Zodion AI analizando..."):
                            try:
                                img = Image.open(foto).convert('RGB')
                                # Nueva forma de llamado más simple para evitar errores de versión
                                response = model.generate_content(["Analiza esta imagen para auditoría de alimentos (Res 2674 Colombia). Describe hallazgos sanitarios brevemente.", img])
                                st.session_state.analisis_dict[f"foto_{i}"] = response.text
                            except Exception as e:
                                st.error(f"Error en el análisis: {e}")
                    else:
                        st.error("IA no configurada.")

            with col_txt:
                titulo = st.text_input(f"Título {i+1}:", value=f"Evidencia {i+1}", key=f"tit_{i}")
                desc_ia = st.text_area(f"Análisis Técnico:", value=st.session_state.analisis_dict.get(f"foto_{i}", ""), key=f"txt_{i}", height=150)

with tab2:
    st.subheader("2. Evaluación Técnica")
    diag_seg = st.selectbox("Segregación:", ["CONFORME", "CUMPLE PARCIALMENTE", "NO CONFORME"])
    obs_seg = st.text_area("Observación Segregación:", key="obs_s")
    riesgo_mip = st.select_slider("Nivel Riesgo MIP:", options=["BAJO", "MODERADO", "ALTO", "CRÍTICO"])

with tab3:
    st.subheader("3. Recomendaciones")
    plan_accion = st.text_area("Plan de Acción:", value="- Reorganización de almacenamiento.\n- Refuerzo de rotulado.")

# 4. GENERACIÓN DE INFORME
st.divider()
if st.button("🚀 GENERAR INFORME"):
    # Consolidar evidencias
    txt_evidencias = ""
    for i in range(len(fotos) if fotos else 0):
        t = st.session_state.get(f"tit_{i}", f"Evidencia {i+1}")
        d = st.session_state.analisis_dict.get(f"foto_{i}", "Sin análisis.")
        txt_evidencias += f"{t.upper()}:\n{d}\n\n"

    informe = f"INFORME ZODION - {cliente.upper()}\nFecha: {fecha_auditoria}\nAuditor: {auditor}\n\n1. EVIDENCIAS:\n{txt_evidencias}\n\n2. EVALUACIÓN:\nSegregación: {diag_seg}\nRiesgo MIP: {riesgo_mip}\n\n3. ACCIÓN:\n{plan_accion}"
    
    st.text_area("Vista Previa:", informe, height=250)
    st.download_button("📥 DESCARGAR (.DOC)", informe, file_name=f"Zodion_{cliente}.doc")




