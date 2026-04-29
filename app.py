import streamlit as st
import pandas as pd
from datetime import datetime

# 1. Configuración y Estilo
st.set_page_config(page_title="Zodion - Auditoría Pro", page_icon="🛡️", layout="wide")

# 2. Captura de Datos (Igual a la anterior para mantener consistencia)
with st.sidebar:
    st.header("📋 Datos Zodion")
    cliente = st.text_input("Establecimiento", value="JAVERIANO")
    fecha = st.date_input("Fecha", datetime.now())
    auditor = st.text_input("Auditor", value="CEO Zodion")

tabs = st.tabs(["🏗️ Infraestructura", "📦 Almacenamiento", "📸 Evidencias"])

with tabs[0]:
    col1, col2 = st.columns(2)
    with col1:
        ins_estado = st.selectbox("Estado Infraestructura:", ["Cumple", "No Cumple"])
    with col2:
        obs_infra = st.text_area("Hallazgos Infraestructura", "Sin hallazgos críticos detectados.")

with tabs[1]:
    c1, c2 = st.columns(2)
    with c1:
        vencidos = st.radio("¿Productos vencidos?", ["No", "Sí"])
        detalles_cad = st.text_area("Análisis de Caducidades y Lotes", "Todos los productos verificados cuentan con fechas vigentes según Art. 16.")
    with c2:
        rotulado = st.radio("¿Rotulado conforme?", ["Sí", "No"])
        condiciones = st.text_area("Características de Almacenamiento", "Productos almacenados sobre estibas, respetando distancias.")

# 3. LÓGICA DEL INFORME TÉCNICO DETALLADO
st.divider()
if st.button("🚀 GENERAR INFORME DEL PROCEDIMIENTO Y DIAGNÓSTICO"):
    
    # Redacción del Cuerpo Técnico del Informe
    cuerpo_informe = f"""
    ============================================================
    INFORME DE AUDITORÍA TÉCNICA - ZODION SERVICIOS AMBIENTALES
    ============================================================
    CLIENTE: {cliente}
    FECHA DE INSPECCIÓN: {fecha}
    AUDITOR RESPONSABLE: {auditor}
    
    1. FUNDAMENTOS DE LA NORMATIVA
    El presente diagnóstico se rige bajo la Resolución 2674 de 2013, la cual dicta 
    las disposiciones obligatorias sobre buenas prácticas de manufactura (BPM) 
    para alimentos destinados al consumo humano en Colombia.
    
    2. ANÁLISIS DETALLADO DEL PROCEDIMIENTO
    - INFRAESTRUCTURA: Se evaluaron las condiciones higiénico-sanitarias de 
      edificación (Art. 6). Resultado: {ins_estado}.
      Detalle: {obs_infra}
      
    - ALMACENAMIENTO Y CADUCIDAD (Art. 16 y 27): 
      Se realizó un muestreo aleatorio de productos almacenados para verificar 
      fechas de vencimiento y trazabilidad de lotes.
      ¿Se hallaron productos vencidos?: {vencidos}.
      Análisis técnico: {detalles_cad}
      
    - CARACTERÍSTICAS ORGANOLÉPTICAS Y ROTULADO:
      Se verificó que el rotulado permita la trazabilidad plena del producto.
      Cumplimiento de rotulado: {rotulado}.
      Estado de almacenamiento: {condiciones}

    3. DIAGNÓSTICO Y EMISIÓN DE JUICIO
    Basado en la inspección, el establecimiento presenta un nivel de riesgo bajo/medio.
    {'ALERTA: Se requiere retiro inmediato de productos' if vencidos == 'Sí' else 'ESTADO: Conforme a estándares preventivos.'}

    4. SUGERENCIAS Y PLAN DE MEJORA
    - Mantener rigurosidad en el sistema PEPS.
    - {'Reforzar el sellado de puntos críticos para control de plagas.' if ins_estado == 'No Cumple' else 'Continuar con el monitoreo biológico periódico.'}
    - Formalizar el Programa MIP bajo estándares de control biológico Zodion.
    
    ------------------------------------------------------------
    Firma Digital: Profesional Zodion - Pasto, Nariño
    """

    # Mostrar en pantalla el informe con formato de documento
    st.success("✅ Diagnóstico generado con éxito.")
    st.text_area("VISTA PREVIA DEL INFORME COMPLETO", cuerpo_informe, height=400)
    
    # BOTÓN DE DESCARGA REAL
    st.download_button(
        label="📥 DESCARGAR INFORME TÉCNICO (TXT)",
        data=cuerpo_informe,
        file_name=f"Informe_Zodion_{cliente}_{fecha}.txt",
        mime="text/plain"
    )



