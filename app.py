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
    st.caption("Pioneros en Saneamiento Ecológico")

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
                desc_foto = st.text_area(f"Análisis Técnico de Evidencia {i+1}:", key=f"desc_{i}")
                analisis_fotos.append(f"Evidencia {i+1} ({titulo_foto}): {desc_foto}")

with tab2:
    st.subheader("2. Evaluación Técnica por Elementos")
    
    st.markdown("### A. SEGREGACIÓN Y DISPOSICIÓN (Art. 16, 27)")
    diag_seg = st.selectbox("Diagnóstico Segregación:", ["CONFORME.", "CUMPLE PARCIALMENTE.", "NO CONFORME."], index=2)
    analisis_seg = st.text_area("Análisis Segregación:", "Según la normativa, los alimentos deben almacenarse según su naturaleza para evitar la contaminación cruzada. Se observa mezcla de elementos en el equipo de frío...")

    st.markdown("### B. TRAZABILIDAD Y CADUCIDAD (Art. 16)")
    diag_tra = st.selectbox("Diagnóstico Trazabilidad:", ["CONFORME.", "CUMPLE PARCIALMENTE.", "NO CONFORME."], index=1)
    analisis_tra = st.text_area("Análisis Trazabilidad:", "Los productos cuentan con rotulado de fábrica. No obstante, en productos trasvasados se requiere implementación de etiquetas internas Zodion...")

    st.markdown("### C. EQUIPOS Y UTENSILIOS (Art. 10-13)")
    diag_equ = st.selectbox("Diagnóstico Equipos:", ["CONFORME.", "CUMPLE PARCIALMENTE.", "NO CONFORME."], index=0)
    analisis_equ = st.text_area("Análisis Equipos:", "Las superficies internas cumplen con material inerte. Se recomienda limpieza profunda en juntas de caucho para evitar biopelículas...")

with tab3:
    st.subheader("3. Diagnóstico MIP y 4. Recomendaciones")
    riesgo_mip = st.select_slider("Nivel de Riesgo MIP:", options=["BAJO", "MODERADO", "ALTO", "CRÍTICO"], value="MODERADO")
    eval_mip = st.text_area("Evaluación MIP:", "El desorden en el almacenamiento y la falta de segregación facilitan la creación de refugios para vectores...")
    
    st.divider()
    plan_accion = st.text_area("Recomendaciones y Plan de Acción:", 
                               "- Reorganización Inmediata: Jerarquía de frío.\n- Etiquetado Interno: Fechas de apertura.\n- Higiene de Equipos: Desinfección profunda.\n- Uso de Recipientes: Hermeticidad grado alimenticio.")

# 4. Procesamiento de Informe Optimizado
st.divider()
if st.button("🚀 GENERAR INFORME TÉCNICO PROFESIONAL"):
    
    txt_fotos = "\n".join(analisis_fotos) if analisis_fotos else "Sin evidencias registradas."
    
    # Construcción del informe con la estructura exacta solicitada
    cuerpo_informe = (
        "INFORME TÉCNICO DE AUDITORÍA Y DIAGNÓSTICO PROFESIONAL\n"
        "ZODION SERVICIOS AMBIENTALES\n\n"
        f"ESTABLECIMIENTO: {cliente.upper()}\n"
        f"FECHA: {fecha_auditoria.strftime('%d de %B de %Y')}\n"
        f"AUDITOR: {auditor}\n"
        f"SISTEMA DE REFERENCIA: Resolución 2674 de 2013 (Colombia)\n\n"
        "------------------------------------------------------------\n"
        "1. ANÁLISIS DETALLADO DE EVIDENCIA FOTOGRÁFICA\n"
        "------------------------------------------------------------\n"
        f"{txt_fotos}\n\n"
        "------------------------------------------------------------\n"
        "2. EVALUACIÓN TÉCNICA POR ELEMENTOS\n"
        "------------------------------------------------------------\n"
        "A. SEGREGACIÓN Y DISPOSICIÓN (Art. 16, 27)\n"
        f"Diagnóstico: {diag_seg}\n"
        f"Análisis: {analisis_seg}\n\n"
        "B. TRAZABILIDAD Y CADUCIDAD (Art. 16)\n"
        f"Diagnóstico: {diag_tra}\n"
        f"Análisis: {analisis_tra}\n\n"
        "C. EQUIPOS Y UTENSILIOS (Art. 10-13)\n"
        f"Diagnóstico: {diag_equ}\n"
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
    st.success("✅ Informe generado exitosamente.")

# 5. Visualización y Descarga Directa
if st.session_state.informe_final:
    st.markdown('<div class="report-preview">', unsafe_allow_html=True)
    st.text(st.session_state.informe_final)
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Optimizamos la descarga como archivo .doc para apertura inmediata en Word
    st.download_button(
        label="📥 DESCARGAR INFORME OFICIAL (.DOC)",
        data=st.session_state.informe_final,
        file_name=f"Informe_Zodion_{cliente}_{datetime.now().strftime('%d_%m_%Y')}.doc",
        mime="application/msword"
    )
 
