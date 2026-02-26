import { generarReporteVentas, generarReporteCompras } from "../reportes";
import { Comprobante, TipoDocumento, TipoIGV } from "../types";

const comprobantesEjemplo: Comprobante[] = [
  {
    rucEmisor: "20100047218",
    razonSocialEmisor: "EMPRESA EJEMPLO SAC",
    tipoDocumento: TipoDocumento.FACTURA,
    serie: "F001",
    numero: "00000001",
    fechaEmision: new Date(2024, 0, 10), // enero 2024
    rucAdquiriente: "20512345678",
    razonSocialAdquiriente: "CLIENTE SAC",
    moneda: "PEN",
    totalGravado: 100,
    totalExonerado: 0,
    totalInafecto: 0,
    totalExportacion: 0,
    totalIGV: 18,
    totalImporte: 118,
    lineas: [
      {
        descripcion: "Producto A",
        cantidad: 2,
        precioUnitario: 59,
        valorVenta: 100,
        tipoIGV: TipoIGV.GRAVADO_ONEROSA,
        igv: 18,
        precioVenta: 118,
      },
    ],
  },
  {
    rucEmisor: "20100047218",
    razonSocialEmisor: "EMPRESA EJEMPLO SAC",
    tipoDocumento: TipoDocumento.BOLETA,
    serie: "B001",
    numero: "00000001",
    fechaEmision: new Date(2024, 0, 15), // enero 2024
    moneda: "PEN",
    totalGravado: 50,
    totalExonerado: 0,
    totalInafecto: 0,
    totalExportacion: 0,
    totalIGV: 9,
    totalImporte: 59,
    lineas: [
      {
        descripcion: "Producto B",
        cantidad: 1,
        precioUnitario: 59,
        valorVenta: 50,
        tipoIGV: TipoIGV.GRAVADO_ONEROSA,
        igv: 9,
        precioVenta: 59,
      },
    ],
  },
  {
    rucEmisor: "20100047218",
    razonSocialEmisor: "EMPRESA EJEMPLO SAC",
    tipoDocumento: TipoDocumento.FACTURA,
    serie: "F001",
    numero: "00000002",
    fechaEmision: new Date(2024, 1, 5), // febrero 2024 - fuera del período
    rucAdquiriente: "20512345678",
    razonSocialAdquiriente: "CLIENTE SAC",
    moneda: "PEN",
    totalGravado: 200,
    totalExonerado: 0,
    totalInafecto: 0,
    totalExportacion: 0,
    totalIGV: 36,
    totalImporte: 236,
    lineas: [],
  },
];

describe("generarReporteVentas", () => {
  it("debería filtrar comprobantes por período correctamente", () => {
    const resultado = generarReporteVentas(comprobantesEjemplo, {
      periodo: { anio: 2024, mes: 1 },
    });

    expect(resultado.periodo).toBe("202401");
    expect(resultado.comprobantes).toHaveLength(2);
  });

  it("debería excluir comprobantes fuera del período", () => {
    const resultado = generarReporteVentas(comprobantesEjemplo, {
      periodo: { anio: 2024, mes: 2 },
    });

    expect(resultado.comprobantes).toHaveLength(1);
    expect(resultado.comprobantes[0].serie).toBe("F001");
    expect(resultado.comprobantes[0].numero).toBe("00000002");
  });

  it("debería calcular totales correctamente", () => {
    const resultado = generarReporteVentas(comprobantesEjemplo, {
      periodo: { anio: 2024, mes: 1 },
    });

    expect(resultado.totales.gravado).toBe(150);
    expect(resultado.totales.igv).toBe(27);
    expect(resultado.totales.importe).toBe(177);
  });

  it("debería filtrar por RUC emisor cuando se especifica", () => {
    const resultado = generarReporteVentas(comprobantesEjemplo, {
      ruc: "20100047218",
      periodo: { anio: 2024, mes: 1 },
    });

    expect(resultado.rucEmisor).toBe("20100047218");
    expect(resultado.comprobantes).toHaveLength(2);
  });

  it("debería retornar lista vacía si no hay comprobantes en el período", () => {
    const resultado = generarReporteVentas(comprobantesEjemplo, {
      periodo: { anio: 2023, mes: 12 },
    });

    expect(resultado.comprobantes).toHaveLength(0);
    expect(resultado.totales.importe).toBe(0);
  });

  it("debería incluir la información del emisor correctamente", () => {
    const resultado = generarReporteVentas(comprobantesEjemplo, {
      periodo: { anio: 2024, mes: 1 },
    });

    expect(resultado.razonSocialEmisor).toBe("EMPRESA EJEMPLO SAC");
  });
});

describe("generarReporteCompras", () => {
  const comprasEjemplo: Comprobante[] = [
    {
      rucEmisor: "20555123456",
      razonSocialEmisor: "PROVEEDOR SAC",
      tipoDocumento: TipoDocumento.FACTURA,
      serie: "F001",
      numero: "00000100",
      fechaEmision: new Date(2024, 0, 20),
      rucAdquiriente: "20100047218",
      razonSocialAdquiriente: "EMPRESA EJEMPLO SAC",
      moneda: "PEN",
      totalGravado: 500,
      totalExonerado: 0,
      totalInafecto: 0,
      totalExportacion: 0,
      totalIGV: 90,
      totalImporte: 590,
      lineas: [],
    },
  ];

  it("debería generar reporte de compras con facturas recibidas", () => {
    const resultado = generarReporteCompras(comprasEjemplo, {
      periodo: { anio: 2024, mes: 1 },
    });

    expect(resultado.comprobantes).toHaveLength(1);
    expect(resultado.totales.gravado).toBe(500);
    expect(resultado.totales.igv).toBe(90);
    expect(resultado.totales.importe).toBe(590);
  });
});
