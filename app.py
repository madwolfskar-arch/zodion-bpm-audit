import streamlit as st
import pandas as pd
from datetime import datetime

# Configuración de página para entorno Cloud
st.set_page_config(
    page_title="Zodion - Auditoría BPM Pro",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Estética Corporativa Zodion
st.markdown("""
    <style>
    .report-card {
        background-color: #ffffff;
        padding: 25px;
        border-radius: 12px;
        border-left: 10px solid #003366;
        box-shadow: 0 4px 12px rgba(0,0,0,0.1);
        margin-top: 20px;
    }
    .stTabs [data-baseweb="tab-list"] { gap: 24px; }
    .stTabs [data-baseweb="tab"] {
        height: 50px;
        white-space: pre-wrap;
        background-color: #f0f2f6;
        border-radius: 5px 5px 0px 0px;
        gap: 1px;
        padding-top: 10px;
        padding-bottom: 10px;
    }
    </style>
    """, unsafe_allow_html=True)

st.title("🛡️ Sistema de Gestión y Diagnóstico ZODION")

# Sidebar - Datos de Auditoría
with st.sidebar:
    st.header("📋 Información del Servicio")
    cliente = st.text_input("Establecimiento / Cliente", placeholder="Ej. Planta de Procesamiento X")
    fecha = st.date_input("Fecha de Inspección", datetime.now())
    auditor = st.text_input("Auditor Responsable", value="CEO Zodion")
    st.divider()
    st.info("Basado en los requisitos de la Resolución 2674 de 2013.")

# Pestañas de Auditoría
tab1, tab2, tab3, tab4 = st.tabs(["🏗️ Infraestructura", "📦 Almacenamiento", "🪳 Control MIP", "📸 Evidencias"])

with tab1:
    st.subheader("Análisis de Edificación e Instalaciones")
    col1, col2 = st.columns(2)
    with col1:
        ins_localizacion = st.selectbox("Localización y accesos:", ["Cumple", "Cumple Parcialmente", "No Cumple"])
        ins_diseno = st.selectbox("Diseño y construcción sanitaria:", ["Cumple", "Cumple Parcialmente", "No Cumple"])
    with col2:
        hallazgos_infra = st.text_area("Hallazgos específicos (Art. 6 - 9):")

with tab2:
    st.subheader("Gestión de Productos y Caducidad")
    c1, c2 = st.columns(2)
    with c1:
        prod_vencidos = st.radio("¿Se detectaron productos con FECHA DE CADUCIDAD VENCIDA?", ["No", "Sí"], help="Incumplimiento grave del Art. 16")
        prod_rotulado = st.radio("¿El rotulado cumple con la normativa vigente?", ["Sí", "No"])
    with c2:
        almacenamiento = st.radio("¿Separación adecuada de productos (evita contaminación)?", ["Sí", "No"])
        detalles_caducidad = st.text_area("Análisis detallado de productos (Lotes/Fechas):")

with tab3:
    st.subheader("Manejo Integral de Plagas (Sello Zodion)")
    p1 = st.checkbox("Programa MIP documentado y actualizado")
    p2 = st.checkbox("Registros de aplicación y fichas técnicas")
    obs_pest = st.text_area("Observaciones del control preventivo:")

with tab4:
    st.subheader("Registro Fotográfico")
    fotos = st.file_uploader("Subir evidencias (JPG/PNG)", accept_multiple_files=True)
    if fotos:
        st.success(f"{len(fotos)} imágenes listas para el reporte.")

# Generación del Informe Diagnóstico
st.divider()
if st.button("🚀 GENERAR DIAGNÓSTICO TÉCNICO E INFORME"):
    if not cliente:
        st.error("Error: Por favor identifique al establecimiento.")
    else:
        st.balloons()
        st.markdown(f"<div class='report-card'>", unsafe_allow_html=True)
        st.header(f"DIAGNÓSTICO TÉCNICO - {cliente.upper()}")
        st.write(f"**Fecha:** {fecha} | **Auditor:** {auditor}")
        
        # 1. Fundamentación
        st.markdown("### 📜 1. Fundamentación Normativa")
        st.write("Evaluación realizada bajo los estándares de la **Resolución 2674 de 2013**, sobre requisitos sanitarios en la manipulación de alimentos.")

        # 2. Análisis de Hallazgos
        st.markdown("### 🔬 2. Análisis de Hallazgos")
        col_res1, col_res2 = st.columns(2)
        
        with col_res1:
            st.write("**Estado de Almacenamiento:**")
            if prod_vencidos == "Sí":
                st.error("❗ ALERTA: Se hallaron productos con fecha de caducidad vencida. Riesgo sanitario alto.")
            else:
                st.success("✅ Control de caducidades conforme a la normativa.")
        
        with col_res2:
            st.write("**Estado de Infraestructura:**")
            if ins_localizacion == "No Cumple":
                st.warning("⚠️ El establecimiento presenta riesgos por localización o accesos.")
            else:
                st.success("✅ Infraestructura cumple con protección básica.")

        # 3. Sugerencias y Plan de Acción
        st.markdown("### 💡 3. Sugerencias y Plan de Mejora")
        sug = []
        if prod_vencidos == "Sí":
            sug.append("- Implementar de inmediato el sistema **PEPS** (Primero en Entrar, Primero en Salir).")
            sug.append("- Realizar auditoría de inventario semanal de fechas críticas.")
        if almacenamiento == "No":
            sug.append("- Reorganizar el almacenamiento para evitar contaminación cruzada (Separación mínima 60cm).")
        if not p1:
            sug.append("- Formalizar el Programa MIP bajo estándares de control biológico Zodion.")
        
        if sug:
            for s in sug: st.write(s)
        else:
            st.write("Mantener los estándares actuales y realizar seguimiento preventivo.")
            
        st.markdown("</div>", unsafe_allow_html=True)
        



