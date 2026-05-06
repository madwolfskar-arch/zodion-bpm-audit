import streamlit as st
import pandas as pd
from datetime import datetime

# 1. Configuración de Identidad y Estética Corporativa (Cero Animaciones)
st.set_page_config(page_title="Zodion - Auditoría Técnica de Evidencias", page_icon="🛡️", layout="wide")

st.markdown("""
    <style>
    .main { background-color: #f0f2f5; }
    .stDownloadButton button {
        background-color: #155724 !important;
        color: white !important;
        width: 100% !important;
        height: 4em !important;
        font-weight: bold !important;
        border: 2px solid #0b2e13 !important;
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

# Inicialización de memoria de informe
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
    st.subheader("Carga y Descripción de Evidencias")
    fotos = st.file_uploader("Suba las fotografías de la inspección", type=["jpg", "png", "jpeg"], accept_multiple_files=True)
    
    analisis_fotos = []
    if fotos:
        st.info(f"Se han cargado {len(fotos)} imágenes para análisis.")
        for i, foto in enumerate(fotos):
            st.write(f"**Identificación de Elemento en Foto {i+1}:**")
            desc = st.text_area(f"Análisis técnico de la imagen {i+1}:", 
                                placeholder="Ej: Se observa equipo de refrigeración con acumulación de escarcha y sellos gastados...", key=f"foto_{i}")
            analisis_fotos.append(f"- Evidencia {i+1}: {desc}")

with tab2:
    st.subheader("Evaluación de Conformidad por Elemento")
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("**Infraestructura y Equipos**")
        eval_infra = st.selectbox("Estado de Edificación (Art. 6):", ["Conforme", "No Conforme", "Riesgo Crítico"])
        eval_equipo = st.selectbox("Estado de Equipos (Art. 10):", ["Conforme", "No Conforme"])
        desc_infra_equipo = st.text_area("Detalle técnico de Activos:", "Evaluación de superficies, materiales y diseño sanitario.")

    with col2:
        st.markdown("**Alimentos, Bebidas y Empaques**")
        eval_prod = st.selectbox("Cumplimiento de Caducidad (Art. 16):", ["Sin Novedad", "Hallazgos Menores", "Incumplimiento Grave"])
        eval_emp = st.selectbox("Integridad de Empaques (Art. 33):", ["Conforme", "No Conforme"])
        desc_prod_emp = st.text_area("Análisis de Productos e Insumos:", "Verificación de rotulado, trazabilidad y condiciones de conservación.")

with tab3:
    st.subheader("Manejo Integral de Plagas y Saneamiento")
    eval_mip = st.radio("Diagnóstico de Actividad de Plagas:", ["Nula", "Baja", "Moderada", "Alta"])
    recomendaciones_extra = st.text_area("Recomendaciones Estratégicas Zodion:", "Basadas en el enfoque de saneamiento ecológico.")

# 4. Generación de Información Extensa y Profesional
st.divider()
if st.button("🚀 PROCESAR AUDITORÍA Y GENERAR DOCUMENTACIÓN"):
    
    # Construcción de la información profesional
    evidencias_texto = "\n".join(analisis_fotos) if analisis_fotos else "No se cargaron descripciones fotográficas."
    
    informe_extenso = f"""
======================================================================
         INFORME TÉCNICO DE AUDITORÍA Y DIAGNÓSTICO PROFESIONAL
                     ZODION SERVICIOS AMBIENTALES
======================================================================
ESTABLECIMIENTO: {cliente.upper()}
FECHA DE INSPECCIÓN: {fecha}
AUDITOR RESPONSABLE: {auditor}
SISTEMA DE REFERENCIA: Resolución 2674 de 2013 (BPM Colombia)
----------------------------------------------------------------------

1. ANÁLISIS DETALLADO DE EVIDENCIA FOTOGRÁFICA
{evidencias_texto}

2. EVALUACIÓN TÉCNICA POR ELEMENTOS
A. EDIFICACIÓN E INSTALACIONES (Cap. I, Art. 6-9):
   Diagnóstico: {eval_infra}
   Observaciones: {desc_infra_equipo}

B. EQUIPOS Y UTENSILIOS (Cap. II, Art. 10-13):
   Diagnóstico: {eval_equipo}
   Análisis: Los equipos evaluados deben garantizar la ausencia de contaminación 
   cruzada y permitir un proceso de higienización profunda.

C. ALIMENTOS, BEBIDAS Y EMPAQUES (Cap. IV y VI):
   Estado de Caducidades: {eval_prod}
   Estado de Empaques: {eval_emp}
   Análisis Técnico: {desc_prod_emp}

3. DIAGNÓSTICO DEL MANEJO INTEGRAL DE PLAGAS (MIP)
   Nivel de Riesgo Detectado: {eval_mip}
   Evaluación: Se prioriza la modificación de factores ambientales para 
   eliminar nichos de anidamiento, siguiendo la filosofía de Saneamiento Ecológico Zodion.

4. RECOMENDACIONES PARA EL CUMPLIMIENTO NORMATIVO (PLAN DE ACCIÓN)
   - Realizar mantenimiento correctivo inmediato en los puntos señalados en la evidencia fotográfica.
   - Fortalecer el protocolo de rotación de inventarios (PEPS) conforme al Art. 16.
   - Ejecutar el sellamiento de juntas y grietas identificadas para evitar el ingreso de vectores.
   - Recomendación Especial Zodion: {recomendaciones_extra}

----------------------------------------------------------------------
ESTE DOCUMENTO CONSTITUYE UN DIAGNÓSTICO TÉCNICO DE REFERENCIA.
JUNTOS LO HACEMOS POSIBLE.
ZODION - PASTO, NARIÑO.
----------------------------------------------------------------------
"""
    st.session_state.informe_final = informe_extenso
    st.success("✅ Análisis realizado exitosamente.")

# 5. Despliegue de Informe y Botón de Descarga Prioritario
if st.session_state.informe_final:
    st.markdown('<div class="report-preview">', unsafe_allow_html=True)
    st.text(st.session_state.informe_final)
    st.markdown('</div>', unsafe_allow_html=True)
    
    st.download_button(
        label="📥 DESCARGAR INFORME TÉCNICO PROFESIONAL (EXTENSO)",
        data=st.session_state.informe_final,
        file_name=f"Informe_Profesional_Zodion_{cliente}_{datetime.now().strftime('%d_%m_%Y')}.txt",
        mime="text/plain",
        key="btn_descarga_final"
    )

