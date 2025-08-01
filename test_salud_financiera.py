import streamlit as st
import plotly.graph_objects as go

# Configurar la aplicación
st.set_page_config(page_title="Test de Salud Financiera", layout="centered")
st.title("🧾 Test de Salud Financiera")

# Definir áreas y preguntas
areas = {
    "Gestión de Ingresos/Gastos": [
        ("¿Llevas un registro detallado de tus ingresos y gastos?", {"Nunca": 0, "A veces": 1, "Siempre": 2}),
        ("¿Haces un presupuesto mensual?", {"No": 0, "Solo para cosas grandes": 1, "Sí, cada mes": 2}),
    ],
    "Ahorro e Inversión": [
        ("¿Ahorras regularmente una parte de tus ingresos?", {"Nunca": 0, "A veces": 1, "Siempre": 2}),
        ("¿Tienes alguna inversión en marcha?", {"Ninguna": 0, "Poca": 1, "Sí, diversificada": 2}),
    ],
    "Deudas y Créditos": [
        ("¿Tienes deudas que te cuesta pagar?", {"Sí, muchas": 0, "Algunas": 1, "Ninguna o manejables": 2}),
        ("¿Pagas tus tarjetas de crédito a tiempo?", {"No": 0, "A veces": 1, "Siempre": 2}),
    ],
    "Protección y Planificación": [
        ("¿Cuentas con un seguro de gastos médicos o vida?", {"Ninguno": 0, "Uno de ellos": 1, "Ambos": 2}),
        ("¿Tienes un fondo de emergencia?", {"No": 0, "En proceso": 1, "Sí, cubre 3-6 meses": 2}),
    ]
}

pesos = {
    "Gestión de Ingresos/Gastos": 0.25,
    "Ahorro e Inversión": 0.25,
    "Deudas y Créditos": 0.25,
    "Protección y Planificación": 0.25
}

# Inicializar estado
if 'area_index' not in st.session_state:
    st.session_state.area_index = 0
if 'respuestas' not in st.session_state:
    st.session_state.respuestas = {}

# Obtener el área actual
area_actual = list(areas.keys())[st.session_state.area_index]
st.subheader(f"Área: {area_actual}")

# Mostrar preguntas
for i, (pregunta, opciones) in enumerate(areas[area_actual]):
    key = f"{area_actual}_{i}"
    respuesta = st.radio(pregunta, list(opciones.keys()), key=key, index=None)
    if respuesta:
        st.session_state.respuestas[key] = opciones[respuesta]

# Navegación
col1, col2 = st.columns(2)
if col1.button("⏮️ Anterior", disabled=st.session_state.area_index == 0):
    st.session_state.area_index -= 1
    st.experimental_rerun()

if col2.button("⏭️ Siguiente", disabled=st.session_state.area_index == len(areas) - 1):
    st.session_state.area_index += 1
    st.experimental_rerun()

# Mostrar resultados al final
if st.session_state.area_index == len(areas) - 1:
    if st.button("🧠 Evaluar Salud Financiera"):
        resultados = {}
        total = 0
        for area, preguntas in areas.items():
            suma = sum([st.session_state.respuestas.get(f"{area}_{i}", 0) for i in range(len(preguntas))])
            maximo = len(preguntas) * 2
            porcentaje = (suma / maximo) * 100
            resultados[area] = porcentaje
            total += porcentaje * pesos[area]

        # Clasificación
        if total < 40:
            estado = "🔴 Salud financiera frágil"
            recomendaciones = [
                "Comienza por registrar todos tus gastos e ingresos durante un mes.",
                "Evita el uso excesivo de crédito y prioriza saldar tus deudas más caras.",
                "Crea un fondo de emergencia aunque sea con pequeñas cantidades mensuales."
            ]
        elif total < 70:
            estado = "🟡 Salud financiera regular"
            recomendaciones = [
                "Refuerza tu hábito de ahorro mensual automatizando transferencias.",
                "Diversifica tus inversiones para que tu dinero no pierda valor.",
                "Evalúa tus seguros y refuerza tu protección financiera personal."
            ]
        else:
            estado = "🟢 Salud financiera sólida"
            recomendaciones = [
                "¡Excelente! Mantén tus hábitos y comparte tu experiencia con otros.",
                "Revisa tus metas a largo plazo y considera inversiones estratégicas.",
                "Evalúa construir patrimonio o emprendimiento para crecer financieramente."
            ]

        # Mostrar resultado general
        st.markdown(f"### Resultado General: {estado}")
        st.markdown(f"**Puntaje total:** {round(total, 2)} / 100")

        # Mostrar gráfico radial
        fig = go.Figure(data=go.Scatterpolar(
            r=list(resultados.values()),
            theta=list(resultados.keys()),
            fill='toself',
            name='Salud Financiera'
        ))
        fig.update_layout(polar=dict(radialaxis=dict(visible=True, range=[0, 100])), showlegend=False)
        st.plotly_chart(fig)

        # Mostrar recomendaciones
        st.markdown("### 📌 Recomendaciones Prioritarias:")
        for rec in recomendaciones:
            st.markdown(f"- {rec}")
