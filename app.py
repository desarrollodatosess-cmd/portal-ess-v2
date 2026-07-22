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
# ESTILOS CSS
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
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05);
        min-height: 125px;
        display: flex;
        flex-direction: column;
        justify-content: space-between;
        position: relative;
        overflow: hidden;
    }

    .kpi-title { font-size: 11px; font-weight: 800; color: #64748B; text-transform: uppercase; letter-spacing: 0.8px; margin-bottom: 4px; }
    .kpi-value { font-size: 28px; font-weight: 900; line-height: 1.1; }
    .kpi-sub { font-size: 12px; font-weight: 600; color: #64748B; margin-top: 6px; }
    .kpi-icon-badge { position: absolute; top: 14px; right: 14px; background: rgba(219, 234, 254, 0.7); width: 40px; height: 40px; border-radius: 12px; display: flex; align-items: center; justify-content: center; font-size: 20px; }

    /* Tarjeta Especial: Indicadores Operador (Estilo Power BI) */
    .operator-indicators-card {
        background: #F1F5F9;
        border-radius: 12px;
        border: 1px solid #CBD5E1;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.08);
        overflow: hidden;
        margin-bottom: 25px;
    }
    .operator-header {
        background-color: #0F3A7D;
        color: #FFFFFF;
        font-weight: 800;
        font-size: 16px;
        text-align: center;
        padding: 10px 15px;
        letter-spacing: 0.5px;
    }
    .operator-grid {
        display: grid;
        grid-template-columns: repeat(5, 1fr);
        padding: 18px 10px;
        text-align: center;
        background-color: #F8FAFC;
    }
    .operator-item {
        border-right: 1px solid #E2E8F0;
        padding: 0 10px;
    }
    .operator-item:last-child { border-right: none; }
    .operator-label {
        font-size: 12px;
        font-weight: 700;
        color: #475569;
        margin-bottom: 8px;
    }
    .operator-value {
        font-size: 28px;
        font-weight: 900;
        line-height: 1;
    }

    /* Histórico de Movimientos */
    .history-card { background: #FFFFFF; border-radius: 16px; border: 1px solid #E2E8F0; box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05); overflow: hidden; margin-top: 8px; }
    .card-header-altas { background: linear-gradient(90deg, #065F46 0%, #047857 100%); color: #FFFFFF; font-weight: 800; font-size: 13px; padding: 10px 16px; text-transform: uppercase; }
    .card-header-bajas { background: linear-gradient(90deg, #991B1B 0%, #B91C1C 100%); color: #FFFFFF; font-weight: 800; font-size: 13px; padding: 10px 16px; text-transform: uppercase; }
    .history-grid { display: grid; grid-template-columns: repeat(4, 1fr); padding: 16px 8px; text-align: center; }
    .history-item { border-right: 1px solid #F1F5F9; padding: 0 8px; }
    .history-item:last-child { border-right: none; }
    .history-label { font-size: 11px; font-weight: 700; color: #64748B; text-transform: uppercase; margin-bottom: 6px; }
    .history-value-altas { font-size: 24px; font-weight: 900; color: #047857; }
    .history-value-bajas { font-size: 24px; font-weight: 900; color: #B91C1C; }

    /* Antigüedad */
    .tenure-card { background: #F8FAFC; border-radius: 12px; border: 1px solid #CBD5E1; overflow: hidden; text-align: center; }
    .tenure-header { color: #FFFFFF; font-weight: 800; font-size: 13px; padding: 8px 12px; }
    .tenure-body { padding: 14px 16px; display: flex; justify-content: space-around; align-items: center; background-color: #FFFFFF; }
    .tenure-count { font-size: 22px; font-weight: 800; }
    .tenure-percentage { font-size: 20px; font-weight: 900; }
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
    st.markdown("## 📊 Indicadores Capital Humano")
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

  # ---------------------------------------------------------
  # CÁLCULOS DAX A PANDAS: INDICADORES OPERADOR
  # ---------------------------------------------------------
  lic_vencidas_cnt = 0
  lic_pvencer_cnt = 0
  doping_vencidos_cnt = 0
  doping_pvencer_cnt = 0
  pct_cumplimiento_antidoping = 0.0

  if not df_operadores.empty:
    hoy = datetime.date.today()

    # Normalizar columnas
    df_operadores["Puesto_Norm"] = (
        df_operadores["Puesto"].fillna("").astype(str).str.strip().str.upper()
    )
    df_operadores["FechaBaja_DT"] = pd.to_datetime(
        df_operadores["FechaBaja"], errors="coerce"
    ).dt.date
    df_operadores["LicenciaVenc_DT"] = pd.to_datetime(
        df_operadores["LicenciaVencimiento"], errors="coerce"
    ).dt.date

    # Condición general de activos válidos
    es_activo = df_operadores["FechaBaja_DT"].isna()
    puesto_valido = ~df_operadores["Puesto_Norm"].isin(
        ["NA", "OPERADOR INCAPACITADO", "INCAPACITADO"]
    )

    # 1. Licencias Vencidas
    cond_lic_venc = (
        es_activo
        & puesto_valido
        & df_operadores["LicenciaVenc_DT"].notna()
        & (df_operadores["LicenciaVenc_DT"] < hoy)
    )
    lic_vencidas_cnt = df_operadores[cond_lic_venc]["Numero"].nunique()

    # 2. Licencias Por Vencer (<90 días)
    cond_lic_pvenc = (
        es_activo
        & (
            ~df_operadores["Puesto_Norm"].isin(
                ["OPERADOR INCAPACITADO", "INCAPACITADO"]
            )
        )
        & df_operadores["LicenciaVenc_DT"].notna()
        & (df_operadores["LicenciaVenc_DT"] >= hoy)
        & (df_operadores["LicenciaVenc_DT"] <= hoy + datetime.timedelta(days=90))
    )
    lic_pvencer_cnt = df_operadores[cond_lic_pvenc]["Numero"].nunique()

    # 3. Antidoping Vencidos (Dias Antidoping > 0)
    if "DiasAntidoping" in df_operadores.columns:
      cond_doping_venc = (
          es_activo
          & puesto_valido
          & df_operadores["DiasAntidoping"].notna()
          & (df_operadores["DiasAntidoping"] > 0)
      )
      doping_vencidos_cnt = df_operadores[cond_doping_venc]["Numero"].nunique()

      # 4. Antidoping Por Vencer (<30 días: entre -30 y 0)
      cond_doping_pvenc = (
          es_activo
          & puesto_valido
          & df_operadores["DiasAntidoping"].notna()
          & (df_operadores["DiasAntidoping"] <= 0)
          & (df_operadores["DiasAntidoping"] >= -30)
      )
      doping_pvencer_cnt = df_operadores[cond_doping_pvenc]["Numero"].nunique()

    # 5. % Cumplimiento Antidoping
    puestos_target = [
        "OPERADOR FULL",
        "OPERADOR PATIO",
        "OPERADOR POSTURA",
        "OPERADOR SENCILLO",
    ]
    cond_total_target = es_activo & df_operadores["Puesto_Norm"].isin(
        puestos_target
    )
    total_ops_target = df_operadores[cond_total_target]["Numero"].nunique()

    if total_ops_target > 0:
      pct_cumplimiento_antidoping = 1.0 - (
          doping_vencidos_cnt / total_ops_target
      )
    else:
      pct_cumplimiento_antidoping = 0.0

  # ---------------------------------------------------------
  # LOGICA DE COLORES DINÁMICOS (BASADA EN REGLAS DE IMÁGENES)
  # ---------------------------------------------------------
  color_lic_venc = "#DC2626" if lic_vencidas_cnt >= 1 else "#059669"
  color_lic_pvenc = "#D97706" if lic_pvencer_cnt >= 1 else "#059669"
  color_doping_venc = "#DC2626" if doping_vencidos_cnt >= 1 else "#059669"
  color_doping_pvenc = "#D97706" if doping_pvencer_cnt >= 1 else "#059669"
  color_cump_antidoping = (
      "#059669" if pct_cumplimiento_antidoping >= 0.95 else "#DC2626"
  )

  # ---------------------------------------------------------
  # RENDER TARJETA "INDICADORES OPERADOR"
  # ---------------------------------------------------------
  st.markdown(
      f"""
        <div class="operator-indicators-card">
            <div class="operator-header">Indicadores Operador</div>
            <div class="operator-grid">
                <div class="operator-item">
                    <div class="operator-label">Licencias Venc.</div>
                    <div class="operator-value" style="color: {color_lic_venc};">{lic_vencidas_cnt}</div>
                </div>
                <div class="operator-item">
                    <div class="operator-label">Lic P. Vencer &lt;90 Días</div>
                    <div class="operator-value" style="color: {color_lic_pvenc};">{lic_pvencer_cnt}</div>
                </div>
                <div class="operator-item">
                    <div class="operator-label">Op. Doping Vencido</div>
                    <div class="operator-value" style="color: {color_doping_venc};">{doping_vencidos_cnt}</div>
                </div>
                <div class="operator-item">
                    <div class="operator-label">Op. Doping &lt; 30 Días</div>
                    <div class="operator-value" style="color: {color_doping_pvenc};">{doping_pvencer_cnt}</div>
                </div>
                <div class="operator-item">
                    <div class="operator-label">% Cump. Antidoping</div>
                    <div class="operator-value" style="color: {color_cump_antidoping};">{pct_cumplimiento_antidoping * 100:.2f}%</div>
                </div>
            </div>
        </div>
    """,
      unsafe_allow_html=True,
  )

  # ---------------------------------------------------------
  # OTROS CÁLCULOS DEL DASHBOARD
  # ---------------------------------------------------------
  if not df_unidades.empty:
    unidades_activas = (
        len(df_unidades[df_unidades["Estatus"] == "ACTIVA"])
        if "Estatus" in df_unidades.columns
        else len(df_unidades)
    )
  else:
    unidades_activas = 0

  plantilla_autorizada = int(round(unidades_activas * 1.1)) or 134
  plantilla_real = (
      df_operadores[
          df_operadores["FechaBaja"].isna()
          & (~df_operadores["Puesto"].isin(["NA", "OPERADOR INCAPACITADO"]))
      ]["Numero"].nunique()
      if not df_operadores.empty
      else 0
  )
  cumplimiento_str = (
      f"{(plantilla_real / plantilla_autorizada) * 100:.2f}%"
      if plantilla_autorizada > 0
      else "0.00%"
  )

  # --- FILA 1: TARJETAS PRINCIPALES ---
  col1, col2, col3, col4 = st.columns(4)
  with col1:
    st.markdown(
        f"""<div class="kpi-card"><div class="kpi-icon-badge">🚜</div><div><div class="kpi-title">Unidades</div><div class="kpi-value" style="color: #1D4ED8;">{unidades_activas}</div></div><div class="kpi-sub">Unidades Activas</div></div>""",
        unsafe_allow_html=True,
    )
  with col2:
    st.markdown(
        f"""<div class="kpi-card"><div class="kpi-icon-badge">👥</div><div><div class="kpi-title">Plantilla Activa</div><div class="kpi-value" style="color: #DC2626;">{cumplimiento_str}</div></div><div class="kpi-sub">Real: <b>{plantilla_real}</b> | Auth: <b>{plantilla_autorizada}</b></div></div>""",
        unsafe_allow_html=True,
    )
  with col3:
    st.markdown(
        """<div class="kpi-card"><div class="kpi-icon-badge">🔄</div><div><div class="kpi-title">Rotación</div><div class="kpi-value" style="color: #059669;">0.00%</div></div><div class="kpi-sub">Mes actual</div></div>""",
        unsafe_allow_html=True,
    )
  with col4:
    st.markdown(
        """<div class="kpi-card"><div class="kpi-icon-badge">📈</div><div><div class="kpi-title">Tasa Contratación</div><div class="kpi-value" style="color: #1D4ED8;">--</div></div><div class="kpi-sub">Mes Ant: <b>--</b></div></div>""",
        unsafe_allow_html=True,
    )

  st.write("")

  # ---------------------------------------------------------
  # HISTÓRICO Y ANTIGÜEDAD (VERDE EN PLANTILLA ACTIVA)
  # ---------------------------------------------------------
  col_sec_activas, col_sec_bajas = st.columns(2)

  with col_sec_activas:
    st.markdown("##### ⏳ Antigüedad de Plantilla Activa")
    a_r1_c1, a_r1_c2 = st.columns(2)
    with a_r1_c1:
      st.markdown(
          """<div class="tenure-card"><div class="tenure-header" style="background-color: #065F46;">0 - 3 Meses</div><div class="tenure-body"><span class="tenure-count" style="color: #065F46;">0</span><span class="tenure-percentage" style="color: #047857;">0.00%</span></div></div>""",
          unsafe_allow_html=True,
      )
    with a_r1_c2:
      st.markdown(
          """<div class="tenure-card"><div class="tenure-header" style="background-color: #065F46;">4 - 6 Meses</div><div class="tenure-body"><span class="tenure-count" style="color: #065F46;">0</span><span class="tenure-percentage" style="color: #047857;">0.00%</span></div></div>""",
          unsafe_allow_html=True,
      )

  with col_sec_bajas:
    st.markdown("##### 📉 Antigüedad de Bajas (Últimos 6 Meses)")
    b_r1_c1, b_r1_c2 = st.columns(2)
    with b_r1_c1:
      st.markdown(
          """<div class="tenure-card"><div class="tenure-header" style="background-color: #991B1B;">0 - 3 Meses</div><div class="tenure-body"><span class="tenure-count" style="color: #991B1B;">0</span><span class="tenure-percentage" style="color: #B91C1C;">0.00%</span></div></div>""",
          unsafe_allow_html=True,
      )
    with b_r1_c2:
      st.markdown(
          """<div class="tenure-card"><div class="tenure-header" style="background-color: #991B1B;">4 - 6 Meses</div><div class="tenure-body"><span class="tenure-count" style="color: #991B1B;">0</span><span class="tenure-percentage" style="color: #B91C1C;">0.00%</span></div></div>""",
          unsafe_allow_html=True,
      )
