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
        padding: 35px;
        border: 1px solid #003366;
        border-left: 12px solid #003366;
        font-family: 'Times New Roman', serif;
        color: #000;
        line-height: 1.5;
    }
    </style>
    """, unsafe_allow_html=True)

st.title("🛡️ Sistema de Análisis y Diagnóstico Fotográfico ZODION")

if 'informe_final' not in st.session_state:
    st.session_state.informe_final = ""

# 2. Captura de Datos Generales
with st.sidebar:
    st.header("📋 Datos del Servicio")
    cliente = st.text_input("Establecimiento / Cliente", value="JAVERIANO")
    fecha = st.date_input("Fecha de Inspección", datetime.now())
    auditor = st.text_input("Auditor Responsable", value="CEO Zodion")
    st.divider()
    st.caption("Pioneros en Saneamiento Ecológico")

# 3. Módulos de Evaluación Técnica
tab1, tab2, tab3 = st.tabs(["📸 Análisis de Evidencia Fotográfica", "🔍 Evaluación de Elementos", "📝 Diagnóstico Final"])

with tab1:
    st.subheader("Carga y Análisis de Evidencias")
    fotos = st.file_uploader("Suba las fotografías de la inspección", type=["jpg", "png", "jpeg"], accept_multiple_files=True)
    
    descripciones = []
    if fotos:
        for i, foto in enumerate(fotos):
            col_img, col_txt = st.columns([1, 2])
            with col_img:
                st.image(foto, caption=f"Evidencia {i+1}", use_container_width=True)
            with col_txt:
                desc = st.text_area(f"Análisis técnico de la imagen {i+1}:", 
                                   placeholder="Ej: Se observa falta de segregación en lácteos y cárnicos...", 
                                   key=f"txt_foto_{i}")
                descripciones.append(f"- Evidencia {i+1}: {desc}")

with tab2:
    st.subheader("Evaluación Normativa (Res. 2674 de 2013)")
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("**Infraestructura y Equipos**")
        eval_infra = st.selectbox("Edificación (Art. 6):", ["Conforme", "No Conforme", "Riesgo Crítico"])
        eval_equipo = st.selectbox("Equipos (Art. 10):", ["Conforme", "No Conforme"])
        desc_activos = st.text_area("Detalle técnico de Activos:", "Superficies inertes y materiales conformes.")
    with col2:
        st.markdown("**Trazabilidad y Disposición**")
        eval_segregacion = st.selectbox("Segregación de Alimentos:", ["Conforme", "Deficiente (Mezcla de tipos)", "Crítico"])
        eval_prod = st.selectbox("Caducidad (Art. 16):", ["Vigente", "Hallazgos de Vencimiento"])
        desc_insumos = st.text_area("Análisis de Productos:", "Verificación de rotulado y cadena de frío.")

with tab3:
    st.subheader("Diagnóstico Zodion")
    eval_mip = st.radio("Riesgo de Plagas:", ["Nula", "Baja", "Moderada", "Alta"])
    recomendaciones = st.text_area("Plan de Mejora y Recomendaciones:", 
                                  "Implementar etiquetas de trazabilidad interna y reordenar cavas de frío.")

# 4. Generación del Informe Profesional Extenso
st.divider()
if st.button("🚀 PROCESAR AUDITORÍA Y GENERAR DOCUMENTACIÓN"):
    
    txt_evidencias = "\n".join(descripciones) if descripciones else "No se registraron evidencias fotográficas."
    
    informe_extenso = f"""
======================================================================
         INFORME TÉCNICO DE AUDITORÍA Y DIAGNÓSTICO PROFESIONAL
                     ZODION SERVICIOS AMBIENTALES
======================================================================
CLIENTE: {cliente.upper()}
FECHA DE INSPECCIÓN: {fecha}
AUDITOR RESPONSABLE: {auditor}
SISTEMA DE REFERENCIA: Resolución 2674 de 2013 (BPM Colombia)
----------------------------------------------------------------------

1. ANÁLISIS DETALLADO DE EVIDENCIA FOTOGRÁFICA
{txt_evidencias}

2. EVALUACIÓN TÉCNICA POR ELEMENTOS
A. EDIFICACIÓN E INSTALACIONES (Cap. I, Art. 6-9):
   Diagnóstico: {eval_infra}
   Observaciones: {desc_activos}

B. EQUIPOS Y UTENSILIOS (Cap. II, Art. 10-13):
   Estado: {eval_equipo}
   Análisis: Los equipos deben garantizar la ausencia de contaminación cruzada.

C. ALIMENTOS, BEBIDAS Y EMPAQUES (Cap. IV y VI):
   Segregación de Productos: {eval_segregacion}
   Control de Caducidades: {eval_prod}
   Análisis Técnico: {desc_insumos}

3. DIAGNÓSTICO DEL MANEJO INTEGRAL DE PLAGAS (MIP)
   Riesgo Detectado: {eval_mip}
   Evaluación: El orden y la limpieza son la base del saneamiento ecológico.

4. RECOMENDACIONES Y PLAN DE ACCIÓN PROFESIONAL
- RECOMENDACIÓN DE SEGREGACIÓN: Separar estrictamente cárnicos de lácteos y verduras (Art. 27).
- RECOMENDACIÓN DE TRAZABILIDAD: Implementar etiquetas de "Producto Abierto" (Art. 16).
- ACCIÓN SUGERIDA: {recomendaciones}

----------------------------------------------------------------------
ESTE DOCUMENTO ES UN DIAGNÓSTICO TÉCNICO BASADO EN EVIDENCIA VISUAL.
JUNTOS LO HACEMOS POSIBLE. ZODION - PASTO, NARIÑO.
======================================================================
"""
    st.session_state.informe_final = informe_extenso
    st.info("✅ Análisis realizado")

# 5. Visualización y Descarga Word
if st.session_state.informe_final:
    st.markdown('<div class="report-preview">', unsafe_allow_html=True)
    st.text(st.session_state.informe_final)
    st.markdown('</div>', unsafe_allow_html=True)
    
    st.download_button(
        label="📥 DESCARGAR INFORME TÉCNICO PROFESIONAL (.DOC)",
        data=st.session_state.informe_final,
        file_name=f"Informe_Zodion_{cliente}_{datetime.now().strftime('%d_%m_%Y')}.doc",
        mime="application/msword",
        key="btn_descarga_word_v5"
    )




