import streamlit as st
import google.generativeai as genai
from PIL import Image
from datetime import datetime
import time

# 1. CONFIGURACIÓN E IDENTIDAD CORPORATIVA
st.set_page_config(page_title="Zodion - Auditoría Profesional", page_icon="🛡️", layout="wide")

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

# 2. SISTEMA DE SEGURIDAD
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

# 3. CONEXIÓN DINÁMICA (Solución al Error 404 y 429)
model = None
if autenticado and "GOOGLE_API_KEY" in st.secrets:
    try:
        genai.configure(api_key=st.secrets["GOOGLE_API_KEY"].strip().replace('"', ''))
        
        # LISTAR Y SELECCIONAR MODELO AUTOMÁTICAMENTE
        modelos_disponibles = [m.name for m in genai.list_models() if 'generateContent' in m.supported_generation_methods]
        
        # Prioridad: 1.5-flash (estable), luego cualquier otro flash, luego el primero disponible
        seleccion = next((m for m in modelos_disponibles if '1.5-flash' in m), 
                         next((m for m in modelos_disponibles if 'flash' in m), 
                         modelos_disponibles[0] if modelos_disponibles else None))
        
        if seleccion:
            model = genai.GenerativeModel(seleccion)
            st.sidebar.caption(f"Motor activo: {seleccion.replace('models/', '')}")
    except Exception as e:
        st.sidebar.error(f"Error de conexión: {e}")

# 4. INTERFAZ DE AUDITORÍA
st.title("🛡️ Sistema de Auditoría Técnica Profesional ZODION")

if autenticado:
    if 'analisis_profesional' not in st.session_state:
        st.session_state.analisis_profesional = {}

    tab1, tab2 = st.tabs(["📸 Evidencias", "📄 Informe Final"])

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
                            with st.spinner("IA Zodion evaluando..."):
                                try:
                                    img = Image.open(foto).convert('RGB')
                                    prompt = ("Actúa como Auditor Senior Res. 2674/2013 de Colombia. "
                                              "Analiza la imagen y entrega: 1. Identificación, 2. Hallazgos técnicos, "
                                              "3. Evaluación de riesgo y 4. Referencia normativa.")
                                    response = model.generate_content([prompt, img])
                                    st.session_state.analisis_profesional[f_id] = response.text
                                    st.rerun()
                                except Exception as e:
                                    if "429" in str(e):
                                        st.error("🛑 CUOTA ALCANZADA: Google solicita una pausa. Espere 60 segundos.")
                                    else:
                                        st.error(f"Error del motor: {e}")
                
                with col_txt:
                    st.text_input(f"Título:", value=f"Evidencia {i+1}", key=f"tit_{f_id}")
                    st.session_state.analisis_profesional[f_id] = st.text_area(
                        "Diagnóstico Normativo:", 
                        value=st.session_state.analisis_profesional.get(f_id, ""), 
                        key=f"txt_{f_id}", 
                        height=200
                    )

    with tab2:
        st.subheader("Consolidación del Informe")
        conclusion = st.text_area("Conclusiones Generales:", key="final_conc")
        
        informe = f"INFORME ZODION - {cliente.upper()}\nAUDITOR: {auditor}\nFECHA: {fecha}\n"
        informe += "="*40 + "\n"
        
        for i, f in enumerate(fotos if fotos else []):
            fid = f"{f.name}_{i}"
            tit_val = st.session_state.get(f'tit_{fid}', f"Evidencia {i+1}")
            diag_val = st.session_state.analisis_profesional.get(fid, "Pendiente.")
            informe += f"\n>>> {tit_val.upper()}:\n{diag_val}\n"
            informe += "-"*40 + "\n"
        
        informe += f"\nCONCLUSIÓN:\n{conclusion}\n\n'Juntos lo hacemos posible'"
        
        st.text_area("Vista previa:", informe, height=300)
        st.download_button("📥 DESCARGAR INFORME (.TXT)", data=informe, file_name=f"Informe_Zodion_{cliente}.txt")
else:
    st.info("Sistema protegido. Por favor ingrese la clave de acceso en la barra lateral.")


