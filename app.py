import streamlit as st
import google.generativeai as genai
from PIL import Image
from datetime import datetime
import io

# 1. CONFIGURACIÓN DE IDENTIDAD ZODION
st.set_page_config(page_title="Zodion IA - Auditoría Técnica", page_icon="🛡️", layout="wide")

# Estética Profesional
st.markdown("""
    <style>
    .main { background-color: #f8f9fa; }
    .stButton>button {
        background-color: #003366;
        color: white;
        border-radius: 8px;
        width: 100%;
    }
    .stDownloadButton>button {
        background-color: #28a745 !important;
        color: white !important;
        font-weight: bold !important;
    }
    </style>
    """, unsafe_allow_html=True)

# 2. CONEXIÓN DINÁMICA (LA QUE FUNCIONÓ)
model = None
if "GOOGLE_API_KEY" in st.secrets:
    try:
        api_key = st.secrets["GOOGLE_API_KEY"].strip().replace('"', '')
        genai.configure(api_key=api_key)
        
        modelos_disponibles = [m.name for m in genai.list_models() if 'generateContent' in m.supported_generation_methods]
        
        # Selección inteligente de modelo
        nombre_modelo = None
        for target in ['models/gemini-1.5-flash', 'models/gemini-1.5-pro', 'models/gemini-pro-vision']:
            if target in modelos_disponibles:
                nombre_modelo = target
                break
        
        if not nombre_modelo and modelos_disponibles:
            nombre_modelo = modelos_disponibles[0]

        if nombre_modelo:
            model = genai.GenerativeModel(nombre_modelo)
            st.sidebar.success(f"🛡️ ZODION ACTIVO: {nombre_modelo.split('/')[-1]}")
    except Exception as e:
        st.sidebar.error(f"Error de conexión: {e}")
else:
    st.sidebar.warning("⚠️ Configura la API Key en Secrets")

# 3. INTERFAZ Y CAPTURA DE DATOS
st.title("🛡️ Sistema de Auditoría Digital ZODION")
st.caption("Gestión de Inocuidad y Saneamiento Ecológico Profesional - Pasto, Nariño")

if 'analisis_datos' not in st.session_state:
    st.session_state.analisis_datos = {}

with st.sidebar:
    st.header("📋 Información del Servicio")
    cliente = st.text_input("Cliente/Establecimiento:", value="JAVERIANO")
    auditor = st.text_input("Auditor Responsable:", value="CEO de Zodion")
    fecha = st.date_input("Fecha de Auditoría:", datetime.now())
    if st.button("🔄 Nueva Auditoría"):
        st.session_state.analisis_datos = {}
        st.rerun()

# 4. PROCESAMIENTO DE EVIDENCIAS
tab1, tab2 = st.tabs(["📸 Registro Fotográfico e IA", "📝 Informe Final"])

with tab1:
    fotos = st.file_uploader("Cargar evidencias (Máximo 10 fotos)", type=["jpg", "png", "jpeg"], accept_multiple_files=True)
    
    if fotos:
        for i, foto in enumerate(fotos):
            col_img, col_txt = st.columns([1, 2])
            
            with col_img:
                st.image(foto, use_container_width=True)
                if st.button(f"🪄 Analizar Hallazgo {i+1}", key=f"btn_{i}"):
                    if model:
                        with st.spinner("Procesando análisis técnico..."):
                            try:
                                img = Image.open(foto).convert('RGB')
                                prompt = (
                                    "Analiza como experto en inocuidad (Res. 2674 Colombia). "
                                    "1. Identifica el objeto. 2. Describe hallazgos sanitarios. "
                                    "3. Define riesgos de plagas o contaminación. Sé profesional y breve."
                                )
                                response = model.generate_content([prompt, img])
                                st.session_state.analisis_datos[f"foto_{i}"] = response.text
                            except Exception as e:
                                st.error(f"Error en IA: {e}")
            
            with col_txt:
                titulo = st.text_input(f"Título de la Evidencia {i+1}:", value=f"Evidencia {i+1}", key=f"tit_{i}")
                resultado = st.text_area("Resultado del Análisis Técnico:", 
                                         value=st.session_state.analisis_datos.get(f"foto_{i}", ""), 
                                         key=f"txt_{i}", height=150)

with tab2:
    st.subheader("Configuración del Reporte")
    riesgo = st.select_slider("Nivel de Riesgo Observado:", options=["BAJO", "MODERADO", "ALTO", "CRÍTICO"])
    plan_accion = st.text_area("Plan de Acción y Recomendaciones:", 
                               value="- Reforzar protocolos de limpieza.\n- Verificar hermeticidad en puntos críticos.")
    
    # 5. GENERACIÓN DEL ARCHIVO DESCARGABLE
    st.divider()
    
    # Consolidación de texto para el informe
    contenido_informe = f"""INFORME DE AUDITORÍA TÉCNICA - ZODION
--------------------------------------------------
CLIENTE: {cliente.upper()}
FECHA: {fecha}
AUDITOR: {auditor.upper()}
ESTADO: {riesgo} RIESGO
--------------------------------------------------

DETALLE DE HALLAZGOS:
"""
    for i in range(len(fotos) if fotos else 0):
        t = st.session_state.get(f"tit_{i}", f"Evidencia {i+1}")
        d = st.session_state.analisis_datos.get(f"foto_{i}", "Sin análisis realizado.")
        contenido_informe += f"\n> {t.upper()}:\n{d}\n"

    contenido_informe += f"""
--------------------------------------------------
PLAN DE ACCIÓN SUGERIDO:
{plan_accion}

Generado por Zodion IA - Saneamiento Ecológico Profesional.
"Juntos lo hacemos posible"
"""

    st.text_area("Previsualización del Informe:", contenido_informe, height=300)
    
    # Botón de descarga
    st.download_button(
        label="📥 DESCARGAR INFORME (.DOC)",
        data=contenido_informe,
        file_name=f"Informe_Zodion_{cliente}_{fecha}.doc",
        mime="application/msword"
    )




