import calendar
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

    .kpi-card {
        background: linear-gradient(135deg, #EFF6FF 0%, #E0F2FE 100%);
        border-radius: 18px;
        padding: 18px 20px;
        border: 1px solid #DBEAFE;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05), 0 2px 4px -1px rgba(0, 0, 0, 0.03);
        min-height: 125px;
        display: flex;
        flex-direction: column;
        justify-content: space-between;
        position: relative;
        overflow: hidden;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        cursor: pointer;
    }

    .kpi-card:hover {
        transform: translateY(-6px);
        box-shadow: 0 12px 20px -3px rgba(37, 99, 235, 0.18), 0 4px 6px -2px rgba(37, 99, 235, 0.08);
        border-color: #93C5FD;
    }

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
        color: #64748B;
        margin-top: 6px;
        text-align: left;
    }

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

  df_operadores = cargar_datos_sql("SELECT * FROM Operadores")
  df_unidades = cargar_datos_sql("SELECT * FROM Unidades")

  # --- CÁLCULOS FILA 1 ---
  if not df_unidades.empty:
    unidades_activas = (
        len(df_unidades[df_unidades["Estatus"] == "ACTIVA"])
        if "Estatus" in df_unidades.columns
        else len(df_unidades)
    )
  else:
    unidades_activas = 0

  plantilla_autorizada = int(round(unidades_activas * 1.1))
  if plantilla_autorizada == 0:
    plantilla_autorizada = 134

  if not df_operadores.empty:
    condicion_activos = df_operadores["FechaBaja"].isna() & (
        df_operadores["Puesto"] != "NA"
    ) & (df_operadores["Puesto"] != "OPERADOR INCAPACITADO")
    df_activos_sin_na = df_operadores[condicion_activos]
    plantilla_real = df_activos_sin_na["Numero"].nunique()
  else:
    plantilla_real = 0

  cumplimiento_str = (
      f"{(plantilla_real / plantilla_autorizada) * 100:.2f}%"
      if plantilla_autorizada > 0
      else "0.00%"
  )

  hoy = datetime.date.today()
  inicio_mes_act = datetime.date(hoy.year, hoy.month, 1)
  dias_mes_act = calendar.monthrange(hoy.year, hoy.month)[1]
  fin_mes_act = datetime.date(hoy.year, hoy.month, dias_mes_act)

  primer_dia_mes_act = datetime.date(hoy.year, hoy.month, 1)
  fin_mes_ant = primer_dia_mes_act - datetime.timedelta(days=1)
  inicio_mes_ant = datetime.date(fin_mes_ant.year, fin_mes_ant.month, 1)

  tasa_mes_act_str = "--"
  tasa_mes_ant_str = "--"

  if not df_operadores.empty:
    df_operadores["FechaContratacion"] = pd.to_datetime(
        df_operadores["FechaContratacion"], errors="coerce"
    ).dt.date
    df_operadores["FechaBaja"] = pd.to_datetime(
        df_operadores["FechaBaja"], errors="coerce"
    ).dt.date

    altas_act = df_operadores[
        (df_operadores["FechaContratacion"] >= inicio_mes_act)
        & (df_operadores["FechaContratacion"] <= fin_mes_act)
    ]["Numero"].nunique()
    bajas_act = df_operadores[
        (df_operadores["FechaBaja"] >= inicio_mes_act)
        & (df_operadores["FechaBaja"] <= fin_mes_act)
    ]["Numero"].nunique()

    if bajas_act > 0:
      tasa_act = altas_act / bajas_act
      tasa_mes_act_str = f"{tasa_act * 100:.2f}%"

    altas_ant = df_operadores[
        (df_operadores["FechaContratacion"] >= inicio_mes_ant)
        & (df_operadores["FechaContratacion"] <= fin_mes_ant)
    ]["Numero"].nunique()
    bajas_ant = df_operadores[
        (df_operadores["FechaBaja"] >= inicio_mes_ant)
        & (df_operadores["FechaBaja"] <= fin_mes_ant)
    ]["Numero"].nunique()

    if bajas_ant > 0:
      tasa_ant = altas_ant / bajas_ant
      tasa_mes_ant_str = f"{tasa_ant * 100:.2f}%"

  # --- CÁLCULOS FILA 2 ---
  # Preparar df_unidades_copy normalizado
  if not df_unidades.empty:
    df_unidades_copy = df_unidades.copy()
    if "Estatus" in df_unidades_copy.columns:
      df_unidades_copy["Estatus"] = (
          df_unidades_copy["Estatus"].astype(str).str.upper()
      )
    if "TipoUnidad" in df_unidades_copy.columns:
      df_unidades_copy["TipoUnidad"] = (
          df_unidades_copy["TipoUnidad"].astype(str).str.upper()
      )
    if "GrupoUnidad" in df_unidades_copy.columns:
      df_unidades_copy["GrupoUnidad"] = (
          df_unidades_copy["GrupoUnidad"].astype(str).str.upper()
      )
  else:
    df_unidades_copy = pd.DataFrame()

  # 1. SENCILLO + REGIO
  if not df_operadores.empty:
    cond_sencillo_regio = (
        df_operadores["FechaBaja"].isna()
        & df_operadores["Puesto"].isin(["OPERADOR SENCILLO", "OPERADOR REGIO"])
    )
    act_sencillo = df_operadores[cond_sencillo_regio]["Numero"].nunique()
  else:
    act_sencillo = 0

  if not df_unidades_copy.empty:
    cond_unidades_sencillo = (
        (df_unidades_copy["Estatus"] == "ACTIVA")
        & (df_unidades_copy["TipoUnidad"] == "TRACTOCAMION")
        & (df_unidades_copy["GrupoUnidad"].isin(["GENERAL", "REGIONAL"]))
    )
    unidades_sencillo = len(df_unidades_copy[cond_unidades_sencillo])
  else:
    unidades_sencillo = 0

  cump_sencillo_str = (
      f"{(act_sencillo / unidades_sencillo) * 100:.0f}%"
      if unidades_sencillo > 0
      else "0%"
  )

  # 2. OPERADOR FULL
  if not df_operadores.empty:
    cond_full = (df_operadores["FechaBaja"].isna()) & (
        df_operadores["Puesto"] == "OPERADOR FULL"
    )
    act_full = df_operadores[cond_full]["Numero"].nunique()
  else:
    act_full = 0

  if not df_unidades_copy.empty:
    cond_unidades_full = (
        (df_unidades_copy["Estatus"] == "ACTIVA")
        & (df_unidades_copy["TipoUnidad"] == "TRACTOCAMION")
        & (df_unidades_copy["GrupoUnidad"] == "FULL")
    )
    unidades_full = len(df_unidades_copy[cond_unidades_full])
  else:
    unidades_full = 0

  cump_full_str = (
      f"{(act_full / unidades_full) * 100:.0f}%" if unidades_full > 0 else "0%"
  )

  # 3. OPERADOR PATIO
  if not df_operadores.empty:
    cond_patio = (df_operadores["FechaBaja"].isna()) & (
        df_operadores["Puesto"] == "OPERADOR PATIO"
    )
    act_patio = df_operadores[cond_patio]["Numero"].nunique()
  else:
    act_patio = 0

  if not df_unidades_copy.empty:
    cond_unidades_patio = (
        (df_unidades_copy["Estatus"] == "ACTIVA")
        & (df_unidades_copy["TipoUnidad"] == "TRACTOCAMION")
        & (df_unidades_copy["GrupoUnidad"] == "PATIERO")
    )
    unidades_patio = len(df_unidades_copy[cond_unidades_patio])
  else:
    unidades_patio = 0

  cump_patio_str = (
      f"{(act_patio / unidades_patio) * 100:.0f}%" if unidades_patio > 0 else "0%"
  )

  # OTROS PUESTOS
  conteo_puestos = {}
  if not df_operadores.empty and "Puesto" in df_operadores.columns:
    conteo_puestos = df_operadores["Puesto"].value_counts().to_dict()

  postura_cnt = conteo_puestos.get("OPERADOR POSTURA", 0)
  incapacitado_cnt = conteo_puestos.get("OPERADOR INCAPACITADO", 0)

  # ---------------------------------------------------------
  # FILA 1: TARJETAS PRINCIPALES
  # ---------------------------------------------------------
  col1, col2, col3, col4 = st.columns(4)

  with col1:
    st.markdown(
        f"""
            <div class="kpi-card">
                <div class="kpi-icon-badge">🚜</div>
                <div>
                    <div class="kpi-title">Unidades</div>
                    <div class="kpi-value" style="color: #1D4ED8;">{unidades_activas}</div>
                </div>
                <div class="kpi-sub">Unidades Activas</div>
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
                    <div class="kpi-value" style="color: #DC2626;">{cumplimiento_str}</div>
                </div>
                <div class="kpi-sub">Real: <b>{plantilla_real}</b> | Auth: <b>{plantilla_autorizada}</b></div>
            </div>
        """,
        unsafe_allow_html=True,
    )

  with col3:
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

  with col4:
    st.markdown(
        f"""
            <div class="kpi-card">
                <div class="kpi-icon-badge">📈</div>
                <div>
                    <div class="kpi-title">Tasa de Contratación</div>
                    <div class="kpi-value" style="color: #1D4ED8;">{tasa_mes_act_str}</div>
                </div>
                <div class="kpi-sub">Mes Ant: <b>{tasa_mes_ant_str}</b></div>
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
                    <div class="kpi-value" style="color: #1D4ED8;">{act_sencillo}</div>
                </div>
                <div class="kpi-sub">Unidades: <b>{unidades_sencillo}</b> | <span style="color: #059669; font-weight: 800;">{cump_sencillo_str}</span></div>
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
                    <div class="kpi-value" style="color: #1D4ED8;">{act_full}</div>
                </div>
                <div class="kpi-sub">Unidades: <b>{unidades_full}</b> | <span style="color: #059669; font-weight: 800;">{cump_full_str}</span></div>
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
                    <div class="kpi-value" style="color: #1D4ED8;">{act_patio}</div>
                </div>
                <div class="kpi-sub">Unidades: <b>{unidades_patio}</b> | <span style="color: #059669; font-weight: 800;">{cump_patio_str}</span></div>
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

  st.markdown("##### 🔍 Vista Previa de Tabla 'Operadores' desde Azure")
  st.dataframe(df_operadores.head(10), use_container_width=True)
