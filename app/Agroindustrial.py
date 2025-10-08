import streamlit as st
import sympy as sp
import numpy as np
import matplotlib.pyplot as plt

# --- G1 — Degradación: Cinética de primer orden y Arrhenius simbólico ---
st.title("G1 — Degradación: Cinética de primer orden en tratamiento térmico")

# Símbolos y ecuaciones
C0, C, k, t, C_lim = sp.symbols('C0 C k t C_lim', real=True, positive=True)
Ea, R, T = sp.symbols('E_a R T', real=True, positive=True)

# Ecuación de vida útil: C(t) = C0 * exp(-k*t)
C_t = C0 * sp.exp(-k * t)

# Despeje de t para C(t) = C_lim
t_sol = sp.solve(sp.Eq(C_t, C_lim), t)[0]

# Expresión simbólica de k(T) por Arrhenius: k = k0 * exp(-Ea/(R*T))
k0 = sp.symbols('k0', real=True, positive=True)
k_T = k0 * sp.exp(-Ea / (R * T))

# --- Interfaz Streamlit ---
st.header("Parámetros cinéticos y condiciones")

C0_val = st.number_input("Concentración inicial (C0)", min_value=0.01, value=1.0)
C_lim_val = st.number_input("Límite de concentración (C_lim)", min_value=0.001, value=0.1)
k0_val = st.number_input("Constante pre-exponencial (k0)", min_value=0.0001, value=1.0)
Ea_val = st.slider("Energía de activación Eₐ [J/mol]", min_value=20000, max_value=120000, value=60000, step=1000)
R_val = st.number_input("Constante de gases R [J/(mol·K)]", min_value=8.0, max_value=9.0, value=8.314, step=0.001, format="%.3f")
T_val = st.slider("Temperatura T [K]", min_value=273, max_value=473, value=353, step=1)

# Cálculo simbólico y numérico
def arrhenius_k(k0, Ea, R, T):
    return float(k0 * np.exp(-Ea / (R * T)))

k_val = arrhenius_k(k0_val, Ea_val, R_val, T_val)

# Vida útil (t) para C(t) = C_lim
t_num = float(sp.solve(sp.Eq(C0_val * sp.exp(-k_val * t), C_lim_val), t)[0])

st.subheader("Despeje simbólico de t para C(t) = C_lim:")
st.latex(sp.latex(sp.Eq(C, C0 * sp.exp(-k * t))))
st.latex(r"t = " + sp.latex(t_sol))

st.subheader("Expresión simbólica de k(T) (Arrhenius):")
st.latex(sp.latex(sp.Eq(k, k_T)))

st.markdown(f"**Valor numérico de k(T):** {k_val:.4e} 1/s")
st.markdown(f"**Vida útil estimada (t):** {t_num:.2f} s")

# Gráfica de C(t)
times = np.linspace(0, t_num * 1.2, 200)
C_curve = C0_val * np.exp(-k_val * times)

fig, ax = plt.subplots()
ax.plot(times, C_curve, label="C(t)")
ax.axhline(C_lim_val, color='r', linestyle='--', label="C_lim")
ax.axvline(t_num, color='g', linestyle=':', label="Vida útil (t)")
ax.set_xlabel("Tiempo [s]")
ax.set_ylabel("Concentración")
ax.set_title("Cinética de primer orden: Degradación de C(t)")
ax.legend()
st.pyplot(fig)

st.caption("Sección G1 — Degradación: Modelos de orden 1 y Arrhenius simbólico para análisis de vida útil y sensibilidad a la temperatura.")
