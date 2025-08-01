import streamlit as st
import plotly.graph_objects as go

st.set_page_config(page_title="Test de Salud Financiera", layout="wide")

st.title("🧮 Test de Salud Financiera")
st.markdown("Responde honestamente cada pregunta. Al final recibirás una evaluación y recomendaciones personalizadas.")

# ===================== CONFIGURACIÓN =====================
areas = {
    "Gestión de ingresos/gastos": [
        "¿Llevas un registro de tus ingresos y egresos?",
        "¿Revisas tu presupuesto mensualmente?",
        "¿Qué haces si te sobra dinero a fin de mes?",
        "¿Qué tan seguido haces compras impulsivas?",
        "¿Sueles planear tus compras grandes con anticipación?"
    ],
    "Ahorro e inversión": [
        "¿Ahorras de forma regular?",
        "¿Tienes un fondo de emergencias?",
        "¿Inviertes parte de tus ahorros?",
        "¿Conoces tu perfil de inversionista?",
        "¿Tienes metas de ahorro definidas?"
    ],
    "Deudas y créditos": [
        "¿Conoces el total de tus deudas?",
        "¿Pagas puntualmente tus créditos?",
        "¿Utilizas más del 30% de tu línea de crédito?",
        "¿Pagas el mínimo en tus tarjetas de crédito?",
        "¿Tienes un plan para liquidar tus deudas?"
    ],
    "Protección y planificación": [
        "¿Tienes seguro de salud o de vida?",
        "¿Has hecho un testamento o plan de herencia?",
        "¿Estás ahorrando para tu retiro?",
        "¿Cuentas con un plan financiero a largo plazo?",
        "¿Revisas tu historial crediticio al menos una vez al año?"
    ]
}

opciones = {
    "Selecciona una opción": None,
    "Nunca": 0,
    "A veces": 1,
    "Siempre": 2
}

pesos_area = {
    "Gestión de ingresos/gastos": 0.25,
    "Ahorro e inversión": 0.25,
    "Deudas y créditos": 0.25,
    "Protección y planificación": 0.25
}

respuestas = {}
puntajes_por_area = {}

# ===================== FORMULARIO =====================
with st.form("test_formulario"):
    for area, preguntas in areas.items():
        st.subheader(area)
        puntajes_por_area[area] = 0
        for pregunta in preguntas:
            seleccion = st.radio(pregunta, list(opciones.keys()), index=0, key=pregunta)
            respuestas[pregunta] = opciones[seleccion]

    submit = st.form_submit_button("Evaluar mi salud financiera")

# ===================== EVALUACIÓN =====================
if submit:
    faltantes = sum(1 for r in respuestas.values() if r is None)
    if faltantes > 0:
        st.warning(f"⚠️ Por favor responde todas las preguntas. Te faltan {faltantes}.")
        st.stop()

    for area, preguntas in areas.items():
        total = sum(respuestas[p] for p in preguntas)
        puntajes_por_area[area] = (total / (len(preguntas) * 2)) * 100  # puntaje sobre 100

    puntaje_total = sum(puntajes_por_area[area] * pesos_area[area] for area in areas)

    if puntaje_total < 41:
        nivel = "🔴 Salud Financiera Frágil"
        recomendaciones = [
            "Empieza por llevar un control básico de tus gastos e ingresos. Tener claridad sobre tu dinero es el primer paso para mejorar.",
            "Evita seguir usando tus tarjetas si estás pagando solo el mínimo. Reestructura tus deudas y busca saldarlas lo antes posible.",
            "Establece una meta sencilla de ahorro, aunque sea mínima. La constancia es más importante que la cantidad al inicio."
        ]
    elif puntaje_total < 71:
        nivel = "🟡 Salud Financiera Regular"
        recomendaciones = [
            "Refuerza tus hábitos de ahorro. Considera separar al menos el 10% de tus ingresos cada mes y busca instrumentos de inversión seguros.",
            "Analiza tus deudas: si alguna te genera intereses altos, busca consolidarlas o negociar mejores condiciones.",
            "Evalúa tus coberturas. Un seguro básico de salud y un fondo de emergencia pueden evitarte grandes problemas."
        ]
    else:
        nivel = "🟢 Salud Financiera Sólida"
        recomendaciones = [
            "¡Felicidades! Ahora enfócate en crecer: revisa instrumentos de inversión a mediano y largo plazo.",
            "Comparte tu conocimiento con tu familia para que también adopten buenos hábitos financieros.",
            "Establece metas financieras grandes (como tu retiro o patrimonio) y planea cómo alcanzarlas con asesoría profesional."
        ]

    # ===================== RESULTADOS =====================
    st.success(f"### Tu nivel financiero es: {nivel}")
    st.markdown(f"**Puntaje total:** {round(puntaje_total, 2)} / 100")

    st.subheader("📊 Desempeño por área")
    fig = go.Figure(data=go.Scatterpolar(
        r=[puntajes_por_area[area] for area in areas],
        theta=list(areas.keys()),
        fill='toself',
        name='Puntaje'
    ))
    fig.update_layout(polar=dict(radialaxis=dict(visible=True, range=[0, 100])), showlegend=False)
    st.plotly_chart(fig, use_container_width=True)

    st.subheader("🧠 Recomendaciones Prioritarias:")
    for rec in recomendaciones:
        st.markdown(f"- {rec}")
