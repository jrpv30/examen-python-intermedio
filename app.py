"""Dashboard interactivo para examen Python Intermedio."""
from pathlib import Path
import pandas as pd
import plotly.express as px
import streamlit as st

st.set_page_config(page_title='Dashboard de Activos TI', page_icon='💻', layout='wide')
st.title('💻 Dashboard de Gestión de Activos TI')
st.caption('Proyecto académico · 600 registros sintéticos · Valores económicos en soles (S/)')

@st.cache_data
def cargar_datos():
    ruta = Path(__file__).parent / 'activos_ti.csv'
    df = pd.read_csv(ruta, encoding='utf-8-sig')
    df['fecha_adquisicion'] = pd.to_datetime(df['fecha_adquisicion'])
    df['costo_soles'] = pd.to_numeric(df['costo_soles'])
    return df

df = cargar_datos()
st.sidebar.header('Filtros')
empresas = st.sidebar.multiselect('Empresa', sorted(df['empresa'].unique()), default=sorted(df['empresa'].unique()))
sedes = st.sidebar.multiselect('Sede', sorted(df['sede'].unique()), default=sorted(df['sede'].unique()))
estados = st.sidebar.multiselect('Estado', sorted(df['estado'].unique()), default=sorted(df['estado'].unique()))
tipos = st.sidebar.multiselect('Tipo de activo', sorted(df['tipo_activo'].unique()), default=sorted(df['tipo_activo'].unique()))
filtrado = df[df['empresa'].isin(empresas) & df['sede'].isin(sedes) & df['estado'].isin(estados) & df['tipo_activo'].isin(tipos)].copy()

if filtrado.empty:
    st.warning('No hay registros para los filtros seleccionados.')
    st.stop()

c1, c2, c3, c4 = st.columns(4)
c1.metric('Total de activos', f'{len(filtrado):,}')
c2.metric('Asignados', f'{(filtrado["estado"] == "Asignado").sum():,}')
c3.metric('Disponibles', f'{(filtrado["estado"] == "Disponible").sum():,}')
c4.metric('Valor total (S/)', f'{filtrado["costo_soles"].sum():,.2f}')

c5, c6, c7 = st.columns(3)
with c5:
    por_estado = filtrado.groupby('estado', as_index=False).size()
    st.plotly_chart(px.pie(por_estado, names='estado', values='size', hole=.45, title='Activos por estado'), use_container_width=True)
with c6:
    por_tipo = filtrado.groupby('tipo_activo', as_index=False).size().sort_values('size',ascending=False)
    st.plotly_chart(px.bar(por_tipo, x='tipo_activo', y='size', title='Activos por tipo', labels={'tipo_activo':'Tipo','size':'Cantidad'}),use_container_width=True)
with c7:
    por_empresa = filtrado.groupby('empresa', as_index=False)['costo_soles'].sum().sort_values('costo_soles',ascending=False)
    st.plotly_chart(px.bar(por_empresa,x='empresa',y='costo_soles',title='Valor de activos por empresa',labels={'costo_soles':'S/','empresa':'Empresa'}),use_container_width=True)

izq, der = st.columns(2)
with izq:
    por_modalidad=filtrado.groupby('modalidad',as_index=False).size()
    st.plotly_chart(px.pie(por_modalidad,names='modalidad',values='size',title='Distribución por modalidad'),use_container_width=True)
with der:
    filtrado['anio'] = filtrado['fecha_adquisicion'].dt.year
    por_anio = filtrado.groupby('anio',as_index=False).size()
    st.plotly_chart(px.line(por_anio,x='anio',y='size',markers=True,title='Activos por año de adquisición',labels={'anio':'Año','size':'Cantidad'}),use_container_width=True)

st.subheader('Detalle de activos')
st.dataframe(filtrado.drop(columns='anio').sort_values('id_activo'),use_container_width=True,hide_index=True)
st.download_button('📥 Descargar datos filtrados (CSV)',filtrado.drop(columns='anio').to_csv(index=False).encode('utf-8-sig'),file_name='activos_ti_filtrados.csv',mime='text/csv')
st.info('Los datos son simulados exclusivamente para fines académicos; no representan información empresarial real.')
