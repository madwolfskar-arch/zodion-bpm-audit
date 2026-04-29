import streamlit as st
import pandas as pd
from datetime import datetime

# 1. Configuración de página y Estética Corporativa
st.set_page_config(page_title="Zodion - Generador de Diagnósticos BPM", page_icon="🛡️", layout="wide")

st.markdown("""
    <style>
    .report-box {
        background-color: #ffffff;
        padding: 30px;
        border: 1px solid #e0e0e0;
        border-radius: 10px;
        font-family: 'Segoe UI', sans-serif;
    }
    .stButton>button {
        background-color: #003366;
        color: white;
        font-weight: bold;
        height: 3em;
    }
    </style>
    """, unsafe_allow_html=True)

# 2. Datos de Entrada (Sidebar)
with st.sidebar:
    st.image("https://via.placeholder.com/200x80?text=ZODION", use_container_width=True)
    st.header("📋 Datos del Servicio")
    fecha = st.date_input("Fecha de Auditoría", datetime.now())
    cliente = st.text_input("Nombre del Establecimiento", placeholder="Ej: Restaurante Central")
    auditor = st.text_input("Auditor Responsable", value="Profesional Zodion")
    st.divider()
    st.info("Este sistema genera diagnósticos basados en la Res. 2674/2013.")

st.title("🛡️ Panel de Auditoría y Diagnóstico BPM")

# 3. Formulario de Captura de Datos
tabs = st.tabs(["🏗️ Instalaciones", "🧊 Almacenamiento y Productos", "🪳 Control de Plagas", "📸 Evidencias"])

with tabs[0]:
    col1, col2 = st.columns(2)
    with col1:
        ins_1 = st.selectbox("Estado de localización y accesos:", ["Cumple", "Cumple Parcialmente", "No Cumple"])
        ins_2 = st.selectbox("Diseño y construcción (Protección):", ["Cumple", "Cumple Parcialmente", "No Cumple"])
    with col2:
        obs_ins = st.text_area("Hallazgos específicos en infraestructura")

with tabs[1]:
    c1, c2 = st.columns(2)
    with c1:
        st.subheader("Control de Productos")
        prod_cad = st.radio("¿Se evidencian productos con fecha de caducidad vencida?", ["No", "Sí"])
        prod_rot = st.radio("¿El rotulado cumple con la normativa vigente?", ["Sí", "No"])
    with c2:
        st.subheader("Almacenamiento")
        alm_sep = st.radio("¿Hay separación adecuada (evita contaminación cruzada)?", ["Sí", "No"])
        obs_alm = st.text_area("Detalles de productos y almacenamiento")

with tabs[2]:
    p1 = st.checkbox("Programa de Control de Plagas documentado")
    p2 = st.checkbox("Registros de aplicación de productos químicos/biológicos")
    obs_pest = st.text_area("Observaciones del manejo integral de plagas")

with tabs[3]:
    fotos = st.file_uploader("Cargar registros fotográficos", type=["jpg", "png"], accept_multiple_files=True)

st.divider()

# 4. Lógica de Generación de Informe Diagnóstico
if st.button("🚀 GENERAR INFORME TÉCNICO DIAGNÓSTICO"):
    if not cliente:
        st.warning("⚠️ Identifique el establecimiento antes de generar el informe.")
    else:
        st.balloons()
        
        # Inicio del Reporte Visual
        st.markdown("---")
        st.markdown(f"## 📋 INFORME DE DIAGNÓSTICO TÉCNICO: {cliente.upper()}")
        
        with st.container():
            st.markdown(f"**Fecha:** {fecha} | **Auditor:** {auditor}")
            
            # Bloque de Análisis de Cumplimiento Normativo
            st.markdown("### 1. Fundamentos de la Normativa")
            st.write("El presente diagnóstico se emite bajo los criterios de la **Resolución 2674 de 2013**, la cual establece los requisitos sanitarios para el funcionamiento de establecimientos de alimentos en Colombia.")

            # Bloque de Hallazgos y Análisis Detallado
            col_a, col_b = st.columns(2)
            
            with col_a:
                st.markdown("#### 🔍 Análisis de Almacenamiento")
                if prod_cad == "Sí":
                    st.error("**ALERTA CRÍTICA:** Se detectaron productos con fechas de caducidad vencidas. Incumplimiento directo del Art. 16.")
                else:
                    st.success("Gestión de inventarios adecuada en términos de vigencia.")
                
                if alm_sep == "No":
                    st.warning("**HALLAZGO:** Riesgo de contaminación cruzada por almacenamiento inadecuado.")

            with col_b:
                st.markdown("#### 🔬 Estado de Instalaciones")
                if ins_1 == "No Cumple" or ins_2 == "No Cumple":
                    st.error("Infraestructura deficiente: No garantiza la protección contra factores externos.")
                else:
                    st.success("Las instalaciones cumplen con los estándares básicos de diseño sanitario.")

            # Bloque de Sugerencias y Plan de Acción
            st.markdown("### 💡 Sugerencias y Plan de Mejora")
            sugerencias = []
            if prod_cad == "Sí":
                sugerencias.append("- Implementar sistema PEPS (Primero en Entrar, Primero en Salir) de manera rigurosa.")
            if alm_sep == "No":
                sugerencias.append("- Reorganizar estanterías manteniendo distancia mínima de 60cm entre grupos de alimentos distintos.")
            if not p1 or not p2:
                sugerencias.append("- Actualizar el manual de MIP (Manejo Integral de Plagas) con énfasis en métodos no contaminantes (Sello Zodion).")
            
            if sugerencias:
                for s in sugerencias:
                    st.write(s)
            else:
                st.write("Mantener los estándares actuales y realizar seguimiento trimestral.")

            # Generación de archivo descargable (Resumen Ejecutivo)
            resumen_texto = f"INFORME ZODION - {cliente}\nFECHA: {fecha}\nDIAGNÓSTICO: Basado en Res. 2674/2013\n\nSugerencias:\n" + "\n".join(sugerencias)
            st.download_button("📥 Descargar Reporte en Texto", resumen_texto, file_name=f"Informe_{cliente}.txt")





