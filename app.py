import streamlit as st
import google.generativeai as genai
from PIL import Image
from datetime import datetime
from fpdf import FPDF # Nueva librería para PDF
import io

# --- FUNCIÓN PARA GENERAR PDF PROFESIONAL ---
def crear_pdf(cliente, auditor, fecha, hallazgos, conclusion):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_auto_page_break(auto=True, margin=15)
    
    # Encabezado Corporativo Zodion
    pdf.set_fill_color(0, 51, 102) # Azul Oscuro
    pdf.rect(0, 0, 210, 40, 'F')
    pdf.set_text_color(255, 255, 255)
    pdf.set_font("Arial", 'B', 16)
    pdf.cell(0, 10, "INFORME TÉCNICO DE AUDITORÍA - ZODION", ln=True, align='C')
    pdf.set_font("Arial", 'I', 10)
    pdf.cell(0, 10, "Saneamiento Ambiental e Inocuidad | Res. 2674 de 2013", ln=True, align='C')
    pdf.ln(15)
    
    # Datos Generales
    pdf.set_text_color(0, 0, 0)
    pdf.set_font("Arial", 'B', 11)
    pdf.cell(0, 7, f"CLIENTE: {cliente.upper()}", ln=True)
    pdf.cell(0, 7, f"AUDITOR: {auditor.upper()}", ln=True)
    pdf.cell(0, 7, f"FECHA: {fecha}", ln=True)
    pdf.cell(0, 7, "UBICACIÓN: Pasto, Nariño, Colombia", ln=True)
    pdf.ln(5)
    pdf.line(10, pdf.get_y(), 200, pdf.get_y())
    pdf.ln(5)
    
    # Hallazgos
    pdf.set_font("Arial", 'B', 12)
    pdf.cell(0, 10, "RESUMEN DE HALLAZGOS TÉCNICOS:", ln=True)
    pdf.set_font("Arial", size=10)
    
    for i, (titulo, contenido) in enumerate(hallazgos.items()):
        pdf.set_font("Arial", 'B', 10)
        pdf.cell(0, 7, f">>> {titulo.upper()}", ln=True)
        pdf.set_font("Arial", size=10)
        # Multi_cell maneja párrafos largos y saltos de línea
        pdf.multi_cell(0, 5, txt=contenido)
        pdf.ln(3)
        pdf.line(15, pdf.get_y(), 100, pdf.get_y())
        pdf.ln(3)

    # Conclusiones
    pdf.ln(5)
    pdf.set_font("Arial", 'B', 11)
    pdf.cell(0, 7, "CONCLUSIONES Y RECOMENDACIONES:", ln=True)
    pdf.set_font("Arial", size=10)
    pdf.multi_cell(0, 5, txt=conclusion)
    
    # Cierre
    pdf.ln(20)
    pdf.set_font("Arial", 'I', 9)
    pdf.set_text_color(128, 128, 128)
    pdf.cell(0, 5, '"Juntos lo hacemos posible"', ln=True, align='C')
    pdf.cell(0, 5, "Zodion - Servicios Ambientales de Élite", ln=True, align='C')
    
    return pdf.output()

# 1. CONFIGURACIÓN DE IDENTIDAD ZODION (Mantenida)
st.set_page_config(page_title="Zodion - Auditoría Técnica Profesional", page_icon="🛡️", layout="wide")

# ... (El código de estética corporativa y conexión IA se mantiene igual) ...

# [OMITIDO POR BREVEDAD: CONEXIÓN IA Y CAPTURA DE FOTOS SEGÚN TU CÓDIGO BASE]

# 4. TAB DE GENERACIÓN DE INFORME
with tab2:
    st.subheader("Consolidación del Informe Técnico Profesional")
    conclusion = st.text_area("Conclusiones Generales de la Auditoría:", 
                             placeholder="Ej: Se observa un cumplimiento del 85%...")

    # Preparar datos para el PDF
    dict_hallazgos = {}
    for i in range(len(fotos) if fotos else 0):
        t = st.session_state.get(f"tit_{i}", f"Evidencia {i+1}")
        d = st.session_state.analisis_profesional.get(f"foto_{i}", "Análisis pendiente.")
        dict_hallazgos[t] = d

    # COLUMNAS PARA BOTONES DE DESCARGA
    col_pdf, col_txt = st.columns(2)

    with col_pdf:
        # BOTÓN GENERADOR DE PDF
        if st.button("📑 PREPARAR INFORME PDF"):
            try:
                pdf_output = crear_pdf(cliente, auditor, fecha, dict_hallazgos, conclusion)
                st.download_button(
                    label="⬇️ DESCARGAR PDF PROFESIONAL",
                    data=bytes(pdf_output),
                    file_name=f"Informe_Zodion_{cliente}_{fecha}.pdf",
                    mime="application/pdf"
                )
                st.success("PDF generado con éxito. Listo para descargar.")
            except Exception as e:
                st.error(f"Error al generar PDF: {e}")

    with col_txt:
        # Tu botón original de TXT (Mantenido)
        informe_txt = f"DATOS GENERALES...\n..." # (Lógica de texto original)
        st.download_button(
            label="📥 DESCARGAR COMO TXT",
            data=informe_txt,
            file_name=f"Informe_Zodion_{cliente}.txt",
            mime="text/plain"
        )





