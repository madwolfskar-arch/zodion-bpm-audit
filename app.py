import streamlit as st
import pandas as pd
from datetime import datetime
import google.generativeai as genai
from PIL import Image
import io

# 1. CONFIGURACIÓN DE IDENTIDAD Y ESTÉTICA CORPORATIVA
st.set_page_config(page_title="Zodion - Auditoría Técnica IA", page_icon="🛡️", layout="wide")

# Inicialización segura del modelo de IA
model = None
if "GOOGLE_API_KEY" in st.secrets:
    try:
        genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
        model = genai.GenerativeModel('gemini-1.5-flash')
    except Exception as e:
        st.error(f"Error al configurar Google AI: {e}")
else:
    st.warning("⚠️ Configuración pendiente: Agrega 'GOOGLE_API_KEY' en los Secrets de Streamlit.")

# Estilo CSS personalizado
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
st.caption("CEO de Zodion - Innovación en Saneamiento Ecológico y Ambiental")

if 'informe_final' not in st.session_state:
    st.session_state.informe_final = ""

# 2. CAPTURA DE DATOS EN BARRA LATERAL
with st.sidebar:
    st.header("📋 Datos de Auditoría")
    cliente = st.text_input("Establecimiento / Cliente", value="JAVERIANO")
    fecha_auditoria = st.date_input("Fecha", datetime.now())
    auditor = st.text_input("Auditor", value="Asesor Ambiental Zodion")
    st.divider()
    if st.button("🔄 Reiniciar Aplicación"):
        for key in list(st.session_state.keys()):
            del st.session_state[key]
        st.rerun()

# 3. MÓDULOS DE INSPECCIÓN
tab1, tab2, tab3 = st.tabs(["📸 IA Vision: Análisis", "🔍 Evaluación Normativa", "📝 Reporte Final"])

with tab1:
    st.subheader("1. Análisis Detallado de Evidencias (IA)")
    fotos = st.file_uploader("Subir fotos de inspección", type=["jpg", "png", "jpeg"], accept_multiple_files=True)
    
    analisis_fotos = []
    if fotos:
        for i, foto in enumerate(fotos):
            col_img, col_txt = st.columns([1, 2])
            with col_img:
                st.image(foto, use_container_width=True)
                if st.button(f"🪄 Analizar Evidencia {i+1}", key=f"btn_{i}"):
                    if model:
                        with st.spinner("Zodion AI analizando..."):
                            img = Image.open(foto)
                            prompt = "Analiza esta imagen para una auditoría de inocuidad alimentaria en Colombia (Res 2674). Identifica el objeto y describe hallazgos técnicos o riesgos sanitarios brevemente."
                            response = model.generate_content([prompt, img])
                            st.session_state[f"desc_{i}"] = response.text
                    else:
                        st.error("IA no configurada. Revisa los Secrets.")

            with col_txt:
                titulo = st.text_input(f"Título {i+1}:", value=f"Evidencia {i+1}", key=f"tit_{i}")
                desc_ia = st.text_area(f"Análisis Técnico:", value=st.session_state.get(f"desc_{i}", ""), key=f"txt_{i}", height=150)
                analisis_fotos.append(f"{titulo.upper()}:\n{desc_ia}")

with tab2:
    st.subheader("2. Evaluación Técnica por Elementos")
    col1, col2 = st.columns(2)
    
    with col1:
        diag_seg = st.selectbox("Segregación (Art. 16, 27):", ["CONFORME", "CUMPLE PARCIALMENTE", "NO CONFORME"], index=0)
        obs_seg = st.text_area("Análisis Segregación:", placeholder="Describa hallazgos...")

        diag_tra = st.selectbox("Trazabilidad (Art. 16):", ["CONFORME", "CUMPLE PARCIALMENTE", "NO CONFORME"], index=0)
        obs_tra = st.text_area("Análisis Trazabilidad:", placeholder="Describa rotulado...")

    with col2:
        diag_equ = st.selectbox("Equipos (Art. 10-13):", ["CONFORME", "CUMPLE PARCIALMENTE", "NO CONFORME"], index=0)
        obs_equ = st.text_area("Análisis Equipos:", placeholder="Estado de superficies...")

        riesgo_mip = st.select_slider("Nivel Riesgo MIP:", options=["BAJO", "MODERADO", "ALTO", "CRÍTICO"])

with tab3:
    st.subheader("3. Diagnóstico y Plan de Acción")
    eval_mip = st.text_area("Evaluación MIP:", placeholder="Análisis de focos de plagas...")
    plan_accion = st.text_area("Recomendaciones:", value="- Reorganización de frío.\n- Mejora en rotulado.\n- Desinfección de superficies.")

# 4. PROCESAMIENTO DEL INFORME
st.divider()
if st.button("🚀 GENERAR ANÁLISIS COMPLETO"):
    txt_evidencias = "\n\n".join(analisis_fotos) if analisis_fotos else "Sin evidencias."
    
    informe = (
        "INFORME TÉCNICO DE AUDITORÍA - ZODION SERVICIOS AMBIENTALES\n"
        f"CLIENTE: {cliente.upper()} | FECHA: {fecha_auditoria}\n"
        f"AUDITOR: {auditor} | CIUDAD: PASTO, NARIÑO\n"
        "------------------------------------------------------------\n"
        "1. ANÁLISIS DE EVIDENCIAS FOTOGRÁFICAS (IA VISION)\n"
        f"{txt_evidencias}\n\n"
        "2. EVALUACIÓN NORMATIVA\n"
        f"- SEGREGACIÓN: {diag_seg} ({obs_seg})\n"
        f"- TRAZABILIDAD: {diag_tra} ({obs_tra})\n"
        f"- EQUIPOS: {diag_equ} ({obs_equ})\n\n"
        "3. DIAGNÓSTICO MIP\n"
        f"Nivel de Riesgo: {riesgo_mip}\n"
        f"Evaluación: {eval_mip}\n\n"
        "4. PLAN DE ACCIÓN\n"
        f"{plan_accion}\n\n"
        "JUNTOS LO HACEMOS POSIBLE.\n"
        "============================================================"
    )
    st.session_state.informe_final = informe
    st.success("✅ Análisis realizado")

if st.session_state.informe_final:
    st.text_area("Vista Previa del Informe:", st.session_state.informe_final, height=300)
    st.download_button("📥 DESCARGAR INFORME (.DOC)", st.session_state.informe_final, 
                       file_name=f"Zodion_{cliente}.doc", mime="application/msword")





