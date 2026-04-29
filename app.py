import streamlit as st
import pandas as pd
from datetime import datetime

# 1. Configuración de Identidad y Estética Corporativa
st.set_page_config(page_title="Zodion - Auditoría Técnica de Evidencias", page_icon="🛡️", layout="wide")

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

st.title("🛡️ Sistema de Diagnóstico Técnico ZODION")

if 'informe_final' not in st.session_state:
    st.session_state.informe_final = ""

# 2. Captura de Datos Generales
with st.sidebar:
    st.header("📋 Datos de Auditoría")
    cliente = st.text_input("Establecimiento / Cliente", value="JAVERIANO")
    fecha_auditoria = st.date_input("Fecha", datetime.now())
    auditor = st.text_input("Auditor", value="CEO Zodion")
    st.divider()
    st.caption("Especialistas en Saneamiento Ecológico")

# 3. Módulos de Inspección Profesional
tab1, tab2, tab3 = st.tabs(["📸 Análisis de Evidencia", "🔍 Evaluación Técnica", "📝 Diagnóstico y Plan"])

with tab1:
    st.subheader("1. Análisis Detallado de Evidencia Fotográfica")
    fotos = st.file_uploader("Cargar registros fotográficos", type=["jpg", "png", "jpeg"], accept_multiple_files=True)
    
    analisis_fotos = []
    if fotos:
        for i, foto in enumerate(fotos):
            col_img, col_txt = st.columns([1, 2])
            with col_img:
                st.image(foto, use_container_width=True)
            with col_txt:
                titulo_foto = st.text_input(f"Título de Evidencia {i+1}:", placeholder="Ej: Refrigeración/Lácteos", key=f"tit_{i}")
                desc_foto = st.text_area(f"Análisis Técnico de Evidenci {i+1}:", key=f"desc_{i}")
                analisis_fotos.append(f"Evidencia {i+1} ({titulo_foto}): {desc_foto}")

with tab2:
    st.subheader("2. Evaluación Técnica por Elementos")
    
    # A. Segregación
    st.markdown("### A. SEGREGACIÓN Y DISPOSICIÓN (Art. 16, 27)")
    diag_seg = st.selectbox("Diagnóstico Segregación:", ["CONFORME.", "CUMPLE PARCIALMENTE.", "NO CONFORME."], key="diag_seg")
    analisis_seg = st.text_area("Análisis Segregación:", "Según la normativa, los alimentos deben almacenarse según su naturaleza...")

    # B. Trazabilidad
    st.markdown("### B. TRAZABILIDAD Y CADUCIDAD (Art. 16)")
    diag_tra = st.selectbox("Diagnóstico Trazabilidad:", ["CONFORME.", "CUMPLE PARCIALMENTE.", "NO CONFORME."], key="diag_tra")
    analisis_tra = st.text_area("Análisis Trazabilidad:", "Los productos cuentan con rotulado de fábrica...")

    # C. Equipos
    st.markdown("### C. EQUIPOS Y UTENSILIOS (Art. 10-13)")
    diag_equ = st.selectbox("Diagnóstico Equipos:", ["CONFORME.", "CUMPLE PARCIALMENTE.", "NO CONFORME."], key="diag_equ")
    analisis_equ = st.text_area("Análisis Equipos:", "Las superficies internas de los equipos parecen ser de material inerte...")

with tab3:
    st.subheader("3. Diagnóstico MIP y 4. Recomendaciones")
    riesgo_mip = st.select_slider("Nivel de Riesgo MIP:", options=["BAJO", "MODERADO", "ALTO", "CRÍTICO"])
    eval_mip = st.text_area("Evaluación MIP:", "El desorden en el almacenamiento facilita la creación de refugios...")
    
    st.divider()
    plan_accion = st.text_area("Recomendaciones y Plan de Acción:", 
                               "- Reorganización Inmediata\n- Etiquetado Interno\n- Higiene de Equipos\n- Uso de Recipientes")

# 4. Procesamiento con Estructura Zodion
st.divider()
if st.button("🚀 GENERAR INFORME TÉCNICO PROFESIONAL"):
    
    txt_fotos = "\n".join(analisis_fotos) if analisis_fotos else "Sin evidencias registradas."
    
    # Formato de presentación exacto solicitado
    informe_final = f"""INFORME TÉCNICO DE AUDITORÍA Y DIAGNÓSTICO PROFESIONAL
ZODION SERVICIOS AMBIENTALES

ESTABLECIMIENTO: {cliente.upper()}
FECHA: {fecha_auditoria.strftime('%d de %B de %Y')}
AUDITOR: {auditor}
SISTEMA DE REFERENCIA: Resolución 2674 de 2013 (Colombia)

------------------------------------------------------------
1. ANÁLISIS DETALLADO DE EVIDENCIA FOTOGRÁFICA
------------------------------------------------------------
{txt_fotos}

------------------------------------------------------------
2. EVALUACIÓN TÉCNICA POR ELEMENTOS
------------------------------------------------------------
A. SEGREGACIÓN Y DISPOSICIÓN (Art. 16, 27)
Diagnóstico: {diag_seg}
Análisis: {analisis_seg}

B. TRAZABILIDAD Y CADUCIDAD (Art. 16)
Diagnóstico: {diag_tra}
Análisis: {analisis_tra}

C. EQUIPOS Y UTENSILIOS (Art. 10-13)
Diagnóstico: {diag_equ}
Análisis: {analisis_equ}

------------------------------------------------------------
3. DIAGNÓSTICO



