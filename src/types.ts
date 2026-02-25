/**
 * Tipos de documentos tributarios SUNAT
 */
export enum TipoDocumento {
  FACTURA = "01",
  BOLETA = "03",
  NOTA_CREDITO = "07",
  NOTA_DEBITO = "08",
  LIQUIDACION_COMPRA = "04",
  RECIBO_HONORARIOS = "02",
}

/**
 * Tipos de IGV aplicados
 */
export enum TipoIGV {
  GRAVADO_ONEROSA = "10",
  GRAVADO_GRATUITA = "11",
  EXONERADO = "20",
  INAFECTO = "30",
  EXPORTACION = "40",
}

/**
 * Estructura de una línea de detalle de comprobante
 */
export interface LineaDetalle {
  descripcion: string;
  cantidad: number;
  precioUnitario: number;
  valorVenta: number;
  tipoIGV: TipoIGV;
  igv: number;
  precioVenta: number;
}

/**
 * Estructura base de un comprobante tributario
 */
export interface Comprobante {
  rucEmisor: string;
  razonSocialEmisor: string;
  tipoDocumento: TipoDocumento;
  serie: string;
  numero: string;
  fechaEmision: Date;
  rucAdquiriente?: string;
  razonSocialAdquiriente?: string;
  moneda: string;
  totalGravado: number;
  totalExonerado: number;
  totalInafecto: number;
  totalExportacion: number;
  totalIGV: number;
  totalImporte: number;
  lineas: LineaDetalle[];
}

/**
 * Filtros para generar reportes
 */
export interface FiltroReporte {
  ruc?: string;
  periodo: {
    anio: number;
    mes: number;
  };
  tipoDocumento?: TipoDocumento[];
}

/**
 * Resumen de un comprobante para reportes
 */
export interface ResumenComprobante {
  tipoDocumento: TipoDocumento;
  serie: string;
  numero: string;
  fechaEmision: string;
  rucAdquiriente: string;
  razonSocialAdquiriente: string;
  moneda: string;
  totalGravado: number;
  totalExonerado: number;
  totalInafecto: number;
  totalExportacion: number;
  totalIGV: number;
  totalImporte: number;
}

/**
 * Resultado del reporte de ventas/compras
 */
export interface ReporteResult {
  periodo: string;
  rucEmisor: string;
  razonSocialEmisor: string;
  comprobantes: ResumenComprobante[];
  totales: {
    gravado: number;
    exonerado: number;
    inafecto: number;
    exportacion: number;
    igv: number;
    importe: number;
  };
}
