import streamlit as st
import pandas as pd
from datetime import datetime
import google.generativeai as genai
from PIL import Image
import io

# 1. CONFIGURACIÓN DE IDENTIDAD ZODION
st.set_page_config(page_title="Zodion - Auditoría Técnica IA", page_icon="🛡️", layout="wide")

# Inicialización segura de la IA con manejo de versión
model = None
status_ia = "🔴 No configurada"

if "GOOGLE_API_KEY" in st.secrets:
    try:
        api_key = st.secrets["GOOGLE_API_KEY"].strip()
        genai.configure(api_key=api_key)
        
        # Intentamos con el nombre estándar. Si falla el 404, Streamlit reportará el error en el botón.
        # Se usa gemini-1.5-flash que es el modelo más compatible actualmente.
        model = genai.GenerativeModel('gemini-1.5-flash')
        status_ia = "🟢 Conectada y Lista"
    except Exception as e:
        status_ia = f"❌ Error de Configuración: {str(e)}"
else:
    status_ia = "⚠️ Falta GOOGLE_API_KEY en Secrets"

# Estética Corporativa Zodion
st.markdown("""
    <style>
    .main { background-color: #f8f9fa; }
    .stDownloadButton button {
        background-color: #003366 !important;
        color: white !important;
        width: 100% !important;
        font-weight: bold !important;
        border-radius: 8px !important;
        height: 3em !important;
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
st.caption("CEO de Zodion - Innovación en Saneamiento Ecológico Profesional")

# 2. BARRA LATERAL
with st.sidebar:
    st.header("📋 Estado del Sistema")
    st.info(f"Estado IA: {status_ia}")
    st.divider()
    cliente = st.text_input("Establecimiento / Cliente", value="JAVERIANO")
    fecha_auditoria = st.date_input("Fecha", datetime.now())
    auditor = st.text_input("Auditor", value="CEO Zodion")
    st.divider()
    if st.button("🔄 Reiniciar App"):
        for key in list(st.session_state.keys()):
            del st.session_state[key]
        st.rerun()

# 3. MÓDULOS DE INSPECCIÓN
tab1, tab2, tab3 = st.tabs(["📸 IA Vision", "🔍 Evaluación Técnica", "📝 Reporte Final"])

with tab1:
    st.subheader("1. Análisis Detallado con IA")
    fotos = st.file_uploader("Subir evidencias fotográficas", type=["jpg", "png", "jpeg"], accept_multiple_files=True)
    
    analisis_fotos = []
    if fotos:
        for i, foto in enumerate(fotos):
            col_img, col_txt = st.columns([1, 2])
            with col_img:
                st.image(foto, use_container_width=True)
                if st.button(f"🪄 Analizar Evidencia {i+1}", key=f"btn_{i}"):
                    if model:
                        with st.spinner("Zodion AI analizando..."):
                            try:
                                # Conversión a RGB para asegurar compatibilidad
                                img = Image.open(foto).convert('RGB')
                                prompt = "Analiza esta imagen para una auditoría de inocuidad alimentaria (Res 2674 Colombia). Identifica el objeto y describe hallazgos sanitarios o riesgos brevemente."
                                
                                # Ejecución del análisis
                                response = model.generate_content(contents=[prompt, img])
                                st.session_state[f"desc_{i}"] = response.text
                            except Exception as e:
                                # Si falla el modelo Flash, intentamos con Pro como respaldo
                                st.error(f"Error técnico: {e}. Reintentando con configuración alterna...")
                                try:
                                    alt_model = genai.GenerativeModel('gemini-pro-vision')
                                    response = alt_model.generate_content([prompt, img])
                                    st.session_state[f"desc_{i}"] = response.text
                                    st.rerun()
                                except:
                                    st.error("No se pudo conectar con los modelos de Google. Verifique su plan en AI Studio.")
            
            with col_txt:
                titulo = st.text_input(f"Título {i+1}:", value=f"Evidencia {i+1}", key=f"tit_{i}")
                desc_ia = st.text_area(f"Análisis Técnico:", value=st.session_state.get(f"desc_{i}", ""), key=f"txt_{i}", height=150)
                analisis_fotos.append(f"{titulo.upper()}:\n{desc_ia}")

# ... (El resto de las pestañas 2 y 3 se mantienen igual para asegurar el informe)
with tab2:
    st.subheader("2. Evaluación Normativa")
    diag_seg = st.selectbox("Segregación:", ["CONFORME", "CUMPLE PARCIALMENTE", "NO CONFORME"])
    obs_seg = st.text_area("Observación Segregación:", key="obs_s")
    riesgo_mip = st.select_slider("Nivel Riesgo MIP:", options=["BAJO", "MODERADO", "ALTO", "CRÍTICO"])

with tab3:
    st.subheader("3. Recomendaciones")
    plan_accion = st.text_area("Plan de Acción:", value="- Reorganización de almacenamiento.\n- Refuerzo de rotulado e higiene.")

st.divider()
if st.button("🚀 GENERAR INFORME TÉCNICO"):
    txt_evidencias = "\n\n".join(analisis_fotos) if analisis_fotos else "Sin evidencias."
    informe = f"INFORME TÉCNICO ZODION - {cliente.upper()}\nFECHA: {fecha_auditoria}\nAUDITOR: {auditor}\n\n1. EVIDENCIAS IA:\n{txt_evidencias}\n\n2. EVALUACIÓN:\nSegregación: {diag_seg}\nRiesgo MIP: {riesgo_mip}\n\n3. PLAN DE ACCIÓN:\n{plan_accion}"
    st.session_state.informe_final = informe
    st.success("✅ Informe generado")

if st.session_state.get('informe_final'):
    st.text_area("Vista Previa:", st.session_state.informe_final, height=250)
    st.download_button("📥 DESCARGAR (.DOC)", st.session_state.informe_final, file_name=f"Zodion_{cliente}.doc")
    

