import streamlit as st
import pandas as pd
import plotly.graph_objects as go

st.set_page_config(page_title="Test de Salud Financiera", layout="wide")

st.title("🧠 Test de Salud Financiera Interactivo")
st.write("Responde honestamente las siguientes preguntas para conocer tu salud financiera actual.")

areas = {
    "1. Ingresos y gastos": [
        "¿Llevas un registro de tus ingresos y gastos mensualmente?",
        "¿Tienes un presupuesto definido que sigues regularmente?",
        "¿Sabes exactamente cuánto gastas al mes en necesidades básicas?",
        "¿Cuentas con ingresos adicionales además de tu trabajo principal?",
        "¿Tienes claro cuánto necesitas para vivir mensualmente?"
    ],
    "2. Ahorro y emergencias": [
        "¿Tienes un fondo de emergencia equivalente a 3-6 meses de gastos?",
        "¿Ahorras una parte de tus ingresos cada mes?",
        "¿Tus ahorros están en un lugar seguro y accesible?",
        "¿Tienes metas de ahorro claras (ej. viaje, casa, retiro)?",
        "¿Automatizas el ahorro (cuenta separada o domiciliación)?"
    ],
    "3. Deudas y créditos": [
        "¿Tus deudas no superan el 30% de tus ingresos mensuales?",
        "¿Pagas tus créditos a tiempo sin recurrir a intereses altos?",
        "¿Conoces tu historial crediticio (ej. Buró de Crédito)?",
        "¿Comparas opciones antes de adquirir una deuda?",
        "¿Tienes un plan para eliminar tus deudas actuales?"
    ],
    "4. Inversión y futuro financiero": [
        "¿Has empezado a invertir tu dinero?",
        "¿Conoces los diferentes instrumentos de inversión disponibles?",
        "¿Tienes un plan para tu retiro?",
        "¿Cuentas con seguros (vida, gastos médicos, auto, etc.)?",
        "¿Planeas tu futuro financiero a mediano y largo plazo?"
    ]
}

opciones = {
    "Nunca": 0,
    "Rara vez": 1,
    "A veces": 2,
    "Frecuentemente": 3,
    "Siempre": 4
}

respuestas = []
puntos_por_area = {}

for area, preguntas in areas.items():
    st.subheader(area)
    area_total = 0
    for pregunta in preguntas:
        respuesta = st.selectbox(pregunta, options=[""] + list(opciones.keys()), key=pregunta)
        valor = opciones.get(respuesta, 0)
        respuestas.append(valor)
        area_total += valor
    puntos_por_area[area] = area_total

total = sum(respuestas)
maximo = len(respuestas) * 4
porcentaje = round((total / maximo) * 100)

st.markdown("---")
st.subheader("🔎 Resultado del Test")

st.metric(label="Puntaje Total", value=f"{total} / {maximo}", delta=f"{porcentaje}%")

if porcentaje <= 40:
    estado = "🔴 Salud Financiera Frágil"
elif porcentaje <= 70:
    estado = "🟠 Salud Financiera Regular"
else:
    estado = "🟢 Salud Financiera Sólida"

st.markdown(f"### {estado}")

# Recomendaciones motivadoras
st.subheader("📌 Recomendaciones Prioritarias:")

if porcentaje <= 40:
    st.markdown("""
**1. Organiza tus ingresos y gastos ya mismo**  
Llevar un registro diario o semanal te ayudará a visualizar a dónde va tu dinero y detectar fugas innecesarias.

**2. Evita las compras impulsivas y crea un fondo de emergencia**  
Comienza con pequeñas cantidades que puedas guardar. ¡Todo suma!

**3. Busca educación financiera básica y gratuita**  
El conocimiento financiero es el primer paso hacia tu libertad. Usa recursos como CONDUSEF o canales de YouTube confiables.
    """)
elif porcentaje <= 70:
    st.markdown("""
**1. Establece metas de ahorro realistas y automáticas**  
Ahorra para emergencias, retiro, viajes o educación. Automatízalo si puedes.

**2. Ordena tus deudas y mejora tu historial crediticio**  
Empieza por las de mayor interés. Considera consolidarlas si aplica.

**3. Comienza a invertir aunque sea poco**  
Usa plataformas seguras como CETES o fondos para empezar.
    """)
else:
    st.markdown("""
**1. Diversifica tus inversiones y mide el riesgo**  
Evalúa opciones como fondos, bienes raíces o acciones.

**2. Protege tu salud financiera con seguros y testamentos**  
Esto es parte fundamental de tu planeación patrimonial.

**3. Comparte tu experiencia y apoya a otros**  
Enseñar fortalece tu aprendizaje y multiplica el bienestar financiero.
    """)

# Radar chart por área
st.subheader("📊 Diagnóstico por Área")
fig = go.Figure()

fig.add_trace(go.Scatterpolar(
    r=list(puntos_por_area.values()),
    theta=list(puntos_por_area.keys()),
    fill='toself',
    name='Puntaje por Área'
))

fig.update_layout(
    polar=dict(
        radialaxis=dict(visible=True, range=[0, 20])
    ),
    showlegend=False
)

st.plotly_chart(fig, use_container_width=True)
