import streamlit as st
import google.generativeai as genai
from PIL import Image
from datetime import datetime
from fpdf import FPDF
import io

# 1. CONFIGURACIÓN DE IDENTIDAD Y ESTÉTICA ZODION
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

# --- INICIALIZACIÓN DE VARIABLES GLOBALES ---
if 'analisis_profesional' not in st.session_state:
    st.session_state.analisis_profesional = {}

cliente = "Colegio Javeriano / La Canasta"
auditor = "CEO de Zodion"
fecha = datetime.now()
fotos = []

# --- FUNCIÓN PARA GENERAR PDF PROFESIONAL ---
def crear_pdf(cliente_nom, auditor_nom, fecha_insp, hallazgos, conclusion_txt):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_auto_page_break(auto=True, margin=15)
    
    pdf.set_fill_color(0, 51, 102) 
    pdf.rect(0, 0, 210, 40, 'F')
    pdf.set_text_color(255, 255, 255)
    pdf.set_font("Arial", 'B', 16)
    pdf.cell(0, 10, "INFORME TÉCNICO DE AUDITORÍA - ZODION", ln=True, align='C')
    pdf.set_font("Arial", 'I', 10)
    pdf.cell(0, 10, "Saneamiento Ambiental e Inocuidad | Res. 2674 de 2013", ln=True, align='C')
    pdf.ln(15)
    
    pdf.set_text_color(0, 0, 0)
    pdf.set_font("Arial", 'B', 11)
    pdf.cell(0, 7, f"CLIENTE: {cliente_nom.upper()}", ln=True)
    pdf.cell(0, 7, f"AUDITOR: {auditor_nom.upper()}", ln=True)
    pdf.cell(0, 7, f"FECHA: {fecha_insp}", ln=True)
    pdf.cell(0, 7, "UBICACIÓN: Pasto, Nariño, Colombia", ln=True)
    pdf.ln(5)
    pdf.line(10, pdf.get_y(), 200, pdf.get_y())
    pdf.ln(5)
    
    pdf.set_font("Arial", 'B', 12)
    pdf.cell(0, 10, "RESUMEN DE HALLAZGOS TÉCNICOS:", ln=True)
    
    for titulo, contenido in hallazgos.items():
        pdf.set_font("Arial", 'B', 10)
        pdf.cell(0, 7, f">>> {titulo.upper()}", ln=True)
        pdf.set_font("Arial", size=10)
        pdf.multi_cell(0, 5, txt=contenido.encode('latin-1', 'replace').decode('latin-1'))
        pdf.ln(3)
        pdf.line(15, pdf.get_y(), 100, pdf.get_y())
        pdf.ln(3)

    pdf.ln(5)
    pdf.set_font("Arial", 'B', 11)
    pdf.cell(0, 7, "CONCLUSIONES Y RECOMENDACIONES:", ln=True)
    pdf.set_font("Arial", size=10)
    pdf.multi_cell(0, 5, txt=conclusion_txt.encode('latin-1', 'replace').decode('latin-1'))
    
    pdf.ln(20)
    pdf.set_font("Arial", 'I', 9)
    pdf.set_text_color(128, 128, 128)
    pdf.cell(0, 5, '"Juntos lo hacemos posible"', ln=True, align='C')
    pdf.cell(0, 5, "Zodion - Servicios Ambientales de Élite", ln=True, align='C')
    
    return pdf.output()

# 2. CONEXIÓN DINÁMICA DE IA (Corrección de Error 404)
model = None
if "GOOGLE_API_KEY" in st.secrets:
    try:
        api_key = st.secrets["GOOGLE_API_KEY"].strip().replace('"', '')
        genai.configure(api_key=api_key)
        
        # Listar modelos disponibles para evitar el error 404
        modelos_disponibles = [m.name for m in genai.list_models() if 'generateContent' in m.supported_generation_methods]
        # Buscar la mejor versión disponible
        target_model = next((m for m in modelos_disponibles if 'gemini-1.5-flash' in m), 
                            next((m for m in modelos_disponibles if 'gemini-pro-vision' in m), 
                            modelos_disponibles[0] if modelos_disponibles else None))
        
        if target_model:
            model = genai.GenerativeModel(target_model)
            st.sidebar.success(f"🛡️ MOTOR ACTIVO: {target_model.split('/')[-1]}")
    except Exception as e:
        st.sidebar.error(f"Error de conexión: {e}")

# 3. CAPTURA DE PARÁMETROS EN SIDEBAR
with st.sidebar:
    st.header("📋 Parámetros de Auditoría")
    cliente = st.text_input("Cliente/Establecimiento:", value=cliente)
    auditor = st.text_input("Auditor Técnico:", value=auditor)
    fecha = st.date_input("Fecha de Inspección:", fecha)
    st.divider()
    st.info("Basado en Resolución 2674 de 2013")

st.title("🛡️ Sistema de Auditoría Técnica Profesional ZODION")
st.caption("Consultoría en Saneamiento Ambiental e Inocuidad Alimentaria")

# 4. ESTRUCTURA DE PESTAÑAS
tab1, tab2 = st.tabs(["📸 Inspección de Campo", "📄 Generación de Informe"])

with tab1:
    fotos = st.file_uploader("Cargar Evidencias Fotográficas", type=["jpg", "png", "jpeg"], accept_multiple_files=True)
    
    if fotos:
        for i, foto in enumerate(fotos):
            col_img, col_txt = st.columns([1, 2])
            with col_img:
                st.image(foto, use_container_width=True, caption=f"Evidencia {i+1}")
                if st.button(f"🔍 Analizar Evidencia {i+1}", key=f"btn_{i}"):
                    if model:
                        with st.spinner("IA Zodion evaluando..."):
                            try:
                                img = Image.open(foto).convert('RGB')
                                prompt = (
                                    "Analiza bajo la Res. 2674/2013 de Colombia: "
                                    "1. IDENTIFICACIÓN del ítem. "
                                    "2. HALLAZGOS TÉCNICOS. "
                                    "3. EVALUACIÓN DE RIESGO. "
                                    "4. REFERENCIA NORMATIVA."
                                )
                                response = model.generate_content([prompt, img])
                                st.session_state.analisis_profesional[f"foto_{i}"] = response.text
                            except Exception as e:
                                st.error(f"Error en análisis: {e}")
            
            with col_txt:
                st.text_input(f"Título hallazgo {i+1}:", value=f"Evidencia {i+1}", key=f"tit_{i}")
                st.text_area("Diagnóstico:", value=st.session_state.analisis_profesional.get(f"foto_{i}", ""), key=f"txt_{i}", height=180)

with tab2:
    st.subheader("Consolidación del Informe Técnico Profesional")
    conclusion = st.text_area("Conclusiones Generales:", placeholder="Resumen del estado sanitario...")

    dict_hallazgos = {}
    if fotos:
        for i in range(len(fotos)):
            t = st.session_state.get(f"tit_{i}", f"Evidencia {i+1}")
            d = st.session_state.get(f"txt_{i}", "Sin diagnóstico.")
            dict_hallazgos[t] = d

    col_pdf, col_txt = st.columns(2)

    with col_pdf:
        if st.button("📑 GENERAR INFORME PDF"):
            if not dict_hallazgos:
                st.warning("No hay hallazgos para exportar.")
            else:
                try:
                    pdf_bytes = crear_pdf(cliente, auditor, str(fecha), dict_hallazgos, conclusion)
                    st.download_button(
                        label="⬇️ DESCARGAR PDF PROFESIONAL",
                        data=bytes(pdf_bytes),
                        file_name=f"Informe_Zodion_{cliente}_{fecha}.pdf",
                        mime="application/pdf"
                    )
                    st.success("PDF generado con éxito.")
                except Exception as e:
                    st.error(f"Error al construir PDF: {e}")

    with col_txt:
        informe_txt_raw = f"CLIENTE: {cliente}\nAUDITOR: {auditor}\n\n"
        for k, v in dict_hallazgos.items():
            informe_txt_raw += f">>> {k}\n{v}\n\n"
        
        st.download_button(
            label="📥 DESCARGAR COMO TXT",
            data=informe_txt_raw,
            file_name=f"Informe_Zodion_{cliente}.txt",
            mime="text/plain"
        )
        



