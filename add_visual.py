"""
Agrega página 'Dashboard GAFA' con 4 tarjetas KPI al .pbix.
EJECUTAR CON POWER BI DESKTOP CERRADO.
"""
import zipfile, json, os, uuid

PBIX_PATH = r"C:\Users\HP\Documents\sunat-powe.pbix"
BACKUP    = r"C:\Users\HP\Documents\sunat-powe.pbix.backup"

# --- Leer todo el ZIP preservando metadata original ---
entries = {}   # filename -> (ZipInfo, bytes)
with zipfile.ZipFile(BACKUP, 'r') as z:
    for info in z.infolist():
        entries[info.filename] = (info, z.read(info.filename))

# --- Decodificar Layout (UTF-16-LE sin BOM) ---
orig_info, raw = entries['Report/Layout']
layout = json.loads(raw.decode('utf-16-le'))

print("Páginas existentes:", [s['displayName'] for s in layout['sections']])

# --- Construir 4 tarjetas con estructura correcta ---
def make_card_vc(card, idx):
    # CORRECTO: medidas usan "Tabla.Medida", sin Sum() (Sum es para columnas)
    qref  = f"SIGERI_Expedientes.{card['measure']}"
    v_cfg = json.dumps({
        "name": uuid.uuid4().hex,
        "layouts": [{"id": 0, "position": {
            "x": card["x"], "y": 30,
            "width": 250, "height": 130,
            "z": 0, "tabOrder": idx * 1000
        }}],
        "singleVisualGroup": False,
        "display": {}
    }, separators=(',', ':'))

    # Estructura mínima — sin active, sin hasDefaultSort, sin vcObjects
    v_visual = json.dumps({
        "visualType": "card",
        "projections": {"Values": [{"queryRef": qref}]},
        "prototypeQuery": {
            "Version": 2,
            "From": [{"Name": "s", "Entity": "SIGERI_Expedientes", "Type": 0}],
            "Select": [{
                "Measure": {
                    "Expression": {"SourceRef": {"Source": "s"}},
                    "Property": card["measure"]
                },
                "Name": qref
            }]
        },
        "drillFilterOtherVisuals": True
    }, separators=(',', ':'))

    # query: formato completo SemanticQueryDataShapeCommand que PBI necesita para renderizar
    v_query = json.dumps({
        "Commands": [{
            "SemanticQueryDataShapeCommand": {
                "Query": {
                    "Version": 2,
                    "From": [{"Name": "s", "Entity": "SIGERI_Expedientes", "Type": 0}],
                    "Select": [{
                        "Measure": {
                            "Expression": {"SourceRef": {"Source": "s"}},
                            "Property": card["measure"]
                        },
                        "Name": qref
                    }]
                },
                "Binding": {
                    "Primary": {"Groupings": [{"Projections": [0]}]},
                    "DataReduction": {"DataVolume": 3, "Primary": {"Top": {}}},
                    "Version": 1
                },
                "ExecutionMetricsKind": 1
            }
        }]
    }, separators=(',', ':'))

    # dataTransforms: mapeo de resultados de query a roles del visual
    v_transforms = json.dumps({
        "roles": {"Values": [{"queryRef": qref}]},
        "selects": [{
            "restatement": card["measure"],
            "kind": 2,
            "queryRef": qref,
            "roles": ["Values"],
            "field": {
                "Measure": {
                    "Expression": {"SourceRef": {"Source": "s"}},
                    "Property": card["measure"]
                }
            }
        }]
    }, separators=(',', ':'))

    return {
        "id": 3000 + idx,
        "config":         v_cfg,
        "filters":        "[]",
        "query":          v_query,
        "dataTransforms": v_transforms,
        "visual":         v_visual
    }

cards = [
    {"displayName": "Total Expedientes",  "measure": "Total Expedientes",      "x": 20,  "color": "#0078D4"},
    {"displayName": "Pendientes",         "measure": "Expedientes Pendientes", "x": 290, "color": "#D83B01"},
    {"displayName": "Resueltos",          "measure": "Expedientes Resueltos",  "x": 560, "color": "#107C10"},
    {"displayName": "Alerta OEA",         "measure": "Con Alerta OEA",         "x": 830, "color": "#FFB900"},
]

# --- Nueva sección con estructura idéntica a "Page 1" ---
# ID único: si usamos 1 y Page1 ya tiene id=1, PBI no carga el reporte
max_id = max(s['id'] for s in layout['sections'])
print(f"IDs existentes: {[s['id'] for s in layout['sections']]} -> nuevo: {max_id + 1}")
new_section = {
    "id":               max_id + 1,
    "name":             uuid.uuid4().hex[:20],   # 20 chars hex como el original
    "displayName":      "Dashboard GAFA",
    "filters":          "[]",
    "ordinal":          len(layout["sections"]),
    "visualContainers": [make_card_vc(c, i) for i, c in enumerate(cards)],
    "config":           "{}",                    # igual que Page 1
    "displayOption":    1,                        # campo que faltaba
    "width":            1280,                     # campo que faltaba
    "height":           720                       # campo que faltaba
}

layout["sections"].append(new_section)

# Actualizar activeSectionIndex para abrir en nuestra página
root_cfg = json.loads(layout["config"])
root_cfg["activeSectionIndex"] = len(layout["sections"]) - 1
layout["config"] = json.dumps(root_cfg, separators=(',', ':'))

print(f"Página añadida. Total páginas: {len(layout['sections'])}")

# --- Validar JSON antes de escribir ---
new_json = json.dumps(layout, ensure_ascii=False, separators=(',', ':'))
json.loads(new_json)  # si falla aquí, el JSON está roto — no se toca el archivo
print("JSON validado OK")

# --- Codificar Layout de vuelta a UTF-16-LE sin BOM ---
new_raw = new_json.encode('utf-16-le')

# --- Reempaquetar preservando ZipInfo original de cada archivo ---
tmp = PBIX_PATH + ".tmp"
with zipfile.ZipFile(tmp, 'w') as zout:
    for fname, (info, data) in entries.items():
        if fname == 'Report/Layout':
            # Crear nuevo ZipInfo copiando los campos del original
            ni = zipfile.ZipInfo(fname, date_time=info.date_time)
            ni.compress_type   = info.compress_type
            ni.flag_bits       = info.flag_bits
            ni.internal_attr   = info.internal_attr
            ni.external_attr   = info.external_attr
            zout.writestr(ni, new_raw)
        elif fname == 'SecurityBindings':
            # CRÍTICO: al modificar Layout el DPAPI se invalida → archivo no carga
            # Solución: escribir SecurityBindings vacío
            ni = zipfile.ZipInfo(fname, date_time=info.date_time)
            ni.compress_type   = info.compress_type
            ni.flag_bits       = info.flag_bits
            ni.internal_attr   = info.internal_attr
            ni.external_attr   = info.external_attr
            print(f"SecurityBindings: {len(data)} bytes -> limpiando (necesario)")
            zout.writestr(ni, b'')
        else:
            ni = zipfile.ZipInfo(fname, date_time=info.date_time)
            ni.compress_type   = info.compress_type
            ni.flag_bits       = info.flag_bits
            ni.internal_attr   = info.internal_attr
            ni.external_attr   = info.external_attr
            zout.writestr(ni, data)

os.replace(tmp, PBIX_PATH)
print(f"Listo: {PBIX_PATH}")
