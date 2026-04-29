import streamlit as st
from datetime import datetime
from io import BytesIO

# PDF
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet

# =====================================
# CONFIGURACIÓN
# =====================================
st.set_page_config(page_title="Zodion - Auditoría Pro", page_icon="🛡️", layout="wide")

st.markdown("""
<style>
.stDownloadButton { text-align: center; margin-top: 20px; }
.stDownloadButton button {
    background-color: #28a745 !important;
    color: white !important;
    width: 100% !important;
    height: 4em !important;
    font-size: 1.1em !important;
    border-radius: 10px !important;
}
.report-frame {
    background-color: #ffffff;
    padding: 40px;
    border: 2px solid #003366;
    border-radius: 10px;
    font-family: 'Courier New', monospace;
}
</style>
""", unsafe_allow_html=True)

st.title("🛡️ Sistema de Diagnóstico Técnico ZODION")

# =====================================
# SIDEBAR
# =====================================
with st.sidebar:
    st.header("📋 Identificación")
    cliente = st.text_input("Establecimiento", value="JAVERIANO")
    fecha = st.date_input("Fecha de Inspección", datetime.now())
    auditor = st.text_input("Auditor Responsable", value="CEO Zodion")

# =====================================
# TABS
# =====================================
tab1, tab2, tab3 = st.tabs(["🏗️ Infraestructura/Equipos", "📦 Alimentos", "🪳 Control MIP"])

with tab1:
    infra_res = st.selectbox("Infraestructura (Art. 6):", ["Cumple", "Cumple Parcialmente", "No Cumple"])
    equ_res = st.selectbox("Equipos (Art. 10):", ["Cumple", "No Cumple"])
    infra_det = st.text_area("Análisis Instalaciones:", "Diseño sanitario adecuado.")

with tab2:
    vencidos = st.radio("¿Productos vencidos?", ["No", "Sí"])
    empaques = st.radio("¿Empaques conformes?", ["Sí", "No"])
    prod_det = st.text_area("Análisis Detallado:", "Condiciones adecuadas.")

with tab3:
    mip_doc = st.checkbox("Programa MIP Documentado")
    mip_det = st.text_area("Observaciones MIP:", "Sin actividad detectable.")

# =====================================
# FUNCIÓN PDF
# =====================================
def generar_pdf(cliente, fecha, auditor, diagnostico, riesgo, prod_det, mip_doc, mip_det, recomendaciones):
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter)
    styles = getSampleStyleSheet()

    contenido = []

    # LOGO
    try:
        logo = Image("logo_zodion.png", width=120, height=60)
        contenido.append(logo)
    except:
        pass

    contenido.append(Spacer(1, 10))

    contenido.append(Paragraph("<b>INFORME TÉCNICO PROFESIONAL</b>", styles["Title"]))
    contenido.append(Spacer(1, 12))

    contenido.append(Paragraph(f"""
    <b>Cliente:</b> {cliente}<br/>
    <b>Fecha:</b> {fecha}<br/>
    <b>Auditor:</b> {auditor}<br/>
    <b>Ubicación:</b> Pasto - Nariño - Colombia<br/>
    <b>Normativa:</b> Resolución 2674 de 2013
    """, styles["Normal"]))

    contenido.append(Spacer(1, 12))

    contenido.append(Paragraph("<b>1. DIAGNÓSTICO SANITARIO</b>", styles["Heading2"]))
    contenido.append(Paragraph(diagnostico, styles["Normal"]))
    contenido.append(Paragraph(f"<b>Nivel de Riesgo:</b> {riesgo}", styles["Normal"]))

    contenido.append(Spacer(1, 12))

    contenido.append(Paragraph("<b>2. ANÁLISIS DETALLADO</b>", styles["Heading2"]))
    contenido.append(Paragraph(prod_det, styles["Normal"]))

    contenido.append(Spacer(1, 12))

    contenido.append(Paragraph("<b>3. MANEJO INTEGRAL DE PLAGAS</b>", styles["Heading2"]))
    contenido.append(Paragraph(f"Estado: {'Implementado' if mip_doc else 'No implementado'}", styles["Normal"]))
    contenido.append(Paragraph(mip_det, styles["Normal"]))

    contenido.append(Spacer(1, 12))

    contenido.append(Paragraph("<b>4. PLAN DE MEJORA</b>", styles["Heading2"]))
    contenido.append(Paragraph(recomendaciones.replace("\n", "<br/>"), styles["Normal"]))

    contenido.append(Spacer(1, 20))

    contenido.append(Paragraph("""
    <b>ZODION SERVICIOS AMBIENTALES COLOMBIA</b><br/>
    Manejo Integral Ambiental (MIA)<br/>
    Modalidad: Freelance & Outsourcing Ambiental
    """, styles["Normal"]))

    doc.build(contenido)
    pdf = buffer.getvalue()
    buffer.close()
    return pdf

# =====================================
# PROCESAMIENTO
# =====================================
st.divider()

if st.button("🚀 PROCESAR ANÁLISIS FINAL"):
    if not cliente:
        st.error("Ingrese el establecimiento.")
    else:
        st.success("✅ Análisis realizado con éxito")

        # RIESGO
        riesgo = "BAJO"
        if infra_res == "No Cumple" or vencidos == "Sí":
            riesgo = "ALTO"
        elif infra_res == "Cumple Parcialmente" or empaques == "No":
            riesgo = "MEDIO"

        # DIAGNÓSTICO
        diagnostico = f"""
Nivel de riesgo sanitario {riesgo} conforme a Resolución 2674 de 2013.

Infraestructura: {infra_res}. {infra_det}
Equipos: {equ_res}.
Alimentos: {"Productos vencidos detectados (riesgo crítico)." if vencidos == "Sí" else "Sin vencimientos detectados."}
Empaques: {"No conformes." if empaques == "No" else "Conformes."}
MIP: {"Implementado." if mip_doc else "No documentado."}
"""

        # RECOMENDACIONES
        recomendaciones = ""

        if vencidos == "Sí":
            recomendaciones += "- Aplicar sistema PEPS inmediatamente.\n"
        if infra_res != "Cumple":
            recomendaciones += "- Adecuaciones según Art. 6.\n"
        if empaques == "No":
            recomendaciones += "- Corregir rotulado/empaque.\n"
        if not mip_doc:
            recomendaciones += "- Implementar programa MIP.\n"
        if recomendaciones == "":
            recomendaciones = "- Mantener condiciones actuales.\n"

        # INFORME TXT
        informe_txt = f"""
INFORME ZODION

Cliente: {cliente}
Fecha: {fecha}
Auditor: {auditor}

Diagnóstico:
{diagnostico}

Recomendaciones:
{recomendaciones}
"""

        # MOSTRAR
        st.markdown('<div class="report-frame">', unsafe_allow_html=True)
        st.text(informe_txt)
        st.markdown('</div>', unsafe_allow_html=True)

        # PDF
        pdf_file = generar_pdf(
            cliente, fecha, auditor,
            diagnostico, riesgo,
            prod_det, mip_doc,
            mip_det, recomendaciones
        )

        # DESCARGAS
        st.download_button(
            "📥 Descargar TXT",
            data=informe_txt,
            file_name=f"Informe_{cliente}.txt"
        )

        st.download_button(
            "📄 Descargar PDF Profesional",
            data=pdf_file,
            file_name=f"Informe_{cliente}.pdf",
            mime="application/pdf"
        )



        



