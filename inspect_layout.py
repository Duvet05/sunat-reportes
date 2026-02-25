"""
Inspecciona la estructura del Layout en el backup para ver el formato exacto.
"""
import zipfile, json

BACKUP = r"C:\Users\HP\Documents\sunat-powe.pbix.backup"

with zipfile.ZipFile(BACKUP, 'r') as z:
    raw = z.read('Report/Layout')

# detectar BOM
if raw[:2] == b'\xff\xfe':
    layout = json.loads(raw[2:].decode('utf-16-le'))
    print("Encoding: UTF-16-LE CON BOM")
else:
    layout = json.loads(raw.decode('utf-16-le'))
    print("Encoding: UTF-16-LE sin BOM")

print(f"\nTotal secciones: {len(layout['sections'])}")

for sec in layout['sections']:
    print(f"\n=== Sección: '{sec['displayName']}' (id={sec['id']}) ===")
    print(f"  ordinal={sec.get('ordinal')}, displayOption={sec.get('displayOption')}")
    print(f"  width={sec.get('width')}, height={sec.get('height')}")
    vcs = sec.get('visualContainers', [])
    print(f"  visualContainers: {len(vcs)}")
    for i, vc in enumerate(vcs[:3]):  # primeros 3
        print(f"\n  --- VisualContainer {i} ---")
        print(f"  id={vc.get('id')}")
        # config
        try:
            cfg = json.loads(vc.get('config', '{}'))
            print(f"  config.layouts: {cfg.get('layouts')}")
        except:
            print(f"  config (raw): {vc.get('config', '')[:100]}")
        # visual
        try:
            vis = json.loads(vc.get('visual', '{}'))
            print(f"  visual.visualType: {vis.get('visualType')}")
            print(f"  visual.projections: {vis.get('projections')}")
            pq = vis.get('prototypeQuery', {})
            print(f"  visual.prototypeQuery.From: {pq.get('From')}")
            print(f"  visual.prototypeQuery.Select: {pq.get('Select')}")
        except Exception as e:
            print(f"  visual (error): {e}")
        # query
        q = vc.get('query', '{}')
        print(f"  query (primeros 200 chars): {q[:200]}")
        print(f"  dataTransforms: {vc.get('dataTransforms', '')[:50]}")
        print(f"  filters: {vc.get('filters', '')[:50]}")

print("\n=== Config raíz (primeros 300 chars) ===")
print(layout.get('config', '')[:300])
