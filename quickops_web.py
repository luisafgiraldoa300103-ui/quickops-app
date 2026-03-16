import streamlit as st
import pandas as pd
import time
import matplotlib.pyplot as plt

st.set_page_config(page_title="QuickOps", layout="wide")

# ----------------------------
# ESTADO GLOBAL
# ----------------------------

if "pedidos" not in st.session_state:
    st.session_state.pedidos = []

if "inventario" not in st.session_state:
    st.session_state.inventario = {
        "Pan":50,
        "Carne":40,
        "Papas":60,
        "Bebidas":30
    }

if "empleados" not in st.session_state:
    st.session_state.empleados = {
        "Gino Florez":"Gino123",
        "Brenda Torres":"Brenda123",
        "Luisa Giraldo":"123"
    }

if "turnos" not in st.session_state:
    st.session_state.turnos = []

# ----------------------------
# TITULO
# ----------------------------

st.title("🍔 QuickOps")
st.subheader("Sistema de gestión operativa para restaurantes")

# ----------------------------
# LOGIN
# ----------------------------

rol = st.sidebar.selectbox(
    "Selecciona usuario",
    ["Seleccionar","Gerencia","Colaborador"]
)

# =========================================================
# GERENCIA
# =========================================================

if rol == "Gerencia":

    clave = st.sidebar.text_input("Clave gerencial", type="password")

    if clave == "Gerencia123***":

        st.header("📊 Dashboard Gerencial")

        col1,col2,col3 = st.columns(3)

        total_pedidos = len(st.session_state.pedidos)

        col1.metric("Pedidos totales", total_pedidos)

        despachados = len([p for p in st.session_state.pedidos if p["estado"]=="despachado"])
        col2.metric("Pedidos despachados", despachados)

        pendientes = total_pedidos - despachados
        col3.metric("Pedidos pendientes", pendientes)

        st.divider()

        # ------------------------
        # GRAFICO PEDIDOS
        # ------------------------

        st.subheader("📈 Estado de pedidos")

        datos = pd.DataFrame({
            "estado":["Pendientes","Despachados"],
            "cantidad":[pendientes,despachados]
        })

        fig, ax = plt.subplots()
        ax.bar(datos["estado"],datos["cantidad"])

        st.pyplot(fig)

        # ------------------------
        # INVENTARIO
        # ------------------------

        st.subheader("📦 Inventario")

        productos = list(st.session_state.inventario.keys())
        valores = list(st.session_state.inventario.values())

        fig2, ax2 = plt.subplots()
        ax2.bar(productos,valores)

        st.pyplot(fig2)

        # ------------------------
        # TIEMPOS DE ATENCION
        # ------------------------

        tiempos = []

        for p in st.session_state.pedidos:
            if "fin" in p:
                tiempos.append(p["fin"] - p["inicio"])

        if tiempos:
            promedio = sum(tiempos)/len(tiempos)
            st.metric("⏱ Tiempo promedio atención (seg)",round(promedio,2))

# =========================================================
# COLABORADOR
# =========================================================

if rol == "Colaborador":

    nombre = st.sidebar.selectbox(
        "Empleado",
        list(st.session_state.empleados.keys())
    )

    clave = st.sidebar.text_input("Clave",type="password")

    if st.session_state.empleados.get(nombre) == clave:

        area = st.sidebar.selectbox(
            "Área",
            ["Caja","Cocina","Inventario","Turnos"]
        )

# =========================================================
# CAJA
# =========================================================

        if area == "Caja":

            st.header("🧾 Registro de pedidos")

            cliente = st.text_input("Nombre cliente")

            tipo = st.selectbox(
                "Tipo pedido",
                ["Mesa","Domicilio"]
            )

            direccion = ""
            mesa = ""

            if tipo == "Mesa":
                mesa = st.number_input("Número mesa",1,20)

            if tipo == "Domicilio":
                direccion = st.text_input("Dirección")

            if st.button("Registrar pedido"):

                pedido = {
                    "cliente":cliente,
                    "tipo":tipo,
                    "direccion":direccion,
                    "mesa":mesa,
                    "estado":"pendiente",
                    "inicio":time.time()
                }

                st.session_state.pedidos.append(pedido)

                st.success("Pedido registrado")

            st.subheader("📋 Cola de pedidos")

            df = pd.DataFrame(st.session_state.pedidos)

            st.dataframe(df)

# =========================================================
# COCINA
# =========================================================

        if area == "Cocina":

            st.header("👨‍🍳 Pedidos en cocina")

            for i,p in enumerate(st.session_state.pedidos):

                if p["estado"]=="pendiente":

                    st.write(f"Pedido de {p['cliente']}")

                    if st.button(f"Despachar {p['cliente']}",key=i):

                        st.session_state.pedidos[i]["estado"]="despachado"
                        st.session_state.pedidos[i]["fin"]=time.time()

                        st.success("Pedido despachado")

# =========================================================
# INVENTARIO
# =========================================================

        if area == "Inventario":

            st.header("📦 Gestión de inventario")

            df = pd.DataFrame(
                list(st.session_state.inventario.items()),
                columns=["Producto","Stock"]
            )

            st.dataframe(df)

            producto = st.selectbox(
                "Producto",
                list(st.session_state.inventario.keys())
            )

            cantidad = st.number_input("Cantidad agregar",1,100)

            if st.button("Actualizar inventario"):

                st.session_state.inventario[producto]+=cantidad

                st.success("Inventario actualizado")

            productos = list(st.session_state.inventario.keys())
            valores = list(st.session_state.inventario.values())

            fig, ax = plt.subplots()
            ax.bar(productos,valores)

            st.pyplot(fig)

# =========================================================
# TURNOS
# =========================================================

        if area == "Turnos":

            st.header("🕒 Gestión de turnos")

            empleado = st.text_input("Nombre empleado")

            dia = st.selectbox(
                "Día",
                ["Lunes","Martes","Miércoles","Jueves","Viernes","Sábado","Domingo"]
            )

            horas = st.number_input("Horas turno",1,12)

            if st.button("Registrar turno"):

                turno = {
                    "empleado":empleado,
                    "dia":dia,
                    "horas":horas
                }

                st.session_state.turnos.append(turno)

                st.success("Turno registrado")

            df_turnos = pd.DataFrame(st.session_state.turnos)

            st.dataframe(df_turnos)