import streamlit as st
import google.generativeai as genai
from PIL import Image
from datetime import datetime
import io

# 1. CONFIGURACIÓN DE IDENTIDAD Y ESTÉTICA CORPORATIVA
st.set_page_config(page_title="Zodion - Auditoría Técnica Profesional", page_icon="🛡️", layout="wide")

st.markdown("""
    <style>
    .main { background-color: #f0f2f6; }
    .stTextArea textarea { font-size: 14px !important; }
    .stDownloadButton>button {
        width: 100%;
        background-color: #000000 !important;
        color: #ffffff !important;
        border-radius: 5px;
        font-weight: bold;
    }
    .stSidebar { background-color: #ffffff; }
    </style>
    """, unsafe_allow_html=True)

# 2. SISTEMA DE SEGURIDAD Y CONTROL DE ACCESO
# Define aquí la clave de acceso para tu equipo
CLAVE_ACCESO_REQUERIDA = "Zodion2026"

with st.sidebar:
    st.header("🔐 Acceso Restringido")
    codigo_ingresado = st.text_input("Código de Autorización:", type="password", help="Solicite su código al administrador de Zodion.")
    
    if codigo_ingresado == CLAVE_ACCESO_REQUERIDA:
        st.success("✅ Acceso Autorizado")
        autenticado = True
    elif codigo_ingresado == "":
        st.info("Ingrese la clave para habilitar la IA.")
        autenticado = False
    else:
        st.error("❌ Código Incorrecto")
        autenticado = False
    
    st.divider()
    st.header("📋 Parámetros de Auditoría")
    cliente = st.text_input("Cliente/Establecimiento:", value="Colegio Javeriano / La Canasta")
    auditor = st.text_input("Auditor Técnico:", value="CEO de Zodion")
    fecha = st.date_input("Fecha de Inspección:", datetime.now())
    st.info("Cumplimiento Resolución 2674 de 2013")

# 3. LÓGICA DE CONEXIÓN IA (Solo si el código es correcto)
model = None
if autenticado and "GOOGLE_API_KEY" in st.secrets:
    try:
        api_key = st.secrets["GOOGLE_API_KEY"].strip().replace('"', '')
        genai.configure(api_key=api_key)
        # Selección dinámica del modelo para evitar errores 404
        modelos_disponibles = [m.name for m in genai.list_models() if 'generateContent' in m.supported_generation_methods]
        target_model = next((m for m in modelos_disponibles if '1.5-flash' in m), modelos_disponibles[0] if modelos_disponibles else None)
        if target_model:
            model = genai.GenerativeModel(target_model)
            st.sidebar.caption(f"Motor activo: {target_model.split('/')[-1]}")
    except Exception as e:
        st.sidebar.error(f"Error de conexión: {e}")

# 4. INTERFAZ PRINCIPAL
st.title("🛡️ Sistema de Auditoría Técnica Profesional ZODION")
st.caption("Consultoría en Saneamiento Ambiental e Inocuidad Alimentaria | Juntos lo hacemos posible")

if not autenticado:
    st.warning("⚠️ El acceso a las herramientas de análisis de IA y generación de informes está bloqueado. Por favor, ingrese el código de autorización en la barra lateral.")
else:
    # --- ESTRUCTURA DE DATOS PERSISTENTE ---
    if 'analisis_profesional' not in st.session_state:
        st.session_state.analisis_profesional = {}

    tab1, tab2 = st.tabs(["📸 Inspección de Campo", "📄 Generación de Informe (.txt)"])

    with tab1:
        fotos = st.file_uploader("Cargar Evidencias Fotográficas", type=["jpg", "png", "jpeg"], accept_multiple_files=True)
        
        if fotos:
            for i, foto in enumerate(fotos):
                # ID único por foto basado en su nombre para evitar pérdida de datos al recargar
                foto_id = f"{foto.name}_{i}"
                col_img, col_txt = st.columns([1, 2])
                
                with col_img:
                    st.image(foto, use_container_width=True, caption=f"Archivo: {foto.name}")
                    
                    # Botón de análisis individual para controlar el consumo de cuota
                    if st.button(f"🔍 Ejecutar Análisis Normativo {i+1}", key=f"btn_{foto_id}"):
                        if model:
                            with st.spinner("IA Zodion evaluando evidencias..."):
                                try:
                                    img = Image.open(foto).convert('RGB')
                                    prompt = (
                                        "Actúa como un Auditor Senior en Inocuidad Alimentaria bajo la Res. 2674 de 2013 de Colombia. "
                                        "Analiza la imagen y entrega: "
                                        "1. IDENTIFICACIÓN: Área o producto. "
                                        "2. HALLAZGOS TÉCNICOS: Descripción de la condición sanitaria. "
                                        "3. EVALUACIÓN DE RIESGO: Riesgos biológicos, físicos o químicos. "
                                        "4. REFERENCIA NORMATIVA: Artículos afectados de la Res. 2674/2013."
                                    )
                                    response = model.generate_content([prompt, img])
                                    st.session_state.analisis_profesional[foto_id] = response.text
                                    st.rerun()
                                except Exception as e:
                                    if "429" in str(e):
                                        st.error("⏳ Cuota de Google alcanzada. Por favor, espere 60 segundos.")
                                    else:
                                        st.error(f"Error en motor IA: {e}")
                
                with col_txt:
                    # Persistencia automática del título y el diagnóstico editado
                    st.text_input(f"Identificación {i+1}:", value=f"Evidencia {i+1}", key=f"tit_{foto_id}")
                    st.session_state.analisis_profesional[foto_id] = st.text_area(
                        "Diagnóstico Profesional Detallado:", 
                        value=st.session_state.analisis_profesional.get(foto_id, ""), 
                        key=f"txt_{foto_id}", 
                        height=220
                    )

    with tab2:
        st.subheader("Consolidación del Informe Técnico")
        conclusion = st.text_area("Conclusiones Generales de la Auditoría:", 
                                  placeholder="Resumen del cumplimiento y recomendaciones críticas...",
                                  key="conclusion_final")
        
        # CONSTRUCCIÓN DINÁMICA DEL INFORME
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
            for i, foto in enumerate(fotos):
                foto_id = f"{foto.name}_{i}"
                t = st.session_state.get(f"tit_{foto_id}", f"Evidencia {i+1}")
                d = st.session_state.analisis_profesional.get(foto_id, "Análisis pendiente.")
                informe_txt += f"\n>>> {t.upper()}:\n{d}\n"
                informe_txt += "-"*50 + "\n"

        informe_txt += f"""
CONCLUSIONES Y RECOMENDACIONES:
--------------------------------------------------
{st.session_state.get('conclusion_final', '')}

--------------------------------------------------
FIN DEL INFORME
"Juntos lo hacemos posible"
Zodion - Servicios Ambientales de Élite
==================================================
"""

        st.text_area("Vista Previa del Informe:", informe_txt, height=350)
        
        st.download_button(
            label="📥 DESCARGAR INFORME (.TXT)",
            data=informe_txt,
            file_name=f"Informe_Zodion_{cliente}_{fecha.strftime('%d_%m_%Y')}.txt",
            mime="text/plain"
        )


