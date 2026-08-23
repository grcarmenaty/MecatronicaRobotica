// Estilo IQS compartido para documentos docx del curso 82514
const {
  Paragraph, TextRun, HeadingLevel, AlignmentType, Table, TableRow, TableCell,
  WidthType, ShadingType, BorderStyle,
} = require("docx");

const IQS = {
  navy: "1B2A80",   // azul marino IQS
  navy2: "2E3FA3",
  green: "2FD26E",  // verde IQS
  greenDark: "1FA355",
  grey: "595959",
  greyLight: "EDF0FA",
};

const F = "Calibri";

function p(text, opts = {}) {
  return new Paragraph({
    spacing: { after: 160, line: 276 },
    alignment: AlignmentType.JUSTIFIED,
    ...opts.para,
    children: [new TextRun({ text, size: 22, font: F, ...opts.run })],
  });
}

function pRuns(runs, para = {}) {
  return new Paragraph({
    spacing: { after: 160, line: 276 },
    alignment: AlignmentType.JUSTIFIED,
    ...para,
    children: runs.map(r => new TextRun({ size: 22, font: F, ...r })),
  });
}

function h1(text) {
  return new Paragraph({
    heading: HeadingLevel.HEADING_1,
    spacing: { before: 400, after: 200 },
    children: [new TextRun({ text, size: 30, bold: true, color: IQS.navy, font: F })],
  });
}

function h2(text) {
  return new Paragraph({
    heading: HeadingLevel.HEADING_2,
    spacing: { before: 300, after: 160 },
    children: [new TextRun({ text, size: 25, bold: true, color: IQS.navy2, font: F })],
  });
}

function h3(text) {
  return new Paragraph({
    heading: HeadingLevel.HEADING_3,
    spacing: { before: 240, after: 120 },
    children: [new TextRun({ text, size: 23, bold: true, color: IQS.greenDark, font: F })],
  });
}

function bullet(text, boldPrefix) {
  const runs = [];
  if (boldPrefix) runs.push(new TextRun({ text: boldPrefix, bold: true, size: 22, font: F }));
  runs.push(new TextRun({ text, size: 22, font: F }));
  return new Paragraph({
    numbering: { reference: "viñetas", level: 0 },
    spacing: { after: 100, line: 276 },
    alignment: AlignmentType.JUSTIFIED,
    children: runs,
  });
}

// Caja destacada estilo IQS (borde izquierdo verde, fondo gris claro)
function box(title, text) {
  return new Table({
    columnWidths: [9360],
    width: { size: 9360, type: WidthType.DXA },
    borders: {
      top: { style: BorderStyle.NONE }, bottom: { style: BorderStyle.NONE },
      right: { style: BorderStyle.NONE }, insideHorizontal: { style: BorderStyle.NONE },
      left: { style: BorderStyle.SINGLE, size: 24, color: IQS.green },
    },
    rows: [new TableRow({
      children: [new TableCell({
        width: { size: 9360, type: WidthType.DXA },
        shading: { type: ShadingType.CLEAR, fill: IQS.greyLight },
        margins: { top: 120, bottom: 120, left: 160, right: 160 },
        children: [
          new Paragraph({ spacing: { after: 60 }, children: [new TextRun({ text: title, bold: true, size: 22, color: IQS.navy, font: F })] }),
          new Paragraph({ spacing: { after: 0, line: 264 }, alignment: AlignmentType.JUSTIFIED, children: [new TextRun({ text, size: 21, font: F })] }),
        ],
      })],
    })],
  });
}

function cell(content, { bold = false, shade = null, width, color = "000000", size = 20 } = {}) {
  return new TableCell({
    width: { size: width, type: WidthType.DXA },
    shading: shade ? { type: ShadingType.CLEAR, fill: shade } : undefined,
    margins: { top: 70, bottom: 70, left: 110, right: 110 },
    children: [new Paragraph({
      spacing: { after: 0, line: 252 },
      children: [new TextRun({ text: content, bold, size, font: F, color })],
    })],
  });
}

function tabla(headers, rows, widths, { headerFill = IQS.navy } = {}) {
  return new Table({
    columnWidths: widths,
    width: { size: widths.reduce((a, b) => a + b, 0), type: WidthType.DXA },
    rows: [
      new TableRow({
        tableHeader: true,
        children: headers.map((t, i) => cell(t, { bold: true, shade: headerFill, width: widths[i], color: "FFFFFF" })),
      }),
      ...rows.map((r, ri) => new TableRow({
        children: r.map((t, i) => cell(t, { width: widths[i], shade: ri % 2 ? IQS.greyLight : null })),
      })),
    ],
  });
}

// Tabla de estructura temporal de una sesión
function tablaTiempos(rows) {
  return tabla(["Tiempo", "Actividad", "Notas para el profesor"], rows, [1300, 3600, 4460], { headerFill: IQS.greenDark });
}

const numberingConfig = {
  config: [{
    reference: "viñetas",
    levels: [{
      level: 0, format: "bullet", text: "•", alignment: AlignmentType.LEFT,
      style: { paragraph: { indent: { left: 432, hanging: 259 } } },
    }],
  }],
};

module.exports = { IQS, F, p, pRuns, h1, h2, h3, bullet, box, cell, tabla, tablaTiempos, numberingConfig };

// Guion de segmento: cabecera de tramo horario + puntos a tratar
const { TextRun: TR2, Paragraph: P2 } = require("docx");
function seg(tramo, titulo) {
  return new P2({
    spacing: { before: 200, after: 80 },
    children: [
      new TR2({ text: tramo + "  ", bold: true, size: 22, color: IQS.greenDark, font: F }),
      new TR2({ text: titulo, bold: true, size: 22, color: IQS.navy, font: F }),
    ],
  });
}
function punto(text, boldPrefix) {
  const runs = [];
  if (boldPrefix) runs.push(new TR2({ text: boldPrefix, bold: true, size: 21, font: F }));
  runs.push(new TR2({ text, size: 21, font: F }));
  return new P2({
    numbering: { reference: "viñetas", level: 0 },
    spacing: { after: 70, line: 264 },
    alignment: "both",
    children: runs,
  });
}
module.exports.seg = seg;
module.exports.punto = punto;
