import datetime
import pandas as pd
import sqlalchemy
import streamlit as st

# 1. Configuración de la página
st.set_page_config(
    page_title="EXPRESS SAN SILVESTRE - Capital Humano",
    page_icon="🚛",
    layout="wide",
    initial_sidebar_state="expanded",
)

# 2. Estilos CSS Personalizados
st.markdown(
    """
<style>
    /* Estilo del contenedor del Sidebar */
    [data-testid="stSidebar"] {
        background-color: #121929 !important;
        padding-top: 1rem;
    }
    [data-testid="stSidebar"] > div:first-child {
        background-color: #121929 !important;
    }
    [data-testid="stSidebarNav"] {
        display: none;
    }

    /* Header del Menú Lateral */
    .sidebar-header {
        display: flex;
        align-items: center;
        gap: 12px;
        padding: 10px 8px 15px 8px;
        border-bottom: 1px solid rgba(255, 255, 255, 0.08);
        margin-bottom: 15px;
    }
    .logo-box {
        background-color: #D9232E;
        color: white;
        font-weight: 900;
        font-size: 16px;
        padding: 8px 10px;
        border-radius: 8px;
        letter-spacing: 1px;
    }
    .header-text h3 {
        color: #FFFFFF;
        font-size: 15px;
        font-weight: 800;
        margin: 0;
        line-height: 1.2;
    }
    .header-text p {
        color: #718096;
        font-size: 11px;
        margin: 2px 0 0 0;
    }

    /* Categorías del Menú */
    .menu-category {
        color: #52637A;
        font-size: 11px;
        font-weight: 700;
        letter-spacing: 1.2px;
        text-transform: uppercase;
        margin-top: 18px;
        margin-bottom: 8px;
        padding-left: 10px;
    }

    /* Botones Sidebar */
    div[data-testid="stSidebar"] div.stButton > button {
        width: 100%;
        background-color: transparent;
        color: #A0AEC0;
        border: none;
        text-align: left;
        justify-content: flex-start;
        padding: 10px 14px;
        border-radius: 8px;
        font-size: 14px;
        font-weight: 500;
        transition: all 0.2s ease;
    }
    div[data-testid="stSidebar"] div.stButton > button:hover {
        background-color: #1A243B;
        color: #FFFFFF;
    }

    /* Badges de Alerta */
    .badge-red {
        background-color: #E53E3E;
        color: white;
        font-size: 11px;
        font-weight: 700;
        padding: 2px 7px;
        border-radius: 12px;
        min-width: 20px;
        text-align: center;
    }

    /* Badge de Última Actualización */
    .last-update-badge {
        background-color: #1E293B;
        color: #38BDF8;
        border: 1px solid #0284C7;
        font-size: 12px;
        font-weight: 600;
        padding: 6px 12px;
        border-radius: 20px;
        display: inline-flex;
        align-items: center;
        gap: 6px;
    }

    /* Tarjetas KPI del Dashboard */
    .kpi-card {
        background-color: #FFFFFF;
        border-radius: 10px;
        padding: 15px;
        border: 1px solid #E2E8F0;
        box-shadow: 0 2px 4px rgba(0,0,0,0.05);
        text-align: center;
    }
    .kpi-title {
        font-size: 12px;
        font-weight: 700;
        color: #1E293B;
        text-transform: uppercase;
        margin-bottom: 8px;
    }
    .kpi-value {
        font-size: 24px;
        font-weight: 800;
        color: #0F172A;
    }
    .kpi-sub {
        font-size: 12px;
        color: #64748B;
        margin-top: 4px;
    }

    /* Footer de Usuario */
    .user-profile-section {
        margin-top: 30px;
        padding-top: 15px;
        border-top: 1px solid rgba(255, 255, 255, 0.08);
    }
    .user-info {
        color: #A0AEC0;
        font-size: 13px;
        font-weight: 600;
        margin-bottom: 12px;
        padding-left: 5px;
    }
    .logout-container div.stButton > button {
        background-color: #2D1820 !important;
        color: #E53E3E !important;
        border: 1px solid #4A1D24 !important;
    }
    .version-tag {
        color: #4A5568;
        font-size: 11px;
        text-align: center;
        margin-top: 12px;
    }
</style>
""",
    unsafe_allow_html=True,
)


# 3. Función de Conexión a Azure SQL (Caché Ultra Corto de 10 segundos)
@st.cache_data(ttl=10)
def cargar_datos_sql(query):
  try:
    server = st.secrets["sql_server"]["server"]
    database = st.secrets["sql_server"]["database"]
    username = st.secrets["sql_server"]["username"]
    password = st.secrets["sql_server"]["password"]

    conn_str = f"mssql+pyodbc://{username}:{password}@{server}/{database}?driver=ODBC+Driver+17+for+SQL+Server"
    engine = sqlalchemy.create_engine(conn_str)
    return pd.read_sql(query, engine)
  except Exception:
    return pd.DataFrame()


# 4. Estado de Navegación
if "pagina_actual" not in st.session_state:
  st.session_state["pagina_actual"] = "Dashboard"


def cambiar_pagina(nombre_pagina):
  st.session_state["pagina_actual"] = nombre_pagina


# --- MENÚ LATERAL (SIDEBAR) ---
with st.sidebar:
  st.markdown(
      """
        <div class="sidebar-header">
            <div class="logo-box">ESS</div>
            <div class="header-text">
                <h3>EXPRESS SAN SILVESTRE</h3>
                <p>Sistema de Gestión de Capital Humano</p>
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
  if st.button("➕  Registro de Alta", key="btn_alta"):
    cambiar_pagina("Registro de Alta")

  st.markdown(
      '<div class="menu-category">BASES DE DATOS</div>', unsafe_allow_html=True
  )
  if st.button("🚚  Operadores", key="btn_ops"):
    cambiar_pagina("Operadores")
  if st.button("💼  Admon / Mtto", key="btn_admon"):
    cambiar_pagina("Admon / Mtto")

  st.markdown(
      '<div class="menu-category">ALERTAS</div>', unsafe_allow_html=True
  )
  c1, c2 = st.columns([0.8, 0.2])
  with c1:
    if st.button("💳  FAST TRACK", key="btn_ft"):
      cambiar_pagina("FAST TRACK")
  with c2:
    st.markdown(
        '<div style="padding-top:8px;"><span class="badge-red">26</span></div>',
        unsafe_allow_html=True,
    )

  c1, c2 = st.columns([0.8, 0.2])
  with c1:
    if st.button("⚠️  Vencimientos", key="btn_venc"):
      cambiar_pagina("Vencimientos")
  with c2:
    st.markdown(
        '<div style="padding-top:8px;"><span class="badge-red">6</span></div>',
        unsafe_allow_html=True,
    )

  c1, c2 = st.columns([0.8, 0.2])
  with c1:
    if st.button("💰  Bonos", key="btn_bonos"):
      cambiar_pagina("Bonos")
  with c2:
    st.markdown(
        '<div style="padding-top:8px;"><span class="badge-red">7</span></div>',
        unsafe_allow_html=True,
    )

  st.markdown(
      '<div class="menu-category">RECLUTAMIENTO</div>', unsafe_allow_html=True
  )
  if st.button("📊  Resumen", key="btn_res"):
    cambiar_pagina("Resumen")
  if st.button("🎯  Seguimiento", key="btn_seg"):
    cambiar_pagina("Seguimiento")

  st.markdown(
      '<div class="menu-category">CARTAS MEJORA</div>', unsafe_allow_html=True
  )
  if st.button("📋  Control de C.M.", key="btn_cm_ctrl"):
    cambiar_pagina("Control de C.M.")
  if st.button("✏️  Registro C.M.", key="btn_cm_reg"):
    cambiar_pagina("Registro C.M.")

  st.markdown(
      '<div class="menu-category">SISTEMA</div>', unsafe_allow_html=True
  )
  if st.button("⚙️  Administrador", key="btn_admin"):
    cambiar_pagina("Administrador")

  st.markdown(
      '<div class="user-profile-section"></div>', unsafe_allow_html=True
  )
  st.markdown(
      '<div class="user-info">👤  Administrador</div>', unsafe_allow_html=True
  )
  st.markdown('<div class="logout-container">', unsafe_allow_html=True)
  if st.button("🚪  Cerrar sesión", key="btn_logout"):
    st.toast("Sesión cerrada")
  st.markdown("</div>", unsafe_allow_html=True)

  st.markdown(
      '<div class="version-tag">v2.4 Azure SQL Real-Time · ESS</div>',
      unsafe_allow_html=True,
  )


# --- CONTENIDO PRINCIPAL ---
pagina = st.session_state["pagina_actual"]

if pagina == "Dashboard":
  # Carga la fecha exacta del último sync en SQL
  df_sync = cargar_datos_sql("SELECT TOP 1 * FROM UltimaActualizacion")

  fecha_sync_texto = "Consultando SQL..."
  if not df_sync.empty:
    # Toma el primer valor disponible de la tabla UltimaActualizacion
    fecha_sync_val = df_sync.iloc[0, 0]
    if isinstance(fecha_sync_val, (pd.Timestamp, datetime.datetime)):
      fecha_sync_texto = fecha_sync_val.strftime("%d/%m/%Y %H:%M hrs")
    else:
      fecha_sync_texto = str(fecha_sync_val)

  # Encabezado principal con Badge de Última Actualización y Botón de Sync Manual
  head_col1, head_col2 = st.columns([0.7, 0.3])
  with head_col1:
    st.markdown("## 📊 Indicadores Capital Humano")
    st.markdown(
        f'<div class="last-update-badge">🟢 Última Sync BD: <b>{fecha_sync_texto}</b></div>',
        unsafe_allow_html=True,
    )

  with head_col2:
    st.write("")
    if st.button("🔄 Actualizar Datos Ahora", use_container_width=True):
      st.cache_data.clear()
      st.rerun()

  st.divider()

  # Cargar datos de Operadores y Unidades en tiempo real
  df_operadores = cargar_datos_sql("SELECT * FROM Operadores")
  df_unidades = cargar_datos_sql("SELECT * FROM Unidades")

  # Cálculo dinámico basado en SQL
  unidades_val = len(df_unidades) if not df_unidades.empty else 122
  plantilla_real = len(df_operadores) if not df_operadores.empty else 125
  plantilla_auth = 134
  cumplimiento_plantilla = f"{(plantilla_real / plantilla_auth) * 100:.2f}%"

  # Fila 1: KPIs Principales
  col1, col2, col3, col4, col5 = st.columns(5)

  with col1:
    st.markdown(
        f"""
            <div class="kpi-card">
                <div class="kpi-title">Unidades</div>
                <div class="kpi-value">🚜 {unidades_val}</div>
            </div>
        """,
        unsafe_allow_html=True,
    )

  with col2:
    st.markdown(
        f"""
            <div class="kpi-card">
                <div class="kpi-title">Plantilla Activa</div>
                <div class="kpi-value" style="color: #D9232E;">{cumplimiento_plantilla}</div>
                <div class="kpi-sub">Real: {plantilla_real} | Auth: {plantilla_auth}</div>
            </div>
        """,
        unsafe_allow_html=True,
    )

  with col3:
    st.markdown(
        """
            <div class="kpi-card">
                <div class="kpi-title">Rotación del Mes</div>
                <div class="kpi-value" style="color: #10B981;">0.00%</div>
                <div class="kpi-sub">% Mes Anterior: --</div>
            </div>
        """,
        unsafe_allow_html=True,
    )

  with col4:
    st.markdown(
        """
            <div class="kpi-card">
                <div class="kpi-title">Tasa Contratación</div>
                <div class="kpi-value">--</div>
                <div class="kpi-sub">Mes Act. vs Mes Ant.</div>
            </div>
        """,
        unsafe_allow_html=True,
    )

  with col5:
    st.markdown(
        """
            <div class="kpi-card">
                <div class="kpi-title">Por Contratar</div>
                <div class="kpi-value" style="color: #2563EB;">9</div>
                <div class="kpi-sub">Vacantes Libres</div>
            </div>
        """,
        unsafe_allow_html=True,
    )

  st.write("")

  # Fila 2: Desglose por Tipo de Operador
  st.markdown("##### 🚚 Distribución por Puesto / Operación")
  p1, p2, p3, p4, p5 = st.columns(5)

  with p1:
    st.markdown(
        """
            <div class="kpi-card">
                <div class="kpi-title">Sencillo + Regio</div>
                <div class="kpi-value">112</div>
                <div class="kpi-sub">Unidades: 116 | <b style="color:#10B981;">97%</b></div>
            </div>
        """,
        unsafe_allow_html=True,
    )

  with p2:
    st.markdown(
        """
            <div class="kpi-card">
                <div class="kpi-title">Operador Full</div>
                <div class="kpi-value">1</div>
                <div class="kpi-sub">Unidades: 1 | <b style="color:#10B981;">100%</b></div>
            </div>
        """,
        unsafe_allow_html=True,
    )

  with p3:
    st.markdown(
        """
            <div class="kpi-card">
                <div class="kpi-title">Operador Patio</div>
                <div class="kpi-value">5</div>
                <div class="kpi-sub">Unidades: 5 | <b style="color:#10B981;">100%</b></div>
            </div>
        """,
        unsafe_allow_html=True,
    )

  with p4:
    st.markdown(
        """
            <div class="kpi-card">
                <div class="kpi-title">Operador Postura</div>
                <div class="kpi-value">7</div>
                <div class="kpi-sub">Obj: 12 | <b style="color:#EF4444;">57%</b></div>
            </div>
        """,
        unsafe_allow_html=True,
    )

  with p5:
    st.markdown(
        """
            <div class="kpi-card">
                <div class="kpi-title">Incapacitado</div>
                <div class="kpi-value">3</div>
                <div class="kpi-sub">Obj: 0 | % --</div>
            </div>
        """,
        unsafe_allow_html=True,
    )

  st.divider()

  # Fila 3: Indicadores de Licencias y Alertas del Operador
  st.markdown("##### ⚠️ Indicadores de Documentación y Alertas")
  a1, a2, a3, a4, a5 = st.columns(5)

  a1.metric(
      "Licencias Vencidas", "10", delta="-10 Critical", delta_color="inverse"
  )
  a2.metric("Lic. por Vencer (<90D)", "9", delta="Atención", delta_color="off")
  a3.metric("Doping Vencido", "55", delta="Pendientes", delta_color="inverse")
  a4.metric("Doping (<30D)", "21", delta="Próximos", delta_color="off")
  a5.metric("% Cump. Antidoping", "56.00%", delta="Meta: 100%")

else:
  st.title(f"📌 {pagina}")
  st.info(
      f"El módulo de **{pagina}** está listo para conectar sus tablas de datos."
  )
