import streamlit as st
import pandas as pd
import time
import matplotlib.pyplot as plt
import math

LAT_RESTAURANTE = 4.682
LON_RESTAURANTE = -74.103

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
if "encuestas" not in st.session_state:
    st.session_state.encuestas = []
if "campañas" not in st.session_state:
    st.session_state.campañas = []

# ----------------------------
# TITULO
# ----------------------------

st.title("🍔 QuickOps")
st.subheader("Bienvenido a QuickOps")

# ----------------------------
# LOGIN
# ----------------------------

rol = st.sidebar.selectbox(
    "Selecciona usuario",
    ["Seleccionar","Gerencia","Colaborador","Comercial","Marketing","Logistica","RRHH","Experiencia"]
)

# =========================================================
# GERENCIA
# =========================================================

if rol == "Gerencia":

    clave = st.sidebar.text_input("Clave gerencial", type="password")

    if clave == "Gerencia123***":

        st.header("📊 Panel de Gerencia")

        opcion_gerencia = st.selectbox(
            "Opciones",
            ["Dashboard","Turnos"]
        )

        # ------------------------
        # DASHBOARD
        # ------------------------

        if opcion_gerencia == "Dashboard":

            col1,col2,col3 = st.columns(3)

            total_pedidos = len(st.session_state.pedidos)
            despachados = len([p for p in st.session_state.pedidos if p["estado"]=="despachado"])
            pendientes = total_pedidos - despachados

            col1.metric("Pedidos totales", total_pedidos)
            col2.metric("Despachados", despachados)
            col3.metric("Pendientes", pendientes)

            st.divider()

            datos = pd.DataFrame({
                "estado":["Pendientes","Despachados"],
                "cantidad":[pendientes,despachados]
            })

            fig, ax = plt.subplots()
            ax.bar(datos["estado"],datos["cantidad"])
            st.pyplot(fig)

        # ------------------------
        # TURNOS (AHORA AQUÍ)
        # ------------------------

        if opcion_gerencia == "Turnos":

            st.subheader("🕒 Gestión de turnos")

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
# =========================================================
# COMERCIAL
# =========================================================

if rol == "Comercial":

    clave = st.sidebar.text_input("Clave comercial", type="password")

    if clave == "Comercial123**":

        st.header("📊 Área Comercial")

        # ------------------------
        # SIMULACIÓN DE VENTAS
        # ------------------------

        ventas = []

        for p in st.session_state.pedidos:
            if p["estado"] == "despachado":

                # Simulación de precios
                if p["tipo"] == "Mesa":
                    ventas.append(15000)
                else:
                    ventas.append(20000)

        total_ventas = sum(ventas)
        num_ventas = len(ventas)

        promedio = total_ventas / num_ventas if num_ventas > 0 else 0

        # ------------------------
        # KPIs
        # ------------------------

        col1, col2, col3 = st.columns(3)

        col1.metric("💰 Ventas totales", f"${total_ventas}")
        col2.metric("🧾 Número de ventas", num_ventas)
        col3.metric("📈 Ticket promedio", f"${round(promedio,0)}")

        st.divider()

        # ------------------------
        # ANÁLISIS DE DESEMPEÑO
        # ------------------------

        st.subheader("📊 Análisis de ventas")

        if total_ventas > 200000:
            st.success("Las ventas son ALTAS ✅")
            estado = "alto"
        elif total_ventas > 100000:
            st.warning("Ventas moderadas ⚠️")
            estado = "medio"
        else:
            st.error("Ventas bajas ❌")
            estado = "bajo"

        # ------------------------
        # GRÁFICO
        # ------------------------

        datos = {
            "Tipo":["Mesa","Domicilio"],
            "Ventas":[
                len([p for p in st.session_state.pedidos if p["tipo"]=="Mesa"]),
                len([p for p in st.session_state.pedidos if p["tipo"]=="Domicilio"])
            ]
        }

        df = pd.DataFrame(datos)

        fig, ax = plt.subplots()
        ax.bar(df["Tipo"], df["Ventas"])

        st.pyplot(fig)

        # ------------------------
        # ESTRATEGIAS
        # ------------------------

        st.subheader("🚀 Estrategias comerciales")

        if estado == "alto":
            st.write("✔ Mantener calidad del servicio")
            st.write("✔ Implementar fidelización de clientes")
            st.write("✔ Promociones por volumen")

        elif estado == "medio":
            st.write("✔ Ofertas en horas valle")
            st.write("✔ Combos promocionales")
            st.write("✔ Publicidad en redes sociales")

        elif estado == "bajo":
            st.write("❗ Descuentos agresivos")
            st.write("❗ Campañas de marketing")
            st.write("❗ Mejorar tiempos de atención")
            st.write("❗ Revisar precios")

# =========================================================
# MARKETING
# =========================================================
if rol == "Marketing":

    clave = st.sidebar.text_input("Clave marketing", type="password")

    if clave == "Marketing123**":

        st.header("📣 Área de Marketing")

        # ------------------------
        # REGISTRO DE CAMPAÑAS
        # ------------------------

        st.subheader("➕ Crear campaña")

        nombre = st.text_input("Nombre de campaña")

        plataforma = st.selectbox(
            "Plataforma",
            ["Instagram","Facebook","TikTok","WhatsApp"]
        )

        dia = st.selectbox(
            "Día publicación",
            ["Lunes","Martes","Miércoles","Jueves","Viernes","Sábado","Domingo"]
        )

        hora = st.selectbox(
            "Hora",
            ["10:00","12:00","14:00","18:00","20:00"]
        )

        contenido = st.text_area("Descripción del contenido")

        estado = st.selectbox(
            "Estado",
            ["Activa","Próxima"]
        )

        if st.button("Guardar campaña"):

            campaña = {
                "nombre": nombre,
                "plataforma": plataforma,
                "dia": dia,
                "hora": hora,
                "contenido": contenido,
                "estado": estado
            }

            st.session_state.campañas.append(campaña)

            st.success("Campaña registrada")

        st.divider()

        # ------------------------
        # CAMPAÑAS ACTIVAS
        # ------------------------

        st.subheader("📢 Campañas activas")

        activas = [c for c in st.session_state.campañas if c["estado"]=="Activa"]

        if activas:
            st.dataframe(pd.DataFrame(activas))
        else:
            st.info("No hay campañas activas")

        # ------------------------
        # PRÓXIMAS CAMPAÑAS
        # ------------------------

        st.subheader("⏳ Próximas campañas")

        proximas = [c for c in st.session_state.campañas if c["estado"]=="Próxima"]

        if proximas:
            st.dataframe(pd.DataFrame(proximas))
        else:
            st.info("No hay campañas programadas")

        st.divider()

        # ------------------------
        # CALENDARIO SEMANAL
        # ------------------------

        st.subheader("📅 Calendario de publicaciones")

        dias = ["Lunes","Martes","Miércoles","Jueves","Viernes","Sábado","Domingo"]

        calendario = {d: "" for d in dias}

        for c in st.session_state.campañas:
            texto = f"{c['nombre']} ({c['plataforma']} - {c['hora']})"
            calendario[c["dia"]] = texto

        df_cal = pd.DataFrame([calendario])

        st.table(df_cal)


# =========================================================
# LOGISTICA PRO
# =========================================================

if rol == "Logistica":

    clave = st.sidebar.text_input("Clave logística", type="password")

    if clave == "Logistica123**":

        st.header("🚚 Logística y Distribución")

        domicilios = [
            p for p in st.session_state.pedidos
            if p["tipo"]=="Domicilio"
        ]

# ------------------------
# KPIs
# ------------------------

        total = len(domicilios)
        despachados = len([p for p in domicilios if p["estado"]=="despachado"])

        tiempo_total = 0

        for p in domicilios:
            if "fin" in p:
                tiempo_total += (p["fin"] - p["inicio"])

        tiempo_promedio = tiempo_total / despachados if despachados > 0 else 0

        eficiencia = (despachados / total)*100 if total > 0 else 0

        col1, col2, col3 = st.columns(3)

        col1.metric("📦 Domicilios", total)
        col2.metric("⏱ Tiempo promedio", round(tiempo_promedio,2))
        col3.metric("📈 Eficiencia %", round(eficiencia,2))

        st.divider()

# ------------------------
# MAPA
# ------------------------

        st.subheader("📍 Mapa de entregas")

        if domicilios:
            # Agregar restaurante al mapa
            df_mapa = pd.DataFrame(domicilios)

            df_restaurante = pd.DataFrame([{
                "latitude": LAT_RESTAURANTE,
                "longitude": LON_RESTAURANTE
            }])

            df_clientes = df_mapa.rename(columns={"lat": "latitude", "lon": "longitude"})

            df_final = pd.concat([df_restaurante, df_clientes])

            st.map(df_final)

        else:
            st.info("No hay domicilios registrados")

# ------------------------
# RUTA SIMULADA
# ------------------------

        st.subheader("🛣 Ruta óptima (simulada)")

        if domicilios:

            rutas = []

            base = {"lat": LAT_RESTAURANTE, "lon": LON_RESTAURANTE}

            for p in domicilios:
                dist = math.sqrt(
                    (p["lat"] - LAT_RESTAURANTE) ** 2 +
                    (p["lon"] - LON_RESTAURANTE) ** 2
                ) * 111

                rutas.append({
                    "Origen": "Restaurante",
                    "Destino": p["cliente"],
                    "Distancia_km": round(dist, 2),
                    "Tiempo_estimado_min": round(dist * 3, 1)
                })

            df_rutas = pd.DataFrame(rutas)

            st.dataframe(df_rutas)

        st.divider()

# ------------------------
# ANÁLISIS INDUSTRIAL
# ------------------------

        st.subheader("🧠 Análisis logístico")

        if eficiencia > 80:
            st.success("Sistema logístico eficiente ✅")

        elif eficiencia > 50:
            st.warning("Eficiencia media ⚠️")

        else:
            st.error("Baja eficiencia ❌")

        st.subheader("🚀 Recomendaciones")

        st.write("✔ Agrupar pedidos por zona")
        st.write("✔ Optimizar rutas de entrega")
        st.write("✔ Reducir tiempos de despacho")
        st.write("✔ Implementar más repartidores en horas pico")


# =========================================================
# RRHH (NUEVO PRO)
# =========================================================

if rol == "RRHH":

    clave = st.sidebar.text_input("Clave RRHH", type="password")

    if clave == "RRHH123**":

        st.header("👥 Gestión de Recursos Humanos")

        seccion = st.selectbox(
            "Selecciona módulo",
            [
                "Planificación y Selección",
                "Gestión Administrativa y Nóminas",
                "Formación y Desarrollo",
                "Evaluación del Desempeño",
                "Relaciones Laborales y Cultura",
                "Cumplimiento Legal y Seguridad"
            ]
        )

# =========================================================
# 1. PLANIFICACIÓN Y SELECCIÓN
# =========================================================

        if seccion == "Planificación y Selección":

            st.subheader("📌 Análisis de puestos")

            puestos = pd.DataFrame({
                "Puesto":["Cajero","Cocinero","Domiciliario"],
                "Funciones":[
                    "Atención al cliente y registro de pedidos",
                    "Preparación de alimentos",
                    "Entrega de pedidos"
                ],
                "Perfil":[
                    "Servicio al cliente, manejo de caja",
                    "Rapidez, higiene, trabajo en equipo",
                    "Responsabilidad, conocimiento de rutas"
                ]
            })

            st.dataframe(puestos)

            st.subheader("🎯 Reclutamiento y selección")
            st.write("✔ Publicación de vacantes")
            st.write("✔ Recepción de hojas de vida")
            st.write("✔ Entrevistas y selección final")

# =========================================================
# 2. GESTIÓN ADMINISTRATIVA
# =========================================================

        if seccion == "Gestión Administrativa y Nóminas":

            st.subheader("📄 Contratos activos")

            contratos = pd.DataFrame({
                "Empleado":["Gino","Brenda","Luisa"],
                "Tipo":["Tiempo completo","Medio tiempo","Tiempo completo"]
            })

            st.dataframe(contratos)

            st.subheader("⏱ Control de horarios")

            if st.session_state.turnos:
                df_turnos = pd.DataFrame(st.session_state.turnos)
                st.dataframe(df_turnos)
            else:
                st.info("No hay turnos registrados")

            st.subheader("💰 Nómina")
            st.write("✔ Pagos mensuales")
            st.write("✔ Seguridad social")
            st.write("✔ Vacaciones")

# =========================================================
# 3. FORMACIÓN Y DESARROLLO
# =========================================================

        if seccion == "Formación y Desarrollo":

            st.subheader("📚 Plan de capacitación")

            st.write("✔ Atención al cliente")
            st.write("✔ Manipulación de alimentos")
            st.write("✔ Optimización de tiempos")

            st.subheader("📈 Plan de carrera")

            st.write("Cajero → Supervisor → Gerente")
            st.write("Cocinero → Jefe de cocina")

# =========================================================
# 4. DESEMPEÑO Y COMPENSACIÓN
# =========================================================

        if seccion == "Evaluación del Desempeño":

            st.subheader("📊 Evaluación del rendimiento")

            empleados = list(st.session_state.empleados.keys())

            datos = []

            for e in empleados:
                productividad = len([p for p in st.session_state.pedidos if p["estado"]=="despachado"])
                datos.append([e, productividad])

            df = pd.DataFrame(datos, columns=["Empleado","Productividad"])

            st.dataframe(df)

            st.subheader("💵 Compensación")
            st.write("✔ Bonos por desempeño")
            st.write("✔ Incentivos por productividad")

# =========================================================
# 5. RELACIONES LABORALES
# =========================================================

        if seccion == "Relaciones Laborales y Cultura":

            st.subheader("🤝 Clima organizacional")

            st.write("✔ Comunicación interna efectiva")
            st.write("✔ Trabajo en equipo")
            st.write("✔ Resolución de conflictos")

            st.subheader("🏢 Cultura organizacional")

            st.write("✔ Valores corporativos")
            st.write("✔ Ambiente laboral positivo")

# =========================================================
# 6. CUMPLIMIENTO LEGAL
# =========================================================

        if seccion == "Cumplimiento Legal y Seguridad":

            st.subheader("⚖️ Normativa laboral")

            st.write("✔ Cumplimiento de leyes laborales")
            st.write("✔ Actualización de políticas")

            st.subheader("🦺 Seguridad y salud")

            st.write("✔ Prevención de riesgos")
            st.write("✔ Protocolos de seguridad")





# =========================================================
# EXPERIENCIA CLIENTE
# =========================================================

if rol == "Experiencia":

    clave = st.sidebar.text_input("Clave cliente", type="password")

    if clave == "Cliente123**":

        st.header("⭐ Experiencia del cliente")

        if st.session_state.encuestas:

            df = pd.DataFrame(st.session_state.encuestas)

            st.subheader("📊 Datos de encuestas")
            st.dataframe(df)

            # Promedio
            promedio = df["calificacion"].mean()
            st.metric("Satisfacción promedio", round(promedio,2))

            st.subheader("🧠 Análisis automático")

            if promedio >= 4:
                st.success("Excelente servicio ✅")
                estado = "alto"
            elif promedio >= 3:
                st.warning("Servicio aceptable ⚠️")
                estado = "medio"
            else:
                st.error("Servicio deficiente ❌")
                estado = "bajo"

            st.subheader("💬 Comentarios de clientes")

            for c in df["comentario"]:
                st.write(f"- {c}")

            st.subheader("🚀 Recomendaciones")

            if estado == "alto":
                st.write("✔ Mantener calidad del servicio")
                st.write("✔ Fidelización de clientes")

            elif estado == "medio":
                st.write("✔ Mejorar tiempos de atención")
                st.write("✔ Capacitación al personal")

            elif estado == "bajo":
                st.write("❗ Revisar procesos operativos")
                st.write("❗ Mejorar atención al cliente")
                st.write("❗ Reducir tiempos de espera")

        else:
            st.info("No hay encuestas registradas aún")
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
        st.subheader("🗓️ Mi horario semanal")

        dias_semana = ["Lunes","Martes","Miércoles","Jueves","Viernes","Sábado","Domingo"]

        # Crear estructura vacía
        horario = {dia: "" for dia in dias_semana}

        # Llenar con los turnos del empleado
        for turno in st.session_state.turnos:
            if turno["empleado"] == nombre:
                horario[turno["dia"]] = f"{turno['horas']} horas"

        # Convertir a DataFrame para mostrar bonito
        df_horario = pd.DataFrame([horario])

        st.table(df_horario)
        area = st.sidebar.selectbox(
            "Área",
            ["Caja","Cocina","Inventario","Encuesta"]
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
                    "inicio":time.time(),
                    "lat": LAT_RESTAURANTE + (0.01 * (len(st.session_state.pedidos) % 5)),
                    "lon": LON_RESTAURANTE + (0.01 * (len(st.session_state.pedidos) % 5))
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
# ENCUESTA DE SATISFACCIÓN
# =========================================================

        if area == "Encuesta":

            st.header("📝 Encuesta de satisfacción del cliente")

            nombre_cliente = st.text_input("Nombre del cliente")

            calificacion = st.slider("Calificación del servicio",1,5)

            comentario = st.text_area("Comentario del cliente")

            if st.button("Guardar encuesta"):

                encuesta = {
                    "cliente": nombre_cliente,
                    "calificacion": calificacion,
                    "comentario": comentario
                }

                st.session_state.encuestas.append(encuesta)

                st.success("Encuesta registrada correctamente")
