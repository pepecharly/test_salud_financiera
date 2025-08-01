import streamlit as st
import plotly.graph_objects as go

st.set_page_config(page_title="Test de Salud Financiera", layout="centered")

st.title("🧾 Test de Salud Financiera")

# Preguntas divididas por áreas
preguntas_por_area = {
    "Gestión de Ingresos/Gastos": [
        {
            "texto": "¿Llevas un registro detallado de tus ingresos y gastos?",
            "opciones": {"Nunca": 0, "A veces": 1, "Siempre": 2},
        },
        {
            "texto": "¿Haces un presupuesto mensual?",
            "opciones": {"No": 0, "Solo para cosas grandes": 1, "Sí, cada mes": 2},
        },
    ],
    "Ahorro e Inversión": [
        {
            "texto": "¿Tienes un ahorro destinado para emergencias?",
            "opciones": {"No tengo": 0, "Sí, pero es poco": 1, "Sí, cubre 3 meses o más": 2},
        },
        {
            "texto": "¿Inviertes regularmente?",
            "opciones": {"No invierto": 0, "A veces": 1, "Sí, con objetivos claros": 2},
        },
    ],
    "Deudas y Créditos": [
        {
            "texto": "¿Pagas puntualmente tus deudas?",
            "opciones": {"Rara vez": 0, "Algunas veces me atraso": 1, "Siempre a tiempo": 2},
        },
        {
            "texto": "¿Cuánta parte de tus ingresos va a pagar deudas?",
            "opciones": {"Más del 50%": 0, "Entre 30-50%": 1, "Menos del 30%": 2},
        },
    ],
    "Protección y Planificación": [
        {
            "texto": "¿Tienes seguro de vida o gastos médicos?",
            "opciones": {"Ninguno": 0, "Solo uno de ellos": 1, "Ambos y actualizados": 2},
        },
        {
            "texto": "¿Tienes metas financieras a largo plazo?",
            "opciones": {"No tengo": 0, "Algunas sin plan": 1, "Sí, con estrategia": 2},
        },
    ],
}

# Estado de navegación por pantallas
if "area_index" not in st.session_state:
    st.session_state.area_index = 0
if "respuestas" not in st.session_state:
    st.session_state.respuestas = {}

# Áreas ordenadas
areas = list(preguntas_por_area.keys())
area_actual = areas[st.session_state.area_index]
st.subheader(f"Área: {area_actual}")

# Mostrar preguntas de la sección actual
for i, pregunta in enumerate(preguntas_por_area[area_actual]):
    key = f"{area_actual}_{i}"
    respuesta = st.radio(
        pregunta["texto"],
        list(pregunta["opciones"].keys()),
        key=key,
        index=None,
    )
    if respuesta:
        st.session_state.respuestas[key] = pregunta["opciones"][respuesta]

# Botón para avanzar
if st.button("Siguiente área ➡️"):
    if all(f"{area_actual}_{i}" in st.session_state.respuestas for i in range(len(preguntas_por_area[area_actual]))):
        if st.session_state.area_index < len(areas) - 1:
            st.session_state.area_index += 1
            st.experimental_rerun()
        else:
            st.session_state.area_index += 1  # señal de fin
            st.experimental_rerun()
    else:
        st.warning("⚠️ Por favor responde todas las preguntas antes de continuar.")

# Evaluación final
if st.session_state.area_index >= len(areas):
    st.header("🔎 Evaluación Final")
    puntajes_por_area = {}
    total_puntos = 0
    total_maximo = 0

    for area, preguntas in preguntas_por_area.items():
        puntos_area = 0
        max_area = 0
        for i, pregunta in enumerate(preguntas):
            key = f"{area}_{i}"
            puntos_area += st.session_state.respuestas.get(key, 0)
            max_area += max(pregunta["opciones"].values())
        puntajes_por_area[area] = (puntos_area / max_area) * 100
        total_puntos += puntos_area
        total_maximo += max_area

    puntaje_total = (total_puntos / total_maximo) * 100
    st.metric("Tu puntaje total", f"{puntaje_total:.2f} / 100")

    if puntaje_total <= 40:
        nivel = "💔 Salud Financiera Frágil"
    elif puntaje_total <= 70:
        nivel = "⚠️ Salud Financiera Regular"
    else:
        nivel = "✅ Salud Financiera Sólida"
    st.subheader(f"Nivel: {nivel}")

    # Gráfico radar
    fig = go.Figure()
    fig.add_trace(go.Scatterpolar(
        r=list(puntajes_por_area.values()),
        theta=list(puntajes_por_area.keys()),
        fill='toself',
        name='Desempeño por área'
    ))
    fig.update_layout(
        polar=dict(radialaxis=dict(visible=True, range=[0, 100])),
        showlegend=False
    )
    st.plotly_chart(fig)

    # Recomendaciones automáticas
    st.markdown("### 📌 Recomendaciones Prioritarias")
    peores_areas = sorted(puntajes_por_area.items(), key=lambda x: x[1])[:3]
    recomendaciones = {
        "Gestión de Ingresos/Gastos": "Empieza con un presupuesto básico y registra tus gastos diarios. Es el primer paso para tomar control de tu dinero.",
        "Ahorro e Inversión": "Destina un porcentaje fijo de tu ingreso al ahorro cada mes. Incluso una pequeña cantidad constante te dará seguridad.",
        "Deudas y Créditos": "Evita deudas innecesarias. Intenta reducirlas poco a poco y no te endeudes más de lo que puedes pagar.",
        "Protección y Planificación": "Considera contratar un seguro básico y establecer objetivos financieros claros. Te protegerán ante imprevistos.",
    }
    for area, _ in peores_areas:
        st.markdown(f"**🧩 {area}:** {recomendaciones[area]}")

