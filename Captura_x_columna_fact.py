import streamlit as st
import pandas as pd
from io import BytesIO
import os

def procesar_archivo(file):
    df = pd.read_excel(file)
    columnas_deseadas = ["nfacturasiigo", "nui", "identificacion", "address", "localidad", "cantidad", "fechaemi", "p_inicial", "p_final", "mes", "ano"]  # Modifica según necesidad
    df_filtrado = df[columnas_deseadas]
    
    # Eliminar guiones de las columnas nfacturasiigo y nui
    df_filtrado["nfacturasiigo"] = df_filtrado["nfacturasiigo"].astype(str).str.replace("-", "", regex=True)
    df_filtrado["nui"] = df_filtrado["nui"].astype(str).str.replace("-", "", regex=True)
    
    # Formatear las fechas a yyyy-mm-dd
    df_filtrado["fechaemi"] = pd.to_datetime(df_filtrado["fechaemi"], errors='coerce').dt.strftime('%Y-%m-%d')
    df_filtrado["p_inicial"] = pd.to_datetime(df_filtrado["p_inicial"], errors='coerce').dt.strftime('%Y-%m-%d')
    df_filtrado["p_final"] = pd.to_datetime(df_filtrado["p_final"], errors='coerce').dt.strftime('%Y-%m-%d')


    # Pasar a mayuscula
    df_filtrado["address"] = df_filtrado["address"].astype(str).upper()
    
    return df_filtrado

def generar_xlsx(df):
    output = BytesIO()
    df.to_excel(output, index=False, engine='openpyxl')
    output.seek(0)
    return output

# Configuración de la página
st.set_page_config(page_title="Captura de datos por columna - Facturación", page_icon="📂", layout="centered")
st.title("📂 Captura de datos por columna - Facturación")

st.markdown("Sube un archivo Excel, extrae columnas específicas y descarga el CSV resultante.")

archivo = st.file_uploader("Cargar archivo Excel", type=["xlsx"])

if archivo is not None:
    df_filtrado = procesar_archivo(archivo)
    st.success("Archivo procesado correctamente.")
    st.dataframe(df_filtrado)  # Muestra la tabla con las columnas seleccionadas
    
    xlsx = generar_xlsx(df_filtrado)
    nombre_salida = os.path.splitext(archivo.name)[0] + ".xlsx"
    st.download_button(label="📥 Descargar Excel", data=xlsx, file_name=nombre_salida, mime="text/xlsx")