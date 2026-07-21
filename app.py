import streamlit as st

# Configuración inicial de la página
st.set_page_config(
    page_title="EXPRESS SAN SILVESTRE - Capital Humano",
    page_icon="🚛",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Estilos CSS Personalizados para replicar el diseño exacto del menú lateral
st.markdown("""
<style>
    /* Estilo del contenedor del Sidebar */
    [data-testid="stSidebar"] {
        background-color: #121929 !important;
        padding-top: 1rem;
    }
    
    [data-testid="stSidebar"] > div:first-child {
        background-color: #121929 !important;
    }

    /* Ocultar elementos predeterminados de Streamlit en el sidebar */
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
        display: flex;
        align-items: center;
        justify-content: center;
    }

    .header-text h3 {
        color: #FFFFFF;
        font-size: 15px;
        font-weight: 800;
        margin: 0;
        line-height: 1.2;
        letter-spacing: 0.5px;
    }

    .header-text p {
        color: #718096;
        font-size: 11px;
        margin: 2px 0 0 0;
    }

    /* Títulos de Categoría (Submenús) */
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

    /* Estilizado de los Botones de Menú en Streamlit */
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
        display: flex;
        align-items: center;
    }

    div[data-testid="stSidebar"] div.stButton > button:hover {
        background-color: #1A243B;
        color: #FFFFFF;
    }

    /* Botón Activo (Seleccionado) */
    div[data-testid="stSidebar"] div.stButton > button[aria-selected="true"],
    div[data-testid="stSidebar"] div.stButton > button.active-menu-item {
        background-color: #1E2B45 !important;
        color: #FFFFFF !important;
        font-weight: 700 !important;
        box-shadow: inset 3px 0px 0px #3182CE;
    }

    /* Fila con Alerta/Badge (FAST TRACK, Vencimientos, Bonos) */
    .menu-item-with-badge {
        display: flex;
        justify-content: space-between;
        align-items: center;
        width: 100%;
    }

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

    /* Footer / Perfil de Usuario */
    .user-profile-section {
        margin-top: 30px;
        padding-top: 15px;
        border-top: 1px solid rgba(255, 255, 255, 0.08);
    }

    .user-info {
        display: flex;
        align-items: center;
        gap: 10px;
        color: #A0AEC0;
        font-size: 13px;
        font-weight: 600;
        margin-bottom: 12px;
        padding-left: 5px;
    }

    /* Botón de Cerrar Sesión Especial */
    .logout-container div.stButton > button {
        background-color: #2D1820 !important;
        color: #E53E3E !important;
        border: 1px solid #4A1D24 !important;
        font-weight: 600 !important;
        text-align: center !important;
        justify-content: center !important;
    }

    .logout-container div.stButton > button:hover {
        background-color: #3D1C26 !important;
        color: #FC8181 !important;
    }

    .version-tag {
        color: #4A5568;
        font-size: 11px;
        text-align: center;
        margin-top: 12px;
    }
</style>
""", unsafe_allow_html=True)

# Inicializar estado de navegación si no existe
if 'pagina_actual' not in st.session_state:
    st.session_state['pagina_actual'] = 'Dashboard'

def cambiar_pagina(nombre_pagina):
    st.session_state['pagina_actual'] = nombre_pagina

# --- RENDERIZADO DEL SIDEBAR ---
with st.sidebar:
    # 1. Header con Logo y Nombre de Empresa
    st.markdown("""
        <div class="sidebar-header">
            <div class="logo-box">ESS</div>
            <div class="header-text">
                <h3>EXPRESS SAN SILVESTRE</h3>
                <p>Sistema de Gestión de Capital Humano</p>
            </div>
        </div>
    """, unsafe_allow_html=True)

    # 2. Categoría: PRINCIPAL
    st.markdown('<div class="menu-category">PRINCIPAL</div>', unsafe_allow_html=True)
    
    col1, col2 = st.columns([1, 1])
    if st.button("🗂️  Dashboard", key="btn_dashboard", use_container_width=True):
        cambiar_pagina("Dashboard")
        
    if st.button("➕  Registro de Alta", key="btn_alta", use_container_width=True):
        cambiar_pagina("Registro de Alta")

    # 3. Categoría: BASES DE DATOS
    st.markdown('<div class="menu-category">BASES DE DATOS</div>', unsafe_allow_html=True)
    if st.button("🚚  Operadores", key="btn_operadores", use_container_width=True):
        cambiar_pagina("Operadores")
        
    if st.button("💼  Admon / Mtto", key="btn_admon", use_container_width=True):
        cambiar_pagina("Admon / Mtto")

    # 4. Categoría: ALERTAS (con Badges)
    st.markdown('<div class="menu-category">ALERTAS</div>', unsafe_allow_html=True)
    
    col_btn, col_badge = st.columns([0.8, 0.2])
    with col_btn:
        if st.button("💳  FAST TRACK", key="btn_fasttrack", use_container_width=True):
            cambiar_pagina("FAST TRACK")
    with col_badge:
        st.markdown('<div style="padding-top:8px;"><span class="badge-red">26</span></div>', unsafe_allow_html=True)

    col_btn2, col_badge2 = st.columns([0.8, 0.2])
    with col_btn2:
        if st.button("⚠️  Vencimientos", key="btn_vencimientos", use_container_width=True):
            cambiar_pagina("Vencimientos")
    with col_badge2:
        st.markdown('<div style="padding-top:8px;"><span class="badge-red">6</span></div>', unsafe_allow_html=True)

    col_btn3, col_badge3 = st.columns([0.8, 0.2])
    with col_btn3:
        if st.button("💰  Bonos", key="btn_bonos", use_container_width=True):
            cambiar_pagina("Bonos")
    with col_badge3:
        st.markdown('<div style="padding-top:8px;"><span class="badge-red">7</span></div>', unsafe_allow_html=True)

    # 5. Categoría: RECLUTAMIENTO
    st.markdown('<div class="menu-category">RECLUTAMIENTO</div>', unsafe_allow_html=True)
    if st.button("📊  Resumen", key="btn_resumen", use_container_width=True):
        cambiar_pagina("Resumen")
        
    if st.button("🎯  Seguimiento", key="btn_seguimiento", use_container_width=True):
        cambiar_pagina("Seguimiento")

    # 6. Categoría: CARTAS MEJORA
    st.markdown('<div class="menu-category">CARTAS MEJORA</div>', unsafe_allow_html=True)
    if st.button("📋  Control de C.M.", key="btn_control_cm", use_container_width=True):
        cambiar_pagina("Control de C.M.")
        
    if st.button("✏️  Registro C.M.", key="btn_registro_cm", use_container_width=True):
        cambiar_pagina("Registro C.M.")

    # 7. Categoría: SISTEMA
    st.markdown('<div class="menu-category">SISTEMA</div>', unsafe_allow_html=True)
    if st.button("⚙️  Administrador", key="btn_admin", use_container_width=True):
        cambiar_pagina("Administrador")

    # 8. Footer de Usuario y Cerrar Sesión
    st.markdown('<div class="user-profile-section"></div>', unsafe_allow_html=True)
    st.markdown('<div class="user-info">👤  Administrador</div>', unsafe_allow_html=True)
    
    st.markdown('<div class="logout-container">', unsafe_allow_html=True)
    if st.button("🚪  Cerrar sesión", key="btn_logout", use_container_width=True):
        st.toast("Sesión cerrada")
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<div class="version-tag">v2.3 Firebase · ESS Capital Humano</div>', unsafe_allow_html=True)


# --- CONTENIDO PRINCIPAL (Según la opción seleccionada) ---
pagina = st.session_state['pagina_actual']

st.title(f"📌 {pagina}")
st.write(f"Bienvenido al módulo de **{pagina}**.")

# Ejemplo de vista para el Dashboard
if pagina == "Dashboard":
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Operadores Activos", "142", "+4 este mes")
    col2.metric("Alertas Vencimiento", "6", "-2 hoy", delta_color="inverse")
    col3.metric("Solicitudes Fast Track", "26", "Pendientes")
    col4.metric("Bonos Registrados", "7", "Procesando")
    
    st.subheader("Últimos Registros")
    st.dataframe({
        "Nombre": ["Rogelio A.", "Giovanni M.", "Porfirio H.", "Cristhian C."],
        "Puesto": ["Operador", "Operador", "Mantenimiento", "Operador"],
        "Estatus": ["Activo", "Activo", "En revisión", "Activo"]
    }, use_container_width=True)
