import {
  validarRUC,
  formatearPeriodo,
  formatearFecha,
  redondear,
  calcularIGV,
  calcularValorVentaDesdeTotal,
  validarSerie,
  formatearNumeroComprobante,
} from "../utils";

describe("validarRUC", () => {
  it("debería aceptar un RUC válido de persona jurídica (20)", () => {
    // RUC válido conocido: 20100047218 (SUNAT)
    expect(validarRUC("20100047218")).toBe(true);
  });

  it("debería aceptar un RUC válido de persona natural (10)", () => {
    expect(validarRUC("10467793549")).toBe(true);
  });

  it("debería rechazar RUC con menos de 11 dígitos", () => {
    expect(validarRUC("2010004721")).toBe(false);
  });

  it("debería rechazar RUC con más de 11 dígitos", () => {
    expect(validarRUC("201000472189")).toBe(false);
  });

  it("debería rechazar RUC con letras", () => {
    expect(validarRUC("2010004721A")).toBe(false);
  });

  it("debería rechazar RUC con prefijo inválido (30)", () => {
    expect(validarRUC("30100047218")).toBe(false);
  });

  it("debería rechazar RUC con dígito verificador incorrecto", () => {
    expect(validarRUC("20100047219")).toBe(false);
  });
});

describe("formatearPeriodo", () => {
  it("debería formatear un período correctamente", () => {
    expect(formatearPeriodo(2024, 1)).toBe("202401");
    expect(formatearPeriodo(2024, 12)).toBe("202412");
    expect(formatearPeriodo(2024, 6)).toBe("202406");
  });

  it("debería lanzar error con mes inválido", () => {
    expect(() => formatearPeriodo(2024, 0)).toThrow("Mes inválido");
    expect(() => formatearPeriodo(2024, 13)).toThrow("Mes inválido");
  });

  it("debería lanzar error con año inválido", () => {
    expect(() => formatearPeriodo(1900, 1)).toThrow("Año inválido");
    expect(() => formatearPeriodo(2200, 1)).toThrow("Año inválido");
  });
});

describe("formatearFecha", () => {
  it("debería formatear fecha en formato DD/MM/AAAA", () => {
    const fecha = new Date(2024, 0, 5); // 5 de enero 2024
    expect(formatearFecha(fecha)).toBe("05/01/2024");
  });

  it("debería formatear fecha con día y mes de dos dígitos", () => {
    const fecha = new Date(2024, 11, 31); // 31 de diciembre 2024
    expect(formatearFecha(fecha)).toBe("31/12/2024");
  });
});

describe("redondear", () => {
  it("debería redondear a 2 decimales", () => {
    expect(redondear(1.235)).toBe(1.24);
    expect(redondear(1.234)).toBe(1.23);
    expect(redondear(100)).toBe(100);
  });
});

describe("calcularIGV", () => {
  it("debería calcular el IGV al 18%", () => {
    expect(calcularIGV(100)).toBe(18);
    expect(calcularIGV(50)).toBe(9);
    expect(calcularIGV(200.5)).toBe(36.09);
  });
});

describe("calcularValorVentaDesdeTotal", () => {
  it("debería calcular el valor de venta neto desde el precio con IGV", () => {
    expect(calcularValorVentaDesdeTotal(118)).toBe(100);
    expect(calcularValorVentaDesdeTotal(59)).toBe(50);
  });
});

describe("validarSerie", () => {
  it("debería validar series de factura (F)", () => {
    expect(validarSerie("F001", "F")).toBe(true);
    expect(validarSerie("F999", "F")).toBe(true);
    expect(validarSerie("B001", "F")).toBe(false);
    expect(validarSerie("F01", "F")).toBe(false);
  });

  it("debería validar series de boleta (B)", () => {
    expect(validarSerie("B001", "B")).toBe(true);
    expect(validarSerie("F001", "B")).toBe(false);
  });
});

describe("formatearNumeroComprobante", () => {
  it("debería formatear el número con padding de ceros", () => {
    expect(formatearNumeroComprobante("F001", "1")).toBe("F001-00000001");
    expect(formatearNumeroComprobante("B001", "12345678")).toBe(
      "B001-12345678"
    );
  });
});
