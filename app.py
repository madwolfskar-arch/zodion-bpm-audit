import streamlit as st
import google.generativeai as genai
from PIL import Image
from datetime import datetime
import time

# 1. CONFIGURACIÓN E IDENTIDAD
st.set_page_config(page_title="Zodion - Auditoría Profesional", page_icon="🛡️", layout="wide")

# 2. SEGURIDAD DE ACCESO
CLAVE_ZODION = "Zodion2026"

with st.sidebar:
    st.header("🔐 Validación")
    pass_input = st.text_input("Código de Acceso:", type="password")
    autenticado = (pass_input == CLAVE_ZODION)
    
    if autenticado:
        st.success("Acceso Autorizado")
    elif pass_input != "":
        st.error("Clave Incorrecta")

    st.divider()
    cliente = st.text_input("Cliente:", value="Colegio Javeriano / La Canasta")
    auditor = st.text_input("Auditor:", value="CEO de Zodion")
    fecha = st.date_input("Fecha:", datetime.now())

# 3. MOTOR DE IA CON SELECCIÓN DE MODELO ESTABLE
model = None
if autenticado and "GOOGLE_API_KEY" in st.secrets:
    try:
        genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
        # Forzamos la búsqueda de la versión 1.5-flash para evitar la cuota de 20 usos de versiones experimentales
        model = genai.GenerativeModel('gemini-1.5-flash')
        st.sidebar.caption("Motor: Gemini 1.5 Flash (Alta Disponibilidad)")
    except Exception as e:
        st.sidebar.error(f"Error de configuración: {e}")

# 4. INTERFAZ DE AUDITORÍA
st.title("🛡️ Sistema de Auditoría Técnica Profesional ZODION")

if autenticado:
    if 'analisis_profesional' not in st.session_state:
        st.session_state.analisis_profesional = {}

    tab1, tab2 = st.tabs(["📸 Evidencias", "📄 Informe"])

    with tab1:
        fotos = st.file_uploader("Cargar Fotos", type=["jpg", "png", "jpeg"], accept_multiple_files=True)
        
        if fotos:
            for i, foto in enumerate(fotos):
                f_id = f"{foto.name}_{i}"
                col_img, col_txt = st.columns([1, 2])
                
                with col_img:
                    st.image(foto, use_container_width=True)
                    if st.button(f"🔍 Analizar {foto.name}", key=f"btn_{f_id}"):
                        if model:
                            with st.spinner("Procesando..."):
                                try:
                                    img = Image.open(foto).convert('RGB')
                                    prompt = "Actúa como Auditor Senior Res. 2674/2013. Entrega Identificación, Hallazgos, Riesgos y Normativa."
                                    response = model.generate_content([prompt, img])
                                    st.session_state.analisis_profesional[f_id] = response.text
                                    st.rerun()
                                except Exception as e:
                                    if "429" in str(e):
                                        st.error("🛑 LÍMITE DE CUOTA: Google solicita una pausa. Por favor, espere 30 segundos antes de procesar la siguiente imagen.")
                                    else:
                                        st.error(f"Aviso del sistema: {e}")
                
                with col_txt:
                    st.text_input(f"Hallazgo:", value=f"Evidencia {i+1}", key=f"tit_{f_id}")
                    st.session_state.analisis_profesional[f_id] = st.text_area(
                        "Resultado del Análisis:", 
                        value=st.session_state.analisis_profesional.get(f_id, ""), 
                        key=f"txt_{f_id}", 
                        height=200
                    )

    with tab2:
        conclusion = st.text_area("Conclusiones:", key="final_conc")
        informe = f"CLIENTE: {cliente}\nAUDITOR: {auditor}\nFECHA: {fecha}\n\n"
        for i, f in enumerate(fotos if fotos else []):
            fid = f"{f.name}_{i}"
            informe += f">>> {st.session_state.get(f'tit_{fid}')}:\n{st.session_state.analisis_profesional.get(fid)}\n\n"
        
        st.download_button("📥 DESCARGAR TXT", data=informe, file_name=f"Zodion_{cliente}.txt")
else:
    st.info("Sistema protegido. Por favor ingrese la clave de acceso.")


