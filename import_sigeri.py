"""
Script para importar SIGERI directamente al modelo de Power BI Desktop via XMLA/TMSL
"""
import os, json

os.environ['DOTNET_ROOT'] = r'C:\Program Files\dotnet'

import pythonnet
pythonnet.load('coreclr', dotnet_root=r'C:\Program Files\dotnet')
import clr

from System.Reflection import Assembly
from System.IO import Path

# Cargar dependencias de PBI
pbi_bin = r'C:\Program Files\Microsoft Power BI Desktop\bin'
for dep in ['Microsoft.Identity.Client', 'Microsoft.Identity.Client.Broker', 'Microsoft.IdentityModel.Abstractions']:
    Assembly.LoadFile(Path.Combine(pbi_bin, dep + '.dll'))
Assembly.LoadFile(Path.Combine(pbi_bin, 'Microsoft.PowerBI.AdomdClient.dll'))

from Microsoft.AnalysisServices.AdomdClient import AdomdConnection, AdomdCommand

CONN_STR = 'Data Source=localhost:59964;Initial Catalog=a6920105-2054-4385-8c6f-cb9fb18bca1a'
EXCEL_PATH = r'C:\Users\HP\Desktop\sunat-reportes\SIGERI 19 ENE 26.xlsx'

M_EXPRESSION = r"""let
    Source = Excel.Workbook(File.Contents("{excel}"), null, true),
    ConsolidadoSheet = Source{{[Item="Consolidado",Kind="Sheet"]}}[Data],
    PromotedHeaders = Table.PromoteHeaders(ConsolidadoSheet, [PromoteAllScalars=true]),
    RenamedColumns = Table.RenameColumns(PromotedHeaders, {{
        {{Table.ColumnNames(PromotedHeaders){{0}}, "Dependencia"}},
        {{Table.ColumnNames(PromotedHeaders){{1}}, "Indicador_Dependencia"}},
        {{Table.ColumnNames(PromotedHeaders){{2}}, "Tipo_Doc_ID"}},
        {{Table.ColumnNames(PromotedHeaders){{3}}, "Numero_Documento"}},
        {{Table.ColumnNames(PromotedHeaders){{4}}, "Razon_Social"}},
        {{Table.ColumnNames(PromotedHeaders){{5}}, "Fecha_Ingreso"}},
        {{Table.ColumnNames(PromotedHeaders){{6}}, "Tamano_Contribuyente"}},
        {{Table.ColumnNames(PromotedHeaders){{7}}, "Tipo_Recurso"}},
        {{Table.ColumnNames(PromotedHeaders){{8}}, "Numero_Expediente"}},
        {{Table.ColumnNames(PromotedHeaders){{9}}, "Etapa_Recurso"}},
        {{Table.ColumnNames(PromotedHeaders){{10}}, "Tipo_Documento"}},
        {{Table.ColumnNames(PromotedHeaders){{11}}, "Numero_Valor_Documento"}},
        {{Table.ColumnNames(PromotedHeaders){{12}}, "Area_Emisora"}},
        {{Table.ColumnNames(PromotedHeaders){{13}}, "Fecha_Emision_Valor"}},
        {{Table.ColumnNames(PromotedHeaders){{14}}, "Nombre_Resolutor"}},
        {{Table.ColumnNames(PromotedHeaders){{15}}, "Nombre_Revisor"}},
        {{Table.ColumnNames(PromotedHeaders){{16}}, "Fecha_Primera_Asignacion"}},
        {{Table.ColumnNames(PromotedHeaders){{17}}, "Fecha_Ultima_Asignacion"}},
        {{Table.ColumnNames(PromotedHeaders){{18}}, "Monto_Impugnado"}},
        {{Table.ColumnNames(PromotedHeaders){{19}}, "Descriptor_Principal"}},
        {{Table.ColumnNames(PromotedHeaders){{20}}, "Descriptor_Secundario"}},
        {{Table.ColumnNames(PromotedHeaders){{21}}, "Resultado_Resolucion"}},
        {{Table.ColumnNames(PromotedHeaders){{22}}, "Numero_Resolucion"}},
        {{Table.ColumnNames(PromotedHeaders){{23}}, "Fecha_Emision_Resolucion"}},
        {{Table.ColumnNames(PromotedHeaders){{24}}, "Fecha_Notificacion"}},
        {{Table.ColumnNames(PromotedHeaders){{25}}, "Incidencia"}},
        {{Table.ColumnNames(PromotedHeaders){{26}}, "OEA"}},
        {{Table.ColumnNames(PromotedHeaders){{27}}, "Dias"}},
        {{Table.ColumnNames(PromotedHeaders){{28}}, "Vcto"}},
        {{Table.ColumnNames(PromotedHeaders){{29}}, "Alerta"}},
        {{Table.ColumnNames(PromotedHeaders){{30}}, "Fecha_RTF"}}
    }}),
    FilteredRows = Table.SelectRows(RenamedColumns, each [Numero_Expediente] <> null and [Numero_Expediente] <> "-"),
    TypedColumns = Table.TransformColumnTypes(FilteredRows, {{
        {{"Fecha_Ingreso", type date}},
        {{"Numero_Expediente", type text}},
        {{"Numero_Documento", type text}},
        {{"Dependencia", type text}},
        {{"Indicador_Dependencia", type text}},
        {{"Razon_Social", type text}},
        {{"Tamano_Contribuyente", type text}},
        {{"Tipo_Recurso", type text}},
        {{"Etapa_Recurso", type text}},
        {{"Resultado_Resolucion", type text}},
        {{"Nombre_Resolutor", type text}},
        {{"Nombre_Revisor", type text}},
        {{"Alerta", type text}},
        {{"OEA", type text}}
    }})
in
    TypedColumns""".format(excel=EXCEL_PATH.replace('\\', '\\\\'))

# Script TMSL para crear la tabla con partición M
TMSL = json.dumps({
    "createOrReplace": {
        "object": {
            "database": "a6920105-2054-4385-8c6f-cb9fb18bca1a",
            "table": "SIGERI_Expedientes"
        },
        "table": {
            "name": "SIGERI_Expedientes",
            "description": "Expedientes del sistema SIGERI - GAFA SUNAT (corte 19 Ene 2026)",
            "columns": [
                {"name": "Dependencia", "dataType": "string", "sourceColumn": "Dependencia"},
                {"name": "Indicador_Dependencia", "dataType": "string", "sourceColumn": "Indicador_Dependencia"},
                {"name": "Tipo_Doc_ID", "dataType": "string", "sourceColumn": "Tipo_Doc_ID"},
                {"name": "Numero_Documento", "dataType": "string", "sourceColumn": "Numero_Documento"},
                {"name": "Razon_Social", "dataType": "string", "sourceColumn": "Razon_Social"},
                {"name": "Fecha_Ingreso", "dataType": "dateTime", "sourceColumn": "Fecha_Ingreso", "formatString": "dd/mm/yyyy"},
                {"name": "Tamano_Contribuyente", "dataType": "string", "sourceColumn": "Tamano_Contribuyente"},
                {"name": "Tipo_Recurso", "dataType": "string", "sourceColumn": "Tipo_Recurso"},
                {"name": "Numero_Expediente", "dataType": "string", "sourceColumn": "Numero_Expediente"},
                {"name": "Etapa_Recurso", "dataType": "string", "sourceColumn": "Etapa_Recurso"},
                {"name": "Tipo_Documento", "dataType": "string", "sourceColumn": "Tipo_Documento"},
                {"name": "Numero_Valor_Documento", "dataType": "string", "sourceColumn": "Numero_Valor_Documento"},
                {"name": "Area_Emisora", "dataType": "string", "sourceColumn": "Area_Emisora"},
                {"name": "Fecha_Emision_Valor", "dataType": "string", "sourceColumn": "Fecha_Emision_Valor"},
                {"name": "Nombre_Resolutor", "dataType": "string", "sourceColumn": "Nombre_Resolutor"},
                {"name": "Nombre_Revisor", "dataType": "string", "sourceColumn": "Nombre_Revisor"},
                {"name": "Fecha_Primera_Asignacion", "dataType": "string", "sourceColumn": "Fecha_Primera_Asignacion"},
                {"name": "Fecha_Ultima_Asignacion", "dataType": "string", "sourceColumn": "Fecha_Ultima_Asignacion"},
                {"name": "Monto_Impugnado", "dataType": "string", "sourceColumn": "Monto_Impugnado"},
                {"name": "Descriptor_Principal", "dataType": "string", "sourceColumn": "Descriptor_Principal"},
                {"name": "Descriptor_Secundario", "dataType": "string", "sourceColumn": "Descriptor_Secundario"},
                {"name": "Resultado_Resolucion", "dataType": "string", "sourceColumn": "Resultado_Resolucion"},
                {"name": "Numero_Resolucion", "dataType": "string", "sourceColumn": "Numero_Resolucion"},
                {"name": "Fecha_Emision_Resolucion", "dataType": "string", "sourceColumn": "Fecha_Emision_Resolucion"},
                {"name": "Fecha_Notificacion", "dataType": "string", "sourceColumn": "Fecha_Notificacion"},
                {"name": "Incidencia", "dataType": "string", "sourceColumn": "Incidencia"},
                {"name": "OEA", "dataType": "string", "sourceColumn": "OEA"},
                {"name": "Dias", "dataType": "string", "sourceColumn": "Dias"},
                {"name": "Vcto", "dataType": "string", "sourceColumn": "Vcto"},
                {"name": "Alerta", "dataType": "string", "sourceColumn": "Alerta"},
                {"name": "Fecha_RTF", "dataType": "string", "sourceColumn": "Fecha_RTF"}
            ],
            "partitions": [
                {
                    "name": "SIGERI_Expedientes",
                    "mode": "import",
                    "source": {
                        "type": "m",
                        "expression": M_EXPRESSION
                    }
                }
            ]
        }
    }
})

print("Conectando a Power BI Desktop...")
conn = AdomdConnection(CONN_STR)
conn.Open()
print("Conexion abierta.")

print("Creando tabla SIGERI_Expedientes...")
cmd = AdomdCommand()
cmd.Connection = conn
cmd.CommandText = TMSL
cmd.ExecuteNonQuery()
print("Tabla creada.")

print("Procesando (cargando datos del Excel - puede tardar 1-2 min)...")
process_tmsl = json.dumps({
    "refresh": {
        "type": "full",
        "objects": [{"database": "a6920105-2054-4385-8c6f-cb9fb18bca1a", "table": "SIGERI_Expedientes"}]
    }
})
cmd.CommandText = process_tmsl
cmd.ExecuteNonQuery()
print("LISTO! Tabla cargada con datos del SIGERI.")

conn.Close()
