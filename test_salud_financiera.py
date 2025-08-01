import streamlit as st
import plotly.graph_objects as go

st.set_page_config(page_title="Test de Salud Financiera", layout="wide")

st.title("💰 Test de Salud Financiera Interactivo")
st.markdown("Evalúa tu salud financiera en menos de 5 minutos. Las respuestas son confidenciales.")

areas = {
    "Gestión de ingresos/gastos": [
        "¿Tienes un presupuesto mensual?",
        "¿Sabes cuánto gastas al mes?",
        "¿Controlas tus gastos hormiga?",
        "¿Tienes ingresos adicionales al sueldo principal?",
        "¿Revisas tus recibos o estados de cuenta?"
    ],
    "Ahorro e inversión": [
        "¿Tienes un fondo de ahorro?",
        "¿Ahorro al menos 10% de tus ingresos?",
        "¿Tienes inversiones activas (CETES, fondos, etc)?",
        "¿Estás ahorrando para el retiro?",
        "¿Tu ahorro supera 3 meses de tus gastos?"
    ],
    "Deudas y créditos": [
        "¿Pagas el total de tus tarjetas cada mes?",
        "¿Tus deudas no superan el 30% de tu ingreso?",
        "¿Conoces el CAT de tus créditos?",
        "¿Has consolidado tus deudas si es necesario?",
        "¿Tienes créditos que ya no puedes pagar?"
    ],
    "Protección y planificación": [
        "¿Tienes seguro médico o de vida?",
        "¿Tienes un testamento o plan de sucesión?",
        "¿Tienes un fondo de emergencia?",
        "¿Tienes un plan financiero a mediano/largo plazo?",
        "¿Has consultado a un asesor financiero?"
    ]
}

opciones = {
    "Siempre / Sí / Excelente": 5,
    "A veces / Regular": 3,
    "Nunca / No / Deficiente": 1
}

respuestas = {}
puntajes_por_area = {}

for area, preguntas in areas.items():
    st.header(area)
    total = 0
    for i, pregunta in enumerate(preguntas, 1):
        r = st.radio(f"{i}. {pregunta}", list(opciones.keys()), key=f"{area}-{i}")
        respuestas[f"{area}-{i}"] = opciones[r]
        total += opciones[r]
    puntajes_por_area[area] = round(total / (len(preguntas)*5) * 100)

total_final = round(sum(puntajes_por_area.values()) / 4)

st.subheader("📊 Resultados Generales")

col1, col2 = st.columns(2)

with col1:
    st.metric("Puntaje Total", f"{total_final}/100")
    if total_final <= 40:
        nivel = "🔴 Salud Financiera Frágil"
        recs = [
            "Haz un presupuesto mensual.",
            "Elimina gastos innecesarios.",
            "Inicia un fondo de emergencia."
        ]
    elif total_final <= 70:
        nivel = "🟠 Salud Financiera Regular"
        recs = [
            "Refuerza tu ahorro.",
            "Evalúa tus deudas.",
            "Comienza a invertir con bajo riesgo."
        ]
    else:
        nivel = "🟢 Salud Financiera Sólida"
        recs = [
            "Consolida tu patrimonio.",
            "Planea tu retiro.",
            "Diversifica tus inversiones."
        ]

    st.success(f"**Nivel Financiero:** {nivel}")
    st.markdown("### 📌 Recomendaciones:")
    for rec in recs:
        st.markdown(f"- {rec}")

with col2:
    fig = go.Figure(data=go.Scatterpolar(
        r=list(puntajes_por_area.values()),
        theta=list(puntajes_por_area.keys()),
        fill='toself',
        name='Puntaje'
    ))

    fig.update_layout(
        polar=dict(radialaxis=dict(visible=True, range=[0, 100])),
        showlegend=False,
        title="Gráfico Radial por Área"
    )

    st.plotly_chart(fig, use_container_width=True)

