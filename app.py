import datetime
import pandas as pd
import sqlalchemy
import streamlit as st

# ---------------------------------------------------------
# CONFIGURACIÓN DE PÁGINA
# ---------------------------------------------------------
st.set_page_config(
    page_title="EXPRESS SAN SILVESTRE - Capital Humano",
    page_icon="🚛",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ---------------------------------------------------------
# ESTILOS CSS REFINADOS Y TARJETAS KPI NATIVAS
# ---------------------------------------------------------
st.markdown(
    """
<style>
    /* Estilos Generales y Sidebar */
    [data-testid="stSidebar"] { background-color: #121929 !important; padding-top: 1rem; }
    [data-testid="stSidebarNav"] { display: none; }
    .sidebar-header { display: flex; align-items: center; gap: 12px; padding: 10px 8px 15px 8px; border-bottom: 1px solid rgba(255, 255, 255, 0.08); margin-bottom: 15px; }
    .logo-box { background-color: #D9232E; color: white; font-weight: 900; font-size: 16px; padding: 8px 10px; border-radius: 8px; }
    .header-text h3 { color: #FFFFFF; font-size: 15px; font-weight: 800; margin: 0; }
    .header-text p { color: #718096; font-size: 11px; margin: 2px 0 0 0; }
    .menu-category { color: #52637A; font-size: 11px; font-weight: 700; text-transform: uppercase; margin-top: 18px; margin-bottom: 8px; padding-left: 10px; }
    div[data-testid="stSidebar"] div.stButton > button { width: 100%; background-color: transparent; color: #A0AEC0; border: none; text-align: left; padding: 10px 14px; border-radius: 8px; font-size: 14px; }
    div[data-testid="stSidebar"] div.stButton > button:hover { background-color: #1A243B; color: #FFFFFF; }
    .last-update-badge { background-color: #1E293B; color: #38BDF8; border: 1px solid #0284C7; font-size: 12px; font-weight: 600; padding: 6px 12px; border-radius: 20px; display: inline-block; }

    /* ESTILO MODERNO PARA TARJETAS KPI CON EFECTO HOVER */
    .kpi-card {
        background: linear-gradient(135deg, #EFF6FF 0%, #E0F2FE 100%);
        border-radius: 18px;
        padding: 18px 20px;
        border: 1px solid #DBEAFE;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05), 0 2px 4px -1px rgba(0, 0, 0, 0.03);
        min-height: 125px; /* Mantiene la misma altura estándar en todas */
        display: flex;
        flex-direction: column;
        justify-content: space-between;
        position: relative;
        overflow: hidden;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        cursor: pointer;
    }

    /* Efecto Hover: Elevar tarjeta y proyectar sombra 3D */
    .kpi-card:hover {
        transform: translateY(-6px);
        box-shadow: 0 12px 20px -3px rgba(37, 99, 235, 0.18), 0 4px 6px -2px rgba(37, 99, 235, 0.08);
        border-color: #93C5FD;
    }

    /* Tipografía interna alineada a la izquierda */
    .kpi-title {
        font-size: 11px;
        font-weight: 800;
        color: #64748B;
        text-transform: uppercase;
        letter-spacing: 0.8px;
        margin-bottom: 4px;
        text-align: left;
    }

    .kpi-value {
        font-size: 28px;
        font-weight: 900;
        color: #1D4ED8;
        line-height: 1.1;
        text-align: left;
    }

    .kpi-sub {
        font-size: 12px;
        font-weight: 600;
        color: #94A3B8;
        margin-top: 6px;
        text-align: left;
    }

    /* Ícono flotante en la esquina superior derecha */
    .kpi-icon-badge {
        position: absolute;
        top: 14px;
        right: 14px;
        background: rgba(219, 234, 254, 0.7);
        width: 40px;
        height: 40px;
        border-radius: 12px;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 20px;
    }
</style>
""",
    unsafe_allow_html=True,
)


# ---------------------------------------------------------
# FUNCIÓN DE CONEXIÓN A AZURE SQL
# ---------------------------------------------------------
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


# ---------------------------------------------------------
# CONTROL DE NAVEGACIÓN
# ---------------------------------------------------------
if "pagina_actual" not in st.session_state:
  st.session_state["pagina_actual"] = "Dashboard"


def cambiar_pagina(nombre_pagina):
  st.session_state["pagina_actual"] = nombre_pagina


# ---------------------------------------------------------
# SIDEBAR
# ---------------------------------------------------------
with st.sidebar:
  st.markdown(
      """
        <div class="sidebar-header">
            <div class="logo-box">ESS</div>
            <div class="header-text">
                <h3>EXPRESS SAN SILVESTRE</h3>
                <p>Capital Humano</p>
            </div>
        </div>
    """,
      unsafe_allow_html=True,
  )
  st.markdown(
      '<div class="menu-category">PRINCIPAL</div>', unsafe_allow_html=True
  )
  if st.button("🗂️  Dashboard", key="btn_dash"):
    cambiar_pagina("Dashboard")
  if st.button("🚚  Operadores", key="btn_ops"):
    cambiar_pagina("Operadores")


# ---------------------------------------------------------
# VISTA PRINCIPAL: DASHBOARD
# ---------------------------------------------------------
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

  # Carga de datos de Azure SQL
  df_operadores = cargar_datos_sql("SELECT * FROM Operadores")
  df_unidades = cargar_datos_sql("SELECT * FROM Unidades")

  total_unidades = len(df_unidades) if not df_unidades.empty else 0
  total_operadores = len(df_operadores) if not df_operadores.empty else 0
  plantilla_autorizada = 134
  vacantes = max(0, plantilla_autorizada - total_operadores)
  cumplimiento = (
      f"{(total_operadores / plantilla_autorizada) * 100:.2f}%"
      if plantilla_autorizada > 0
      else "0.00%"
  )

  # Conteo dinámico por puesto
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

  # ---------------------------------------------------------
  # FILA 1: TARJETAS PRINCIPALES (ALTURA UNIFORME Y EFECTO HOVER)
  # ---------------------------------------------------------
  col1, col2, col3, col4, col5 = st.columns(5)

  with col1:
    st.markdown(
        f"""
            <div class="kpi-card">
                <div class="kpi-icon-badge">🚜</div>
                <div>
                    <div class="kpi-title">Unidades</div>
                    <div class="kpi-value" style="color: #1D4ED8;">{total_unidades}</div>
                </div>
                <div class="kpi-sub">Registradas en SQL</div>
            </div>
        """,
        unsafe_allow_html=True,
    )

  with col2:
    st.markdown(
        f"""
            <div class="kpi-card">
                <div class="kpi-icon-badge">👥</div>
                <div>
                    <div class="kpi-title">Plantilla Activa</div>
                    <div class="kpi-value" style="color: #DC2626;">{cumplimiento}</div>
                </div>
                <div class="kpi-sub">Real: {total_operadores} | Auth: {plantilla_autorizada}</div>
            </div>
        """,
        unsafe_allow_html=True,
    )

  with col3:
    st.markdown(
        f"""
            <div class="kpi-card">
                <div class="kpi-icon-badge">🎯</div>
                <div>
                    <div class="kpi-title">Vacantes</div>
                    <div class="kpi-value" style="color: #2563EB;">{vacantes}</div>
                </div>
                <div class="kpi-sub">Por contratar</div>
            </div>
        """,
        unsafe_allow_html=True,
    )

  with col4:
    st.markdown(
        """
            <div class="kpi-card">
                <div class="kpi-icon-badge">🔄</div>
                <div>
                    <div class="kpi-title">Rotación</div>
                    <div class="kpi-value" style="color: #059669;">0.00%</div>
                </div>
                <div class="kpi-sub">Mes actual</div>
            </div>
        """,
        unsafe_allow_html=True,
    )

  with col5:
    st.markdown(
        """
            <div class="kpi-card">
                <div class="kpi-icon-badge">📈</div>
                <div>
                    <div class="kpi-title">Contratación</div>
                    <div class="kpi-value" style="color: #4F46E5;">--</div>
                </div>
                <div class="kpi-sub">Tasa del mes</div>
            </div>
        """,
        unsafe_allow_html=True,
    )

  st.write("")
  st.write("")

  # ---------------------------------------------------------
  # FILA 2: DISTRIBUCIÓN POR PUESTO
  # ---------------------------------------------------------
  st.markdown("##### 🚚 Distribución Real por Puesto")

  p1, p2, p3, p4, p5 = st.columns(5)

  with p1:
    st.markdown(
        f"""
            <div class="kpi-card">
                <div class="kpi-icon-badge">🚛</div>
                <div>
                    <div class="kpi-title">Sencillo + Regio</div>
                    <div class="kpi-value" style="color: #1D4ED8;">{sencillo_cnt}</div>
                </div>
                <div class="kpi-sub">Operadores activos</div>
            </div>
        """,
        unsafe_allow_html=True,
    )

  with p2:
    st.markdown(
        f"""
            <div class="kpi-card">
                <div class="kpi-icon-badge">🚛</div>
                <div>
                    <div class="kpi-title">Operador Full</div>
                    <div class="kpi-value" style="color: #1D4ED8;">{full_cnt}</div>
                </div>
                <div class="kpi-sub">Operadores activos</div>
            </div>
        """,
        unsafe_allow_html=True,
    )

  with p3:
    st.markdown(
        f"""
            <div class="kpi-card">
                <div class="kpi-icon-badge">🏗️</div>
                <div>
                    <div class="kpi-title">Operador Patio</div>
                    <div class="kpi-value" style="color: #1D4ED8;">{patio_cnt}</div>
                </div>
                <div class="kpi-sub">Operadores activos</div>
            </div>
        """,
        unsafe_allow_html=True,
    )

  with p4:
    st.markdown(
        f"""
            <div class="kpi-card">
                <div class="kpi-icon-badge">🅿️</div>
                <div>
                    <div class="kpi-title">Operador Postura</div>
                    <div class="kpi-value" style="color: #1D4ED8;">{postura_cnt}</div>
                </div>
                <div class="kpi-sub">Operadores activos</div>
            </div>
        """,
        unsafe_allow_html=True,
    )

  with p5:
    st.markdown(
        f"""
            <div class="kpi-card">
                <div class="kpi-icon-badge">🏥</div>
                <div>
                    <div class="kpi-title">Incapacitados</div>
                    <div class="kpi-value" style="color: #D97706;">{incapacitado_cnt}</div>
                </div>
                <div class="kpi-sub">Estatus médico</div>
            </div>
        """,
        unsafe_allow_html=True,
    )

  st.divider()

  # Vista previa de datos cargados de SQL
  st.markdown("##### 🔍 Vista Previa de Tabla 'Operadores' desde Azure")
  st.dataframe(df_operadores.head(10), use_container_width=True)
