import streamlit as st
import google.generativeai as genai
from PIL import Image
from datetime import datetime
import io

# 1. CONFIGURACIÓN DE IDENTIDAD ZODION
st.set_page_config(page_title="Zodion - Auditoría Técnica Profesional", page_icon="🛡️", layout="wide")

# Estética Corporativa
st.markdown("""
    <style>
    .main { background-color: #f0f2f6; }
    .stTextArea textarea { font-size: 14px !important; }
    .stBadge { background-color: #003366 !important; }
    .stDownloadButton>button {
        width: 100%;
        background-color: #000000 !important;
        color: #ffffff !important;
        border-radius: 5px;
        font-weight: bold;
    }
    </style>
    """, unsafe_allow_html=True)

# 2. SISTEMA DE SEGURIDAD (CLAVE DE ACCESO)
CLAVE_REQUERIDA = "Zodion2026"

with st.sidebar:
    st.header("🔐 Seguridad")
    password_input = st.text_input("Código de Autorización:", type="password")
    
    if password_input == CLAVE_REQUERIDA:
        st.success("Acceso Autorizado")
        autenticado = True
    elif password_input == "":
        st.info("Ingrese la clave para activar el sistema.")
        autenticado = False
    else:
        st.error("Código Incorrecto")
        autenticado = False

    st.divider()
    st.header("📋 Parámetros de Auditoría")
    cliente = st.text_input("Cliente/Establecimiento:", value="Colegio Javeriano / La Canasta")
    auditor = st.text_input("Auditor Técnico:", value="CEO de Zodion")
    fecha = st.date_input("Fecha de Inspección:", datetime.now())
    st.divider()
    st.info("Basado en Resolución 2674 de 2013 (Colombia)")

# 3. CONEXIÓN DINÁMICA DE IA (Solo si está autenticado)
model = None
if autenticado and "GOOGLE_API_KEY" in st.secrets:
    try:
        api_key = st.secrets["GOOGLE_API_KEY"].strip().replace('"', '')
        genai.configure(api_key=api_key)
        modelos = [m.name for m in genai.list_models() if 'generateContent' in m.supported_generation_methods]
        nombre_modelo = next((m for m in modelos if '1.5-flash' in m), modelos[0] if modelos else None)
        if nombre_modelo:
            model = genai.GenerativeModel(nombre_modelo)
            st.sidebar.success(f"🛡️ MOTOR ACTIVO: {nombre_modelo.split('/')[-1]}")
    except Exception as e:
        st.sidebar.error(f"Error de conexión: {e}")

# 4. INTERFAZ PRINCIPAL
st.title("🛡️ Sistema de Auditoría Técnica Profesional ZODION")
st.caption("Consultoría en Saneamiento Ambiental e Inocuidad Alimentaria | Juntos lo hacemos posible")

if not autenticado:
    st.warning("⚠️ Ingrese el código de acceso en la barra lateral para habilitar las funciones de análisis e informes.")
else:
    # ESTRUCTURA DE DATOS
    if 'analisis_profesional' not in st.session_state:
        st.session_state.analisis_profesional = {}

    tab1, tab2 = st.tabs(["📸 Inspección de Campo", "📄 Generación de Informe (.txt)"])

    with tab1:
        fotos = st.file_uploader("Cargar Evidencias Fotográficas", type=["jpg", "png", "jpeg"], accept_multiple_files=True)
        
        if fotos:
            for i, foto in enumerate(fotos):
                col_img, col_txt = st.columns([1, 2])
                
                with col_img:
                    st.image(foto, use_container_width=True, caption=f"Evidencia {i+1}")
                    if st.button(f"🔍 Ejecutar Análisis Normativo {i+1}", key=f"btn_{i}"):
                        if model:
                            with st.spinner("IA Zodion evaluando bajo normativa técnica..."):
                                try:
                                    img = Image.open(foto).convert('RGB')
                                    prompt = (
                                        "Actúa como un Auditor Senior en Inocuidad Alimentaria bajo la Res. 2674 de 2013. "
                                        "Analiza detalladamente la imagen y entrega: "
                                        "1. IDENTIFICACIÓN: Producto, equipo o área detectada. "
                                        "2. HALLAZGOS TÉCNICOS: Descripción objetiva de la condición (higiene, rotulado, temperatura, infraestructura). "
                                        "3. EVALUACIÓN DE RIESGO: Riesgos de contaminación (física, química o biológica) y atracción de plagas. "
                                        "4. REFERENCIA NORMATIVA: Menciona brevemente qué aspecto de la norma se está afectando. "
                                        "Usa un lenguaje profesional y riguroso."
                                    )
                                    response = model.generate_content([prompt, img])
                                    st.session_state.analisis_profesional[f"foto_{i}"] = response.text
                                except Exception as e:
                                    st.error(f"Fallo en motor de IA: {e}")
                
                with col_txt:
                    st.text_input(f"Identificación del hallazgo {i+1}:", value=f"Evidencia {i+1}", key=f"tit_{i}")
                    st.text_area("Diagnóstico Profesional Detallado:", 
                                 value=st.session_state.analisis_profesional.get(f"foto_{i}", ""), 
                                 key=f"txt_{i}", height=200)

    with tab2:
        st.subheader("Consolidación del Informe Técnico")
        conclusion = st.text_area("Conclusiones Generales de la Auditoría:", 
                                  placeholder="Ej: Cumplimiento del 85%, requiere corrección en puntos críticos...",
                                  key="conclusion_input")
        
        # CONSTRUCCIÓN DEL TEXTO
        informe_txt = f"""==================================================
   INFORME TÉCNICO DE AUDITORÍA - ZODION
   Saneamiento Ambiental e Inocuidad
==================================================

DATOS GENERALES:
--------------------------------------------------
CLIENTE: {cliente.upper()}
AUDITOR: {auditor.upper()}
FECHA: {fecha}
UBICACIÓN: Pasto, Nariño, Colombia
NORMATIVA: Resolución 2674 de 2013

RESUMEN DE HALLAZGOS:
--------------------------------------------------
"""
        if fotos:
            for i in range(len(fotos)):
                t = st.session_state.get(f"tit_{i}", f"Evidencia {i+1}")
                d = st.session_state.analisis_profesional.get(f"foto_{i}", "Análisis pendiente.")
                informe_txt += f"\n>>> {t.upper()}:\n{d}\n"
                informe_txt += "-"*50 + "\n"

        informe_txt += f"""
CONCLUSIONES Y RECOMENDACIONES:
--------------------------------------------------
{conclusion}

--------------------------------------------------
FIN DEL INFORME
"Juntos lo hacemos posible"
Zodion - Servicios Ambientales de Élite
==================================================
"""
        st.text_area("Vista Previa (Formato TXT):", informe_txt, height=350)
        
        st.download_button(
            label="📥 DESCARGAR INFORME (.TXT)",
            data=informe_txt,
            file_name=f"Informe_Zodion_{cliente}_{fecha.strftime('%d_%m_%Y')}.txt",
            mime="text/plain"
        )




