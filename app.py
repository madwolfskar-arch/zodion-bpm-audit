import streamlit as st
import pandas as pd
from datetime import datetime
import google.generativeai as genai
from PIL import Image
import io

# 1. Configuración de Identidad y API
st.set_page_config(page_title="Zodion - Auditoría Inteligente", page_icon="🛡️", layout="wide")

# Configuración de IA (Se asume que la clave está en st.secrets)
try:
    genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
    model = genai.GenerativeModel('gemini-1.5-flash')
except Exception as e:
    st.error("⚠️ Error de configuración: Verifica la API Key en los Secrets de Streamlit.")

# Estética Corporativa
st.markdown("""
    <style>
    .main { background-color: #f0f2f5; }
    .stDownloadButton button {
        background-color: #003366 !important;
        color: white !important;
        width: 100% !important;
        height: 3.5em !important;
        font-weight: bold !important;
        border-radius: 8px !important;
    }
    .report-preview {
        background-color: #ffffff;
        padding: 40px;
        border: 2px solid #003366;
        border-radius: 10px;
        font-family: 'Courier New', Courier, monospace;
        color: #000;
        white-space: pre-wrap;
    }
    </style>
    """, unsafe_allow_html=True)

st.title("🛡️ Sistema de Diagnóstico Técnico ZODION (IA)")

if 'informe_final' not in st.session_state:
    st.session_state.informe_final = ""

# 2. Captura de Datos Generales
with st.sidebar:
    st.header("📋 Datos de Auditoría")
    cliente = st.text_input("Establecimiento / Cliente", value="CLIENTE NUEVO")
    fecha_auditoria = st.date_input("Fecha", datetime.now())
    auditor = st.text_input("Auditor", value="CEO Zodion")
    st.divider()
    st.caption("Pioneros en Saneamiento Ecológico")
    if st.button("Limpiar Aplicación"):
        st.rerun()

# 3. Módulos de Inspección
tab1, tab2, tab3 = st.tabs(["📸 IA Vision: Evidencias", "🔍 Evaluación Técnica", "📝 Diagnóstico Final"])

with tab1:
    st.subheader("1. Análisis de Evidencia con Inteligencia Artificial")
    fotos = st.file_uploader("Cargar registros fotográficos", type=["jpg", "png", "jpeg"], accept_multiple_files=True)
    
    analisis_fotos = []
    
    if fotos:
        for i, foto in enumerate(fotos):
            col_img, col_txt = st.columns([1, 2])
            with col_img:
                st.image(foto, use_container_width=True)
                if st.button(f"🪄 Analizar Foto {i+1}", key=f"btn_{i}"):
                    with st.spinner("Analizando con Zodion AI..."):
                        img = Image.open(foto)
                        prompt = (
                            "Eres un auditor experto en inocuidad alimentaria (Res. 2674 de 2013, Colombia). "
                            "Analiza esta imagen y describe brevemente: 1. Qué se observa. 2. Posibles riesgos sanitarios "
                            "o de plagas (MIP). 3. Hallazgo técnico. Sé conciso y profesional."
                        )
                        response = model.generate_content([prompt, img])
                        st.session_state[f"desc_{i}"] = response.text

            with col_txt:
                titulo_foto = st.text_input(f"Título Evidencia {i+1}:", value=f"Evidencia {i+1}", key=f"tit_{i}")
                # El área de texto toma el valor generado por la IA o permite escritura manual
                desc_final = st.text_area(f"Análisis Técnico {i+1}:", value=st.session_state.get(f"desc_{i}", ""), key=f"txt_{i}", height=150)
                analisis_fotos.append(f"{titulo_foto.upper()}:\n{desc_final}")

with tab2:
    st.subheader("2. Evaluación Técnica (Basada en Res. 2674)")
    
    st.markdown("### A. SEGREGACIÓN Y DISPOSICIÓN")
    diag_seg = st.selectbox("Estado:", ["CONFORME", "CUMPLE PARCIALMENTE", "NO CONFORME"], index=0)
    analisis_seg = st.text_area("Observación Segregación:", placeholder="Describa el manejo de contaminación cruzada...")

    st.markdown("### B. TRAZABILIDAD Y CADUCIDAD")
    diag_tra = st.selectbox("Estado Trazabilidad:", ["CONFORME", "CUMPLE PARCIALMENTE", "NO CONFORME"], index=0)
    analisis_tra = st.text_area("Observación Trazabilidad:", placeholder="Estado de rotulado y fechas...")

    st.markdown("### C. EQUIPOS Y UTENSILIOS")
    diag_equ = st.selectbox("Estado Equipos:", ["CONFORME", "CUMPLE PARCIALMENTE", "NO CONFORME"], index=0)
    analisis_equ = st.text_area("Observación Equipos:", placeholder="Higiene de superficies y juntas...")

with tab3:
    st.subheader("3. Diagnóstico MIP y Recomendaciones")
    riesgo_mip = st.select_slider("Nivel de Riesgo MIP:", options=["BAJO", "MODERADO", "ALTO", "CRÍTICO"], value="BAJO")
    eval_mip = st.text_area("Evaluación de Plagas:", placeholder="Presencia de indicios, refugios o deficiencias estructurales...")
    
    st.divider()
    plan_accion = st.text_area("Recomendaciones y Plan de Acción:", 
                               "- Reorganización de almacenamiento.\n- Refuerzo de rotulado.\n- Cronograma de limpieza profunda.")

# 4. Generación de Informe
if st.button("🚀 GENERAR INFORME TÉCNICO FINAL"):
    txt_fotos = "\n\n".join(analisis_fotos) if analisis_fotos else "No se registraron evidencias fotográficas."
    
    cuerpo_informe = (
        "INFORME TÉCNICO DE AUDITORÍA Y DIAGNÓSTICO PROFESIONAL\n"
        "ZODION SERVICIOS AMBIENTALES\n\n"
        f"ESTABLECIMIENTO: {cliente.upper()}\n"
        f"FECHA: {fecha_auditoria.strftime('%d de %B de %Y')}\n"
        f"AUDITOR: {auditor}\n"
        f"SISTEMA DE REFERENCIA: Resolución 2674 de 2013 (Colombia)\n\n"
        "------------------------------------------------------------\n"
        "1. ANÁLISIS DETALLADO DE EVIDENCIA FOTOGRÁFICA (IA VISION)\n"
        "------------------------------------------------------------\n"
        f"{txt_fotos}\n\n"
        "------------------------------------------------------------\n"
        "2. EVALUACIÓN TÉCNICA POR ELEMENTOS\n"
        "------------------------------------------------------------\n"
        f"A. SEGREGACIÓN Y DISPOSICIÓN: {diag_seg}\n"
        f"Análisis: {analisis_seg}\n\n"
        f"B. TRAZABILIDAD Y CADUCIDAD: {diag_tra}\n"
        f"Análisis: {analisis_tra}\n\n"
        f"C. EQUIPOS Y UTENSILIOS: {diag_equ}\n"
        f"Análisis: {analisis_equ}\n\n"
        "------------------------------------------------------------\n"
        "3. DIAGNÓSTICO DEL MANEJO INTEGRAL DE PLAGAS (MIP)\n"
        "------------------------------------------------------------\n"
        f"Nivel de Riesgo: {riesgo_mip}.\n"
        f"Evaluación: {eval_mip}\n\n"
        "------------------------------------------------------------\n"
        "4. RECOMENDACIONES Y PLAN DE ACCIÓN\n"
        "------------------------------------------------------------\n"
        f"{plan_accion}\n\n"
        "------------------------------------------------------------\n"
        "JUNTOS LO HACEMOS POSIBLE.\n"
        "ZODION - PASTO, NARIÑO.\n"
        "============================================================"
    )

    st.session_state.informe_final = cuerpo_informe
    st.success("✅ Informe generado con éxito.")

# 5. Visualización y Descarga
if st.session_state.informe_final:
    st.markdown('<div class="report-preview">', unsafe_allow_html=True)
    st.text(st.session_state.informe_final)
    st.markdown('</div>', unsafe_allow_html=True)
    
    st.download_button(
        label="📥 DESCARGAR INFORME OFICIAL (.DOC)",
        data=st.session_state.informe_final,
        file_name=f"Informe_Zodion_{cliente}_{datetime.now().strftime('%d_%m_%Y')}.doc",
        mime="application/msword"
    )
    

