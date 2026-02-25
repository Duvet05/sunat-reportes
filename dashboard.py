"""
Dashboard GAFA - SUNAT
Ejecutar: streamlit run dashboard.py
"""
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from pathlib import Path

st.set_page_config(
    page_title="Dashboard GAFA · SUNAT",
    page_icon="🏛",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ── Estilo ──────────────────────────────────────────────────────────────────
st.markdown("""
<style>
    .block-container { padding-top: 1.5rem; }
    .metric-container { background: #f8f9fa; border-radius: 8px; padding: 1rem; }
    h1 { color: #1a1a2e; }
    .stMetric label { font-size: 0.85rem !important; color: #555 !important; }
    .stMetric [data-testid="metric-container"] {
        background: white;
        border: 1px solid #e0e0e0;
        border-radius: 8px;
        padding: 1rem;
        box-shadow: 0 1px 4px rgba(0,0,0,.06);
    }
</style>
""", unsafe_allow_html=True)

# ── Columnas del Excel ───────────────────────────────────────────────────────
COL_DEP       = "Dependencia – Para Tributos Internos/ Por Aduana de origen – Para Aduanas"
COL_TIPO      = "Tipo de Recurso"
COL_ETAPA     = "Etapa del Recurso"
COL_RESULTADO = "Resultado de la Resolución"
COL_TAMANO    = "Tamaño del Contribuyente"
COL_ALERTA    = "Alerta"
COL_FECHA     = "Fecha de ingreso"
COL_RESOLUTOR = "Nombre del Resolutor"
COL_MONTO     = "Monto Total Impugnado"
COL_DESC1     = "Descriptor Principal"

ETAPAS_PENDIENTE = {
    "RECURSO EN ANÁLISIS DE FONDO",
    "RECURSO EN EVALUACIÓN DE ADMISIBILIDAD",
    "RECURSO EN EVALUACION DE ADMISIBILIDAD",
    "RECURSO INGRESADO",
}

# ── Carga de datos ───────────────────────────────────────────────────────────
@st.cache_data(show_spinner="Cargando datos SIGERI…")
def cargar():
    path = Path(__file__).parent / "SIGERI 19 ENE 26.xlsx"
    df = pd.read_excel(path, engine="openpyxl")
    df[COL_FECHA] = pd.to_datetime(df[COL_FECHA], errors="coerce")
    return df

df = cargar()

# ── KPIs ─────────────────────────────────────────────────────────────────────
total        = len(df)
resueltos    = ((df[COL_RESULTADO] != "-") & df[COL_RESULTADO].notna()).sum()
pendientes   = df[COL_ETAPA].isin(ETAPAS_PENDIENTE).sum()
fundados     = df[COL_RESULTADO].isin(["FUNDADO", "FUNDADO EN PARTE"]).sum()
infundados   = (df[COL_RESULTADO] == "INFUNDADO").sum()
alerta_oea   = (df[COL_ALERTA] == "Alerta OEA").sum()
apelaciones  = (df[COL_TIPO] == "APELACIÓN").sum()
reclamaciones= (df[COL_TIPO] == "RECLAMACIÓN").sum()
grandes      = (df[COL_TAMANO] == "PRINCIPAL").sum()
trib_fiscal  = (df[COL_ETAPA] == "REMITIDO AL TRIBUNAL FISCAL").sum()

pct_res  = resueltos / total if total else 0
pct_fund = fundados  / resueltos if resueltos else 0

# ── Título ───────────────────────────────────────────────────────────────────
st.markdown("## 🏛 Dashboard GAFA · SUNAT")
st.caption(f"Corte: **19 Enero 2026** · {total:,} expedientes cargados")
st.divider()

# ── Fila 1: KPIs principales ─────────────────────────────────────────────────
c1, c2, c3, c4, c5 = st.columns(5)
c1.metric("📋 Total Expedientes",  f"{total:,}")
c2.metric("⏳ Pendientes",         f"{pendientes:,}",
          delta=f"{pendientes/total:.1%} del total", delta_color="inverse")
c3.metric("✅ Resueltos",          f"{resueltos:,}",
          delta=f"{pct_res:.1%} resolución")
c4.metric("🔴 Con Alerta OEA",    f"{alerta_oea:,}", delta_color="off")
c5.metric("🏢 Grandes Contrib.",   f"{grandes:,}",   delta_color="off")

st.markdown("")

# ── Fila 2: KPIs secundarios ─────────────────────────────────────────────────
c6, c7, c8, c9, c10 = st.columns(5)
c6.metric("✔ Fundados",           f"{fundados:,}",
          delta=f"{pct_fund:.1%} de resueltos")
c7.metric("✘ Infundados",         f"{infundados:,}")
c8.metric("📨 Apelaciones",        f"{apelaciones:,}")
c9.metric("📝 Reclamaciones",      f"{reclamaciones:,}")
c10.metric("⚖ Tribunal Fiscal",   f"{trib_fiscal:,}")

st.divider()

# ── Gráficos ─────────────────────────────────────────────────────────────────
g1, g2, g3 = st.columns([2, 1, 1])

# Barras: Resultado de la Resolución
with g1:
    st.subheader("Resultado de la Resolución")
    res_vc = (df[df[COL_RESULTADO] != "-"][COL_RESULTADO]
              .value_counts().head(10).reset_index())
    res_vc.columns = ["Resultado", "Cantidad"]
    fig = px.bar(res_vc, x="Cantidad", y="Resultado", orientation="h",
                 color="Cantidad", color_continuous_scale="Blues",
                 text="Cantidad")
    fig.update_traces(texttemplate="%{text:,}", textposition="outside")
    fig.update_layout(showlegend=False, coloraxis_showscale=False,
                      height=340, margin=dict(l=0, r=30, t=10, b=0))
    st.plotly_chart(fig, use_container_width=True)

# Donut: Tipo de Recurso
with g2:
    st.subheader("Tipo de Recurso")
    tipo_vc = df[COL_TIPO].value_counts().reset_index()
    tipo_vc.columns = ["Tipo", "Cantidad"]
    fig2 = px.pie(tipo_vc, values="Cantidad", names="Tipo", hole=0.55,
                  color_discrete_sequence=["#0078D4", "#D83B01"])
    fig2.update_layout(height=340, margin=dict(l=0, r=0, t=10, b=0),
                       legend=dict(orientation="h", y=-0.1))
    st.plotly_chart(fig2, use_container_width=True)

# Donut: Tamaño Contribuyente
with g3:
    st.subheader("Tamaño Contribuyente")
    tam_vc = df[COL_TAMANO].value_counts().reset_index()
    tam_vc.columns = ["Tamaño", "Cantidad"]
    fig3 = px.pie(tam_vc, values="Cantidad", names="Tamaño", hole=0.55,
                  color_discrete_sequence=["#107C10", "#FFB900", "#888"])
    fig3.update_layout(height=340, margin=dict(l=0, r=0, t=10, b=0),
                       legend=dict(orientation="h", y=-0.1))
    st.plotly_chart(fig3, use_container_width=True)

# ── Ingreso mensual ──────────────────────────────────────────────────────────
st.subheader("Ingreso de Expedientes por Mes")
df_time = df.dropna(subset=[COL_FECHA]).copy()
df_time["Mes"] = df_time[COL_FECHA].dt.to_period("M").astype(str)
mensual = df_time.groupby(["Mes", COL_TIPO]).size().reset_index(name="Cantidad")
fig4 = px.bar(mensual, x="Mes", y="Cantidad", color=COL_TIPO, barmode="stack",
              color_discrete_map={"APELACIÓN": "#0078D4", "RECLAMACIÓN": "#D83B01"})
fig4.update_layout(height=280, margin=dict(l=0, r=0, t=10, b=0),
                   legend_title="")
st.plotly_chart(fig4, use_container_width=True)

# ── Top Dependencias ─────────────────────────────────────────────────────────
d1, d2 = st.columns([3, 2])

with d1:
    st.subheader("Top 15 Dependencias")
    top_dep = df[COL_DEP].value_counts().head(15).reset_index()
    top_dep.columns = ["Dependencia", "Cantidad"]
    fig5 = px.bar(top_dep, x="Cantidad", y="Dependencia", orientation="h",
                  color="Cantidad", color_continuous_scale="Teal", text="Cantidad")
    fig5.update_traces(texttemplate="%{text:,}", textposition="outside")
    fig5.update_layout(showlegend=False, coloraxis_showscale=False,
                       height=420, margin=dict(l=0, r=40, t=10, b=0))
    st.plotly_chart(fig5, use_container_width=True)

with d2:
    st.subheader("Top 10 Resolutores")
    top_res = (df[df[COL_RESOLUTOR].notna() & (df[COL_RESOLUTOR] != "-")]
               [COL_RESOLUTOR].value_counts().head(10).reset_index())
    top_res.columns = ["Resolutor", "Expedientes"]
    st.dataframe(top_res, use_container_width=True, hide_index=True,
                 column_config={"Expedientes": st.column_config.ProgressColumn(
                     min_value=0, max_value=int(top_res["Expedientes"].max()),
                     format="%d")})

st.divider()
st.caption("Dashboard GAFA · SUNAT | Datos: SIGERI 19 Ene 2026")
