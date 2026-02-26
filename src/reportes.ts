import {
  Comprobante,
  FiltroReporte,
  ResumenComprobante,
  ReporteResult,
  TipoDocumento,
} from "./types";
import { formatearFecha, formatearPeriodo, redondear } from "./utils";

/**
 * Genera el reporte de ventas (Registro de Ventas e Ingresos)
 * basado en los comprobantes emitidos en el período indicado.
 */
export function generarReporteVentas(
  comprobantes: Comprobante[],
  filtro: FiltroReporte
): ReporteResult {
  const tiposVentas = [
    TipoDocumento.FACTURA,
    TipoDocumento.BOLETA,
    TipoDocumento.NOTA_CREDITO,
    TipoDocumento.NOTA_DEBITO,
  ];

  return generarReporte(comprobantes, filtro, tiposVentas);
}

/**
 * Genera el reporte de compras (Registro de Compras)
 * basado en los comprobantes recibidos en el período indicado.
 */
export function generarReporteCompras(
  comprobantes: Comprobante[],
  filtro: FiltroReporte
): ReporteResult {
  const tiposCompras = [
    TipoDocumento.FACTURA,
    TipoDocumento.LIQUIDACION_COMPRA,
    TipoDocumento.RECIBO_HONORARIOS,
    TipoDocumento.NOTA_CREDITO,
    TipoDocumento.NOTA_DEBITO,
  ];

  return generarReporte(comprobantes, filtro, tiposCompras);
}

/**
 * Función interna que filtra y agrupa comprobantes para un reporte
 */
function generarReporte(
  comprobantes: Comprobante[],
  filtro: FiltroReporte,
  tiposPermitidos: TipoDocumento[]
): ReporteResult {
  const periodo = formatearPeriodo(filtro.periodo.anio, filtro.periodo.mes);
  const tiposEfectivos = filtro.tipoDocumento ?? tiposPermitidos;

  const comprobantesFiltrados = comprobantes.filter((c) => {
    const anioDoc = c.fechaEmision.getFullYear();
    const mesDoc = c.fechaEmision.getMonth() + 1;
    const enPeriodo =
      anioDoc === filtro.periodo.anio && mesDoc === filtro.periodo.mes;
    const tipoValido = tiposEfectivos.includes(c.tipoDocumento);
    const rucValido = filtro.ruc ? c.rucEmisor === filtro.ruc : true;
    return enPeriodo && tipoValido && rucValido;
  });

  const resumen: ResumenComprobante[] = comprobantesFiltrados.map((c) => ({
    tipoDocumento: c.tipoDocumento,
    serie: c.serie,
    numero: c.numero,
    fechaEmision: formatearFecha(c.fechaEmision),
    rucAdquiriente: c.rucAdquiriente ?? "",
    razonSocialAdquiriente: c.razonSocialAdquiriente ?? "",
    moneda: c.moneda,
    totalGravado: c.totalGravado,
    totalExonerado: c.totalExonerado,
    totalInafecto: c.totalInafecto,
    totalExportacion: c.totalExportacion,
    totalIGV: c.totalIGV,
    totalImporte: c.totalImporte,
  }));

  const totales = resumen.reduce(
    (acc, c) => ({
      gravado: redondear(acc.gravado + c.totalGravado),
      exonerado: redondear(acc.exonerado + c.totalExonerado),
      inafecto: redondear(acc.inafecto + c.totalInafecto),
      exportacion: redondear(acc.exportacion + c.totalExportacion),
      igv: redondear(acc.igv + c.totalIGV),
      importe: redondear(acc.importe + c.totalImporte),
    }),
    {
      gravado: 0,
      exonerado: 0,
      inafecto: 0,
      exportacion: 0,
      igv: 0,
      importe: 0,
    }
  );

  const primerComprobante = comprobantesFiltrados[0];

  return {
    periodo,
    rucEmisor: filtro.ruc ?? primerComprobante?.rucEmisor ?? "",
    razonSocialEmisor: primerComprobante?.razonSocialEmisor ?? "",
    comprobantes: resumen,
    totales,
  };
}
