import os
import re
import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

st.set_page_config(
    page_title="Auditoría BIM & Cumplimiento BEP - APV",
    page_icon="📋",
    layout="wide"
)

st.title("📋 Dashboard Integral de Auditoría BIM - APV")

# Lista exclusiva y sin duplicados de los parámetros oficiales APV
PARAMETROS_APV = list(dict.fromkeys([
    "01_01_APV_PROYECTO", "01_02_APV_FASE",
    "01_03_APV_ESTADO", "01_04_APV_TIPOLOGIA",
    "01_05_APV_DISCIPLINA", "01_06_APV_SUBDISCIPLINA",
    "01_07_APV_ELEMENTO", "01_08_APV_CLASIFICACION",
    "01_09_APV_NOMBRE", "01_10_APV_ALINEACION",
    "01_11_APV_NUMERO", "01_12_APV_MATERIAL",
    "01_13_APV_CAD", "01_14_APV_ZONA",
    "02_01_APV_CAPITULO", "02_02_APV_SUBCAPITULO-1",
    "02_03_APV_SUBCAPITULO-2", "02_04_01_APV_MEDICION",
    "02_04_02_APV_MEDICION-ASOC-1", "02_04_03_APV_MEDICION-ASOC-2",
    "02_04_04_APV_MEDICION-ASOC-3", "02_05_01_APV_UNIDAD-OBRA",
    "02_05_02_APV_UO-ASOC-1", "02_05_03_APV_UO-ASOC-2",
    "02_05_04_APV_UO-ASOC-3", "02_06_01_APV_TIPO-MED",
    "02_06_02_APV_TM-ASOC-1", "02_06_03_APV_TM-ASOC-2",
    "02_06_04_APV_TM-ASOC-3", "03_01_APV_FASE-OBRA",
    "03_02_APV_PLANOS", "03_03_APV_PPTP",
    "03_04_APV_CALIDAD-MOD", "04_01_APV_CÓDIGO-TAREA",
    "04_02_APV_NOMBRE-TAREA", "04_03_APV_INICIO-EJECUCION",
    "04_04_APV_FIN-EJECUCION", "04_05_APV_PLAN-REF",
    "04_06_APV_CERTIF-REF", "04_07_APV_CERTIF",
    "04_08_APV_PORCENTAJE-EJECUTADO", "04_09_APV_CERTIF-MED",
    "04_10_APV_CERTIF-MED-ASOC-1", "04_11_APV_CERTIF-MED-ASOC-2",
    "04_12_APV_CERTIF-MED-ASOC-3", "05_01_APV_SEG-SALUD",
    "05_02_APV_INFORMES-APROBACION", "05_03_APV_CONTROL-CALIDAD",
    "05_03_01_APV_COD-TRAZ", "05_04_APV_ENSAYOS",
    "05_05_APV_FOTOGRAFIAS", "05_06_APV_MEDIO-AMBIENTE",
    "05_07_APV_GESTION-RESIDUOS", "05_08_APV_SERV-AFECTADOS",
    "06_01_APV_PRY-LIQUIDACION", "06_02_APV_LIBRO-EDIF",
    "07_01_APV_CAPA-GIS", "07_02_APV_CAMPO-1",
    "07_03_APV_CAMPO-2", "07_04_APV_CAMPO-3",
    "07_05_APV_CAMPO-4", "07_06_APV_CAMPO-5",
    "07_07_APV_CAMPO-6", "07_08_APV_CAMPO-7",
    "07_09_APV_CAMPO-8", "07_10_APV_CAMPO-9",
    "07_11_APV_CAMPO-10", "07_12_APV_CAMPO-N",
    "08_01_APV_PLAN-MANTENIMIENTO", "08_02_APV_MANUALES-FICHAS",
    "08_03_APV_COD-MANTENIMIENTO", "08_04_APV_COD-EXPLOTACION",
    "08_05_APV_AUX-EXPLOTACION", "08_06_APV_COD-CONTABLE",
    "08_07_APV_CAP-CONTABLE", "08_08_APV_SUB-CAP-CONTABLE",
    "09-02_00_APV_PROYECTO", "09-02_01_APV_SONDEO",
    "09-02_02_APV_COTA-MUESTRA(m)", "09-02_03_APV_DESC-ESTRATO",
    "09-02_04_APV_TIPO", "09-02_05_APV_NÚMERO MUESTRA",
    "09-03_01_APV_PASA-100 (%)", "09-03_02_APV_PASA-80 (%)",
    "09-03_03_APV_PASA-63 (%)", "09-03_04_APV_PASA-50 (%)",
    "09-03_05_APV_PASA-40 (%)", "09-03_06_APV_PASA-25 (%)",
    "09-03_07_APV_PASA-20 (%)", "09-03_08_APV_PASA-12,5 (%)",
    "09-03_09_APV_PASA-10 (%)", "09-03_10_APV_PASA-6,3 (%)",
    "09-03_11_APV_PASA-5 (%)", "09-03_12_APV_PASA-2 (%)",
    "09-03_13_APV_PASA-1,25 (%)", "09-03_14_APV_PASA-0,4 (%)",
    "09-03_15_APV_PASA-0,16 (%)", "09-03_16_APV_PASA-0,08 (%)",
    "09-03_17_APV_ATTERBERG-LL", "09-03_18_APV_ATTERBERG-LP",
    "09-03_19_APV_ATTERBERG-IP", "09-03_20_APV_HN (%)",
    "09-03_21_APV_DENS-APAR-HUMEDA (g/cm3)",
    "09-03_22_APV_DENS-APAR-SECA (g/cm3)",
    "09-03_23_APV_DENS-APAR-SECA (g/cm3)",
    "09-04_01_APV_ACIDEZ BG (ml/Kg)", "09-04_02_APV_SULFATOS (mg/Kg)",
    "09-04_03_APV_CARBONATOS (mg/Kg)", "09-04_04_APV_YESO (%SO4CaH2O)",
    "09-04_05_APV_SALES SOLUBLES", "09-04_06_APV_MAT ORGANICA (%)",
    "09-05_01_APV_CS (kPa)", "09-05_02_APV_CU (MPa)",
    "09-05_03_APV_BRASILEÑO (MPa)", "09-05_04_APV_FRANKLIN (Mpa)",
    "09-05_05_APV_CORTE DIRECTO-c(kPa)", "09-05_06_APV_CORTE DIRECTO-fi(°)",
    "09-05_07_APV_TRIAXIAL-c(kPa)", "09-05_08_APV_TRIAXIAL-fi(°)",
    "09-05_09_APV_EDOMETRO-Cc", "09-05_10_APV_EDOMETRO-Cs",
    "09-05_11_APV_EDOMETRO-e0", "09-05_12_APV_EDOMETRO-sigma'p (Kg/cm2)",
    "09-05_13_APV_EDOMETRO-Cv (m2/año)",
    "09-05_14_APV_LAMBE-HINCHAMIENTO (Mpa)",
    "09-05_15_APV_LAMBE-CAMBIO-POT-VOL",
    "09-05_16_APV_DENSIDAD-MAX(g/cm3)", "09-05_17_APV_DENSIDAD-MIN(g/cm3)",
    "09-05_18_APV_INDICE-COLAPSO (%)", "09-06_01_APV_LEFRANC-PERMEAB (%)",
    "09-07_01_APV_CO2-LIBRE (mg/l)", "09-07_02_APV_ACIDEZ (ud PH)",
    "09-07_03_APV_AMONIO (mg/l)", "09-07_04_APV_MAGNESIO (mg/l)",
    "09-07_05_APV_SULFATOS (mg/l)", "09-07_06_APV_RESIDUO SECO (mg/l)",
    "10_01_APV_ENLACE A FOTO", "10_02_APV_FECHA", "10_03_APV_DISCIPLINA"
]))

VALORES_VACIOS = {"", "nan", "none", "<na>", "null"}


def diagnosticar_nombre_bep(nombre_archivo):
    if not str(nombre_archivo).lower().endswith(".ifc"):
        return "❌ No tiene extensión .ifc"
    base = str(nombre_archivo)[:-4]
    partes = base.split("_")
    if len(partes) != 7:
        return (
            f"❌ Estructura incorrecta: tiene {len(partes)} "
            "bloques separados por '_' (se esperan 7)"
        )
    puerto, contrato, fase, tipo, disc, desc, rev = partes
    errores = []
    if puerto.upper() not in ["V", "S", "G"]:
        errores.append(f"Bloque 1 Puerto ('{puerto}'): debe ser V, S o G")
    if contrato.upper() != "N035":
        if contrato.upper() == "NO35":
            errores.append(
                "Bloque 2 Contrato ('NO35'): tiene letra 'O' en lugar "
                "del número '0' (debe ser N035)"
            )
        else:
            errores.append(f"Bloque 2 Contrato ('{contrato}'): debe ser 'N035'")
    if fase.upper() != "OB":
        if fase == "0B":
            errores.append(
                "Bloque 3 Fase ('0B'): tiene un cero '0' en vez "
                "de la letra 'O' (debe ser 'OB')"
            )
        else:
            errores.append(f"Bloque 3 Fase ('{fase}'): debe ser 'OB'")
    if not re.match(r"^[A-Za-z]{3}$", tipo):
        errores.append(
            f"Bloque 4 Tipo ('{tipo}'): debe tener 3 letras (ej. MOD, SEG)"
        )
    if not re.match(r"^[A-Za-z]{3}$", disc):
        errores.append(f"Bloque 5 Disciplina ('{disc}'): debe tener 3 letras")
    if not re.match(r"^[A-Za-z0-9\-]+$", desc):
        errores.append(f"Bloque 6 Descripción ('{desc}'): caracteres inválidos")
    if not re.match(r"^\d{2}[A-Za-z]$", rev):
        errores.append(
            f"Bloque 7 Revisión ('{rev}'): debe ser 2 dígitos + 1 letra"
        )
    if not errores:
        return "✅ Cumple patrón BEP"
    return "❌ No cumple: " + " | ".join(errores)


def generar_xml_navisworks(
    df_errores,
    nombre_set="Auditoria_APV_Elementos_Vacios",
    usar_id_nativo=False
):
    schema_url = (
        "http://download.autodesk.com/us/navisworks/schemas/"
        "nw-exchange-12.0.xsd"
    )
    xml = '<?xml version="1.0" encoding="UTF-8" ?>\n'
    xml += (
        '<exchange xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" '
        f'xsi:noNamespaceSchemaLocation="{schema_url}" units="m">\n'
    )
    xml += '  <selectionsets>\n'
    xml += f'    <selectionset name="{nombre_set}">\n'
    xml += '      <findspec mode="some" disjoint="0">\n'
    xml += '        <conditions>\n'
    if usar_id_nativo and "ID_Elemento" in df_errores.columns:
        valores = (
            df_errores["ID_Elemento"].dropna().astype(str).unique()[:1000]
        )
        prop_name = "Id"
    else:
        valores = df_errores["GlobalId"].dropna().astype(str).unique()[:1000]
        prop_name = "GlobalId"
    for val in valores:
        xml += '          <condition test="equals" flags="10">\n'
        xml += f'            <property><name>{prop_name}</name></property>\n'
        xml += f'            <value><data type="wstring">{val}</data></value>\n'
        xml += '          </condition>\n'
    xml += '        </conditions>\n'
    xml += '        <locator>/</locator>\n'
    xml += '      </findspec>\n'
    xml += '    </selectionset>\n'
    xml += '  </selectionsets>\n'
    xml += '</exchange>'
    return xml


BASE_DIR = os.path.dirname(os.path.abspath(__file__))
RUTA_PARQUET = os.path.join(BASE_DIR, "resumen_ifc_consolidado.parquet")

if not os.path.isfile(RUTA_PARQUET):
    st.error(f"No se encuentra el archivo: {RUTA_PARQUET}")
    st.stop()


@st.cache_data(show_spinner="Cargando base de datos BIM...")
def cargar_y_preparar_datos(ruta):
    df_load = pd.read_parquet(ruta, engine="pyarrow")
    df_load = df_load.loc[:, ~df_load.columns.duplicated()].copy()

    if "Peso_Archivo_MB" not in df_load.columns:
        df_load["Peso_Archivo_MB"] = 0.0
    else:
        df_load["Peso_Archivo_MB"] = pd.to_numeric(
            df_load["Peso_Archivo_MB"], errors="coerce"
        ).fillna(0.0)

    if "ID_Elemento" not in df_load.columns:
        df_load["ID_Elemento"] = df_load.get("GlobalId", "Sin_ID")

    cols_faltantes = [c for c in PARAMETROS_APV if c not in df_load.columns]
    if cols_faltantes:
        for col in cols_faltantes:
            df_load[col] = np.nan

    return df_load


try:
    df_original = cargar_y_preparar_datos(RUTA_PARQUET)
except Exception as e:
    st.error("Error al leer el archivo Parquet.")
    st.exception(e)
    st.stop()

if df_original.empty:
    st.error("El archivo Parquet no contiene registros.")
    st.stop()

# --- BARRA LATERAL Y FILTROS ---
st.sidebar.header("⚙ Filtros de Auditoría")
incluir_geo = st.sidebar.checkbox("Incluir Psets 09 (Geotecnia)", value=False)
if incluir_geo:
    params_auditar = PARAMETROS_APV
else:
    params_auditar = [p for p in PARAMETROS_APV if not p.startswith("09")]

ocultar_fantasmas = st.sidebar.checkbox(
    "Omitir sub-elementos fantasma (sin ningún Pset APV)", value=True
)
unificar_duplicados = st.sidebar.checkbox(
    "Eliminar/Unificar elementos duplicados", value=False
)

archivos_disp = sorted(
    df_original["Archivo_Origen"].dropna().unique().tolist()
)
sel_archivos = st.sidebar.multiselect(
    "Modelos IFC Auditados:", archivos_disp, default=archivos_disp
)

if not sel_archivos:
    st.warning("Selecciona al menos un modelo IFC en la barra lateral.")
    st.stop()

df = df_original[df_original["Archivo_Origen"].isin(sel_archivos)].copy()

if unificar_duplicados and not df.empty:
    df = df.drop_duplicates(
        subset=["Archivo_Origen", "GlobalId"], keep="first"
    ).copy()

# --- CÁLCULO VECTORIZADO POR COLUMNA ---
n_filas = len(df)
cant_apv_presentes = np.zeros(n_filas, dtype=np.uint16)
cant_vacios = np.zeros(n_filas, dtype=np.uint16)
cant_comodines = np.zeros(n_filas, dtype=np.uint16)

for col in params_auditar:
    s = df[col]
    s_str = s.astype(str).str.strip()
    es_vacio = (s.isna() | s_str.str.lower().isin(VALORES_VACIOS)).to_numpy()
    es_comodin = (s_str == "-").to_numpy()

    cant_vacios += es_vacio.astype(np.uint16)
    cant_comodines += es_comodin.astype(np.uint16)
    cant_apv_presentes += (~es_vacio).astype(np.uint16)

df["Cant_APV_Presentes"] = cant_apv_presentes
df["Cant_Vacios"] = cant_vacios
df["Cant_Comodines"] = cant_comodines
df["Tiene_Vacios"] = cant_vacios > 0

archivos_totalmente_vacios = [
    arch_name for arch_name, grp_raw in df.groupby("Archivo_Origen")
    if (grp_raw["Cant_APV_Presentes"] > 0).sum() == 0
]

n_fantasmas_detectados = int((df["Cant_APV_Presentes"] == 0).sum())
if ocultar_fantasmas and n_fantasmas_detectados > 0:
    if (df["Cant_APV_Presentes"] > 0).sum() > 0:
        cond_real = df["Cant_APV_Presentes"] > 0
        cond_vacio = df["Archivo_Origen"].isin(archivos_totalmente_vacios)
        df = df[cond_real | cond_vacio].copy()
        st.sidebar.success(
            f"🧹 Filtrados {n_fantasmas_detectados:,} sub-elementos "
            f"sin Psets APV. Auditando {len(df):,} elementos."
        )

# --- PESTAÑAS ---
tab1, tab2, tab3, tab4, tab5, tab6, tab7, tab8, tab9 = st.tabs([
    "📖 1. Cumplimiento BEP Naming",
    "🌍 2. Georreferenciación",
    "🧱 3. Integridad IFC",
    "✍️ 4. Calidad de Formato",
    "🕳️ 5. Auditoría de Vacíos",
    "🎯 6. Navisworks Manage",
    "❤️ 7. Salud del Proyecto",
    "🚨 8. Alertas IFCs Vacíos",
    "📐 9. Grupos de parámetros"
])

# --- PESTAÑA 1 ---
with tab1:
    st.subheader("1. Cumplimiento BEP Naming (Anejo 02)")
    res_naming = []
    for arch, grp in df.groupby("Archivo_Origen"):
        diag = diagnosticar_nombre_bep(arch)
        esquema = (
            grp["Esquema_IFC"].iloc[0]
            if "Esquema_IFC" in grp.columns else "No definido"
        )
        peso = grp["Peso_Archivo_MB"].iloc[0]
        es_ifc_ok = (
            "IFC4" in str(esquema).upper()
            or "IFC2X3" in str(esquema).upper()
        )
        res_naming.append({
            "Archivo IFC": arch,
            "Cumple Nomenclatura BEP (y Razón Exacta)": diag,
            "Esquema IFC": esquema,
            "Estado Esquema": "✅ IFC4 / IFC2x3" if es_ifc_ok else "⚠️ Revisar",
            "Peso Extraído (MB)": peso,
            "Elementos Reales Auditados": len(grp)
        })
    st.dataframe(pd.DataFrame(res_naming), use_container_width=True)

# --- PESTAÑA 2 ---
with tab2:
    st.subheader("2. Auditoría de Georreferenciación (ETRS89 / IfcSite)")
    res_geo = []
    for arch, grp in df.groupby("Archivo_Origen"):
        res_geo.append({
            "Archivo IFC": arch,
            "CRS / EPSG": (
                grp["EPSG"].iloc[0] if "EPSG" in grp.columns else "No definido"
            ),
            "Origen Site X": (
                grp["Origen_X"].iloc[0] if "Origen_X" in grp.columns else 0.0
            ),
            "Origen Site Y": (
                grp["Origen_Y"].iloc[0] if "Origen_Y" in grp.columns else 0.0
            ),
            "Origen Site Z": (
                grp["Origen_Z"].iloc[0] if "Origen_Z" in grp.columns else 0.0
            ),
            "Elevación Ref (m)": (
                grp["Elevacion_Site"].iloc[0]
                if "Elevacion_Site" in grp.columns else 0.0
            ),
            "Latitud (IfcSite)": (
                grp["Latitud_Site"].iloc[0]
                if "Latitud_Site" in grp.columns else "No definida"
            ),
            "Longitud (IfcSite)": (
                grp["Longitud_Site"].iloc[0]
                if "Longitud_Site" in grp.columns else "No definida"
            )
        })
    df_geo = pd.DataFrame(res_geo)
    st.dataframe(df_geo, use_container_width=True)
    dif_x = df_geo["Origen Site X"].nunique() > 1
    dif_y = df_geo["Origen Site Y"].nunique() > 1
    if len(df_geo) > 1 and (dif_x or dif_y):
        st.warning(
            "⚠️ Se detectan diferencias en las coordenadas de origen "
            "(IfcSite) entre los distintos modelos."
        )
    else:
        st.success(
            "✅ Consistencia espacial verificada en el emplazamiento (IfcSite)."
        )

# --- PESTAÑA 3 ---
with tab3:
    st.subheader("3. Integridad IFC y Clasificación de Entidades")
    conteo_clases = (
        df.groupby(["Archivo_Origen", "Clase_IFC"])
        .size()
        .reset_index(name="Cantidad")
    )
    fig_clases = px.bar(
        conteo_clases,
        x="Clase_IFC",
        y="Cantidad",
        color="Archivo_Origen",
        barmode="group",
        title="Distribución de Clases IFC por Modelo"
    )
    st.plotly_chart(fig_clases, use_container_width=True)

    proxys = df[df["Clase_IFC"] == "IfcBuildingElementProxy"]
    st.metric("Elementos Genéricos (IfcBuildingElementProxy)", len(proxys))
    if not proxys.empty:
        st.warning(
            f"Mostrando primeros 1.000 de {len(proxys):,} "
            "elementos genéricos detectados:"
        )
        cols_proxy = [
            "Archivo_Origen", "ID_Elemento", "GlobalId", "Clase_IFC", "Nombre"
        ]
        st.dataframe(
            proxys[cols_proxy].head(1000),
            use_container_width=True
        )

# --- PESTAÑA 4 ---
with tab4:
    st.subheader("4. Calidad de Formato (Estricto APV vs BEP)")
    st.markdown(
        "El comodín **`-`** está permitido por el BEP y no genera error. "
        "Se auditan unidades, estados, espacios y comodines inválidos."
    )

    errores_fmt = []
    uni_validas = {"ud", "m", "m2", "dm3", "m3", "kg", "tn", "pa"}
    est_validos = {
        "Existente", "Demolido", "Temporal", "Proyectado", "Construido"
    }
    placeholders_malos = {
        "n/a", "na", "null", "none", "tbd",
        "sin definir", "por definir", "--", "."
    }

    for col in params_auditar:
        s_raw = df[col].dropna().astype(str)
        if s_raw.empty:
            continue
        s_strip = s_raw.str.strip()
        s_low = s_strip.str.lower()

        mask_valido = ~s_low.isin(VALORES_VACIOS) & (s_strip != "-")
        s_raw = s_raw[mask_valido]
        if s_raw.empty:
            continue

        s_strip = s_strip[mask_valido]
        s_low = s_low[mask_valido]

        err_esp = s_raw != s_strip
        err_plc = s_low.isin(placeholders_malos)
        if "TIPO-MED" in col.upper():
            err_uni = ~s_low.isin(uni_validas)
        else:
            err_uni = pd.Series(False, index=s_raw.index)

        if "ESTADO" in col.upper():
            err_est = ~s_strip.str.capitalize().isin(est_validos)
        else:
            err_est = pd.Series(False, index=s_raw.index)

        mask_err = err_esp | err_plc | err_uni | err_est
        if mask_err.any():
            for idx in s_raw[mask_err].index[:500]:
                mot = []
                if err_esp.loc[idx]:
                    mot.append("Espacios en blanco al inicio o final")
                if err_plc.loc[idx]:
                    mot.append("Comodín no permitido (debe usarse '-')")
                if err_uni.loc[idx]:
                    mot.append(f"Unidad no permitida ('{s_strip.loc[idx]}')")
                if err_est.loc[idx]:
                    mot.append(f"Estado no válido ('{s_strip.loc[idx]}')")
                errores_fmt.append({
                    "Archivo": df.at[idx, "Archivo_Origen"],
                    "ID_Elemento": df.at[idx, "ID_Elemento"],
                    "GlobalId": df.at[idx, "GlobalId"],
                    "Parámetro": col,
                    "Contenido Detectado": s_raw.loc[idx],
                    "Infracción BEP": " + ".join(mot)
                })
                if len(errores_fmt) >= 2000:
                    break
        if len(errores_fmt) >= 2000:
            break

    if errores_fmt:
        df_err_fmt = pd.DataFrame(errores_fmt)
        st.error(
            f"⚠️ Se detectaron infracciones de formato "
            f"(mostrando primeros {len(df_err_fmt)} registros):"
        )
        st.dataframe(df_err_fmt, use_container_width=True)
    else:
        st.success(
            "✅ Todos los parámetros rellenos cumplen con el formato del BEP."
        )

# --- PESTAÑA 5 ---
with tab5:
    st.subheader(
        f"5. Auditoría Exclusiva de los {len(params_auditar)} "
        "Parámetros Oficiales APV"
    )
    st.markdown(
        "Si un parámetro contiene **`-`**, se valida como **Comodín BEP "
        "en Verde (`🟢`)**. Si faltan elementos (`🔴`), se muestran "
        "hasta 50 IDs para localizarlos en tu NWD."
    )

    resumen_params = []
    total_el = len(df)
    for p in params_auditar:
        s_str = df[p].astype(str).str.strip()
        es_vac = df[p].isna() | s_str.str.lower().isin(VALORES_VACIOS)
        es_com = (s_str == "-")
        n_vac = int(es_vac.sum())
        n_com = int(es_com.sum())
        n_datos = total_el - n_vac - n_com
        pct_valido = (
            round(((n_datos + n_com) / total_el) * 100, 1)
            if total_el > 0 else 0.0
        )

        if n_vac == 0 and n_com > 0:
            estado_str = "🟢 Comodín BEP (-)"
            ids_faltantes, guids_faltantes = "-", "-"
        elif n_vac == 0:
            estado_str = "🟢 Completo (Dato)"
            ids_faltantes, guids_faltantes = "-", "-"
        else:
            estado_str = f"🔴 Faltan {n_vac:,} elementos"
            ids_faltantes = ", ".join(
                df.loc[es_vac, "ID_Elemento"].astype(str).head(50).tolist()
            )
            guids_faltantes = ", ".join(
                df.loc[es_vac, "GlobalId"].astype(str).head(50).tolist()
            )

        resumen_params.append({
            "Parámetro Oficial APV": p,
            "Estado Auditoría": estado_str,
            "Con Dato Real": n_datos,
            "Con Comodín (-) Válido": n_com,
            "Vacíos (Error)": n_vac,
            "% Cumplimiento (Dato + '-')": pct_valido,
            "ID_Elemento Faltantes (Muestra 50)": ids_faltantes,
            "GlobalId Faltantes (Muestra 50)": guids_faltantes
        })
    df_res_vacios = pd.DataFrame(resumen_params)

    def colorear_estado(val):
        if "🟢" in str(val):
            return "background-color: #d4edda; color: #155724; font-weight: bold;"
        return "background-color: #f8d7da; color: #721c24; font-weight: bold;"

    st.dataframe(
        df_res_vacios.style.map(colorear_estado, subset=["Estado Auditoría"]),
        use_container_width=True
    )

    df_elem_inc = df[df["Tiene_Vacios"]].head(500).copy()
    if not df_elem_inc.empty:
        tot_inc = int(df["Tiene_Vacios"].sum())
        st.markdown(
            f"#### 🔍 Muestra de los primeros 500 Elementos con algún "
            f"parámetro vacío (de {tot_inc:,} totales):"
        )
        mat_vac = (
            df_elem_inc[params_auditar].isna()
            | df_elem_inc[params_auditar].astype(str).apply(
                lambda s: s.str.strip().str.lower().isin(VALORES_VACIOS)
            )
        )
        df_elem_inc["Parámetros_Vacíos"] = mat_vac.apply(
            lambda r: ", ".join(r.index[r]), axis=1
        )
        cols_inc = [
            "Archivo_Origen", "ID_Elemento", "GlobalId",
            "Clase_IFC", "Nombre", "Cant_Vacios", "Parámetros_Vacíos"
        ]
        st.dataframe(df_elem_inc[cols_inc], use_container_width=True)

# --- PESTAÑA 6 ---
with tab6:
    st.subheader(
        "6. Centro de Coordinación e Interferencias para Navisworks Manage"
    )
    df_con_vacios = df[df["Tiene_Vacios"]]

    c1, c2 = st.columns(2)
    with c1:
        st.markdown("#### 📥 1. Descargar Search Sets XML para Navisworks")
        opciones_nw = (
            ["TODOS los elementos con algún vacío"] + params_auditar
        )
        param_filtro_nw = st.selectbox(
            "Seleccionar grupo de elementos vacíos a aislar:", opciones_nw
        )
        if param_filtro_nw == "TODOS los elementos con algún vacío":
            df_target_nw = df_con_vacios
            nombre_xml = "APV_Todos_Los_Vacios"
        else:
            s_col_nw = df[param_filtro_nw].astype(str).str.strip()
            cond_nw = (
                df[param_filtro_nw].isna()
                | s_col_nw.str.lower().isin(VALORES_VACIOS)
            )
            df_target_nw = df[cond_nw]
            nombre_xml = f"APV_Vacio_{param_filtro_nw}"

        usar_id_nativo = st.checkbox(
            "Usar ID_Elemento nativo (Tag) en lugar de GlobalId", value=True
        )
        st.write(
            f"Elementos seleccionados: **{len(df_target_nw):,}** "
            "(exporta hasta 1.000 únicos por lote)"
        )

        if not df_target_nw.empty:
            xml_str = generar_xml_navisworks(
                df_target_nw,
                nombre_set=nombre_xml,
                usar_id_nativo=usar_id_nativo
            )
            st.download_button(
                label=f"⬇️ Descargar XML ({min(len(df_target_nw), 1000)} elem.)",
                data=xml_str,
                file_name=f"{nombre_xml}.xml",
                mime="text/xml"
            )
        else:
            st.info("No hay elementos vacíos para este filtro seleccionado.")

    with c2:
        st.markdown("#### 🔍 2. Auditoría de IDs Duplicados")
        if not df.empty and "ID_Elemento" in df.columns:
            duplicados_id = df[
                df.duplicated(
                    subset=["Archivo_Origen", "ID_Elemento"], keep=False
                )
            ]
            n_dups = len(duplicados_id)
            if n_dups > 0:
                st.warning(
                    f"⚠️ Se detectaron **{n_dups:,} elementos** con "
                    "ID_Elemento duplicado (mostrando primeros 500):"
                )
                cols_dup = [
                    "Archivo_Origen", "ID_Elemento",
                    "GlobalId", "Clase_IFC", "Nombre"
                ]
                st.dataframe(
                    duplicados_id[cols_dup].head(500),
                    use_container_width=True
                )
            else:
                st.success(
                    "✅ No existen ID_Elemento duplicados en los modelos."
                )
        else:
            st.info("Sin datos para analizar duplicados.")

# --- PESTAÑA 7 ---
with tab7:
    st.subheader("7. Salud del Proyecto y Métricas Generales")
    c_s1, c_s2, c_s3 = st.columns(3)
    c_s1.metric("Modelos IFC Analizados", len(archivos_disp))
    c_s2.metric("Total Elementos en Parquet", f"{len(df_original):,}")
    df_pesos = (
        df_original[["Archivo_Origen", "Peso_Archivo_MB"]].drop_duplicates()
    )
    peso_total = df_pesos["Peso_Archivo_MB"].sum()
    c_s3.metric("Peso Consolidado de Modelos", f"{round(peso_total, 2)} MB")

    fig_peso = px.bar(
        df_pesos,
        x="Archivo_Origen",
        y="Peso_Archivo_MB",
        title="Peso de Modelos IFC (MB)",
        text="Peso_Archivo_MB"
    )
    st.plotly_chart(fig_peso, use_container_width=True)

# --- PESTAÑA 8 ---
with tab8:
    st.subheader("🚨 8. Alertas y Diagnóstico de IFCs Vacíos por Modelo")
    resumen_modelos_alt = []
    for arch, grp in df.groupby("Archivo_Origen"):
        tot = len(grp)
        n_v_m = int(grp["Tiene_Vacios"].sum())
        if tot == 0:
            est = "🚨 IFC Vacío"
        elif n_v_m == tot:
            est = "🚨 100% Incompleto"
        elif n_v_m > 0:
            est = f"🔴 Parcial ({n_v_m:,} con algún vacío)"
        else:
            est = "🟢 100% Completo"
        resumen_modelos_alt.append({
            "Archivo IFC": arch,
            "Elementos Auditados": tot,
            "Estado General": est
        })
    st.dataframe(pd.DataFrame(resumen_modelos_alt), use_container_width=True)

# --- PESTAÑA 9 ---
with tab9:
    st.subheader("📐 9. Grupos de parámetros")
    st.markdown(
        "Informe detallado por modelo sobre los grupos de parámetros "
        "detectados según el BEP (**Geotecnia = 11 grupos**; "
        "**Resto = 9 grupos**)."
    )

    info_grupos = []
    cols_todas_apv = [c for c in df_original.columns if "APV" in c]

    for arch, df_m in df_original.groupby("Archivo_Origen"):
        nombre_inf = str(arch).lower()
        if "geo" in nombre_inf:
            tipo_modelo = "Modelo de Geotecnia"
            grupos_teoricos = 11
        else:
            tipo_modelo = "Modelo Estándar / Proyecto"
            grupos_teoricos = 9

        grupos_hallados = set()
        for c in cols_todas_apv:
            prefijo = c.split("_")[0] if "_" in c else ""
            s_col_m = df_m[c].dropna().astype(str).str.strip().str.lower()
            if (~s_col_m.isin(VALORES_VACIOS)).any():
                grupos_hallados.add(prefijo)

        listado_str = (
            ", ".join(sorted(list(grupos_hallados)))
            if grupos_hallados else "Ninguno"
        )
        info_grupos.append({
            "Archivo IFC": arch,
            "Tipo de Modelo": tipo_modelo,
            "Grupos Teóricos (BEP)": grupos_teoricos,
            "Grupos Totales Detectados": len(grupos_hallados),
            "Grupos Específicos Detectados": listado_str
        })

    st.dataframe(pd.DataFrame(info_grupos), use_container_width=True)