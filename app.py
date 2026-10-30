import streamlit as st
import matplotlib.pyplot as plt

# Configuración de la página (Optimizado para pantallas móviles)
st.set_page_config(
    page_title="Finanzas Pro - Crédito",
    page_icon="📊",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# Estilo personalizado para el modo oscuro y tarjetas limpias
st.markdown("""
    <style>
    .main { background-color: #0f1116; }
    div[data-testid="stMetricValue"] { font-size: 24px !important; font-weight: bold; color: #2ecc71; }
    div[data-testid="stMetricLabel"] { font-size: 12px !important; color: #b3b3b3; }
    </style>
""", unsafe_allow_html=True)

st.title("📊 Dashboard de Crédito Pro")
st.caption("Optimizado para el mercado financiero colombiano")

st.write("---")

# --- SECCIÓN DE ENTRADA DE DATOS ---
st.subheader("⚙️ Configuración del Préstamo")

# Inputs nativos móviles (fáciles de tocar en iOS)
monto_prestamo = st.number_input("Monto del préstamo ($ COP)", min_value=100000, value=20000000, step=1000000, format="%d")
tasa_ea = st.number_input("Tasa de interés (% Efectiva Anual)", min_value=0.1, value=22.0, step=0.5, format="%.2f")
plazo_meses = st.slider("Plazo del crédito (Meses)", min_value=1, max_value=72, value=36)

# --- CÁLCULOS MATEMÁTICOS ---
tasa_mensual = ((1 + (tasa_ea / 100)) ** (1 / 12)) - 1
cuota_mensual = (monto_prestamo * tasa_mensual) / (1 - (1 + tasa_mensual) ** (-plazo_meses))

# --- GENERACIÓN DE DATOS Y GRÁFICO ---
saldo_restante = monto_prestamo
total_intereses = 0
meses_eje = []
capital_acumulado_eje = []
intereses_acumulados_eje = []
interes_acumulado_temp = 0

datos_tabla = []

for mes in range(1, plazo_meses + 1):
    interes_mes = saldo_restante * tasa_mensual
    capital_mes = cuota_mensual - interes_mes
    saldo_restante -= capital_mes
    
    total_intereses += interes_mes
    interes_acumulado_temp += interes_mes
    
    meses_eje.append(mes)
    capital_acumulado_eje.append(monto_prestamo - max(0, saldo_restante))
    intereses_acumulados_eje.append(interes_acumulado_temp)
    
    datos_tabla.append([
        mes,
        f"$ {cuota_mensual:,.0f}",
        f"$ {capital_mes:,.0f}",
        f"$ {interes_mes:,.0f}",
        f"$ {max(0, saldo_restante):,.0f}"
    ])

total_pagar = monto_prestamo + total_intereses

# --- MOSTRAR RESULTADOS (TARJETAS KPI) ---
st.write("---")
st.subheader("📈 Resumen del Crédito")

col1, col2 = st.columns(2)
with col1:
    st.metric(label="CUOTA MENSUAL ESTIMADA", value=f"$ {cuota_mensual:,.2f}")
with col2:
    st.metric(label="TOTAL INTERESES A PAGAR", value=f"$ {total_intereses:,.2f}")

st.metric(label="DESEMBOLSO TOTAL FINAL", value=f"$ {total_pagar:,.2f}")

# --- SECCIÓN GRÁFICA ---
st.write("---")
st.subheader("📊 Estructura de Pagos en el Tiempo")

fig, ax = plt.subplots(figsize=(6, 3.5))
fig.patch.set_facecolor('#0f1116')
ax.set_facecolor('#151922')

# Barras apiladas
ax.bar(meses_eje, capital_acumulado_eje, label="Capital Recuperado", color="#2ecc71", alpha=0.9)
ax.bar(meses_eje, intereses_acumulados_eje, bottom=capital_acumulado_eje, label="Intereses Pagados", color="#e74c3c", alpha=0.9)

ax.set_xlabel("Mes de amortización", color="#b3b3b3", fontsize=8)
ax.set_ylabel("Valor acumulado ($)", color="#b3b3b3", fontsize=8)
ax.tick_params(colors="white", labelsize=7)
ax.legend(facecolor="#151922", edgecolor="none", labelcolor="white", loc="upper left", fontsize=7)
ax.grid(True, linestyle="--", alpha=0.05, color="white")

st.pyplot(fig)

# --- TABLA DETALLADA ---
st.write("---")
with st.expander("📋 Ver Tabla de Amortización Completa"):
    import pandas as pd
    df = pd.DataFrame(datos_tabla, columns=["Mes", "Cuota", "Abono Capital", "Interés", "Saldo Restante"])
    st.dataframe(df, use_container_width=True, hide_index=True)