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
        # Usamos flash por su velocidad y compatibilidad con visión
        model = genai.GenerativeModel('gemini-1.5-flash')
    except Exception as e:
        st.error(f"Error al configurar Google AI: {e}")
else:
    st.warning("⚠️ Configuración pendiente: Agrega 'GOOGLE_API_KEY' en los Secrets de Streamlit.")

# Estilo CSS personalizado para el branding de Zodion
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
        margin-bottom: 20px;
    }
    </style>
    """, unsafe_allow_html=True)

st.title("🛡️ Sistema de Diagnóstico Técnico ZODION")
st.caption("CEO de Zodion - Innovación en Saneamiento Ecológico y Ambiental - Pasto, Nariño")

# Inicialización de estados de sesión
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
    st.caption("Juntos lo hacemos posible")

# 3. MÓDULOS DE INSPECCIÓN
tab1, tab2, tab3 = st.tabs(["📸 IA Vision: Análisis", "🔍 Evaluación Normativa", "📝 Reporte Final"])

with tab1:
    st.subheader("1. Análisis Detallado de Evidencias (IA Vision)")
    fotos = st.file_uploader("Subir fotos de inspección (Pan, lácteos, equipos, etc.)", type=["jpg", "png", "jpeg"], accept_multiple_files=True)
    
    analisis_fotos = []
    if fotos:
        for i, foto in enumerate(fotos):
            col_img, col_txt = st.columns([1, 2])
            with col_img:
                st.image(foto, use_container_width=True)
                
                # Botón de análisis con IA corregido
                if st.button(f"🪄 Analizar Evidencia {i+1}", key=f"btn_{i}"):
                    if model:
                        with st.spinner("Zodion AI analizando imagen..."):
                            try:
                                # PROCESAMIENTO DE IMAGEN PARA EVITAR INVALIDARGUMENT
                                img_raw = Image.open(foto)
                                # Convertimos a RGB para eliminar canales alfa (transparencia) que causan error
                                img_rgb = img_raw.convert('RGB')
                                
                                prompt = (
                                    "Actúa como un auditor experto en inocuidad alimentaria bajo la Res. 2674 de Colombia. "
                                    "Analiza esta imagen y describe: 1. Qué objeto o material es. 2. Estado sanitario visible. "
                                    "3. Riesgos asociados (plagas o contaminación). Sé técnico y breve."
                                )
                                
                                # Llamada a la API
                                response = model.generate_content([prompt, img_rgb])
                                st.session_state[f"desc_{i}"] = response.text
                            except Exception as e:
                                st.error(f"Error técnico en el análisis: {str(e)}")
                    else:
                        st.error("IA no disponible. Verifica la API Key en Secrets.")

            with col_txt:
                titulo = st.text_input(f"Título de la Evidencia {i+1}:", value=f"Evidencia {i+1}", key=f"tit_{i}")
                # El área de texto recupera lo que la IA escribió o permite edición manual
                desc_final = st.text_area(f"Análisis Técnico de Evidencia {i+1}:", 
                                         value=st.session_state.get(f"desc_{i}", ""), 
                                         key=f"txt_{i}", height=150)
                analisis_fotos.append(f"{titulo.upper()}:\n{desc_final}")

with tab2:
    st.subheader("2. Evaluación Técnica Normativa")
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### A. SEGREGACIÓN Y DISPOSICIÓN")
        diag_seg = st.selectbox("Diagnóstico Segregación:", ["CONFORME", "CUMPLE PARCIALMENTE", "NO CONFORME"], index=0, key="sel_seg")
        obs_seg = st.text_area("Observaciones Segregación:", placeholder="Describa hallazgos sobre contaminación cruzada...", key="obs_seg")

        st.markdown("### B. TRAZABILIDAD Y CADUCIDAD")
        diag_tra = st.selectbox("Diagnóstico Trazabilidad:", ["CONFORME", "CUMPLE PARCIALMENTE", "NO CONFORME"], index=0, key="sel_tra")
        obs_tra = st.text_area("Observaciones Trazabilidad:", placeholder="Describa hallazgos sobre rotulado y fechas...", key="obs_tra")

    with col2:
        st.markdown("### C. EQUIPOS Y UTENSILIOS")
        diag_equ = st.selectbox("Diagnóstico Equipos:", ["CONFORME", "CUMPLE PARCIALMENTE", "NO CONFORME"], index=0, key="sel_equ")
        obs_equ = st.text_area("Observaciones Equipos:", placeholder="Describa hallazgos sobre limpieza y mantenimiento...", key="obs_equ")

        st.markdown("### D. MANEJO INTEGRAL DE PLAGAS")
        riesgo_mip = st.select_slider("Nivel de Riesgo MIP:", options=["BAJO", "MODERADO", "ALTO", "CRÍTICO"], value="BAJO", key="slide_mip")

with tab3:
    st.subheader("3. Diagnóstico Final y Recomendaciones")
    eval_mip = st.text_area("Evaluación General MIP:", placeholder="Análisis de focos, refugios o indicios de vectores...", key="final_mip")
    plan_accion = st.text_area("Recomendaciones y Plan de Acción:", 
                               value="- Reorganización inmediata de almacenamiento por naturaleza.\n- Refuerzo en el sistema de rotulado interno.\n- Mantenimiento preventivo de juntas y superficies de contacto.",
                               height=150, key="plan")

# 4. PROCESAMIENTO Y GENERACIÓN DEL INFORME
st.divider()
if st.button("🚀 GENERAR INFORME TÉCNICO COMPLETO"):
    txt_evidencias = "\n\n".join(analisis_fotos) if analisis_fotos else "Sin evidencias registradas."
    
    informe = (
        "INFORME TÉCNICO DE AUDITORÍA Y DIAGNÓSTICO PROFESIONAL\n"
        "ZODION SERVICIOS AMBIENTALES\n"
        "============================================================\n\n"
        f"ESTABLECIMIENTO: {cliente.upper()}\n"
        f"FECHA: {fecha_auditoria.strftime('%d de %B de %Y')}\n"
        f"AUDITOR: {auditor}\n"
        f"UBICACIÓN: Pasto, Nariño, Colombia\n"
        f"NORMATIVA: Resolución 2674 de 2013\n\n"
        "------------------------------------------------------------\n"
        "1. ANÁLISIS DE EVIDENCIAS FOTOGRÁFICAS (IA VISION)\n"
        "------------------------------------------------------------\n"
        f"{txt_evidencias}\n\n"
        "------------------------------------------------------------\n"
        "2. EVALUACIÓN TÉCNICA POR COMPONENTES\n"
        "------------------------------------------------------------\n"
        f"A. SEGREGACIÓN Y DISPOSICIÓN: {diag_seg}\n"
        f"   Análisis: {obs_seg}\n\n"
        f"B. TRAZABILIDAD Y CADUCIDAD: {diag_tra}\n"
        f"   Análisis: {obs_tra}\n\n"
        f"C. EQUIPOS Y UTENSILIOS: {diag_equ}\n"
        f"   Análisis: {obs_equ}\n\n"
        "------------------------------------------------------------\n"
        "3. DIAGNÓSTICO DEL MANEJO INTEGRAL DE PLAGAS (MIP)\n"
        "------------------------------------------------------------\n"
        f"Nivel de Riesgo detectado: {riesgo_mip}.\n"
        f"Evaluación técnica: {eval_mip}\n\n"
        "------------------------------------------------------------\n"
        "4. RECOMENDACIONES Y PLAN DE ACCIÓN\n"
        "------------------------------------------------------------\n"
        f"{plan_accion}\n\n"
        "------------------------------------------------------------\n"
        "JUNTOS LO HACEMOS POSIBLE.\n"
        "ZODION - PASTO, NARIÑO.\n"
        "============================================================"
    )
    st.session_state.informe_final = informe
    st.success("✅ Informe generado correctamente. Revise la vista previa abajo.")

# 5. VISUALIZACIÓN Y DESCARGA
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



