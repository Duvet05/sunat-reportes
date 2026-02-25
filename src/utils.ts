/**
 * Utilidades para validación y formateo de datos SUNAT
 */

/**
 * Valida un número de RUC peruano (11 dígitos con dígito verificador)
 */
export function validarRUC(ruc: string): boolean {
  if (!/^\d{11}$/.test(ruc)) {
    return false;
  }

  // El RUC debe comenzar con 10, 15, 17, 20 o 21
  const prefijo = parseInt(ruc.substring(0, 2), 10);
  const prefijosValidos = [10, 15, 17, 20, 21];
  if (!prefijosValidos.includes(prefijo)) {
    return false;
  }

  // Verificar dígito de control
  const factores = [5, 4, 3, 2, 7, 6, 5, 4, 3, 2];
  let suma = 0;
  for (let i = 0; i < factores.length; i++) {
    suma += parseInt(ruc[i], 10) * factores[i];
  }
  const residuo = suma % 11;
  const digitoControl = residuo === 0 ? 0 : residuo === 1 ? 1 : 11 - residuo;
  return digitoControl === parseInt(ruc[10], 10);
}

/**
 * Formatea un período SUNAT como AAAAMM
 */
export function formatearPeriodo(anio: number, mes: number): string {
  if (anio < 1990 || anio > 2100) {
    throw new Error(`Año inválido: ${anio}`);
  }
  if (mes < 1 || mes > 12) {
    throw new Error(`Mes inválido: ${mes}`);
  }
  return `${anio}${String(mes).padStart(2, "0")}`;
}

/**
 * Formatea una fecha como DD/MM/AAAA (formato SUNAT)
 */
export function formatearFecha(fecha: Date): string {
  const dia = String(fecha.getDate()).padStart(2, "0");
  const mes = String(fecha.getMonth() + 1).padStart(2, "0");
  const anio = fecha.getFullYear();
  return `${dia}/${mes}/${anio}`;
}

/**
 * Redondea un número a 2 decimales (como exige SUNAT)
 */
export function redondear(valor: number): number {
  return Math.round(valor * 100) / 100;
}

/**
 * Calcula el IGV a partir del valor de venta (18%)
 */
export function calcularIGV(valorVenta: number): number {
  return redondear(valorVenta * 0.18);
}

/**
 * Calcula el valor de venta dado el precio con IGV incluido
 */
export function calcularValorVentaDesdeTotal(precioConIGV: number): number {
  return redondear(precioConIGV / 1.18);
}

/**
 * Valida que una serie de comprobante tenga el formato correcto
 * Facturas/NC/ND: F + 3 dígitos (e.g. F001)
 * Boletas: B + 3 dígitos (e.g. B001)
 */
export function validarSerie(serie: string, prefijo: "F" | "B"): boolean {
  const patron = new RegExp(`^${prefijo}\\d{3}$`);
  return patron.test(serie);
}

/**
 * Genera el número completo del comprobante (serie-número)
 */
export function formatearNumeroComprobante(
  serie: string,
  numero: string
): string {
  const numPadded = numero.padStart(8, "0");
  return `${serie}-${numPadded}`;
}
