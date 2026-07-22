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
# ESTILOS CSS REFINADOS Y TARJETAS CUSTOM
# ---------------------------------------------------------
st.markdown(
    """
<style>
    /* Estilos del Sidebar */
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

    /* Tarjetas KPI Principales */
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

    /* Tarjetas de Histórico de Movimientos */
    .history-card {
        background: #FFFFFF;
        border-radius: 16px;
        border: 1px solid #E2E8F0;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05);
        overflow: hidden;
        margin-top: 8px;
    }

    .card-header-altas {
        background: linear-gradient(90deg, #065F46 0%, #047857 100%);
        color: #FFFFFF;
        font-weight: 800;
        font-size: 13px;
        padding: 10px 16px;
        text-transform: uppercase;
        letter-spacing: 0.5px;
        display: flex;
        align-items: center;
        gap: 8px;
    }

    .card-header-bajas {
        background: linear-gradient(90deg, #991B1B 0%, #B91C1C 100%);
        color: #FFFFFF;
        font-weight: 800;
        font-size: 13px;
        padding: 10px 16px;
        text-transform: uppercase;
        letter-spacing: 0.5px;
        display: flex;
        align-items: center;
        gap: 8px;
    }

    .history-grid {
        display: grid;
        grid-template-columns: repeat(4, 1fr);
        padding: 16px 8px;
        text-align: center;
    }

    .history-item {
        border-right: 1px solid #F1F5F9;
        padding: 0 8px;
    }

    .history-item:last-child {
        border-right: none;
    }

    .history-label {
        font-size: 11px;
        font-weight: 700;
        color: #64748B;
        text-transform: uppercase;
        margin-bottom: 6px;
    }

    .history-value-altas {
        font-size: 24px;
        font-weight: 900;
        color: #047857;
        line-height: 1;
    }

    .history-value-bajas {
        font-size: 24px;
        font-weight: 900;
        color: #B91C1C;
        line-height: 1;
    }

    /* Tarjetas de Antigüedad Base */
    .tenure-card {
        background: #F8FAFC;
        border-radius: 12px;
        border: 1px solid #CBD5E1;
        box-shadow: 0 2px 4px rgba(0,0,0,0.04);
        overflow: hidden;
        text-align: center;
    }

    .tenure-header {
        color: #FFFFFF;
        font-weight: 800;
        font-size: 13px;
        padding: 8px 12px;
        letter-spacing: 0.5px;
    }

    .tenure-body {
        padding: 14px 16px;
        display: flex;
        justify-content: space-around;
        align-items: center;
        background-color: #FFFFFF;
    }

    .tenure-count {
        font-size: 22px;
        font-weight: 800;
    }

    .tenure-percentage {
        font-size: 20px;
        font-weight: 900;
    }

    /* Tarjeta de Indicadores Operador */
    .indicator-card {
        background: #FFFFFF;
        border-radius: 16px;
        border: 1px solid #E2E8F0;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05);
        overflow: hidden;
        margin-top: 8px;
    }

    .indicator-header {
        background: linear-gradient(90deg, #1E293B 0%, #334155 100%);
        color: #FFFFFF;
        font-weight: 800;
        font-size: 13px;
        padding: 10px 16px;
        text-transform: uppercase;
        letter-spacing: 0.5px;
        text-align: center;
    }

    .indicator-grid {
        display: grid;
        grid-template-columns: repeat(5, 1fr);
        padding: 16px 8px;
        text-align: center;
    }

    .indicator-item {
        border-right: 1px solid #F1F5F9;
        padding: 0 8px;
    }

    .indicator-item:last-child { border-right: none; }

    .indicator-label {
        font-size: 11px;
        font-weight: 700;
        color: #64748B;
        text-transform: uppercase;
        margin-bottom: 6px;
    }

    .indicator-value {
        font-size: 22px;
        font-weight: 900;
        line-height: 1;
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

  st.markdown(
      '<div class="menu-category">FILTROS</div>', unsafe_allow_html=True
  )

  _hoy_ref = datetime.date.today()
  _anios_disponibles = list(range(_hoy_ref.year - 3, _hoy_ref.year + 1))
  anio_sel = st.selectbox(
      "Año",
      options=_anios_disponibles,
      index=len(_anios_disponibles) - 1,
      key="filtro_anio",
  )

  _meses_nombres = [
      "Actual",
      "Enero",
      "Febrero",
      "Marzo",
      "Abril",
      "Mayo",
      "Junio",
      "Julio",
      "Agosto",
      "Septiembre",
      "Octubre",
      "Noviembre",
      "Diciembre",
  ]
  mes_sel = st.selectbox(
      "Mes", options=_meses_nombres, index=0, key="filtro_mes"
  )

  # fecha_base: mismo patrón que tu medida DAX de Motivos de Baja
  # (si hay un periodo seleccionado se usa ese, si no, TODAY())
  if mes_sel == "Actual":
    fecha_base = datetime.date.today()
  else:
    _mes_num = _meses_nombres.index(mes_sel)  # Enero=1 ... Diciembre=12
    _ultimo_dia = calendar.monthrange(anio_sel, _mes_num)[1]
    fecha_base = datetime.date(anio_sel, _mes_num, _ultimo_dia)


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
  df_operadores_documentos = cargar_datos_sql("SELECT * FROM OperadoresDocumentos")

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

  hoy = fecha_base
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

  # --- PREPARACIÓN DF UNIDADES NORMALIZADO ---
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
          df_unidades_copy["GrupoUnidad"].astype(str).str.upper().str.strip()
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

  # 4. OPERADOR POSTURA
  if not df_operadores.empty:
    cond_postura = (df_operadores["FechaBaja"].isna()) & (
        df_operadores["Puesto"].astype(str).str.upper() == "OPERADOR POSTURA"
    )
    act_postura = df_operadores[cond_postura]["Numero"].nunique()
  else:
    act_postura = 0

  if not df_unidades_copy.empty:
    excluir_grupos = ["A VENTA", "SINIESTRO", "MULA", "", "NONE", "NAN"]
    cond_unidades_postura = (
        (df_unidades_copy["Estatus"] == "ACTIVA")
        & (df_unidades_copy["TipoUnidad"] == "TRACTOCAMION")
        & (~df_unidades_copy["GrupoUnidad"].isin(excluir_grupos))
    )
    unidades_activas_postura = len(df_unidades_copy[cond_unidades_postura])
  else:
    unidades_activas_postura = 0

  meta_postura = unidades_activas_postura / 10.0
  cump_postura_str = (
      f"{(act_postura / meta_postura) * 100:.0f}%" if meta_postura > 0 else "0%"
  )

  # 5. OPERADOR INCAPACITADO
  if not df_operadores.empty:
    cond_incapacitado = (df_operadores["FechaBaja"].isna()) & (
        df_operadores["Puesto"].astype(str).str.upper() == "OPERADOR INCAPACITADO"
    )
    act_incapacitado = df_operadores[cond_incapacitado]["Numero"].nunique()
  else:
    act_incapacitado = 0

  meta_incapacitado = 0
  if meta_incapacitado == 0:
    cump_incapacitado_str = "100%" if act_incapacitado == 0 else "0%"
  else:
    cump_incapacitado_str = (
        f"{(act_incapacitado / meta_incapacitado) * 100:.0f}%"
    )

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
                    <div class="kpi-value" style="color: #1D4ED8;">{act_postura}</div>
                </div>
                <div class="kpi-sub">Meta: <b>{meta_postura:.1f}</b> | <span style="color: #059669; font-weight: 800;">{cump_postura_str}</span></div>
            </div>
        """,
        unsafe_allow_html=True,
    )

  with p5:
    color_cump_incapacitado = (
        "#059669" if act_incapacitado == 0 else "#DC2626"
    )
    st.markdown(
        f"""
            <div class="kpi-card">
                <div class="kpi-icon-badge">🏥</div>
                <div>
                    <div class="kpi-title">Incapacitados</div>
                    <div class="kpi-value" style="color: #D97706;">{act_incapacitado}</div>
                </div>
                <div class="kpi-sub">Meta: <b>{meta_incapacitado}</b> | <span style="color: {color_cump_incapacitado}; font-weight: 800;">{cump_incapacitado_str}</span></div>
            </div>
        """,
        unsafe_allow_html=True,
    )

  st.write("")
  st.write("")

  # ---------------------------------------------------------
  # FILA 3: HISTÓRICO DE MOVIMIENTOS (ALTAS Y BAJAS)
  # ---------------------------------------------------------
  st.markdown("##### 📈 Histórico de Movimientos de Personal")

  datos_altas = {
      "mes_actual": 12,
      "mes_menos_1": 15,
      "mes_menos_2": 10,
      "ano_actual": 27,
  }

  datos_bajas = {
      "mes_actual": 13,
      "mes_menos_1": 13,
      "mes_menos_2": 9,
      "ano_actual": 26,
  }

  col_altas, col_bajas = st.columns(2)

  with col_altas:
    st.markdown(
        f"""
            <div class="history-card">
                <div class="card-header-altas">
                    <span>📈</span> Histórico de Altas
                </div>
                <div class="history-grid">
                    <div class="history-item">
                        <div class="history-label">Altas Del Mes</div>
                        <div class="history-value-altas">{datos_altas['mes_actual']}</div>
                    </div>
                    <div class="history-item">
                        <div class="history-label">Altas -1</div>
                        <div class="history-value-altas">{datos_altas['mes_menos_1']}</div>
                    </div>
                    <div class="history-item">
                        <div class="history-label">Altas -2</div>
                        <div class="history-value-altas">{datos_altas['mes_menos_2']}</div>
                    </div>
                    <div class="history-item">
                        <div class="history-label">Altas Año Act.</div>
                        <div class="history-value-altas">{datos_altas['ano_actual']}</div>
                    </div>
                </div>
            </div>
        """,
        unsafe_allow_html=True,
    )

  with col_bajas:
    st.markdown(
        f"""
            <div class="history-card">
                <div class="card-header-bajas">
                    <span>📉</span> Histórico de Bajas
                </div>
                <div class="history-grid">
                    <div class="history-item">
                        <div class="history-label">Bajas / Mes</div>
                        <div class="history-value-bajas">{datos_bajas['mes_actual']}</div>
                    </div>
                    <div class="history-item">
                        <div class="history-label">Bajas -1</div>
                        <div class="history-value-bajas">{datos_bajas['mes_menos_1']}</div>
                    </div>
                    <div class="history-item">
                        <div class="history-label">Bajas -2</div>
                        <div class="history-value-bajas">{datos_bajas['mes_menos_2']}</div>
                    </div>
                    <div class="history-item">
                        <div class="history-label">Bajas Año Act.</div>
                        <div class="history-value-bajas">{datos_bajas['ano_actual']}</div>
                    </div>
                </div>
            </div>
        """,
        unsafe_allow_html=True,
    )

  st.write("")
  st.write("")

  # ---------------------------------------------------------
  # FILA 4 & 5: CÁLCULOS Y SECCIONES DE ANTIGÜEDAD (ACTIVAS vs BAJAS)
  # ---------------------------------------------------------

  # --- CÁLCULOS ACTIVAS ---
  cnt_0_3, pct_0_3 = 0, "0.00%"
  cnt_4_6, pct_4_6 = 0, "0.00%"
  cnt_7_12, pct_7_12 = 0, "0.00%"
  cnt_1mas, pct_1mas = 0, "0.00%"

  # --- CÁLCULOS BAJAS (ÚLTIMOS 6 MESES) ---
  cnt_baja_0_3, pct_baja_0_3 = 0, "0.00%"
  cnt_baja_4_6, pct_baja_4_6 = 0, "0.00%"
  cnt_baja_7_12, pct_baja_7_12 = 0, "0.00%"
  cnt_baja_1mas, pct_baja_1mas = 0, "0.00%"

  if not df_operadores.empty:
    fecha_hoy = fecha_base

    # 1. ANTIGÜEDAD ACTIVAS
    cond_plantilla = (
        df_operadores["FechaBaja"].isna() & (df_operadores["Puesto"] != "NA")
    )
    total_plantilla_activa = df_operadores[cond_plantilla]["Numero"].nunique()

    # Activas 0 - 3 meses
    f_inc_0_3 = fecha_hoy - datetime.timedelta(days=90)
    cond_0_3 = (
        df_operadores["FechaBaja"].isna()
        & df_operadores["FechaContratacion"].notna()
        & (df_operadores["FechaContratacion"] >= f_inc_0_3)
        & (df_operadores["FechaContratacion"] <= fecha_hoy)
    )
    cnt_0_3 = df_operadores[cond_0_3]["Numero"].nunique()
    if total_plantilla_activa > 0:
      pct_0_3 = f"{(cnt_0_3 / total_plantilla_activa) * 100:.2f}%"

    # Activas 4 - 6 meses
    f_max_4_6 = fecha_hoy - datetime.timedelta(days=91)
    f_min_4_6 = fecha_hoy - datetime.timedelta(days=180)
    cond_4_6 = (
        df_operadores["FechaBaja"].isna()
        & df_operadores["FechaContratacion"].notna()
        & (df_operadores["FechaContratacion"] <= f_max_4_6)
        & (df_operadores["FechaContratacion"] > f_min_4_6)
    )
    cnt_4_6 = df_operadores[cond_4_6]["Numero"].nunique()
    if total_plantilla_activa > 0:
      pct_4_6 = f"{(cnt_4_6 / total_plantilla_activa) * 100:.2f}%"

    # Activas 7 - 12 meses
    f_max_7_12 = fecha_hoy - datetime.timedelta(days=181)
    f_min_7_12 = fecha_hoy - datetime.timedelta(days=365)
    cond_7_12 = (
        df_operadores["FechaBaja"].isna()
        & df_operadores["FechaContratacion"].notna()
        & (df_operadores["FechaContratacion"] <= f_max_7_12)
        & (df_operadores["FechaContratacion"] > f_min_7_12)
    )
    cnt_7_12 = df_operadores[cond_7_12]["Numero"].nunique()
    if total_plantilla_activa > 0:
      pct_7_12 = f"{(cnt_7_12 / total_plantilla_activa) * 100:.2f}%"

    # Activas +1 año
    f_corte_1mas = fecha_hoy - datetime.timedelta(days=365)
    excluir_nums = [1038, 1036, 1035]
    cond_1mas = (
        df_operadores["FechaBaja"].isna()
        & df_operadores["FechaContratacion"].notna()
        & (df_operadores["FechaContratacion"] <= f_corte_1mas)
        & (~df_operadores["Numero"].isin(excluir_nums))
    )
    cnt_1mas = df_operadores[cond_1mas]["Numero"].nunique()
    if total_plantilla_activa > 0:
      pct_1mas = f"{(cnt_1mas / total_plantilla_activa) * 100:.2f}%"

    # 2. ANTIGÜEDAD BAJAS (TRADUCCIÓN EXACTA FÓRMULAS DAX)
    inicio_6m = fecha_hoy - datetime.timedelta(days=180)

    cond_bajas_ult6m = (
        df_operadores["FechaBaja"].notna()
        & (df_operadores["FechaBaja"] >= inicio_6m)
        & (df_operadores["FechaBaja"] <= fecha_hoy)
    )

    df_bajas_6m = df_operadores[cond_bajas_ult6m].copy()
    total_bajas_6m = df_bajas_6m["Numero"].nunique()

    if total_bajas_6m > 0:

      def diff_meses(row):
        if pd.isna(row["FechaContratacion"]) or pd.isna(row["FechaBaja"]):
          return -1
        f_inc = row["FechaContratacion"]
        f_fin = row["FechaBaja"]
        return (f_fin.year - f_inc.year) * 12 + (f_fin.month - f_inc.month)

      df_bajas_6m["MesesAntiguedad"] = df_bajas_6m.apply(diff_meses, axis=1)

      # Bajas 0 - 3 Meses
      cond_b_0_3 = (df_bajas_6m["MesesAntiguedad"] >= 0) & (
          df_bajas_6m["MesesAntiguedad"] <= 3
      )
      cnt_baja_0_3 = df_bajas_6m[cond_b_0_3]["Numero"].nunique()
      pct_baja_0_3 = f"{(cnt_baja_0_3 / total_bajas_6m) * 100:.2f}%"

      # Bajas 4 - 6 Meses
      cond_b_4_6 = (df_bajas_6m["MesesAntiguedad"] > 3) & (
          df_bajas_6m["MesesAntiguedad"] <= 6
      )
      cnt_baja_4_6 = df_bajas_6m[cond_b_4_6]["Numero"].nunique()
      pct_baja_4_6 = f"{(cnt_baja_4_6 / total_bajas_6m) * 100:.2f}%"

      # Bajas 7 - 12 Meses
      cond_b_7_12 = (df_bajas_6m["MesesAntiguedad"] > 6) & (
          df_bajas_6m["MesesAntiguedad"] <= 12
      )
      cnt_baja_7_12 = df_bajas_6m[cond_b_7_12]["Numero"].nunique()
      pct_baja_7_12 = f"{(cnt_baja_7_12 / total_bajas_6m) * 100:.2f}%"

      # Bajas +12 Meses
      cond_b_1mas = df_bajas_6m["MesesAntiguedad"] > 12
      cnt_baja_1mas = df_bajas_6m[cond_b_1mas]["Numero"].nunique()
      pct_baja_1mas = f"{(cnt_baja_1mas / total_bajas_6m) * 100:.2f}%"

  # ---------------------------------------------------------
  # INDICADORES OPERADOR (Licencias / Antidoping)
  # ---------------------------------------------------------
  lic_venc = 0
  lic_por_vencer = 0
  op_doping_vencido = 0
  op_doping_por_vencer = 0
  pct_antidoping_str = "--"

  if not df_operadores.empty:
    hoy_ind = fecha_base

    # Base: activos, sin NA, sin incapacitados
    cond_activos_sin_na = (
        df_operadores["FechaBaja"].isna()
        & (df_operadores["Puesto"] != "NA")
        & (df_operadores["Puesto"] != "OPERADOR INCAPACITADO")
    )

    # --- Licencias ---
    if "LicenciaVencimiento" in df_operadores.columns:
      df_operadores["LicenciaVencimiento"] = pd.to_datetime(
          df_operadores["LicenciaVencimiento"], errors="coerce"
      ).dt.date

      cond_lic_venc = (
          df_operadores["LicenciaVencimiento"].notna()
          & (df_operadores["LicenciaVencimiento"] < hoy_ind)
          & cond_activos_sin_na
      )
      lic_venc = df_operadores[cond_lic_venc]["Numero"].nunique()

      cond_lic_por_vencer = (
          df_operadores["FechaBaja"].isna()
          & df_operadores["LicenciaVencimiento"].notna()
          & (df_operadores["LicenciaVencimiento"] >= hoy_ind)
          & (
              df_operadores["LicenciaVencimiento"]
              <= hoy_ind + datetime.timedelta(days=90)
          )
          & (df_operadores["Puesto"] != "OPERADOR INCAPACITADO")
      )
      lic_por_vencer = df_operadores[cond_lic_por_vencer]["Numero"].nunique()

    # --- Antidoping ---
    # Traducción de la medida DAX "Dias Antidoping": para cada operador se toma
    # el registro MÁS RECIENTE (por UltimaActualizacion) de OperadoresDocumentos
    # cuyo DescripcionDocumento = "ANTIDOPING", y se usa su FechaVencimiento.
    fecha_venc_antidoping = pd.Series(dtype="object")

    if (
        not df_operadores_documentos.empty
        and "DescripcionDocumento" in df_operadores_documentos.columns
    ):
      df_docs = df_operadores_documentos.copy()
      df_docs["UltimaActualizacion"] = pd.to_datetime(
          df_docs["UltimaActualizacion"], errors="coerce"
      )
      df_docs["FechaVencimiento"] = pd.to_datetime(
          df_docs["FechaVencimiento"], errors="coerce"
      ).dt.date

      cond_antidoping = (
          df_docs["DescripcionDocumento"].astype(str).str.upper()
          == "ANTIDOPING"
      ) & df_docs["FechaVencimiento"].notna()

      df_antidoping = df_docs[cond_antidoping].sort_values(
          "UltimaActualizacion", ascending=False
      )
      # Nos quedamos con el registro más reciente por operador (TOPN 1 del DAX)
      df_antidoping_latest = df_antidoping.drop_duplicates(
          subset="Numero", keep="first"
      )
      fecha_venc_antidoping = df_antidoping_latest.set_index("Numero")[
          "FechaVencimiento"
      ]

    df_operadores["FechaVencimientoAntidoping"] = df_operadores["Numero"].map(
        fecha_venc_antidoping
    )
    # Dias Antidoping (DAX) = DATEDIFF(FechaVencimiento, Hoy, DAY) = Hoy - FechaVencimiento
    df_operadores["DiasAntidoping"] = df_operadores[
        "FechaVencimientoAntidoping"
    ].apply(lambda f: (hoy_ind - f).days if pd.notna(f) else None)

    cond_doping_vencido = (
        df_operadores["DiasAntidoping"].notna()
        & (df_operadores["DiasAntidoping"] > 0)
        & cond_activos_sin_na
    )
    op_doping_vencido = df_operadores[cond_doping_vencido]["Numero"].nunique()

    cond_doping_por_vencer = (
        df_operadores["DiasAntidoping"].notna()
        & (df_operadores["DiasAntidoping"] <= 0)
        & (df_operadores["DiasAntidoping"] >= -30)
        & cond_activos_sin_na
    )
    op_doping_por_vencer = df_operadores[cond_doping_por_vencer][
        "Numero"
    ].nunique()

    # --- % Cumplimiento Antidoping ---
    puestos_operativos = [
        "OPERADOR FULL",
        "OPERADOR PATIO",
        "OPERADOR POSTURA",
        "OPERADOR SENCILLO",
    ]
    cond_total_ops = (
        df_operadores["FechaBaja"].isna()
        & df_operadores["Puesto"].isin(puestos_operativos)
    )
    total_operadores_activos = df_operadores[cond_total_ops]["Numero"].nunique()

    if total_operadores_activos > 0:
      pct_cump = 1 - (op_doping_vencido / total_operadores_activos)
      pct_antidoping_str = f"{pct_cump * 100:.2f}%"

  # ---------------------------------------------------------
  # MOTIVOS DE BAJA (B01-B05, últimos 3 meses)
  # ---------------------------------------------------------
  def edate(d, meses):
    """Equivalente a EDATE de DAX: suma/resta meses a una fecha."""
    total_meses = d.month - 1 + meses
    anio = d.year + total_meses // 12
    mes = total_meses % 12 + 1
    dia = min(d.day, calendar.monthrange(anio, mes)[1])
    return datetime.date(anio, mes, dia)

  bajas_b01 = bajas_b02 = bajas_b03 = bajas_b04 = bajas_b05 = 0

  if not df_operadores.empty and "Observaciones" in df_operadores.columns:
    inicio_mes_actual_mb = datetime.date(fecha_base.year, fecha_base.month, 1)
    fin_mes_actual_mb = datetime.date(
        fecha_base.year,
        fecha_base.month,
        calendar.monthrange(fecha_base.year, fecha_base.month)[1],
    )
    inicio_rango_mb = edate(inicio_mes_actual_mb, -2)
    fin_rango_mb = fin_mes_actual_mb

    obs_upper = df_operadores["Observaciones"].fillna("").astype(str).str.upper()

    cond_rango_baja = (
        df_operadores["FechaBaja"].notna()
        & (df_operadores["FechaBaja"] >= inicio_rango_mb)
        & (df_operadores["FechaBaja"] <= fin_rango_mb)
    )

    bajas_b01 = df_operadores[
        cond_rango_baja & obs_upper.str.contains("B01")
    ]["Numero"].nunique()

    bajas_b02 = df_operadores[
        cond_rango_baja & obs_upper.str.contains("B02")
    ]["Numero"].nunique()

    bajas_b03 = df_operadores[
        cond_rango_baja & obs_upper.str.contains("B03")
    ]["Numero"].nunique()

    bajas_b04 = df_operadores[
        cond_rango_baja
        & obs_upper.str.contains("B04")
        & ~obs_upper.str.contains("B041")
        & ~obs_upper.str.contains("B042")
    ]["Numero"].nunique()

    bajas_b05 = df_operadores[
        cond_rango_baja & obs_upper.str.contains("B05")
    ]["Numero"].nunique()

  # --- PRESENTACIÓN EN PANTALLA: ACTIVAS vs BAJAS ---
  col_sec_activas, col_sec_bajas = st.columns(2)

  # COLUMNA IZQUIERDA: PLANTILLA ACTIVA (VERDE)
  with col_sec_activas:
    st.markdown("##### ⏳ Antigüedad de Plantilla Activa")

    a_r1_c1, a_r1_c2 = st.columns(2)
    with a_r1_c1:
      st.markdown(
          f"""
                <div class="tenure-card">
                    <div class="tenure-header" style="background-color: #065F46;">0 - 3 Meses</div>
                    <div class="tenure-body">
                        <span class="tenure-count" style="color: #065F46;">{cnt_0_3}</span>
                        <span class="tenure-percentage" style="color: #047857;">{pct_0_3}</span>
                    </div>
                </div>
            """,
          unsafe_allow_html=True,
      )

    with a_r1_c2:
      st.markdown(
          f"""
                <div class="tenure-card">
                    <div class="tenure-header" style="background-color: #065F46;">4 - 6 Meses</div>
                    <div class="tenure-body">
                        <span class="tenure-count" style="color: #065F46;">{cnt_4_6}</span>
                        <span class="tenure-percentage" style="color: #047857;">{pct_4_6}</span>
                    </div>
                </div>
            """,
          unsafe_allow_html=True,
      )

    st.write("")

    a_r2_c1, a_r2_c2 = st.columns(2)
    with a_r2_c1:
      st.markdown(
          f"""
                <div class="tenure-card">
                    <div class="tenure-header" style="background-color: #065F46;">7 - 12 Meses</div>
                    <div class="tenure-body">
                        <span class="tenure-count" style="color: #065F46;">{cnt_7_12}</span>
                        <span class="tenure-percentage" style="color: #047857;">{pct_7_12}</span>
                    </div>
                </div>
            """,
          unsafe_allow_html=True,
      )

    with a_r2_c2:
      st.markdown(
          f"""
                <div class="tenure-card">
                    <div class="tenure-header" style="background-color: #065F46;">+1 Año</div>
                    <div class="tenure-body">
                        <span class="tenure-count" style="color: #065F46;">{cnt_1mas}</span>
                        <span class="tenure-percentage" style="color: #047857;">{pct_1mas}</span>
                    </div>
                </div>
            """,
          unsafe_allow_html=True,
      )

  # COLUMNA DERECHA: BAJAS (ROJO)
  with col_sec_bajas:
    st.markdown("##### 📉 Antigüedad de Bajas (Últimos 6 Meses)")

    b_r1_c1, b_r1_c2 = st.columns(2)
    with b_r1_c1:
      st.markdown(
          f"""
                <div class="tenure-card">
                    <div class="tenure-header" style="background-color: #991B1B;">0 - 3 Meses</div>
                    <div class="tenure-body">
                        <span class="tenure-count" style="color: #991B1B;">{cnt_baja_0_3}</span>
                        <span class="tenure-percentage" style="color: #B91C1C;">{pct_baja_0_3}</span>
                    </div>
                </div>
            """,
          unsafe_allow_html=True,
      )

    with b_r1_c2:
      st.markdown(
          f"""
                <div class="tenure-card">
                    <div class="tenure-header" style="background-color: #991B1B;">4 - 6 Meses</div>
                    <div class="tenure-body">
                        <span class="tenure-count" style="color: #991B1B;">{cnt_baja_4_6}</span>
                        <span class="tenure-percentage" style="color: #B91C1C;">{pct_baja_4_6}</span>
                    </div>
                </div>
            """,
          unsafe_allow_html=True,
      )

    st.write("")

    b_r2_c1, b_r2_c2 = st.columns(2)
    with b_r2_c1:
      st.markdown(
          f"""
                <div class="tenure-card">
                    <div class="tenure-header" style="background-color: #991B1B;">7 - 12 Meses</div>
                    <div class="tenure-body">
                        <span class="tenure-count" style="color: #991B1B;">{cnt_baja_7_12}</span>
                        <span class="tenure-percentage" style="color: #B91C1C;">{pct_baja_7_12}</span>
                    </div>
                </div>
            """,
          unsafe_allow_html=True,
      )

    with b_r2_c2:
      st.markdown(
          f"""
                <div class="tenure-card">
                    <div class="tenure-header" style="background-color: #991B1B;">+1 Año</div>
                    <div class="tenure-body">
                        <span class="tenure-count" style="color: #991B1B;">{cnt_baja_1mas}</span>
                        <span class="tenure-percentage" style="color: #B91C1C;">{pct_baja_1mas}</span>
                    </div>
                </div>
            """,
          unsafe_allow_html=True,
      )

  st.write("")
  st.write("")

  # ---------------------------------------------------------
  # SECCIÓN: INDICADORES OPERADOR (debajo de Antigüedad)
  # ---------------------------------------------------------
  st.markdown("##### 🧾 Indicadores Operador")

  st.markdown(
      f"""
            <div class="indicator-card">
                <div class="indicator-header">Indicadores Operador</div>
                <div class="indicator-grid">
                    <div class="indicator-item">
                        <div class="indicator-label">Licencias Venc.</div>
                        <div class="indicator-value" style="color: #B91C1C;">{lic_venc}</div>
                    </div>
                    <div class="indicator-item">
                        <div class="indicator-label">Lic. p/ Vencer &lt;90 Días</div>
                        <div class="indicator-value" style="color: #D97706;">{lic_por_vencer}</div>
                    </div>
                    <div class="indicator-item">
                        <div class="indicator-label">Op. Doping Vencido</div>
                        <div class="indicator-value" style="color: #B91C1C;">{op_doping_vencido}</div>
                    </div>
                    <div class="indicator-item">
                        <div class="indicator-label">Op. Doping &lt;30 Días</div>
                        <div class="indicator-value" style="color: #D97706;">{op_doping_por_vencer}</div>
                    </div>
                    <div class="indicator-item">
                        <div class="indicator-label">% Cump. Antidoping</div>
                        <div class="indicator-value" style="color: #047857;">{pct_antidoping_str}</div>
                    </div>
                </div>
            </div>
        """,
      unsafe_allow_html=True,
  )

  st.write("")
  st.write("")

  # ---------------------------------------------------------
  # TARJETA: MOTIVOS DE BAJA
  # ---------------------------------------------------------
  st.markdown("##### 📋 Motivos de Baja")

  st.markdown(
      f"""
            <div class="indicator-card">
                <div class="indicator-header">Motivos de Baja</div>
                <div class="indicator-grid">
                    <div class="indicator-item">
                        <div class="indicator-label">B01 Doping</div>
                        <div class="indicator-value" style="color: #1D4ED8;">{bajas_b01}</div>
                    </div>
                    <div class="indicator-item">
                        <div class="indicator-label">B02 Resición</div>
                        <div class="indicator-value" style="color: #1D4ED8;">{bajas_b02}</div>
                    </div>
                    <div class="indicator-item">
                        <div class="indicator-label">B03 Abandono</div>
                        <div class="indicator-value" style="color: #1D4ED8;">{bajas_b03}</div>
                    </div>
                    <div class="indicator-item">
                        <div class="indicator-label">B04 Baja Vol</div>
                        <div class="indicator-value" style="color: #1D4ED8;">{bajas_b04}</div>
                    </div>
                    <div class="indicator-item">
                        <div class="indicator-label">B05 Pensión</div>
                        <div class="indicator-value" style="color: #1D4ED8;">{bajas_b05}</div>
                    </div>
                </div>
            </div>
        """,
      unsafe_allow_html=True,
  )

  st.divider()

  st.markdown("##### 🔍 Vista Previa de Tabla 'Operadores' desde Azure")
  st.dataframe(df_operadores.head(10), use_container_width=True)
