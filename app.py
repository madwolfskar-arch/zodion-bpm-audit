import streamlit as st
import google.generativeai as genai
from PIL import Image
from datetime import datetime
import time

# 1. CONFIGURACIÓN DE IDENTIDAD ZODION
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
    </style>
    """, unsafe_allow_html=True)

# 2. SEGURIDAD Y ACCESO
CLAVE_ACCESO = "Zodion2026"

with st.sidebar:
    st.header("🔐 Acceso Zodion")
    codigo = st.text_input("Código de Autorización:", type="password")
    autenticado = (codigo == CLAVE_ACCESO)
    
    if autenticado:
        st.success("Acceso Autorizado")
    elif codigo != "":
        st.error("Código Incorrecto")

    st.divider()
    cliente = st.text_input("Cliente:", value="Colegio Javeriano / La Canasta")
    auditor = st.text_input("Auditor:", value="CEO de Zodion")
    fecha = st.date_input("Fecha:", datetime.now())

# 3. CONEXIÓN OPTIMIZADA (Para evitar Error 404 y 429)
model = None
if autenticado and "GOOGLE_API_KEY" in st.secrets:
    try:
        genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
        # Selección automática del modelo más eficiente
        modelos = [m.name for m in genai.list_models() if 'generateContent' in m.supported_generation_methods]
        target = next((m for m in modelos if '1.5-flash' in m), modelos[0] if modelos else None)
        if target:
            model = genai.GenerativeModel(target)
    except Exception as e:
        st.sidebar.error(f"Error de conexión: {e}")

# 4. INTERFAZ Y LÓGICA DE PERSISTENCIA
st.title("🛡️ Sistema de Auditoría Técnica Profesional ZODION")

if not autenticado:
    st.warning("Ingrese el código en la barra lateral para comenzar.")
else:
    # Inicializar el almacén de análisis si no existe
    if 'analisis_profesional' not in st.session_state:
        st.session_state.analisis_profesional = {}

    tab1, tab2 = st.tabs(["📸 Inspección de Campo", "📄 Informe Final"])

    with tab1:
        fotos = st.file_uploader("Cargar Evidencias", type=["jpg", "png", "jpeg"], accept_multiple_files=True)
        
        if fotos:
            for i, foto in enumerate(fotos):
                # ID ÚNICO: Clave para que la IA no trabaje dos veces por la misma foto
                foto_id = f"{foto.name}_{i}"
                col_img, col_txt = st.columns([1, 2])
                
                with col_img:
                    st.image(foto, use_container_width=True)
                    
                    # BOTÓN CON LÓGICA DE CONTROL DE CUOTA
                    if st.button(f"🔍 Analizar {foto.name}", key=f"btn_{foto_id}"):
                        if model:
                            with st.spinner("IA Zodion evaluando..."):
                                try:
                                    img = Image.open(foto).convert('RGB')
                                    prompt = "Actúa como Auditor Senior Res. 2674/2013. Analiza IDENTIFICACIÓN, HALLAZGOS, RIESGO y NORMATIVA."
                                    response = model.generate_content([prompt, img])
                                    # Guardamos en el estado para que no se pierda al recargar
                                    st.session_state.analisis_profesional[foto_id] = response.text
                                    st.rerun()
                                except Exception as e:
                                    if "429" in str(e):
                                        st.error("⏳ CUOTA ALCANZADA: Google requiere una pausa. Por favor, espera 60 segundos antes de analizar la siguiente imagen.")
                                    else:
                                        st.error(f"Error: {e}")
                
                with col_txt:
                    st.text_input(f"Título:", value=f"Evidencia {i+1}", key=f"tit_{foto_id}")
                    # El área de texto lee directamente del estado guardado
                    st.session_state.analisis_profesional[foto_id] = st.text_area(
                        "Diagnóstico Normativo:", 
                        value=st.session_state.analisis_profesional.get(foto_id, ""), 
                        key=f"txt_{foto_id}", 
                        height=200
                    )

    with tab2:
        st.subheader("Consolidación del Informe")
        conclusion = st.text_area("Conclusiones Generales:", key="conc_final")
        
        informe_txt = f"INFORME ZODION - {cliente.upper()}\nAUDITOR: {auditor}\nFECHA: {fecha}\n"
        informe_txt += "="*40 + "\n"
        
        for i, foto in enumerate(fotos if fotos else []):
            f_id = f"{foto.name}_{i}"
            tit = st.session_state.get(f"tit_{f_id}", f"Evidencia {i+1}")
            diag = st.session_state.analisis_profesional.get(f_id, "Pendiente.")
            informe_txt += f"\n>>> {tit.upper()}:\n{diag}\n"
            informe_txt += "-"*40 + "\n"

        informe_txt += f"\nCONCLUSIÓN:\n{conclusion}\n\n'Juntos lo hacemos posible'"
        st.text_area("Vista Previa:", informe_txt, height=300)
        st.download_button("📥 DESCARGAR INFORME (.TXT)", data=informe_txt, file_name=f"Informe_Zodion_{cliente}.txt")




