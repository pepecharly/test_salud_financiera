import streamlit as st
import pandas as pd
import plotly.graph_objects as go

st.set_page_config(page_title="Test de Salud Financiera", layout="centered")

st.title("💰 Test de Salud Financiera Interactivo")

areas = {
    "Gestión de ingresos/gastos": [
        "¿Llevas un registro mensual de tus ingresos y egresos?",
        "¿Tienes un presupuesto mensual establecido?",
        "¿Gastas más de lo que ganas?",
        "¿Tienes gastos hormiga identificados y controlados?",
        "¿Tienes ingresos adicionales a tu sueldo?"
    ],
    "Ahorro e inversión": [
        "¿Ahorras regularmente cada mes?",
        "¿Tienes un fondo de emergencia?",
        "¿Inviertes tu dinero en instrumentos financieros?",
        "¿Revisas y comparas productos de ahorro e inversión?",
        "¿Conoces la diferencia entre ahorro e inversión?"
    ],
    "Deudas y créditos": [
        "¿Tienes deudas que superan el 30% de tus ingresos?",
        "¿Pagas el total de tus tarjetas de crédito cada mes?",
        "¿Has dejado de pagar alguna deuda en el último año?",
        "¿Conoces tu historial crediticio?",
        "¿Has solicitado préstamos para pagar otras deudas?"
    ],
    "Protección y planificación": [
        "¿Tienes un seguro de vida, salud o auto?",
        "¿Tienes una planificación financiera para el futuro?",
        "¿Sabes cuánto necesitas para tu retiro?",
        "¿Conoces los beneficios de los seguros?",
        "¿Has dejado instrucciones financieras para tu familia?"
    ]
}

opciones = {
    "Siempre": 5,
    "A veces": 3,
    "Nunca": 0
}

respuestas = {}
puntaje_por_area = {}

for area, preguntas in areas.items():
    st.subheader(area)
    total_area = 0
    for i, pregunta in enumerate(preguntas, start=1):
        respuesta = st.radio(pregunta, list(opciones.keys()), key=f"{area}-{i}")
        total_area += opciones[respuesta]
    puntaje_por_area[area] = total_area

# Calcular puntaje total ponderado
total_max = 5 * 5 * 4  # 5 preguntas * 5 puntos * 4 áreas = 100
total_usuario = sum(puntaje_por_area.values())
porcentaje_total = round((total_usuario / total_max) * 100, 2)

st.markdown("---")
st.subheader("Resultado General")

st.metric("Puntaje Total", f"{porcentaje_total}/100")

if porcentaje_total <= 40:
    nivel = "🟥 Salud Financiera Frágil"
elif porcentaje_total <= 70:
    nivel = "🟨 Salud Financiera Regular"
else:
    nivel = "🟩 Salud Financiera Sólida"

st.success(f"Nivel: {nivel}")

# Recomendaciones según nivel
if porcentaje_total <= 40:
    recomendaciones = [
        "Reduce tus deudas y evita gastar más de lo que ganas.",
        "Crea un fondo de emergencia de al menos 3 meses.",
        "Evita usar tarjetas de crédito si no puedes pagar el total."
    ]
elif porcentaje_total <= 70:
    recomendaciones = [
        "Establece metas de ahorro claras.",
        "Evalúa opciones de inversión seguras.",
        "Mejora tu historial crediticio."
    ]
else:
    recomendaciones = [
        "Diversifica tus inversiones.",
        "Continúa planificando tu retiro.",
        "Evalúa seguros adicionales que complementen tu protección."
    ]

st.markdown("### Recomendaciones Prioritarias:")
for rec in recomendaciones:
    st.markdown(f"- {rec}")

# Gráfico radial
st.subheader("Desempeño por Área")
fig = go.Figure()

fig.add_trace(go.Scatterpolar(
    r=list(puntaje_por_area.values()),
    theta=list(puntaje_por_area.keys()),
    fill='toself',
    name='Resultado'
))

fig.update_layout(
    polar=dict(
        radialaxis=dict(
            visible=True,
            range=[0, 25]  # 5 preguntas * 5 puntos
        )
    ),
    showlegend=False
)

st.plotly_chart(fig)
