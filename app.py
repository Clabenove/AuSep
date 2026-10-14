import os
import re
import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import time

st.set_page_config(page_title="Auditoría BIM & Cumplimiento BEP - APV", page_icon="📋", layout="wide")
st.title("📋 Dashboard Integral de Auditoría BIM - APV")

# Lista exclusiva y sin duplicados de los parámetros oficiales APV
PARAMETROS_APV = list(dict.fromkeys([
    "01_01_APV_PROYECTO", "01_02_APV_FASE", "01_03_APV_ESTADO", "01_04_APV_TIPOLOGIA",
    "01_05_APV_DISCIPLINA", "01_06_APV_SUBDISCIPLINA", "01_07_APV_ELEMENTO", "01_08_APV_CLASIFICACION",
    "01_09_APV_NOMBRE", "01_10_APV_ALINEACION", "01_11_APV_NUMERO", "01_12_APV_MATERIAL",
    "01_13_APV_CAD", "01_14_APV_ZONA", "02_01_APV_CAPITULO", "02_02_APV_SUBCAPITULO-1",
    "02_03_APV_SUBCAPITULO-2", "02_04_01_APV_MEDICION", "02_04_02_APV_MEDICION-ASOC-1",
    "02_04_03_APV_MEDICION-ASOC-2", "02_04_04_APV_MEDICION-ASOC-3", "02_05_01_APV_UNIDAD-OBRA",
    "02_05_02_APV_UO-ASOC-1", "02_05_03_APV_UO-ASOC-2", "02_05_04_APV_UO-ASOC-3",
    "02_06_01_APV_TIPO-MED", "02_06_02_APV_TM-ASOC-1", "02_06_03_APV_TM-ASOC-2",
    "02_06_04_APV_TM-ASOC-3", "03_01_APV_FASE-OBRA", "03_02_APV_PLANOS", "03_03_APV_PPTP",
    "03_04_APV_CALIDAD-MOD", "04_01_APV_CÓDIGO-TAREA", "04_02_APV_NOMBRE-TAREA",
    "04_03_APV_INICIO-EJECUCION", "04_04_APV_FIN-EJECUCION", "04_05_APV_PLAN-REF",
    "04_06_APV_CERTIF-REF", "04_07_APV_CERTIF", "04_08_APV_PORCENTAJE-EJECUTADO",
    "04_09_APV_CERTIF-MED", "04_10_APV_CERTIF-MED-ASOC-1", "04_11_APV_CERTIF-MED-ASOC-2",
    "04_12_APV_CERTIF-MED-ASOC-3", "05_01_APV_SEG-SALUD", "05_02_APV_INFORMES-APROBACION",
    "05_03_APV_CONTROL-CALIDAD", "05_03_01_APV_COD-TRAZ", "05_04_APV_ENSAYOS",
    "05_05_APV_FOTOGRAFIAS", "05_06_APV_MEDIO-AMBIENTE", "05_07_APV_GESTION-RESIDUOS",
    "05_08_APV_SERV-AFECTADOS", "06_01_APV_PRY-LIQUIDACION", "06_02_APV_LIBRO-EDIF",
    "07_01_APV_CAPA-GIS", "07_02_APV_CAMPO-1", "07_03_APV_CAMPO-2", "07_04_APV_CAMPO-3",
    "07_05_APV_CAMPO-4", "07_06_APV_CAMPO-5", "07_07_APV_CAMPO-6", "07_08_APV_CAMPO-7",
    "07_09_APV_CAMPO-8", "07_10_APV_CAMPO-9", "07_11_APV_CAMPO-10", "07_12_APV_CAMPO-N",
    "08_01_APV_PLAN-MANTENIMIENTO", "08_02_APV_MANUALES-FICHAS", "08_03_APV_COD-MANTENIMIENTO",
    "08_04_APV_COD-EXPLOTACION", "08_05_APV_AUX-EXPLOTACION", "08_06_APV_COD-CONTABLE",
    "08_07_APV_CAP-CONTABLE", "08_08_APV_SUB-CAP-CONTABLE", "09-02_00_APV_PROYECTO",
    "09-02_01_APV_SONDEO", "09-02_02_APV_COTA-MUESTRA(m)", "09-02_03_APV_DESC-ESTRATO",
    "09-02_04_APV_TIPO", "09-02_05_APV_NÚMERO MUESTRA", "09-03_01_APV_PASA-100 (%)",
    "09-03_02_APV_PASA-80 (%)", "09-03_03_APV_PASA-63 (%)", "09-03_04_APV_PASA-50 (%)",
    "09-03_05_APV_PASA-40 (%)", "09-03_06_APV_PASA-25 (%)", "09-03_07_APV_PASA-20 (%)",
    "09-03_08_APV_PASA-12,5 (%)", "09-03_09_APV_PASA-10 (%)", "09-03_10_APV_PASA-6,3 (%)",
    "09-03_11_APV_PASA-5 (%)", "09-03_12_APV_PASA-2 (%)", "09-03_13_APV_PASA-1,25 (%)",
    "09-03_14_APV_PASA-0,4 (%)", "09-03_15_APV_PASA-0,16 (%)", "09-03_16_APV_PASA-0,08 (%)",
    "09-03_17_APV_ATTERBERG-LL", "09-03_18_APV_ATTERBERG-LP", "09-03_19_APV_ATTERBERG-IP",
    "09-03_20_APV_HN (%)", "09-03_21_APV_DENS-APAR-HUMEDA (g/cm3)", "09-03_22_APV_DENS-APAR-SECA (g/cm3)",
    "09-03_23_APV_DENS-APAR-SECA (g/cm3)", "09-04_01_APV_ACIDEZ BG (ml/Kg)", "09-04_02_APV_SULFATOS (mg/Kg)",
    "09-04_03_APV_CARBONATOS (mg/Kg)", "09-04_04_APV_YESO (%SO4CaH2O)", "09-04_05_APV_SALES SOLUBLES",
    "09-04_06_APV_MAT ORGANICA (%)", "09-05_01_APV_CS (kPa)", "09-05_02_APV_CU (MPa)",
    "09-05_03_APV_BRASILEÑO (MPa)", "09-05_04_APV_FRANKLIN (Mpa)", "09-05_05_APV_CORTE DIRECTO-c(kPa)",
    "09-05_06_APV_CORTE DIRECTO-fi(°)", "09-05_07_APV_TRIAXIAL-c(kPa)", "09-05_08_APV_TRIAXIAL-fi(°)",
    "09-05_09_APV_EDOMETRO-Cc", "09-05_10_APV_EDOMETRO-Cs", "09-05_11_APV_EDOMETRO-e0",
    "09-05_12_APV_EDOMETRO-sigma'p (Kg/cm2)", "09-05_13_APV_EDOMETRO-Cv (m2/año)",
    "09-05_14_APV_LAMBE-HINCHAMIENTO (Mpa)", "09-05_15_APV_LAMBE-CAMBIO-POT-VOL",
    "09-05_16_APV_DENSIDAD-MAX(g/cm3)", "09-05_17_APV_DENSIDAD-MIN(g/cm3)",
    "09-05_18_APV_INDICE-COLAPSO (%)", "09-06_01_APV_LEFRANC-PERMEAB (%)", "09-07_01_APV_CO2-LIBRE (mg/l)",
    "09-07_02_APV_ACIDEZ (ud PH)", "09-07_03_APV_AMONIO (mg/l)", "09-07_04_APV_MAGNESIO (mg/l)",
    "09-07_05_APV_SULFATOS (mg/l)", "09-07_06_APV_RESIDUO SECO (mg/l)", "10_01_APV_ENLACE A FOTO",
    "10_02_APV_FECHA", "10_03_APV_DISCIPLINA"
]))

def diagnosticar_nombre_bep(nombre_archivo):
    if not str(nombre_archivo).lower().endswith(".ifc"):
        return "❌ No tiene extensión .ifc"
    base = str(nombre_archivo)[:-4]
    partes = base.split("_")
    if len(partes) != 7:
        return f"❌ Estructura incorrecta: tiene {len(partes)} bloques separados por '_' (se esperan 7)"
    puerto, contrato, fase, tipo, disc, desc, rev = partes
    errores = []
    if puerto.upper() not in ["V", "S", "G"]:
        errores.append(f"Bloque 1 Puerto ('{puerto}'): debe ser V, S o G")
    if contrato.upper() != "N035":
        if contrato.upper() == "NO35":
            errores.append("Bloque 2 Contrato ('NO35'): tiene letra 'O' en lugar del número '0' (debe ser N035)")
        else:
            errores.append(f"Bloque 2 Contrato ('{contrato}'): debe ser 'N035'")
    if fase.upper() != "OB":
        if fase == "0B":
            errores.append("Bloque 3 Fase ('0B'): tiene un número cero '0' en vez de la letra 'O' (debe ser 'OB')")
        else:
            errores.append(f"Bloque 3 Fase ('{fase}'): debe ser 'OB'")
    if not re.match(r"^[A-Za-z]{3}$", tipo):
        errores.append(f"Bloque 4 Tipo ('{tipo}'): debe tener 3 letras (ej. MOD, SEG, MOF)")
    if not re.match(r"^[A-Za-z]{3}$", disc):
        errores.append(f"Bloque 5 Disciplina ('{disc}'): debe tener 3 letras")
    if not re.match(r"^[A-Za-z0-9\-]+$", desc):
        errores.append(f"Bloque 6 Descripción ('{desc}'): caracteres no válidos")
    if not re.match(r"^\d{2}[A-Za-z]$", rev):
        errores.append(f"Bloque 7 Revisión ('{rev}'): debe ser 2 dígitos + 1 letra (ej. 01E)")
    return "✅ Cumple patrón BEP" if not errores else "❌ No cumple: " + " | ".join(errores)

def generar_xml_navisworks(df_errores, nombre_set="Auditoria_APV_Elementos_Vacios", usar_id_nativo=False):
    xml = '<?xml version="1.0" encoding="UTF-8" ?>\n'
    xml += '<exchange xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:noNamespaceSchemaLocation="http://download.autodesk.com/us/navisworks/schemas/nw-exchange-12.0.xsd" units="m">\n'
    xml += '  <selectionsets>\n'
    xml += f'    <selectionset name="{nombre_set}">\n'
    xml += '      <findspec mode="some" disjoint="0">\n'
    xml += '        <conditions>\n'
    if usar_id_nativo and "ID_Elemento" in df_errores.columns:
        valores = df_errores["ID_Elemento"].dropna().astype(str).unique()[:1000]
        prop_name = "Id"
    else:
        valores = df_errores["GlobalId"].dropna().astype(str).unique()[:1000]
        prop_name = "GlobalId"
    for val in valores:
        xml += f'          <condition test="equals" flags="10">\n'
        xml += f'            <property><name>{prop_name}</name></property>\n'
        xml += f'            <value><data type="wstring">{val}</data></value>\n'
        xml += f'          </condition>\n'
    xml += '        </conditions>\n'
    xml += '        <locator>/</locator>\n'
    xml += '      </findspec>\n'
    xml += '    </selectionset>\n'
    xml += '  </selectionsets>\n'
    xml += '</exchange>'
    return xml

# DIAGNÓSTICO TEMPORAL: CARGA EXCLUSIVA DESDE PARQUET
# Este bloque no usa Excel ni caché para identificar dónde se detiene la ejecución.
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
RUTA_PARQUET = os.path.join(
    BASE_DIR,
    "resumen_ifc_consolidado.parquet"
)

print("[DIAG 1] Inicio de carga del Parquet", flush=True)
print(f"[DIAG] Ruta: {RUTA_PARQUET}", flush=True)

if not os.path.isfile(RUTA_PARQUET):
    st.error(f"No se encuentra el archivo: {RUTA_PARQUET}")
    print("[DIAG ERROR] El archivo no existe", flush=True)
    st.stop()

try:
    inicio = time.perf_counter()

    with st.spinner("Leyendo archivo Parquet..."):
        # Temporalmente sin @st.cache_data para diagnosticar la lectura real.
        df_original = pd.read_parquet(
            RUTA_PARQUET,
            engine="pyarrow"
        )

    duracion = time.perf_counter() - inicio

    print(
        f"[DIAG 2] Lectura completada: "
        f"{df_original.shape[0]} filas, "
        f"{df_original.shape[1]} columnas, "
        f"{duracion:.2f} segundos",
        flush=True
    )

    st.success(
        f"Parquet leído correctamente en {duracion:.2f} segundos."
    )
    st.write(
        f"Registros: {len(df_original):,} | "
        f"Columnas: {len(df_original.columns):,}"
    )

except Exception as e:
    print(f"[DIAG ERROR] {type(e).__name__}: {e}", flush=True)
    st.error("Error al leer el archivo Parquet.")
    st.exception(e)
    st.stop()

# Evitar nombres de columna duplicados antes de procesar la auditoría.
df_original = df_original.loc[
    :, ~df_original.columns.duplicated()
].copy()

if df_original.empty:
    st.error("El archivo Parquet no contiene registros.")
    st.stop()

print(
    "[DIAG 3] Preparación inicial completada. "
    "Continúa el procesamiento de la auditoría.",
    flush=True
)

if "Peso_Archivo_MB" not in df_original.columns:
    df_original["Peso_Archivo_MB"] = 0.0
else:
    df_original["Peso_Archivo_MB"] = pd.to_numeric(df_original["Peso_Archivo_MB"], errors="coerce").fillna(0.0)

if "ID_Elemento" not in df_original.columns:
    df_original["ID_Elemento"] = df_original.get("GlobalId", "Sin_ID")

for col in PARAMETROS_APV:
    if col not in df_original.columns:
        df_original[col] = np.nan
print(f"[DIAG 4] Parámetros APV preparados: {df_original.shape[0]} filas x {df_original.shape[1]} columnas", flush=True)

st.sidebar.header("⚙ Filtros de Auditoría")
incluir_geo = st.sidebar.checkbox("Incluir Psets 09 (Geotecnia)", value=False)
params_auditar = PARAMETROS_APV if incluir_geo else [p for p in PARAMETROS_APV if not p.startswith("09")]

ocultar_fantasmas = st.sidebar.checkbox(
    "Omitir sub-elementos fantasma (sin ningún Pset APV)",
    value=True
)
unificar_duplicados = st.sidebar.checkbox(
    "Eliminar/Unificar elementos duplicados (quedarse con dato lleno)",
    value=True
)

archivos_disp = sorted(df_original["Archivo_Origen"].dropna().unique().tolist())
sel_archivos = st.sidebar.multiselect("Modelos IFC Auditados:", archivos_disp, default=archivos_disp)
df = df_original[df_original["Archivo_Origen"].isin(sel_archivos)].copy()
print(f"[DIAG 5] Filtro de modelos completado: {df.shape[0]} filas x {df.shape[1]} columnas", flush=True)

if unificar_duplicados and not df.empty:
    print("[DIAG 6A] Inicio de unificación de duplicados", flush=True)
    df = df.replace(["", "nan", "None", "<NA>"], np.nan)
    df = df.groupby(["Archivo_Origen", "GlobalId"], as_index=False).first()
    print(f"[DIAG 6B] Unificación terminada: {df.shape[0]} filas x {df.shape[1]} columnas", flush=True)

print(f"[DIAG 7A] Inicio de cálculo de presencia APV: {len(df):,} filas x {len(params_auditar)} parámetros", flush=True)
matriz_apv = df[params_auditar].astype(str).apply(lambda s: s.str.strip())
matriz_llena = df[params_auditar].notna() & ~matriz_apv.apply(lambda s: s.str.lower().isin(["", "nan", "none", "<na>"]))
df["Cant_APV_Presentes"] = matriz_llena.sum(axis=1)
print("[DIAG 7B] Cálculo de presencia APV terminado", flush=True)

archivos_totalmente_vacios = []
for arch_name, grp_raw in df.groupby("Archivo_Origen"):
    if (grp_raw["Cant_APV_Presentes"] > 0).sum() == 0:
        archivos_totalmente_vacios.append(arch_name)

n_fantasmas_detectados = int((df["Cant_APV_Presentes"] == 0).sum())
if ocultar_fantasmas and n_fantasmas_detectados > 0:
    if (df["Cant_APV_Presentes"] > 0).sum() > 0:
        df = df[(df["Cant_APV_Presentes"] > 0) | (df["Archivo_Origen"].isin(archivos_totalmente_vacios))].copy()
        st.sidebar.success(f"🧹 Se filtraron {n_fantasmas_detectados} sub-elementos internos sin Psets APV. Auditando {len(df)} elementos reales.")

print("[DIAG 8A] Inicio del cálculo de parámetros vacíos y comodines", flush=True)
dict_vacios_elem = {idx: [] for idx in df.index}
dict_comodines_elem = {idx: 0 for idx in df.index}

for col in params_auditar:
    s_str = df[col].astype(str).str.strip()
    es_vacio = df[col].isna() | s_str.str.lower().isin(["", "nan", "none", "<na>"])
    es_comodin = (s_str == "-")
    for idx in es_vacio[es_vacio].index:
        dict_vacios_elem[idx].append(col)
    for idx in es_comodin[es_comodin].index:
        dict_comodines_elem[idx] += 1

df["Cant_Vacios"] = [len(dict_vacios_elem[i]) for i in df.index]
df["Cant_Comodines"] = [dict_comodines_elem[i] for i in df.index]
df["Tiene_Vacios"] = df["Cant_Vacios"] > 0
df["Parámetros_Vacíos"] = [", ".join(dict_vacios_elem[i]) for i in df.index]
print("[DIAG 8B] Cálculo de vacíos terminado; comenzando a construir las pestañas", flush=True)

# 8 pestañas originales + 1 nueva pestaña "Grupos de parámetros"
tab1, tab2, tab3, tab4, tab5, tab6, tab7, tab8, tab9 = st.tabs([
    "📖 1. Cumplimiento BEP Naming",
    "🌍 2. Georreferenciación",
    "🧱 3. Integridad IFC",
    "✍️ 4. Calidad de Formato",
    "🕳️ 5. Auditoría de Vacíos",
    "🎯 6. Navisworks Manage",
    "❤️ 7. Salud del Proyecto",
    "🚨 8. Alertas IFCs Vacíos",
    "Grupos de parámetros"
])

# --- PESTAÑA 1: CUMPLIMIENTO BEP NAMING ---
print("[DIAG TAB 1] Inicio de la pestaña 1", flush=True)
with tab1:
    st.subheader("1. Cumplimiento BEP Naming (Anejo 02)")
    res_naming = []
    for arch, grp in df.groupby("Archivo_Origen"):
        diag = diagnosticar_nombre_bep(arch)
        esquema = grp["Esquema_IFC"].iloc[0] if "Esquema_IFC" in grp.columns else "No definido"
        peso = grp["Peso_Archivo_MB"].iloc[0]
        res_naming.append({
            "Archivo IFC": arch,
            "Cumple Nomenclatura BEP (y Razón Exacta)": diag,
            "Esquema IFC": esquema,
            "Estado Esquema": "✅ IFC4 / IFC2x3" if ("IFC4" in str(esquema).upper() or "IFC2X3" in str(esquema).upper()) else "⚠️ Revisar",
            "Peso Extraído (MB)": peso,
            "Elementos Reales Auditados": len(grp)
        })
    st.dataframe(pd.DataFrame(res_naming), use_container_width=True)

# --- PESTAÑA 2: GEORREFERENCIACIÓN ---
print("[DIAG TAB 2] Inicio de la pestaña 2", flush=True)
with tab2:
    st.subheader("2. Auditoría de Georreferenciación (ETRS89 / IfcSite)")
    res_geo = []
    for arch, grp in df.groupby("Archivo_Origen"):
        epsg = grp["EPSG"].iloc[0] if "EPSG" in grp.columns else "No definido"
        lat = grp["Latitud_Site"].iloc[0] if "Latitud_Site" in grp.columns else "No definida"
        lon = grp["Longitud_Site"].iloc[0] if "Longitud_Site" in grp.columns else "No definida"
        elev = grp["Elevacion_Site"].iloc[0] if "Elevacion_Site" in grp.columns else 0.0
        ox = grp["Origen_X"].iloc[0] if "Origen_X" in grp.columns else 0.0
        oy = grp["Origen_Y"].iloc[0] if "Origen_Y" in grp.columns else 0.0
        oz = grp["Origen_Z"].iloc[0] if "Origen_Z" in grp.columns else 0.0
        res_geo.append({
            "Archivo IFC": arch,
            "CRS / EPSG": epsg,
            "Origen Site X": ox, "Origen Site Y": oy, "Origen Site Z": oz,
            "Elevación Ref (m)": elev,
            "Latitud (IfcSite)": lat, "Longitud (IfcSite)": lon
        })
    df_geo = pd.DataFrame(res_geo)
    st.dataframe(df_geo, use_container_width=True)
    if len(df_geo) > 1 and (df_geo["Origen Site X"].nunique() > 1 or df_geo["Origen Site Y"].nunique() > 1):
        st.warning("⚠️ Se detectan diferencias en las coordenadas de origen (IfcSite) entre los distintos modelos.")
    else:
        st.success("✅ Consistencia espacial verificada en el emplazamiento (IfcSite).")

# --- PESTAÑA 3: INTEGRIDAD IFC ---
print("[DIAG TAB 3] Inicio de la pestaña 3", flush=True)
with tab3:
    st.subheader("3. Integridad IFC y Clasificación de Entidades")
    conteo_clases = df.groupby(["Archivo_Origen", "Clase_IFC"]).size().reset_index(name="Cantidad")
    fig_clases = px.bar(conteo_clases, x="Clase_IFC", y="Cantidad", color="Archivo_Origen", barmode="group", title="Distribución de Clases IFC por Modelo")
    st.plotly_chart(fig_clases, use_container_width=True)
    
    proxys = df[df["Clase_IFC"] == "IfcBuildingElementProxy"]
    st.metric("Elementos Genéricos (IfcBuildingElementProxy)", len(proxys))
    if not proxys.empty:
        st.warning("Listado de elementos genéricos detectados (con su ID de Elemento):")
        st.dataframe(proxys[["Archivo_Origen", "ID_Elemento", "GlobalId", "Clase_IFC", "Nombre"]], use_container_width=True)

# --- PESTAÑA 4: CALIDAD DE FORMATO ---
print("[DIAG TAB 4] Inicio de la pestaña 4", flush=True)
with tab4:
    st.subheader("4. Calidad de Formato (Estricto APV vs BEP)")
    st.markdown("El comodín **`-`** está permitido por el BEP y no genera error. Se auditan unidades, estados, espacios en blanco y textos comodín inválidos.")
    
    errores_fmt = []
    uni_validas = ["ud", "m", "m2", "dm3", "m3", "kg", "tn", "pa"]
    est_validos = ["Existente", "Demolido", "Temporal", "Proyectado", "Construido"]
    placeholders_malos = {"n/a", "na", "null", "none", "tbd", "sin definir", "por definir", "--", "."}

    for col in params_auditar:
        s_col = df[col]
        validos = df[s_col.notna() & ~s_col.astype(str).str.strip().str.lower().isin(["", "nan", "none", "<na>"])]
        for idx, row in validos.iterrows():
            v = str(row[col])
            v_limpio = v.strip()
            if v_limpio == "-":
                continue
            mot = []
            if v != v_limpio:
                mot.append("Espacios en blanco al inicio o final")
            if v_limpio.lower() in placeholders_malos:
                mot.append("Comodín no permitido (debe usarse '-')")
            if "TIPO-MED" in col.upper() and v_limpio.lower() not in uni_validas:
                mot.append(f"Unidad no permitida ('{v_limpio}')")
            elif "ESTADO" in col.upper() and v_limpio.capitalize() not in est_validos:
                mot.append(f"Estado de obra no válido ('{v_limpio}')")
            if mot:
                errores_fmt.append({
                    "Archivo": row["Archivo_Origen"],
                    "ID_Elemento": row["ID_Elemento"],
                    "GlobalId": row["GlobalId"],
                    "Parámetro": col,
                    "Contenido Detectado": v,
                    "Infracción BEP": " + ".join(mot)
                })
    if errores_fmt:
        df_err_fmt = pd.DataFrame(errores_fmt)
        st.error(f"⚠️ Se detectaron {len(df_err_fmt)} errores de formato en contra del BEP.")
        st.dataframe(df_err_fmt, use_container_width=True)
    else:
        st.success("✅ Todos los parámetros rellenos cumplen con el formato del BEP.")

# --- PESTAÑA 5: AUDITORÍA DE VACÍOS ---
print("[DIAG TAB 5] Inicio de la pestaña 5", flush=True)
with tab5:
    st.subheader(f"5. Auditoría Exclusiva de los {len(params_auditar)} Parámetros Oficiales APV")
    st.markdown("Si un parámetro contiene **`-`**, se valida como **Comodín BEP en Verde (`🟢`)**. Si faltan elementos (`🔴`), **a la derecha tienes sus IDs exactos (`ID_Elemento` y `GlobalId`) para localizarlos em tu NWD**.")
    
    resumen_params = []
    total_el = len(df)
    for p in params_auditar:
        s_str = df[p].astype(str).str.strip()
        es_vac = df[p].isna() | s_str.str.lower().isin(["", "nan", "none", "<na>"])
        es_com = (s_str == "-")
        n_vac = int(es_vac.sum())
        n_com = int(es_com.sum())
        n_datos = total_el - n_vac - n_com
        pct_valido = round(((n_datos + n_com) / total_el) * 100, 1) if total_el > 0 else 0.0
        
        if n_vac == 0 and n_com > 0:
            estado_str = "🟢 Comodín BEP (-)"
            ids_faltantes = "-"
            guids_faltantes = "-"
        elif n_vac == 0:
            estado_str = "🟢 Completo (Dato)"
            ids_faltantes = "-"
            guids_faltantes = "-"
        else:
            estado_str = f"🔴 Faltan {n_vac} elementos"
            ids_faltantes = ", ".join(df.loc[es_vac, "ID_Elemento"].astype(str).tolist())
            guids_faltantes = ", ".join(df.loc[es_vac, "GlobalId"].astype(str).tolist())
            
        resumen_params.append({
            "Parámetro Oficial APV": p,
            "Estado Auditoría": estado_str,
            "Con Dato Real": n_datos,
            "Con Comodín (-) Válido": n_com,
            "Vacíos (Error)": n_vac,
            "% Cumplimiento (Dato + '-')": pct_valido,
            "ID_Elemento Faltantes (Revit/C3D)": ids_faltantes,
            "GlobalId Faltantes (NWD/IFC)": guids_faltantes
        })
    df_res_vacios = pd.DataFrame(resumen_params)
    
    def colorear_estado(val):
        if "🟢" in str(val):
            return "background-color: #d4edda; color: #155724; font-weight: bold;"
        return "background-color: #f8d7da; color: #721c24; font-weight: bold;"

    st.dataframe(df_res_vacios.style.map(colorear_estado, subset=["Estado Auditoría"]), use_container_width=True)

    df_elem_incompletos = df[df["Tiene_Vacios"]]
    if not df_elem_incompletos.empty:
        st.markdown("#### 🔍 Detalle directo de los Elementos que tienen algún parámetro vacío:")
        st.dataframe(
            df_elem_incompletos[["Archivo_Origen", "ID_Elemento", "GlobalId", "Clase_IFC", "Nombre", "Cant_Vacios", "Parámetros_Vacíos"]],
            use_container_width=True
        )

# --- PESTAÑA 6: NAVISWORKS MANAGE ---
print("[DIAG TAB 6] Inicio de la pestaña 6", flush=True)
with tab6:
    st.subheader("6. Centro de Coordinación e Interferencias de Datos para Navisworks Manage")
    df_con_vacios = df[df["Tiene_Vacios"]]
    
    c1, c2 = st.columns(2)
    with c1:
        st.markdown("#### 📥 1. Descargar Search Sets XML para Navisworks (.NWD / .NWF)")
        param_filtro_nw = st.selectbox("Seleccionar grupo de elementos vacíos a aislar:", ["TODOS los elementos con algún vacío"] + params_auditar)
        if param_filtro_nw == "TODOS los elementos con algún vacío":
            df_target_nw = df_con_vacios
            nombre_xml = "APV_Todos_Los_Vacios"
        else:
            s_col_nw = df[param_filtro_nw].astype(str).str.strip()
            df_target_nw = df[df[param_filtro_nw].isna() | s_col_nw.str.lower().isin(["", "nan", "none", "<na>"])]
            nombre_xml = f"APV_Vacio_{param_filtro_nw}"
            
        usar_id_nativo = st.checkbox("Usar ID_Elemento nativo (Tag) en lugar de GlobalId para el XML", value=True)
        st.write(f"Elementos seleccionados para el XML: **{len(df_target_nw)}**")
        
        if not df_target_nw.empty:
            xml_str = generar_xml_navisworks(df_target_nw, nombre_set=nombre_xml, usar_id_nativo=usar_id_nativo)
            st.download_button(
                label=f"⬇️ Descargar XML ({len(df_target_nw)} elementos)",
                data=xml_str,
                file_name=f"{nombre_xml}.xml",
                mime="text/xml"
            )
        else:
            st.info("No hay elementos vacíos para este filtro seleccionado.")
            
    with c2:
        st.markdown("#### 🔍 2. Auditoría e Interferencias de Datos (IDs Duplicados y Huérfanos)")
        if not df.empty and "ID_Elemento" in df.columns:
            duplicados_id = df[df.duplicated(subset=["Archivo_Origen", "ID_Elemento"], keep=False)]
            n_dups = len(duplicados_id)
            if n_dups > 0:
                st.warning(f"⚠️ Se detectaron **{n_dups} elementos** con ID_Elemento duplicado dentro del mismo modelo:")
                st.dataframe(duplicados_id[["Archivo_Origen", "ID_Elemento", "GlobalId", "Clase_IFC", "Nombre"]], use_container_width=True)
            else:
                st.success("✅ No existen ID_Elemento duplicados en los modelos auditados.")
        else:
            st.info("Sin datos para analizar duplicados.")

# --- PESTAÑA 7: SALUD DEL PROYECTO ---
print("[DIAG TAB 7] Inicio de la pestaña 7", flush=True)
with tab7:
    st.subheader("7. Salud del Proyecto y Métricas Generales")
    c_s1, c_s2, c_s3 = st.columns(3)
    c_s1.metric("Modelos IFC Analizados", len(archivos_disp))
    c_s2.metric("Total Elementos Auditados", len(df_original))
    peso_total = df_original["Peso_Archivo_MB"].sum() if "Peso_Archivo_MB" in df_original.columns else 0.0
    c_s3.metric("Peso Consolidado de Modelos", f"{round(peso_total, 2)} MB")
    
    if "Peso_Archivo_MB" in df_original.columns:
        df_pesos = df_original[["Archivo_Origen", "Peso_Archivo_MB"]].drop_duplicates()
        fig_peso = px.bar(df_pesos, x="Archivo_Origen", y="Peso_Archivo_MB", title="Peso de Modelos IFC (MB)", text="Peso_Archivo_MB")
        st.plotly_chart(fig_peso, use_container_width=True)

# --- PESTAÑA 8: ALERTAS IFCS VACÍOS ---
print("[DIAG TAB 8] Inicio de la pestaña 8", flush=True)
with tab8:
    st.subheader("🚨 8. Alertas y Diagnóstico de IFCs Vacíos por Modelo")
    resumen_modelos_alt = []
    for arch in archivos_disp:
        df_m = df_original[df_original["Archivo_Origen"] == arch]
        tot = len(df_m)
        if tot == 0:
            est = "🚨 IFC Vacío"
        else:
            m_v_m = df_m[params_auditar].apply(lambda s: s.astype(str).str.strip().isin(["", "None", "nan", "<NA>"])).any(axis=1)
            n_v_m = m_v_m.sum()
            if n_v_m == tot:
                est = "🚨 100% Incompleto"
            elif n_v_m > 0:
                est = f"🔴 Parcial ({n_v_m} vacíos)"
            else:
                est = "🟢 100% Completo"
        resumen_modelos_alt.append({"Archivo IFC": arch, "Elementos": tot, "Estado General": est})
    st.dataframe(pd.DataFrame(resumen_modelos_alt), use_container_width=True)

# --- PESTAÑA 9: GRUPOS DE PARÁMETROS ---
print("[DIAG TAB 9] Inicio de la pestaña 9", flush=True)
with tab9:
    st.subheader("📐 Grupos de parámetros")
    st.markdown("Informe detallado por modelo sobre los bloques y grupos de parámetros detectados según la directriz del BEP (**Geotecnia = 11 grupos**; **Resto de modelos = 9 grupos**).")
    
    if "Archivo_Origen" in df_original.columns:
        info_grupos = []
        cols_todas_apv = [c for c in df_original.columns if "APV" in c]
        
        for arch in df_original["Archivo_Origen"].unique():
            df_m = df_original[df_original["Archivo_Origen"] == arch]
            nombre_inf = arch.lower()
            
            # Criterio BEP estricto: Geotecnia = 11 grupos, Resto = 9 grupos
            if "geo" in nombre_inf:
                tipo_modelo = "Modelo de Geotecnia"
                grupos_teoricos = 11
            else:
                tipo_modelo = "Modelo Estándar / Proyecto"
                grupos_teoricos = 9
                
            # Identificar prefijos de grupos con datos o comodines presentes
            grupos_hallados = set()
            for c in cols_todas_apv:
                prefijo = c.split("_")[0] if "_" in c else ""
                s_col_m = df_m[c].astype(str).str.strip().str.lower()
                tiene_contenido = (~s_col_m.isin(["", "none", "nan", "<na>"])).any()
                if tiene_contenido:
                    grupos_hallados.add(prefijo)
                    
            total_hallados = len(grupos_hallados)
            listado_grupos_str = ", ".join(sorted(list(grupos_hallados))) if grupos_hallados else "Ninguno"
            
            info_grupos.append({
                "Archivo IFC": arch,
                "Tipo de Modelo": tipo_modelo,
                "Grupos Teóricos (BEP)": grupos_teoricos,
                "Grupos Totales Detectados": total_hallados,
                "Grupos Específicos Detectados": listado_grupos_str
            })
            
        df_informe_grupos = pd.DataFrame(info_grupos)
        st.dataframe(df_informe_grupos, use_container_width=True)
    else:
        st.info("No hay datos disponibles para generar el informe de grupos.")