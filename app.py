import streamlit as st

# Configuración de página amplia
st.set_page_config(
    page_title="Portal BI - ESS",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Estilos CSS personalizados para UI elegante estilo Capital Humano
st.markdown(
    """
    <style>
    .main-header {
        font-size: 2.2rem;
        font-weight: 700;
        color: #1E293B;
        margin-bottom: 0.5rem;
    }
    .sub-header {
        font-size: 1.1rem;
        color: #64748B;
        margin-bottom: 2rem;
    }
    .kpi-card {
        background-color: #FFFFFF;
        border-radius: 12px;
        padding: 20px;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06);
        border: 1px solid #E2E8F0;
        text-align: center;
    }
    .kpi-title {
        font-size: 0.875rem;
        color: #64748B;
        font-weight: 600;
        text-transform: uppercase;
    }
    .kpi-value {
        font-size: 1.875rem;
        font-weight: 700;
        color: #0F172A;
        margin-top: 8px;
    }
    </style>
""",
    unsafe_allow_html=True,
)

# Encabezado principal
st.markdown(
    '<div class="main-header">🚀 Portal de Inteligencia de Negocios</div>',
    unsafe_allow_html=True,
)
st.markdown(
    '<div class="sub-header">Express San Silvestre — Sistema de Gestión Centralizado</div>',
    unsafe_allow_html=True,
)

st.divider()

# Tarjetas de KPI estilizadas estilo Dashboard Pro
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.markdown(
        """
        <div class="kpi-card">
            <div class="kpi-title">Módulo Activo</div>
            <div class="kpi-value">Liquidaciones</div>
        </div>
    """,
        unsafe_allow_html=True,
    )

with col2:
    st.markdown(
        """
        <div class="kpi-card">
            <div class="kpi-title">Conexión</div>
            <div class="kpi-value" style="color: #10B981;">En línea</div>
        </div>
    """,
        unsafe_allow_html=True,
    )

with col3:
    st.markdown(
        """
        <div class="kpi-card">
            <div class="kpi-title">Base de Datos</div>
            <div class="kpi-value">SQL Nivel 1</div>
        </div>
    """,
        unsafe_allow_html=True,
    )

with col4:
    st.markdown(
        """
        <div class="kpi-card">
            <div class="kpi-title">Versión</div>
            <div class="kpi-value">2.0 Cloud</div>
        </div>
    """,
        unsafe_allow_html=True,
    )

st.write("")
st.success(
    "✅ ¡Portal configurado con éxito! El lienzo de diseño personalizado está listo."
)
