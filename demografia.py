# -----------------------------------------------------------
# Dashboard Demográfico de Antioquia - Censo 2018
# -----------------------------------------------------------

import streamlit as st
import pandas as pd
import altair as alt
import warnings
warnings.filterwarnings('ignore')

# -----------------------------------------------------------
# Configuración general de la página
# -----------------------------------------------------------
st.set_page_config(
    page_title="Análisis Demográfico de Antioquia",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# -----------------------------------------------------------
# Encabezado
# -----------------------------------------------------------
st.title("📊 Análisis Demográfico del Departamento de Antioquia")
st.subheader("Indicadores de Mortalidad y Fecundidad (2023) y Migración (2018)")
st.markdown("---")

# -----------------------------------------------------------
# Sidebar de navegación
# -----------------------------------------------------------
st.sidebar.title("🧭 Navegación")
section = st.sidebar.radio(
    "Selecciona una sección:",
    [
        "📋 Población (2018)",
        "💀 Mortalidad (2023)",
        "👶 Fecundidad (2023)",
        "🚶‍♂️ Migración (2018)",
    ]
)

# -----------------------------------------------------------
# SECCIÓN: Población (2018)
# -----------------------------------------------------------
if section == "📋 Población (2018)":
    st.header("📊 Datos Demográficos - Censo 2018 (Antioquia) - Indicadores Departamentales")

    # ---------------------------
    # 1️⃣ Datos base
    # ---------------------------
    data_tot = {
        "Edad": [
            "Total", "0 a 4", "5 a 9", "10 a 14", "15 a 19", "20 a 24",
            "25 a 29", "30 a 34", "35 a 39", "40 a 44", "45 a 49",
            "50 a 54", "55 a 59", "60 a 64", "65 a 69", "70 a 74",
            "75 a 79", "80 a 84", "85 y más"
        ],
        "Total": [
            5974788,345333,381885,450754,498542,541149,525871,473849,
            449108,367163,364200,382513,339892,271563,204426,145598,
            102126,67557,63259
        ],
        "Hombres": [
            2885383,176817,195622,230481,254659,272044,262798,234582,
            217593,172252,167730,174935,153994,121372,90607,63813,
            44037,27764,24283
        ],
        "Mujeres": [
            3089405,168516,186263,220273,243883,269105,263073,239267,
            231515,194911,196470,207578,185898,150191,113819,81785,
            58089,39793,38976
        ]
    }
    df_tot = pd.DataFrame(data_tot)

    # ---------------------------
    # 2️⃣ Porcentajes sobre total
    # ---------------------------
    total_pop = df_tot.loc[df_tot["Edad"] == "Total", "Total"].values[0]
    df_tot["% Total"] = (df_tot["Total"] / total_pop) * 100
    df_tot["% Hombres"] = (df_tot["Hombres"] / total_pop) * 100
    df_tot["% Mujeres"] = (df_tot["Mujeres"] / total_pop) * 100
    df_tot = df_tot.round(2)

    # --- 3) Layout similar al estilo que tenías: dos columnas ---
    col1, col2 = st.columns([1.6, 1])

    # --------- COLUMNA IZQUIERDA: tabla + gráficos -------------
    with col1:
        st.subheader("📋 Cuadro de población por grupos quinquenales (2018)")
        st.dataframe(df_tot, use_container_width=True)
        st.markdown("---")

        # Funciones gráficas
        def plot_piramide(df_input, title="Pirámide Poblacional - Antioquia (2018)"):
            # Filtrar fila "Total"
            dfp = df_input[df_input["Edad"] != "Total"].copy()
            
            # Hombres en negativo para que queden a la izquierda
            dfp["% Hombres (neg)"] = -dfp["% Hombres"]
            
            # Escalas compartidas
            x_scale = alt.Scale(domain=[-dfp["% Hombres"].max()*1.1, dfp["% Mujeres"].max()*1.1])

            # Hombres (izquierda)
            left = alt.Chart(dfp).mark_bar(color="#1f2eb4").encode(
                x=alt.X("% Hombres (neg):Q", scale=x_scale, title="% Hombres"),
                y=alt.Y("Edad:O", sort=alt.SortField("Edad", order="descending")),
                tooltip=["Edad", "% Hombres"]
            )

            # Mujeres (derecha)
            right = alt.Chart(dfp).mark_bar(color="#eb0eff").encode(
                x=alt.X("% Mujeres:Q", scale=x_scale, title="% Mujeres"),
                y=alt.Y("Edad:O", sort=alt.SortField("Edad", order="descending")),
                tooltip=["Edad", "% Mujeres"]
            )

            # Combinar
            chart = (left + right).properties(
                title=title,
                width=500,
                height=500
            ).configure_title(
                fontSize=16,
                anchor="middle"
            ).configure_axis(
                labelFontSize=12,
                titleFontSize=14
            )
            
            return chart

        def plot_distribucion(df_input, title="Distribución porcentual por edad (2018)"):
            dfp = df_input[df_input["Edad"] != "Total"].copy()
            chart = (
                alt.Chart(dfp)
                .mark_line(point=True, color="#009e73")
                .encode(
                    x=alt.X("Edad:O", sort=None, title="Grupo de edad"),
                    y=alt.Y("% Total:Q", title="% del total poblacional"),
                    tooltip=["Edad", "% Total"]
                )
                .properties(title=title, width=520, height=300)
            )
            return chart

        st.subheader("🧭 Visualizaciones")
        st.altair_chart(plot_piramide(df_tot), use_container_width=True)
        st.markdown("")
        st.altair_chart(plot_distribucion(df_tot), use_container_width=True)

    # --------- COLUMNA DERECHA: índices y distribución -------------
    with col2:
        st.subheader("📘 Resumen Poblacional (Censo 2018)")

        # Población por grupos de edad
        youth = df_tot.loc[df_tot["Edad"].isin(["0 a 4", "5 a 9", "10 a 14"]), "Total"].sum()
        working = df_tot.loc[df_tot["Edad"].isin([
            "15 a 19", "20 a 24", "25 a 29", "30 a 34", "35 a 39", "40 a 44",
            "45 a 49", "50 a 54", "55 a 59", "60 a 64"
        ]), "Total"].sum()
        elderly = df_tot.loc[df_tot["Edad"].isin([
            "65 a 69", "70 a 74", "75 a 79", "80 a 84", "85 y más"
        ]), "Total"].sum()

        st.metric("Población total (Censo 2018)", f"{int(total_pop):,}")
        st.markdown(f"- Población 0–14 años: **{int(youth):,}**")
        st.markdown(f"- Población 15–64 años: **{int(working):,}**")
        st.markdown(f"- Población 65 años y más: **{int(elderly):,}**")
        st.markdown("---")

        st.subheader("🧮 Indicadores Demográficos Oficiales (Censo 2018)")
        st.markdown("**Superficie y densidad poblacional**")
        st.markdown("- Superficie del Departamento (km²): **63.612**")
        st.markdown("- Densidad poblacional en el departamento de Antioquia años 2018: **93,9 hab/km²**")
        st.markdown("---")
        st.markdown("**Índices de Dependencia (ET - 2018)**")
        st.markdown("- Índice de dependencia total: **51,56**")
        st.markdown("- Índice de dependencia juvenil: **29,88**")
        st.markdown("- Índice de dependencia senil: **21,68**")
        st.markdown("- Índice de envejecimiento: **72,54**")
        st.markdown("- Índice de masculinidad: **93,40**")
        st.markdown("---")

        st.subheader("🏙️ Distribución por tipo de asentamiento (2018)")
        areas = pd.DataFrame({
            "Asentamiento": ["Cabecera Urbana", "Centros Poblados", "Rural Disperso"],
            "Total": [4779570, 331657, 863561]
        })
        areas["%"] = (areas["Total"] / total_pop) * 100

        st.dataframe(areas.set_index("Asentamiento").round(2))

        pie = (
            alt.Chart(areas)
            .mark_arc()
            .encode(
                theta=alt.Theta(field="Total", type="quantitative"),
                color=alt.Color(field="Asentamiento", type="nominal"),
                tooltip=["Asentamiento", "Total", "%"]
            )
            .properties(width=300, height=300, title="Distribución por Asentamiento (2018)")
        )
        st.altair_chart(pie, use_container_width=True)

    # Separador final fuera del bloque
    st.markdown("---")

# -----------------------------------------------------------
# SECCIÓN: Mortalidad (2023)
# -----------------------------------------------------------
elif section == "💀 Mortalidad (2023)":
    st.header("💀 Análisis de Mortalidad - Antioquia 2023")
    
    # ---------------------------
    # 1️⃣ Tasas Brutas de Mortalidad
    # ---------------------------
    st.subheader("📊 Tasas Bruta de Mortalidad por sexo - Antioquia 2023")
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        # Datos TBM
        data_tbm = {
            "Indicador": ["Defunciones 2023", "Población 2023", "TBM 2023"],
            "Hombres": [19585, 3314221, 5.91],
            "Mujeres": [17093, 3511904, 4.87],
            "Total": [36680, 6826125, 5.37]
        }
        df_tbm = pd.DataFrame(data_tbm)
        st.dataframe(df_tbm, use_container_width=True)
        
        # Métricas destacadas
        st.markdown("### 🔢 Indicadores Generales")
        col_a, col_b, col_c = st.columns(3)
        col_a.metric("TBM Hombres", "5,91")
        col_b.metric("TBM Mujeres", "4,87")
        col_c.metric("TBM Total", "5,37")
    
    with col2:
        # Gráfico de barras TBM
        df_tbm_chart = df_tbm[df_tbm["Indicador"] == "TBM 2023"].melt(
            id_vars=["Indicador"], 
            var_name="Sexo", 
            value_name="TBM"
        )
        
        chart_tbm = alt.Chart(df_tbm_chart).mark_bar().encode(
            x=alt.X("Sexo:N", title="Sexo"),
            y=alt.Y("TBM:Q", title="Tasa Bruta de Mortalidad"),
            color=alt.Color("Sexo:N", scale=alt.Scale(
                domain=["Hombres", "Mujeres", "Total"],
                range=["#1f2eb4", "#eb0eff", "#009e73"]
            )),
            tooltip=["Sexo", "TBM"]
        ).properties(
            title="Tasa Bruta de Mortalidad por Sexo 2023",
            width=400,
            height=300
        )
        st.altair_chart(chart_tbm, use_container_width=True)
    
    st.markdown("---")
    
    # ---------------------------
    # 2️⃣ Tasas Específicas por Edad y Sexo
    # ---------------------------
    st.subheader("📈 Tasas Específicas de Mortalidad por Edad y Sexo - 2023")
    
    data_tasas = {
        "x": ["0", "1", "2-4", "5-9", "10-14", "15-19", "20-24", "25-29", "30-34", 
              "35-39", "40-44", "45-49", "50-54", "55-59", "60-64", "65-69", "70-74", 
              "75-79", "80-84", "85 y más"],
        "Hombres": [8.424, 0.683, 0.360, 0.187, 0.255, 1.171, 2.047, 2.007, 2.126, 
                   2.135, 2.600, 2.864, 4.005, 6.207, 10.211, 16.358, 26.037, 41.618, 
                   65.534, 143.943],
        "Mujeres": [7.172, 0.526, 0.240, 0.127, 0.187, 0.388, 0.513, 0.492, 0.661, 
                   0.854, 1.328, 1.679, 2.456, 3.979, 5.701, 9.181, 14.737, 26.917, 
                   48.514, 132.142],
        "Total": [7.812, 0.607, 0.302, 0.158, 0.222, 0.788, 1.289, 1.282, 1.396, 
                 1.487, 1.942, 2.235, 3.172, 4.996, 7.722, 12.310, 19.583, 33.096, 
                 55.457, 136.565]
    }
    df_tasas = pd.DataFrame(data_tasas)
    
    col1, col2 = st.columns([1.25, 1.25])
    
    with col1:
        st.dataframe(df_tasas, use_container_width=True)
    
    with col2:
        # Gráfico de líneas
        df_tasas_long = df_tasas.melt(id_vars=["x"], var_name="Sexo", value_name="Tasa")
        
        # Dividir las tasas entre 1000 para mejor visualización
        df_tasas_long["Tasa_ajustada"] = df_tasas_long["Tasa"] / 1000
        
        chart_tasas = alt.Chart(df_tasas_long).mark_line(point=True, size=3).encode(
            x=alt.X("x:N", title="Grupos de Edad", sort=None),
            y=alt.Y("Tasa_ajustada:Q", 
                   title="mx",
                   scale=alt.Scale(type="log", domain=[0.0001, 0.2])),
            color=alt.Color("Sexo:N", 
                          scale=alt.Scale(
                              domain=["Hombres", "Mujeres", "Total"],
                              range=["#1f2eb4", "#eb0eff", "#009e73"]
                          ),
                          legend=alt.Legend(
                              title=None,
                              labelExpr="datum.label == 'Hombres' ? 'mxH' : datum.label == 'Mujeres' ? 'mxM' : 'mxT'"
                          )),
            tooltip=[
                alt.Tooltip("x:N", title="Grupo de Edad"), 
                "Sexo", 
                alt.Tooltip("Tasa_ajustada:Q", title="Tasa (mx)", format=".6f")
            ]
        ).properties(
            title="Tasas específicas de mortalidad de la población del departamento de Antioquia durante el año 2023",
            width=700,
            height=450
        ).configure_axis(
            gridOpacity=0.3
        )
        st.altair_chart(chart_tasas, use_container_width=True)
    st.markdown("---")
    
    # ---------------------------
    # 3️⃣ Mortalidad Infantil y de la Niñez
    # ---------------------------
    st.subheader("👶 Mortalidad Infantil y de la Niñez - Antioquia 2023")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("**Mortalidad Infantil 2023**")
        data_mi = {
            "Indicador": ["Menores 1 año", "Nacimientos"],
            "Cantidad": [461, 59017]
        }
        df_mi = pd.DataFrame(data_mi)
        st.dataframe(df_mi, use_container_width=True)
        st.metric("TMI 2023", "7,81", help="Tasa de Mortalidad Infantil")
    
    with col2:
        st.markdown("**Mortalidad de la Niñez 2023**")
        data_mn = {
            "Indicador": ["Menores 5 años", "Nacimientos"],
            "Cantidad": [593, 59017]
        }
        df_mn = pd.DataFrame(data_mn)
        st.dataframe(df_mn, use_container_width=True)
        st.metric("TN 2023", "10,05", help="Tasa de Mortalidad de la Niñez")
    
    with col3:
        st.markdown("**Mortalidad Niñez (0-4 años) 2023**")
        data_mn04 = {
            "Indicador": ["Menores 5 años", "Pob 0 a 4 años"],
            "Cantidad": [593, 435379]
        }
        df_mn04 = pd.DataFrame(data_mn04)
        st.dataframe(df_mn04, use_container_width=True)
        st.metric("TN 2023", "1,36", help="Tasa de Mortalidad de la Niñez")
    
    st.markdown("---")
    
    # ---------------------------
    # 4️⃣ Principales Causas de Mortalidad
    # ---------------------------
    st.subheader("🏥 17 Principales Causas de Mortalidad - Antioquia 2023")
    
    data_causas = {
        "Causa": [
            "303 Enfermedades isquémicas del corazón",
            "605 Enfermedades crónicas de las vías respiratorias inferiores",
            "307 Enfermedades cerebrovasculares",
            "3 Tumor maligno de los órganos digestivos y del peritoneo, excepto estómago y colon",
            "302 Enfermedades hipertensivas",
            "512 Agresiones (homicidios)",
            "108 Infecciones respiratorias agudas",
            "609 Resto de enfermedades del sistema digestivo",
            "604 Enfermedades del sistema nervioso, excepto meningitis",
            "204 Tumor maligno de la tráquea, los bronquios y el pulmón",
            "214 Tumores malignos de otras localizaciones y de las no especificadas",
            "610 Enfermedades del sistema urinario",
            "614 Resto de las enfermedades",
            "501 Accidentes de transporte terrestre",
            "Cardiovascular, enfermedad reumática crónica del corazón, pulmonar y otras formas de enferme",
            "601 Diabetes mellitus",
            "201 Tumor maligno del estómago"
        ],
        "Total": [5511, 3679, 2095, 1506, 1477, 1393, 1305, 1292, 1267, 1167, 1067, 1014, 942, 923, 885, 748, 700],
        "%": [15.02, 7.30, 5.71, 4.11, 4.03, 3.80, 3.56, 3.52, 3.45, 3.18, 2.91, 2.76, 2.57, 2.53, 2.41, 2.04, 1.91],
        "TMxCE": [0.807339, 0.392463, 0.306909, 0.220623, 0.216375, 0.204069, 0.191177, 0.189273, 0.185610, 0.170961, 0.156311, 0.148547, 0.137999, 0.136095, 0.129649, 0.109579, 0.102547]
    }
    df_causas = pd.DataFrame(data_causas)
    
    # Crear nombres cortos para el treemap
    df_causas["Causa_corta"] = [
        "Isquémicas corazón",
        "Vías resp. inferiores",
        "Cerebrovasculares",
        "Tumor órg. digestivos",
        "Hipertensivas",
        "Homicidios",
        "Infecciones respiratorias",
        "Sistema digestivo",
        "Sistema nervioso",
        "Tumor tráquea/bronquios",
        "Tumores otros",
        "Sistema urinario",
        "Resto enfermedades",
        "Accidentes tránsito",
        "Cardiovascular otras",
        "Diabetes mellitus",
        "Tumor estómago"
    ]
    
    st.dataframe(df_causas[["Causa", "Total", "%", "TMxCE"]], use_container_width=True, height=400)
    
    st.markdown("### 📊 Resumen")
    col_a, col_b, col_c = st.columns(3)
    col_a.metric("Total Defunciones", "36,680")
    col_b.metric("Total Población", "6,826,125")
    col_c.metric("Causa Principal", "15,02", help="Enfermedades isquémicas del corazón")
    
    st.markdown("---")
    
    # Treemap de causas de mortalidad
    st.subheader("🗺️ Treemap - Distribución de Causas de Mortalidad")
    
    treemap = alt.Chart(df_causas).mark_rect().encode(
        x=alt.X('sum(Total):Q', stack='zero', axis=None),
        y=alt.Y('Causa_corta:N', axis=None),
        color=alt.Color('Total:Q', 
                       scale=alt.Scale(scheme='reds'),
                       legend=alt.Legend(title="Defunciones")),
        tooltip=[
            alt.Tooltip('Causa:N', title='Causa'),
            alt.Tooltip('Total:Q', title='Defunciones', format=','),
            alt.Tooltip('%:Q', title='Porcentaje', format='.2f')
        ]
    ).properties(
        width=800,
        height=500,
        title='Distribución de las 17 Principales Causas de Mortalidad'
    )
    
    # Agregar texto con las etiquetas
    text = alt.Chart(df_causas).mark_text(
        align='center',
        baseline='middle',
        fontSize=10,
        fontWeight='bold',
        color='white'
    ).encode(
        x=alt.X('sum(Total):Q', stack='zero'),
        y=alt.Y('Causa_corta:N'),
        text=alt.Text('Causa_corta:N'),
        detail='Causa_corta:N'
    )
    
    st.altair_chart(treemap + text, use_container_width=True)
    
    st.markdown("---")
# -----------------------------------------------------------
# SECCIÓN: Fecundidad (2023)
# -----------------------------------------------------------
elif section == "👶 Fecundidad (2023)":
    st.header("👶 Análisis de Fecundidad - Antioquia 2023")
    
    # ---------------------------
    # 1️⃣ Indicadores Generales
    # ---------------------------
    st.subheader("📊 Indicadores Generales de Fecundidad")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Tasa Bruta de Natalidad", "8,645754363", help="Por 1000 habitantes")
        st.metric("Total Nacimientos", "59,017")
    
    with col2:
        st.metric("Tasa General de Fecundidad (TGF)", "32,33", help="Por 1000 mujeres en edad fértil")
        st.metric("Población Media 2023", "6,826,125")
    
    with col3:
        st.metric("Índice Sintético de Fecundidad (ISF)", "1,06238362", help="Hijos por mujer")
        st.metric("Edad Media Materna (EMM)", "29,56884046")
    
    with col4:
        st.metric("Tasa Bruta de Reproductividad (TBR)", "0,519450526")
        st.metric("TNR (15-49)", "0,5113291")
    
    st.markdown("---")
    
    # ---------------------------
    # 2️⃣ Nacimientos por Edad de la Madre
    # ---------------------------
    st.subheader("👩‍👧 Nacimientos Ocurridos según Edad de la Madre - 2023")
    
    col1, col2 = st.columns([1, 1.5])
    
    with col1:
        data_nacimientos = {
            "Grupos de edad": ["15-19", "20-24", "25-29", "30-34", "35-39", "40-44", "45-49", "15-49"],
            "Total": [8575, 16257, 15245, 11134, 5807, 1457, 89, 58564]
        }
        df_nacimientos = pd.DataFrame(data_nacimientos)
        st.dataframe(df_nacimientos, use_container_width=True)
    
    with col2:
        # Gráfico de barras de nacimientos
        df_nac_chart = df_nacimientos[df_nacimientos["Grupos de edad"] != "15-49"]
        
        chart_nac = alt.Chart(df_nac_chart).mark_bar(color="#eb0eff").encode(
            x=alt.X("Grupos de edad:N", title="Edad de la Madre", sort=None),
            y=alt.Y("Total:Q", title="Número de Nacimientos"),
            tooltip=["Grupos de edad", "Total"]
        ).properties(
            title="Distribución de Nacimientos por Edad de la Madre",
            width=500,
            height=300
        )
        st.altair_chart(chart_nac, use_container_width=True)
    
    st.markdown("---")
    
    # ---------------------------
    # 3️⃣ Tasas Específicas de Fecundidad (TEF)
    # ---------------------------
    st.subheader("📈 Tasas Específicas de Fecundidad por Edad - 2023")
    
    data_tef = {
        "Grupos de edad": ["15-19", "20-24", "25-29", "30-34", "35-39", "40-44", "45-49"],
        "TEF": [32.6592017, 58.7863052, 51.7505923, 39.7610196, 22.9680022, 6.121000029, 0.430602796]
    }
    df_tef = pd.DataFrame(data_tef)
    
    col1, col2 = st.columns([1, 1.5])
    
    with col1:
        st.dataframe(df_tef, use_container_width=True)
        
        st.markdown("### 🔍 Observaciones")
        st.markdown("- **Pico de fecundidad:** 20-24 años (58,79 por 1000)")
        st.markdown("- **Segundo pico:** 25-29 años (51,75 por 1000)")
        st.markdown("- **Fecundidad adolescente:** 32,66 por 1000 (15-19 años)")
        st.markdown("- **Descenso marcado:** A partir de los 30 años")
    
    with col2:
        # Gráfico TEF
        chart_tef = alt.Chart(df_tef).mark_line(point=True, color="#009e73", size=3).encode(
            x=alt.X("Grupos de edad:N", title="Grupo de Edad", sort=None),
            y=alt.Y("TEF:Q", title="TEF (por 1000 mujeres)", scale=alt.Scale(domain=[0, 70])),
            tooltip=["Grupos de edad", alt.Tooltip("TEF:Q", format=".2f")]
        ).properties(
            title="Tasa Específica de Fecundidad (TEF) por Edad",
            width=500,
            height=400
        )
        st.altair_chart(chart_tef, use_container_width=True)
    
    st.markdown("---")
    
    # ---------------------------
    # 4️⃣ Población de Mujeres y Niñas
    # ---------------------------
    st.subheader("👩 Población Media de Mujeres en Edad Fértil - 2023")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("**Población Media de Mujeres**")
        data_pob_mujeres = {
            "Grupos de edad": ["15-19", "20-24", "25-29", "30-34", "35-39", "40-44", "45-49", "15-49"],
            "30.06.2023": [262560, 276544, 294586, 286023, 252830, 238033, 206687, 1811263],
            "Marca de Clase": [17.5, 22.5, 27.5, 32.5, 37.5, 42.5, 47.5, 33],
            "nLx": [494542.0, 493428.0, 492189.0, 490773.0, 488918.0, 486260.0, 482620.0, "-"]
        }
        df_pob_mujeres = pd.DataFrame(data_pob_mujeres)
        st.dataframe(df_pob_mujeres, use_container_width=True, height=300)
    
    with col2:
        st.markdown("**Población Nacimientos Niñas**")
        data_nac_ninas = {
            "Grupos de edad": ["15-19", "20-24", "25-29", "30-34", "35-39", "40-44", "45-49", "15-49", "Nacimientos niñas totales"],
            "Población/Nacimientos": [4137, 7924, 7470, 5508, 2859, 699, 43, 28640, 28862],
            "TEFm": [15.75639854, 28.65366813, 25.35762053, 19.66981284, 11.30799351, 2.936567619, 0.208044047, "-", "-"]
        }
        df_nac_ninas = pd.DataFrame(data_nac_ninas)
        st.dataframe(df_nac_ninas, use_container_width=True, height=300)
    
    st.markdown("---")
    
    # ---------------------------
    # 5️⃣ Tasa Neta de Reproducción (TNR)
    # ---------------------------
    st.subheader("🔄 Tasa Neta de Reproducción por Grupos de Edad")
    
    data_tnr = {
        "Grupos de edad": ["15-19", "20-24", "25-29", "30-34", "35-39", "40-44", "45-49", "15-49 TNR"],
        "TNR": [161.513469, 290.068090, 254.710723, 195.136348, 112.294697, 29.763974, 2.078175, 0.511329]
    }
    df_tnr = pd.DataFrame(data_tnr)
    
    col1, col2 = st.columns([1, 1.5])
    
    with col1:
        st.dataframe(df_tnr, use_container_width=True)
        
        st.markdown("### 📌 Interpretación TNR")
        st.info("**TNR = 0,511** indica que cada mujer está siendo reemplazada por aproximadamente 0,51 hijas, lo que significa que la población tiende a **decrecer** en el largo plazo.")
    
    with col2:
        # Gráfico TNR
        df_tnr_chart = df_tnr[df_tnr["Grupos de edad"] != "15-49 TNR"]
        
        chart_tnr = alt.Chart(df_tnr_chart).mark_bar(color="#1f2eb4").encode(
            x=alt.X("Grupos de edad:N", title="Edad de la Madre", sort=None),
            y=alt.Y("TNR:Q", title="Tasa Neta de Reproducción"),
            tooltip=["Grupos de edad", alt.Tooltip("TNR:Q", format=".2f")]
        ).properties(
            title="Tasa Neta de Reproducción por Edad",
            width=500,
            height=350
        )
        st.altair_chart(chart_tnr, use_container_width=True)
    
    st.markdown("---")

# -----------------------------------------------------------
# SECCIÓN: Migración (2018)
# -----------------------------------------------------------
elif section == "🚶‍♂️ Migración (2018)":
    st.header("🚶‍♂️ Análisis de Migración - Valle de Aburrá (2015-2020)")
    
    # ---------------------------
    # 1️⃣ Datos de Migración
    # ---------------------------
    st.subheader("📊 Indicadores de Migración por Municipio")
    
    data_migracion = {
        "Municipio": [
            "TOTAL", "MEDELLÍN", "BARBOSA", "BELLO", "CALDAS", "COPACABANA",
            "ENVIGADO", "GIRARDOTA", "ITAGÜÍ", "LA ESTRELLA", "SABANETA"
        ],
        "Poblacion_2020": [
            2580420, 540095, 102045, 72626, 43362, 275874,
            108695, 396632, 78838, 573234, 381019
        ],
        "Poblacion_2015": [
            3396101, 216148, 41735, 43384, 70999, 70714,
            195836, 44810, 240340, 62284, 74040
        ],
        "No_migrantes": [
            2472125, 522749, 100026, 61739, 44206, 264608,
            108042, 389897, 73319, 561851, 345688
        ],
        "Inmigrantes": [
            108295, 17346, 2019, 10887, 5156, 11266,
            653, 8735, 5519, 11383, 35331
        ],
        "Emigrantes": [
            108295, 19438, 2540, 1308, 1694, 3070,
            32986, 22741, 3163, 40887, 10168
        ],
        "Migracion_Neta": [
            0, -2092, -521, 9579, 3462, 8196,
            -1943, -14006, 2366, -29504, 25163
        ],
        "Migracion_Bruta": [
            216590, 36784, 4559, 12195, 6850, 14336,
            33639, 31476, 8672, 52270, 45499
        ],
        "Poblacion_Media": [
            2988262, 1350781.5, 71890, 253237, 60180.5, 173309,
            152265.5, 22171, 159583, 317759, 227529.5
        ],
        "Tasa_Inmigracion": [
            7.248026776, 2.87, 5.62, 8.60, 17.14, 13.00,
            0.86, 7.88, 6.92, 7.16, 31.06
        ],
        "Tasa_Emigracion": [
            7.248025776, 2.88, 7.07, 1.03, 5.63, 3.54,
            4.33, 20.51, 3.95, 25.73, 8.94
        ],
        "Tasa_migracion": [
            0, -0.31, -1.45, 7.57, 11.51, 9.46,
            -3.47, -12.63, 2.97, -18.57, 22.12
        ],
        "Indice_Eficacia_Migratoria": [
            0, -5.69, -11.43, 78.55, 50.54, 57.17,
            -66.93, -44.50, 27.28, -56.45, 55.30
        ]
    }
    df_migracion = pd.DataFrame(data_migracion)
    
    # Mostrar tabla completa
    st.dataframe(df_migracion, use_container_width=True, height=400)
    
    st.markdown("---")
    
    # ---------------------------
    # 2️⃣ Indicadores Destacados
    # ---------------------------
    st.subheader("🔢 Indicadores Generales del Valle de Aburrá")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Población 2020", "2,580,420")
        st.metric("Población 2015", "3,396,101")
    
    with col2:
        st.metric("Total Inmigrantes", "108,295")
        st.metric("Total Emigrantes", "108,295")
    
    with col3:
        st.metric("Migración Neta Total", "0")
        st.metric("Migración Bruta", "216,590")
    
    with col4:
        st.metric("Tasa Inmigración", "7,25‰")
        st.metric("Tasa Emigración", "7,25‰")
    
    st.markdown("---")
    
    # ---------------------------
    # 3️⃣ Análisis por Municipio
    # ---------------------------
    st.subheader("📈 Análisis Comparativo de Migración")
    
    # Filtrar solo municipios (sin TOTAL)
    df_mpio = df_migracion[df_migracion["Municipio"] != "TOTAL"].copy()
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Gráfico de Migración Neta
        chart_neta = alt.Chart(df_mpio).mark_bar().encode(
            x=alt.X("Migracion_Neta:Q", title="Migración Neta"),
            y=alt.Y("Municipio:N", sort="-x", title="Municipio"),
            color=alt.condition(
                alt.datum.Migracion_Neta > 0,
                alt.value("#009e73"),  # verde para positivo
                alt.value("#d55e00")   # naranja para negativo
            ),
            tooltip=["Municipio", "Migracion_Neta", "Tasa_migracion"]
        ).properties(
            title="Migración Neta por Municipio",
            width=400,
            height=400
        )
        st.altair_chart(chart_neta, use_container_width=True)
    
    with col2:
        # Gráfico de Tasas de Migración
        chart_tasas = alt.Chart(df_mpio).mark_bar().encode(
            x=alt.X("Tasa_migracion:Q", title="Tasa de Migración (‰)"),
            y=alt.Y("Municipio:N", sort="-x", title="Municipio"),
            color=alt.condition(
                alt.datum.Tasa_migracion > 0,
                alt.value("#1f2eb4"),  # azul para positivo
                alt.value("#eb0eff")   # magenta para negativo
            ),
            tooltip=["Municipio", "Tasa_migracion", "Indice_Eficacia_Migratoria"]
        ).properties(
            title="Tasa de Migración por Municipio (‰)",
            width=400,
            height=400
        )
        st.altair_chart(chart_tasas, use_container_width=True)
    
    st.markdown("---")
    
    # ---------------------------
    # 4️⃣ Municipios con Mayor y Menor Migración
    # ---------------------------
    st.subheader("🏆 Ranking de Migración")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### ⬆️ Mayor Atracción Migratoria")
        top_atraccion = df_mpio.nlargest(5, "Tasa_migracion")[["Municipio", "Tasa_migracion", "Migracion_Neta"]]
        st.dataframe(top_atraccion.reset_index(drop=True), use_container_width=True)
    
    with col2:
        st.markdown("### ⬇️ Mayor Expulsión Migratoria")
        top_expulsion = df_mpio.nsmallest(5, "Tasa_migracion")[["Municipio", "Tasa_migracion", "Migracion_Neta"]]
        st.dataframe(top_expulsion.reset_index(drop=True), use_container_width=True)
    
    st.markdown("---")
    
    # ---------------------------
    # 5️⃣ Mapas Interactivos (Opcional - requiere instalación adicional)
    # ---------------------------
    st.subheader("🗺️ Visualización Geográfica de la Migración")
    
    st.info("""
    Los mapas mostrarán:
    - **Mapa 1:** Tasa de migración (verde = atracción, rojo = expulsión)
    - **Mapa 2:** Índice de Eficacia Migratoria (%)
    """)
    
    # Si tienes los archivos shapefile y las librerías instaladas, descomenta esto:
    
    try:
        import geopandas as gpd
        import folium
        from streamlit_folium import st_folium
        import unicodedata
        
        # Función para normalizar nombres (quitar tildes)
        def normalizar(texto):
            texto = str(texto).upper().strip()
            # Remover acentos
            texto = ''.join(c for c in unicodedata.normalize('NFD', texto) if unicodedata.category(c) != 'Mn')
            return texto
        
        # Cargar shapefile con encoding correcto
        antioquia = gpd.read_file("antioquia_simplificado.shp", encoding='iso-8859-1')
        antioquia = antioquia.to_crs(epsg=4326)

        # Preparar datos para los mapas
        datos_mapa = df_mpio[["Municipio", "Tasa_migracion", "Indice_Eficacia_Migratoria"]].copy()
        
        # Normalizar ambos lados
        antioquia["mpio_norm"] = antioquia["mpio_cnmbr"].apply(normalizar)
        datos_mapa["Municipio_norm"] = datos_mapa["Municipio"].apply(normalizar)

        # --- MAPA 1: TASA DE MIGRACIÓN ---
        st.markdown("### 📍 Mapa 1: Tasa de Migración")

        antioquia_tasa = antioquia.merge(datos_mapa, how="left", left_on="mpio_norm", right_on="Municipio_norm")

        m1 = folium.Map(location=[6.25, -75.56], zoom_start=10, tiles="CartoDB positron")

        # Fondo gris para Antioquia
        folium.GeoJson(
            antioquia,
            style_function=lambda x: {"fillColor": "lightgray", "color": "white", "weight": 0.5}
        ).add_to(m1)

        # Choropleth para Tasa de Migración
        folium.Choropleth(
            geo_data=antioquia_tasa.dropna(subset=["Tasa_migracion"]),
            data=antioquia_tasa.dropna(subset=["Tasa_migracion"]),
            columns=["Municipio_norm", "Tasa_migracion"],
            key_on="feature.properties.mpio_norm",
            fill_color="RdYlGn",
            fill_opacity=0.8,
            line_opacity=0.5,
            nan_fill_color="lightgray",
            legend_name="Tasa de Migración"
        ).add_to(m1)

        # Etiquetas interactivas
        for _, row in antioquia_tasa.iterrows():
            if pd.notnull(row["Tasa_migracion"]):
                folium.Marker(
                    location=[row.geometry.centroid.y, row.geometry.centroid.x],
                    popup=f"<b>{row['Municipio']}</b><br>Tasa: {row['Tasa_migracion']:.2f} por mil",
                    icon=folium.Icon(color="blue", icon="info-sign")
                ).add_to(m1)

        st_folium(m1, width=800, height=500)

        st.markdown("---")

        # --- MAPA 2: ÍNDICE DE EFICACIA MIGRATORIA ---
        st.markdown("### 📍 Mapa 2: Índice de Eficacia Migratoria")

        antioquia_eficacia = antioquia.merge(datos_mapa, how="left", left_on="mpio_norm", right_on="Municipio_norm")

        m2 = folium.Map(location=[6.25, -75.56], zoom_start=10, tiles="CartoDB positron")

        # Fondo gris para Antioquia
        folium.GeoJson(
            antioquia,
            style_function=lambda x: {"fillColor": "lightgray", "color": "white", "weight": 0.5}
        ).add_to(m2)

        # Choropleth para Eficacia Migratoria
        folium.Choropleth(
            geo_data=antioquia_eficacia.dropna(subset=["Indice_Eficacia_Migratoria"]),
            data=antioquia_eficacia.dropna(subset=["Indice_Eficacia_Migratoria"]),
            columns=["Municipio_norm", "Indice_Eficacia_Migratoria"],
            key_on="feature.properties.mpio_norm",
            fill_color="RdYlGn",
            fill_opacity=0.8,
            line_opacity=0.5,
            nan_fill_color="lightgray",
            legend_name="Índice Eficacia Migratoria"
        ).add_to(m2)

        # Etiquetas interactivas
        for _, row in antioquia_eficacia.iterrows():
            if pd.notnull(row["Indice_Eficacia_Migratoria"]):
                folium.Marker(
                    location=[row.geometry.centroid.y, row.geometry.centroid.x],
                    popup=f"<b>{row['Municipio']}</b><br>Eficacia: {row['Indice_Eficacia_Migratoria']:.2f}",
                    icon=folium.Icon(color="purple", icon="info-sign")
                ).add_to(m2)

        st_folium(m2, width=800, height=500)
        
    except Exception as e:
        st.error(f"No se pudo cargar el mapa: {e}")
        st.info("Verifica que el archivo shapefile esté en la carpeta correcta.")
    
    st.markdown("---")
    
    # ---------------------------
    # 6️⃣ Análisis del Efecto de la Migración en el Índice de Masculinidad
    # ---------------------------
    st.header("📊 Análisis del Efecto de la Migración en el Índice de Masculinidad del Área Metropolitana de Antioquia al año 2018")
    
    st.markdown("""
    **Índice de Masculinidad:** Número de hombres por cada 100 mujeres
    - **Factual (F):** Índice de masculinidad de los inmigrantes
    - **ContraFactual (CF):** Índice de masculinidad de los emigrantes  
    - **No migrantes (NM):** Índice de masculinidad de población que no migra
    """)
    
    st.markdown("---")
    
    # Datos del índice de masculinidad
    data_masc = {
        "Municipio": [
            "MEDELLÍN", "BARBOSA", "BELLO", "CALDAS", "COPACABANA",
            "ENVIGADO", "GIRARDOTA", "ITAGÜÍ", "LA ESTRELLA", "SABANETA"
        ],
        "Total_AM": [87.00, 97.51, 88.98, 91.28, 92.92, 84.26, 94.09, 88.55, 93.05, 85.98],
        "Factual": [87.00, 97.51, 88.98, 91.28, 92.92, 84.26, 94.09, 88.55, 93.05, 85.98],
        "ContraFactual": [87.06, 96.56, 88.74, 91.04, 92.09, 84.99, 93.54, 88.38, 93.02, 87.07],
        "No_migrantes": [86.98, 97.14, 88.83, 91.03, 92.24, 84.59, 93.80, 88.30, 93.01, 86.71],
        "Efecto_absoluto_migracion_Neta": [-0.07, 0.95, 0.24, 0.25, 0.82, -0.72, 0.55, 0.17, 0.03, -1.09],
        "Efecto_Relativo_migracion_Neta": [-0.076, 0.981, 0.271, 0.269, 0.894, -0.849, 0.586, 0.197, 0.031, -1.253],
        "Diferencia_Relativa_Inmigracion": [0.162, 3.855, 1.613, 2.840, 7.373, -3.857, 3.108, 2.861, 0.406, -8.335],
        "Diferencia_Relativa_Emigracion": [-0.92, 5.95, 1.10, -0.15, 1.57, -4.63, 2.75, -0.89, -0.10, -4.19]
    }
    df_masc = pd.DataFrame(data_masc)
    
    # ---------------------------
    # Tabla de Datos
    # ---------------------------
    st.subheader("📋 Índices de Masculinidad por Municipio")
    st.dataframe(df_masc, use_container_width=True, height=380)
    
    st.markdown("---")
    
    # ---------------------------
    # Sección 1: Comparación de Índices
    # ---------------------------
    st.subheader("📊 Comparación: Inmigrantes, Emigrantes y No Migrantes")
    
    col1, col2 = st.columns([1.2, 1])
    
    with col1:
        # Gráfico de barras agrupadas
        df_comparacion = df_masc[["Municipio", "Factual", "ContraFactual", "No_migrantes"]].melt(
            id_vars=["Municipio"],
            var_name="Tipo_Poblacion",
            value_name="Indice_Masculinidad"
        )
        
        df_comparacion["Tipo_Poblacion"] = df_comparacion["Tipo_Poblacion"].replace({
            "Factual": "Inmigrantes (F)",
            "ContraFactual": "Emigrantes (CF)",
            "No_migrantes": "No migrantes (NM)"
        })
        
        chart_comp = alt.Chart(df_comparacion).mark_bar().encode(
            x=alt.X("Municipio:N", title="Municipio", sort=None),
            y=alt.Y("Indice_Masculinidad:Q", title="Índice de Masculinidad (hombres por 100 mujeres)"),
            color=alt.Color("Tipo_Poblacion:N", 
                          scale=alt.Scale(
                              domain=["Inmigrantes (F)", "Emigrantes (CF)", "No migrantes (NM)"],
                              range=["#1f2eb4", "#eb0eff", "#009e73"]
                          ),
                          legend=alt.Legend(title="Tipo de Población")),
            xOffset="Tipo_Poblacion:N",
            tooltip=["Municipio", "Tipo_Poblacion", alt.Tooltip("Indice_Masculinidad:Q", format=".2f")]
        ).properties(
            title="Índice de Masculinidad por Tipo de Población",
            width=600,
            height=400
        )
        st.altair_chart(chart_comp, use_container_width=True)
    
    with col2:
        st.markdown("### 🔍 Interpretación")
        st.info("""
        **¿Qué observar?**
        
        - Si **Factual > No migrantes**: La inmigración trae proporcionalmente más hombres
        
        - Si **ContraFactual > No migrantes**: La emigración se lleva proporcionalmente más hombres
        
        - La diferencia entre barras muestra el impacto de la migración en la composición por sexo
        """)
    
    st.markdown("---")
    
    # ---------------------------
    # Sección 2: Efectos Relativos
    # ---------------------------
    st.subheader("📈 Efectos Relativos de la Migración (por 1000)")
    
    st.markdown("""
    **Diferencia Relativa de Inmigración:** $\\frac{F - NM}{CF} \\times 1000$
    
    Indica cuántos hombres adicionales (o menos) aporta la inmigración por cada 1000 mujeres, 
    comparado con la población no migrante y relativizado por el índice de emigrantes.
    """)
    
    col3, col4 = st.columns(2)
    
    with col3:
        # Efecto de Inmigración
        chart_inm = alt.Chart(df_masc).mark_bar().encode(
            x=alt.X("Diferencia_Relativa_Inmigracion:Q", title="Diferencia Relativa (por 1000)"),
            y=alt.Y("Municipio:N", sort="-x", title="Municipio"),
            color=alt.condition(
                alt.datum.Diferencia_Relativa_Inmigracion > 0,
                alt.value("#1f2eb4"),  # azul para positivo
                alt.value("#d55e00")   # naranja para negativo
            ),
            tooltip=[
                "Municipio", 
                alt.Tooltip("Diferencia_Relativa_Inmigracion:Q", title="Dif. Relativa", format=".3f")
            ]
        ).properties(
            title="Efecto Relativo de la Inmigración",
            width=400,
            height=400
        )
        st.altair_chart(chart_inm, use_container_width=True)
        
        st.markdown("**Interpretación:**")
        st.markdown("- **Positivo:** Inmigración aumenta proporción de hombres")
        st.markdown("- **Negativo:** Inmigración disminuye proporción de hombres")
    
    with col4:
        # Efecto de Emigración
        chart_em = alt.Chart(df_masc).mark_bar().encode(
            x=alt.X("Diferencia_Relativa_Emigracion:Q", title="Diferencia Relativa (por 1000)"),
            y=alt.Y("Municipio:N", sort="-x", title="Municipio"),
            color=alt.condition(
                alt.datum.Diferencia_Relativa_Emigracion > 0,
                alt.value("#009e73"),  # verde para positivo
                alt.value("#eb0eff")   # magenta para negativo
            ),
            tooltip=[
                "Municipio",
                alt.Tooltip("Diferencia_Relativa_Emigracion:Q", title="Dif. Relativa", format=".2f")
            ]
        ).properties(
            title="Efecto Relativo de la Emigración",
            width=400,
            height=400
        )
        st.altair_chart(chart_em, use_container_width=True)
        
        st.markdown("**Interpretación:**")
        st.markdown("- **Positivo:** Emigración retiene más mujeres (se van más hombres)")
        st.markdown("- **Negativo:** Emigración retiene más hombres (se van más mujeres)")
    
    st.markdown("---")
    
    # ---------------------------
    # Sección 3: Efecto Neto
    # ---------------------------
    st.subheader("⚖️ Efecto Neto de la Migración")
    
    col5, col6 = st.columns([1.5, 1])
    
    with col5:
        chart_neto = alt.Chart(df_masc).mark_bar().encode(
            x=alt.X("Efecto_absoluto_migracion_Neta:Q", title="Efecto Absoluto Neto (F - CF)"),
            y=alt.Y("Municipio:N", sort="-x", title="Municipio"),
            color=alt.condition(
                alt.datum.Efecto_absoluto_migracion_Neta > 0,
                alt.value("#009e73"),
                alt.value("#d55e00")
            ),
            tooltip=[
                "Municipio",
                alt.Tooltip("Efecto_absoluto_migracion_Neta:Q", title="Efecto Neto", format=".2f"),
                alt.Tooltip("Efecto_Relativo_migracion_Neta:Q", title="Efecto Relativo (%)", format=".2f")
            ]
        ).properties(
            title="Cambio Neto en Índice de Masculinidad por Migración",
            width=500,
            height=400
        )
        st.altair_chart(chart_neto, use_container_width=True)
    
    with col6:
        st.markdown("### 📊 Hallazgos Clave")
        
        # Efecto neto más positivo
        max_neto = df_masc.loc[df_masc["Efecto_absoluto_migracion_Neta"].idxmax()]
        st.success(f"""
        **Mayor aumento:**  
        **{max_neto['Municipio']}**  
        +{max_neto['Efecto_absoluto_migracion_Neta']:.2f} puntos
        """)
        
        # Efecto neto más negativo
        min_neto = df_masc.loc[df_masc["Efecto_absoluto_migracion_Neta"].idxmin()]
        st.error(f"""
        **Mayor disminución:**  
        **{min_neto['Municipio']}**  
        {min_neto['Efecto_absoluto_migracion_Neta']:.2f} puntos
        """)
        
        st.info("""
        **Efecto Neto = F - CF**
        
        Muestra si la migración neta aumenta o disminuye el índice de masculinidad
        """)
    
    st.markdown("---")
    
    # ---------------------------
    # Sección 4: Conclusiones
    # ---------------------------
    st.subheader("💡 Conclusiones del Análisis")
    
    col7, col8 = st.columns(2)
    
    with col7:
        st.markdown("### 🔵 Inmigración")
        positivos_inm = df_masc[df_masc["Diferencia_Relativa_Inmigracion"] > 0]
        st.write(f"**{len(positivos_inm)} municipios** reciben inmigración masculinizada")
        
        max_inm = df_masc.loc[df_masc["Diferencia_Relativa_Inmigracion"].idxmax()]
        st.success(f"**Mayor efecto:** {max_inm['Municipio']} (+{max_inm['Diferencia_Relativa_Inmigracion']:.2f} por 1000)")
        
        min_inm = df_masc.loc[df_masc["Diferencia_Relativa_Inmigracion"].idxmin()]
        st.error(f"**Menor efecto:** {min_inm['Municipio']} ({min_inm['Diferencia_Relativa_Inmigracion']:.2f} por 1000)")
    
    with col8:
        st.markdown("### 🟣 Emigración")
        positivos_em = df_masc[df_masc["Diferencia_Relativa_Emigracion"] > 0]
        st.write(f"**{len(positivos_em)} municipios** pierden población masculina por emigración")
        
        max_em = df_masc.loc[df_masc["Diferencia_Relativa_Emigracion"].idxmax()]
        st.success(f"**Mayor efecto:** {max_em['Municipio']} (+{max_em['Diferencia_Relativa_Emigracion']:.2f} por 1000)")
        
        min_em = df_masc.loc[df_masc["Diferencia_Relativa_Emigracion"].idxmin()]
        st.error(f"**Menor efecto:** {min_em['Municipio']} ({min_em['Diferencia_Relativa_Emigracion']:.2f} por 1000)")
    
    st.markdown("---")