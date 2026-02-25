# sunat-reportes

Módulo Node.js/TypeScript para la generación de reportes tributarios SUNAT (Perú).

## Características

- Generación de **Reporte de Ventas** (Registro de Ventas e Ingresos)
- Generación de **Reporte de Compras** (Registro de Compras)
- Validación de RUC peruano (11 dígitos con dígito verificador)
- Formateo de períodos, fechas y números de comprobante según estándares SUNAT
- Cálculo de IGV (18%)
- Soporte de tipos de documentos: Facturas, Boletas, Notas de Crédito, Notas de Débito, Liquidaciones de Compra, Recibos por Honorarios

## Instalación

```bash
npm install sunat-reportes
```

## Uso

```typescript
import {
  generarReporteVentas,
  generarReporteCompras,
  validarRUC,
  TipoDocumento,
  TipoIGV,
  Comprobante,
} from "sunat-reportes";

// Validar un RUC
console.log(validarRUC("20100047218")); // true

// Crear un comprobante de ejemplo
const factura: Comprobante = {
  rucEmisor: "20100047218",
  razonSocialEmisor: "MI EMPRESA SAC",
  tipoDocumento: TipoDocumento.FACTURA,
  serie: "F001",
  numero: "00000001",
  fechaEmision: new Date(2024, 0, 15),
  rucAdquiriente: "20512345678",
  razonSocialAdquiriente: "CLIENTE SAC",
  moneda: "PEN",
  totalGravado: 1000,
  totalExonerado: 0,
  totalInafecto: 0,
  totalExportacion: 0,
  totalIGV: 180,
  totalImporte: 1180,
  lineas: [
    {
      descripcion: "Servicio de consultoría",
      cantidad: 1,
      precioUnitario: 1180,
      valorVenta: 1000,
      tipoIGV: TipoIGV.GRAVADO_ONEROSA,
      igv: 180,
      precioVenta: 1180,
    },
  ],
};

// Generar reporte de ventas para enero 2024
const reporte = generarReporteVentas([factura], {
  periodo: { anio: 2024, mes: 1 },
});

console.log(reporte);
// {
//   periodo: '202401',
//   rucEmisor: '20100047218',
//   razonSocialEmisor: 'MI EMPRESA SAC',
//   comprobantes: [...],
//   totales: { gravado: 1000, igv: 180, importe: 1180, ... }
// }
```

## API

### Funciones de Reporte

#### `generarReporteVentas(comprobantes, filtro)`

Genera el reporte de ventas filtrando por período y opcionalmente por RUC.

#### `generarReporteCompras(comprobantes, filtro)`

Genera el reporte de compras filtrando por período y opcionalmente por RUC.

### Utilidades

| Función | Descripción |
|---|---|
| `validarRUC(ruc)` | Valida un número de RUC peruano (11 dígitos) |
| `formatearPeriodo(anio, mes)` | Formatea como `AAAAMM` (ej. `202401`) |
| `formatearFecha(fecha)` | Formatea como `DD/MM/AAAA` |
| `calcularIGV(valorVenta)` | Calcula IGV al 18% |
| `calcularValorVentaDesdeTotal(precio)` | Obtiene valor neto desde precio con IGV |
| `validarSerie(serie, prefijo)` | Valida formato de serie (F001, B001, etc.) |
| `formatearNumeroComprobante(serie, numero)` | Formatea como `F001-00000001` |
| `redondear(valor)` | Redondea a 2 decimales |

## Tipos

- `TipoDocumento` – Enum con códigos SUNAT (01=Factura, 03=Boleta, etc.)
- `TipoIGV` – Enum con tipos de afectación IGV
- `Comprobante` – Estructura completa de un comprobante tributario
- `LineaDetalle` – Línea de detalle de un comprobante
- `FiltroReporte` – Filtros para generar reportes
- `ReporteResult` – Resultado de un reporte generado

## Desarrollo

```bash
npm install
npm run build    # Compila TypeScript
npm test         # Ejecuta las pruebas
```

## Licencia

ISC
