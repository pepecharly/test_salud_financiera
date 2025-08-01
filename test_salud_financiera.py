import streamlit as st
import plotly.graph_objects as go

# --- Inicialización de sesión ---
if "page" not in st.session_state:
    st.session_state.page = 0
if "answers" not in st.session_state:
    st.session_state.answers = {}

# --- Definición de preguntas por área ---
areas = [
    ("Gestión de Ingresos/Gastos", [
        "¿Llevas un registro de todos tus ingresos y gastos?",
        "¿Sabes cuánto dinero tienes disponible al final del mes?",
        "¿Tu nivel de vida se adapta a tus ingresos?",
        "¿Tienes un presupuesto mensual que respetas?"
    ]),
    ("Ahorro e Inversión", [
        "¿Tienes el hábito de ahorrar regularmente?",
        "¿Tienes un fondo de emergencia (mínimo 3 meses de gastos)?",
        "¿Inviertes parte de tu dinero para hacerlo crecer?",
        "¿Comprendes los productos en los que inviertes?"
    ]),
    ("Deudas y Créditos", [
        "¿Tus deudas superan el 30% de tus ingresos?",
        "¿Pagas puntualmente tus créditos?",
        "¿Comparas antes de contratar un crédito?",
        "¿Conoces el Costo Anual Total (CAT) de tus créditos?"
    ]),
    ("Protección y Planificación", [
        "¿Tienes algún tipo de seguro (vida, salud, auto)?",
        "¿Cuentas con un plan de retiro o pensión?",
        "¿Tienes documentos financieros importantes organizados?",
        "¿Has definido metas financieras claras?"
    ]),
]

opciones = {
    "Nunca": 0,
    "A veces": 1,
    "Siempre": 2
}

# --- Encabezado ---
st.title("🧾 Test de Salud Financiera")
st.markdown("Área actual: **" + areas[st.session_state.page][0] + "**")

# --- Mostrar preguntas de la sección actual ---
with st.form(f"form_{st.session_state.page}"):
    for i, pregunta in enumerate(areas[st.session_state.page][1]):
        key = f"{st.session_state.page}_{i}"
        respuesta = st.radio(pregunta, list(opciones.keys()), key=key, index=-1)
        st.session_state.answers[key] = opciones.get(respuesta, 0)
    submitted = st.form_submit_button("Siguiente")

if submitted:
    if st.session_state.page < len(areas) - 1:
        st.session_state.page += 1
        st.experimental_rerun()

# --- Resultado final ---
if st.session_state.page == len(areas) - 1 and submitted:
    st.markdown("---")
    st.header("📊 Resultados del Test")

    puntajes = [0, 0, 0, 0]
    for idx, (_, preguntas) in enumerate(areas):
        for i in range(len(preguntas)):
            puntajes[idx] += st.session_state.answers.get(f"{idx}_{i}", 0)
        puntajes[idx] = round((puntajes[idx] / (2 * len(preguntas))) * 100)

    total = round(sum(puntajes) / len(puntajes))
    estado = "Salud Sólida ✅" if total > 70 else "Salud Regular ⚠️" if total > 40 else "Salud Financiera Frágil ❌"

    st.subheader(f"Resultado General: {estado}")
    st.metric("Puntaje Total", f"{total}/100")

    # --- Gráfico radial ---
    fig = go.Figure()
    fig.add_trace(go.Scatterpolar(
        r=puntajes,
        theta=[a[0] for a in areas],
        fill='toself',
        name='Puntaje'
    ))
    fig.update_layout(polar=dict(radialaxis=dict(visible=True, range=[0, 100])), showlegend=False)
    st.plotly_chart(fig)

    # --- Recomendaciones extendidas ---
    st.subheader("📌 Recomendaciones Prioritarias:")
    recomendaciones = []

    if puntajes[0] < 70:
        recomendaciones.append("💡 *Mejora tu control de ingresos y gastos.* Te recomiendo usar herramientas como apps de presupuesto o una hoja de cálculo para registrar tus movimientos. Saber en qué gastas te da poder para ahorrar.")
    if puntajes[1] < 70:
        recomendaciones.append("💡 *Refuerza tu cultura del ahorro e inversión.* Considera abrir una cuenta de ahorro separada, automatiza depósitos y aprende sobre instrumentos básicos como CETES o fondos de inversión.")
    if puntajes[2] < 70:
        recomendaciones.append("💡 *Revisa tus deudas.* Si más del 30% de tu ingreso se va a pagar deudas, estás en zona de riesgo. Considera consolidarlas o buscar mejores tasas.")
    if puntajes[3] < 70:
        recomendaciones.append("💡 *Planifica tu futuro.* Un seguro básico y un plan de retiro hacen toda la diferencia a largo plazo. Evalúa tus riesgos y toma medidas preventivas hoy.")

    for r in recomendaciones[:3]:
        st.markdown(r)

    st.success("Puedes volver a comenzar si deseas mejorar tu puntuación.")
