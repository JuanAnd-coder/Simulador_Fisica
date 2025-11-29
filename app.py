import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

# Constante de Coulomb
k = 9e9

# ---------------------- CLASES Y FUNCIONES ----------------------

class Carga:
    def __init__(self, q, x, y, nombre):
        self.q = q
        self.pos = np.array([x, y])
        self.nombre = nombre

def campo_electrico(q, r_vec):
    r = np.linalg.norm(r_vec)
    if r == 0:
        return np.array([0.0, 0.0])
    return k * q * r_vec / (r ** 3)

def potencial(q, r):
    if r == 0:
        return 0
    return k * q / r

def campo_total(cargas, puntos):
    E_total = np.zeros((len(puntos), 2))
    for i, p in enumerate(puntos):
        for carga in cargas:
            r_vec = p - carga.pos
            E_total[i] += campo_electrico(carga.q, r_vec)
    return E_total

def potencial_total(cargas, puntos):
    V = np.zeros(len(puntos))
    for i, p in enumerate(puntos):
        for carga in cargas:
            r = np.linalg.norm(p - carga.pos)
            V[i] += potencial(carga.q, r)
    return V

# ---------------------- INTERFAZ STREAMLIT ----------------------

st.set_page_config(page_title="Simulador de Campos Eléctricos", layout="wide")
st.title("⚡ Simulador Interactivo de Campos Eléctricos en Dispositivos Computacionales")
st.markdown(
    "Visualiza cómo los campos eléctricos y potenciales determinan el funcionamiento de componentes "
    "como memorias, transistores, buses y pantallas."
)

# ---------------------- SELECCIÓN DE ESCENARIO ----------------------

st.sidebar.header("⚙️ Selección de Escenario")
escenario = st.sidebar.selectbox(
    "Selecciona un escenario:",
    ["Personalizado", "Memoria RAM", "Transistor MOSFET", "Bus de Datos", "Pantalla LCD"]
)

cargas = []

# ---------------------- CONFIGURACIÓN DE CADA ESCENARIO ----------------------

if escenario == "Personalizado":
    st.sidebar.subheader("🔧 Configuración Manual")
    n_cargas = st.sidebar.slider("Número de cargas", 1, 3, 2, key="num_cargas")
    for i in range(n_cargas):
        st.sidebar.subheader(f"Carga {i+1}")
        q = st.sidebar.number_input(f"Valor de q{i+1} (C)", value=1e-9 if i == 0 else -1e-9, format="%.1e", key=f"q_{i}")
        x = st.sidebar.slider(f"Posición X{i+1}", -1.0, 1.0, (-0.5 if i == 0 else 0.5), key=f"x_{i}")
        y = st.sidebar.slider(f"Posición Y{i+1}", -1.0, 1.0, 0.0, key=f"y_{i}")
        cargas.append(Carga(q, x, y, f"q{i+1}"))

elif escenario == "Memoria RAM":
    st.sidebar.markdown("**Campo entre dos placas paralelas (bit cargado).**")
    cargas = [
        Carga(2e-9, 0.0, 1.0, "Placa Superior (+)"),
        Carga(-2e-9, 0.0, -1.0, "Placa Inferior (-)")
    ]

elif escenario == "Transistor MOSFET":
    st.sidebar.markdown("**Campo entre compuerta, fuente y drenador.**")
    cargas = [
        Carga(2e-9, -0.8, 0.0, "Fuente (+)"),
        Carga(-2e-9, 0.8, 0.0, "Drenador (-)"),
        Carga(1e-9, 0.0, 0.8, "Compuerta (G)")
    ]

elif escenario == "Bus de Datos":
    st.sidebar.markdown("**Varias líneas cargadas paralelas (transmisión de señales).**")
    cargas = [
        Carga(1e-9, -1.0, 0.5, "Línea 1 (+)"),
        Carga(1e-9, 0.0, 0.5, "Línea 2 (+)"),
        Carga(1e-9, 1.0, 0.5, "Línea 3 (+)"),
        Carga(-1e-9, 0.0, -0.5, "Plano Tierra (-)")
    ]

elif escenario == "Pantalla LCD":
    st.sidebar.markdown("**Campo alterno entre placas que orienta cristales líquidos.**")

    if "polaridad" not in st.session_state:
        st.session_state.polaridad = 1

    if st.sidebar.button("🔁 Alternar Polaridad"):
        st.session_state.polaridad *= -1

    cargas = [
        Carga(2e-9 * st.session_state.polaridad, 0.0, 1.0, "Placa Superior (+)"),
        Carga(-2e-9 * st.session_state.polaridad, 0.0, -1.0, "Placa Inferior (-)")
    ]

    st.sidebar.write(f"**Polaridad actual:** {'Normal' if st.session_state.polaridad > 0 else 'Invertida'}")

# ---------------------- PARÁMETROS DE GRILLA ----------------------

xmin, xmax, ymin, ymax = -2, 2, -2, 2
nx, ny = 60, 60
x = np.linspace(xmin, xmax, nx)
y = np.linspace(ymin, ymax, ny)
X, Y = np.meshgrid(x, y)
puntos = np.vstack([X.ravel(), Y.ravel()]).T

E = campo_total(cargas, puntos)
Ex = E[:, 0].reshape(X.shape)
Ey = E[:, 1].reshape(Y.shape)
V = potencial_total(cargas, puntos).reshape(X.shape)
magE = np.sqrt(Ex**2 + Ey**2)

# ---------------------- GRÁFICAS ----------------------

col1, col2 = st.columns(2)

# Campo eléctrico
with col1:
    fig, ax = plt.subplots(figsize=(6, 6))
    color = np.log10(magE + 1e-12)
    ax.streamplot(X, Y, Ex, Ey, color=color, cmap='plasma', linewidth=1)
    
    for c in cargas:
        color_c = 'red' if c.q > 0 else 'blue'
        ax.scatter(c.pos[0], c.pos[1], c=color_c, s=150, edgecolors='k')
        ax.text(c.pos[0]+0.05, c.pos[1]+0.05, c.nombre, fontsize=9)
    
    ax.set_xlim(xmin, xmax)
    ax.set_ylim(ymin, ymax)
    ax.set_aspect('equal')
    ax.set_title(" Líneas de Campo Eléctrico")
    st.pyplot(fig)

# Potencial eléctrico
with col2:
    fig2, ax2 = plt.subplots(figsize=(6, 6))
    cont = ax2.contourf(X, Y, V, levels=25, cmap='coolwarm')
    fig2.colorbar(cont, ax=ax2, label='Potencial (V)')
    ax2.set_title("Mapa de Potencial Eléctrico")
    ax2.set_xlabel("x (m)")
    ax2.set_ylabel("y (m)")
    st.pyplot(fig2)

# ---------------------- DESCRIPCIÓN DEL ESCENARIO ----------------------

# ---------------------- DESCRIPCIÓN E IMÁGENES ----------------------
st.markdown("---")
st.subheader("📘 Explicación del Escenario")

if escenario == "Memoria RAM":
    col1, col2 = st.columns([1, 1.2])
    with col1:
        st.image("assets/RAM.png", caption="Estructura básica de una celda de memoria RAM", use_container_width=True)
    with col2:
        st.write("""
        En la **Memoria RAM**, cada celda actúa como un pequeño capacitor.
        Las **dos placas cargadas** almacenan energía en forma de campo eléctrico.
        - Bit **1**: el capacitor está cargado.
        - Bit **0**: el capacitor está descargado.
        
        El campo eléctrico entre las placas permite escribir y leer información de forma casi instantánea.
        """)

elif escenario == "Transistor MOSFET":
    col1, col2 = st.columns([1, 1.2])
    with col1:
        st.image("assets/MOSFET.png", caption="Estructura del transistor MOSFET (Fuente, Compuerta, Drenador)", use_container_width=True)
    with col2:
        st.write("""
        En un **Transistor MOSFET**, la **compuerta (G)** controla el paso de corriente entre la **fuente (S)** y el **drenador (D)**.
        Al aplicar un campo eléctrico en la compuerta, se genera o bloquea el canal conductor.
        
        Este principio de control por campo eléctrico es la base del funcionamiento de los **microprocesadores**.
        """)

elif escenario == "Bus de Datos":
    col1, col2 = st.columns([1, 1.2])
    with col1:
        st.image("assets/BusDatos.png", caption="Líneas paralelas que transportan señales eléctricas (bus de datos)", use_container_width=True)
    with col2:
        st.write("""
        Un **Bus de Datos** transmite información mediante varias líneas cargadas en paralelo.
        Cada línea puede tener un potencial diferente, representando bits individuales.
        
        El campo eléctrico entre las líneas puede generar interferencia, lo cual se mitiga usando **tierra** o blindajes intermedios.
        """)

elif escenario == "Pantalla LCD":
    col1, col2 = st.columns([1, 1.2])
    with col1:
        st.image("assets/LCD.png", caption="Celda de cristal líquido entre dos placas transparentes", use_container_width=True)
    with col2:
        st.write("""
        En una **Pantalla LCD**, un campo eléctrico alterno cambia la orientación de moléculas de cristal líquido.
        Este cambio altera la cantidad de luz que atraviesa el píxel, produciendo diferentes colores o niveles de brillo.
        """)

else:
    st.write("""
    En el modo **Personalizado**, puedes definir tus propias cargas y posiciones
    para observar cómo se forman los campos eléctricos resultantes.
    """)
