import datetime
import pandas as pd
import sqlalchemy
import streamlit as st

# Configuración de página
st.set_page_config(
    page_title="EXPRESS SAN SILVESTRE - Capital Humano",
    page_icon="🚛",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Estilos CSS
st.markdown(
    """
<style>
    [data-testid="stSidebar"] { background-color: #121929 !important; padding-top: 1rem; }
    [data-testid="stSidebarNav"] { display: none; }
    .sidebar-header { display: flex; align-items: center; gap: 12px; padding: 10px 8px 15px 8px; border-bottom: 1px solid rgba(255, 255, 255, 0.08); margin-bottom: 15px; }
    .logo-box { background-color: #D9232E; color: white; font-weight: 900; font-size: 16px; padding: 8px 10px; border-radius: 8px; }
    .header-text h3 { color: #FFFFFF; font-size: 15px; font-weight: 800; margin: 0; }
    .header-text p { color: #718096; font-size: 11px; margin: 2px 0 0 0; }
    .menu-category { color: #52637A; font-size: 11px; font-weight: 700; text-transform: uppercase; margin-top: 18px; margin-bottom: 8px; padding-left: 10px; }
    div[data-testid="stSidebar"] div.stButton > button { width: 100%; background-color: transparent; color: #A0AEC0; border: none; text-align: left; padding: 10px 14px; border-radius: 8px; font-size: 14px; }
    div[data-testid="stSidebar"] div.stButton > button:hover { background-color: #1A243B; color: #FFFFFF; }
    .badge-red { background-color: #E53E3E; color: white; font-size: 11px; font-weight: 700; padding: 2px 7px; border-radius: 12px; }
    .last-update-badge { background-color: #1E293B; color: #38BDF8; border: 1px solid #0284C7; font-size: 12px; font-weight: 600; padding: 6px 12px; border-radius: 20px; }
    .kpi-card { background-color: #FFFFFF; border-radius: 10px; padding: 15px; border: 1px solid #E2E8F0; box-shadow: 0 2px 4px rgba(0,0,0,0.05); text-align: center; }
    .kpi-title { font-size: 12px; font-weight: 700; color: #1E293B; text-transform: uppercase; margin-bottom: 8px; }
    .kpi-value { font-size: 24px; font-weight: 800; color: #0F172A; }
    .kpi-sub { font-size: 12px; color: #64748B; margin-top: 4px; }
</style>
""",
    unsafe_allow_html=True,
)


# Conexión directa a Azure SQL sin caché extendido
@st.cache_data(ttl=5)
def cargar_datos_sql(query):
  try:
    server = st.secrets["sql_server"]["server"]
    database = st.secrets["sql_server"]["database"]
    username = st.secrets["sql_server"]["username"]
    password = st.secrets["sql_server"]["password"]

    conn_str = f"mssql+pyodbc://{username}:{password}@{server}/{database}?driver=ODBC+Driver+17+for+SQL+Server"
    engine = sqlalchemy.create_engine(conn_str)
    return pd.read_sql(query, engine)
  except Exception as e:
    st.error(f"Error de lectura SQL: {e}")
    return pd.DataFrame()


if "pagina_actual" not in st.session_state:
  st.session_state["pagina_actual"] = "Dashboard"


def cambiar_pagina(nombre_pagina):
  st.session_state["pagina_actual"] = nombre_pagina


# Sidebar
with st.sidebar:
  st.markdown(
      """<div class="sidebar-header"><div class="logo-box">ESS</div><div class="header-text"><h3>EXPRESS SAN SILVESTRE</h3><p>Capital Humano</p></div></div>""",
      unsafe_allow_html=True,
  )
  st.markdown(
      '<div class="menu-category">PRINCIPAL</div>', unsafe_allow_html=True
  )
  if st.button("🗂️  Dashboard", key="btn_dash"):
    cambiar_pagina("Dashboard")
  if st.button("🚚  Operadores", key="btn_ops"):
    cambiar_pagina("Operadores")

# Contenido Dashboard
pagina = st.session_state["pagina_actual"]

if pagina == "Dashboard":
  df_sync = cargar_datos_sql("SELECT TOP 1 * FROM UltimaActualizacion")
  fecha_sync_texto = (
      df_sync.iloc[0, 0].strftime("%d/%m/%Y %H:%M hrs")
      if not df_sync.empty
      else "En línea"
  )

  head_col1, head_col2 = st.columns([0.7, 0.3])
  with head_col1:
    st.markdown("## 📊 Indicadores Capital Humano (Datos Reales SQL)")
    st.markdown(
        f'<div class="last-update-badge">🟢 Sync Azure: <b>{fecha_sync_texto}</b></div>',
        unsafe_allow_html=True,
    )
  with head_col2:
    if st.button("🔄 Refrescar SQL", use_container_width=True):
      st.cache_data.clear()
      st.rerun()

  st.divider()

  # Consultas Reales de Conteo
  df_operadores = cargar_datos_sql("SELECT * FROM Operadores")
  df_unidades = cargar_datos_sql("SELECT * FROM Unidades")

  total_unidades = len(df_unidades) if not df_unidades.empty else 0
  total_operadores = len(df_operadores) if not df_operadores.empty else 0
  plantilla_autorizada = 134
  cumplimiento = (
      f"{(total_operadores / plantilla_autorizada) * 100:.2f}%"
      if plantilla_autorizada > 0
      else "0%"
  )

  # Conteo por puestos si existe la columna 'Puesto'
  conteo_puestos = {}
  if not df_operadores.empty and "Puesto" in df_operadores.columns:
    conteo_puestos = df_operadores["Puesto"].value_counts().to_dict()

  sencillo_cnt = conteo_puestos.get("OPERADOR SENCILLO", 0) + conteo_puestos.get(
      "OPERADOR REGIO", 0
  )
  full_cnt = conteo_puestos.get("OPERADOR FULL", 0)
  patio_cnt = conteo_puestos.get("OPERADOR PATIO", 0)
  postura_cnt = conteo_puestos.get("OPERADOR POSTURA", 0)
  incapacitado_cnt = conteo_puestos.get("INCAPACITADO", 0)

  # KPI Fila 1
  c1, c2, c3, c4, c5 = st.columns(5)
  c1.markdown(
      f'<div class="kpi-card"><div class="kpi-title">Unidades</div><div class="kpi-value">🚜 {total_unidades}</div></div>',
      unsafe_allow_html=True,
  )
  c2.markdown(
      f'<div class="kpi-card"><div class="kpi-title">Plantilla Activa</div><div class="kpi-value" style="color:#D9232E;">{cumplimiento}</div><div class="kpi-sub">Real: {total_operadores} | Auth: {plantilla_autorizada}</div></div>',
      unsafe_allow_html=True,
  )
  c3.markdown(
      '<div class="kpi-card"><div class="kpi-title">Vacantes</div><div class="kpi-value" style="color:#2563EB;">'
      + str(max(0, plantilla_autorizada - total_operadores))
      + "</div></div>",
      unsafe_allow_html=True,
  )
  c4.markdown(
      '<div class="kpi-card"><div class="kpi-title">Rotación</div><div class="kpi-value">0.00%</div></div>',
      unsafe_allow_html=True,
  )
  c5.markdown(
      '<div class="kpi-card"><div class="kpi-title">Contratación</div><div class="kpi-value">--</div></div>',
      unsafe_allow_html=True,
  )

  st.write("")
  st.markdown("##### 🚚 Distribución Real por Puesto (Tabla Operadores)")

  # KPI Fila 2 (Valores Reales del SQL)
  p1, p2, p3, p4, p5 = st.columns(5)
  p1.markdown(
      f'<div class="kpi-card"><div class="kpi-title">Sencillo + Regio</div><div class="kpi-value">{sencillo_cnt}</div></div>',
      unsafe_allow_html=True,
  )
  p2.markdown(
      f'<div class="kpi-card"><div class="kpi-title">Operador Full</div><div class="kpi-value">{full_cnt}</div></div>',
      unsafe_allow_html=True,
  )
  p3.markdown(
      f'<div class="kpi-card"><div class="kpi-title">Operador Patio</div><div class="kpi-value">{patio_cnt}</div></div>',
      unsafe_allow_html=True,
  )
  p4.markdown(
      f'<div class="kpi-card"><div class="kpi-title">Operador Postura</div><div class="kpi-value">{postura_cnt}</div></div>',
      unsafe_allow_html=True,
  )
  p5.markdown(
      f'<div class="kpi-card"><div class="kpi-title">Incapacitados</div><div class="kpi-value">{incapacitado_cnt}</div></div>',
      unsafe_allow_html=True,
  )

  st.divider()

  # Vista previa de datos cargados de SQL
  st.markdown("##### 🔍 Vista Previa de Tabla 'Operadores' desde Azure")
  st.dataframe(df_operadores.head(10), use_container_width=True)
