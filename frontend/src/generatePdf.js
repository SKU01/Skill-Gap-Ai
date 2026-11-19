import { jsPDF } from "jspdf";
import autoTable from "jspdf-autotable";

export function generateReportPdf(report, student) {
  const doc = new jsPDF({
    orientation: "portrait",
    unit: "pt",
    format: "letter"
  });

  const pageWidth = doc.internal.pageSize.getWidth();
  const pageHeight = doc.internal.pageSize.getHeight();
  const margin = 40;
  const contentWidth = pageWidth - margin * 2;

  const roleName = report?.role || "Target Role";
  const studentName = student?.name || "Student";
  const studentEmail = student?.email || "N/A";
  const marks = report?.marks ? `${report.marks}%` : "Not specified";
  const now = new Date();
  const dateStr = now.toLocaleDateString("en-US", {
    month: "long",
    day: "numeric",
    year: "numeric"
  }) + " · " + now.toLocaleTimeString("en-US", { hour: "2-digit", minute: "2-digit" });

  let currentY = 32;

  // Top accent bar
  doc.setFillColor(37, 99, 235); // #2563eb
  doc.rect(margin, currentY, contentWidth, 3, "F");
  currentY += 18;

  // Brand and title
  doc.setFont("helvetica", "bold");
  doc.setFontSize(18);
  doc.setTextColor(30, 58, 138); // #1e3a8a
  doc.text("SkillPath AI", margin, currentY);

  doc.setFont("helvetica", "normal");
  doc.setFontSize(8.5);
  doc.setTextColor(100, 116, 139);
  doc.text(`Generated: ${dateStr}`, pageWidth - margin, currentY, { align: "right" });
  currentY += 14;

  doc.setFont("helvetica", "normal");
  doc.setFontSize(9);
  doc.setTextColor(71, 85, 105);
  doc.text("AI-Powered Career Readiness & Skill Gap Analysis", margin, currentY);
  currentY += 14;

  // Divider
  doc.setDrawColor(226, 232, 240);
  doc.setLineWidth(0.75);
  doc.line(margin, currentY, pageWidth - margin, currentY);
  currentY += 12;

  // Student Profile Card
  const profileRows = [
    [
      { content: "Candidate Name:", styles: { fontStyle: "bold", textColor: [15, 23, 42] } },
      { content: studentName, styles: { textColor: [51, 65, 85] } },
      { content: "Target Role:", styles: { fontStyle: "bold", textColor: [15, 23, 42] } },
      { content: roleName, styles: { fontStyle: "bold", textColor: [29, 78, 216] } }
    ],
    [
      { content: "Email Address:", styles: { fontStyle: "bold", textColor: [15, 23, 42] } },
      { content: studentEmail, styles: { textColor: [51, 65, 85] } },
      { content: "Academic Marks:", styles: { fontStyle: "bold", textColor: [15, 23, 42] } },
      { content: marks, styles: { textColor: [51, 65, 85] } }
    ]
  ];

  autoTable(doc, {
    startY: currentY,
    margin: { left: margin, right: margin },
    body: profileRows,
    theme: "plain",
    styles: {
      fontSize: 8.5,
      cellPadding: 5
    },
    tableLineColor: [203, 213, 225],
    tableLineWidth: 0.75,
    didDrawCell: function (data) {
      // background for the whole profile box
    }
  });

  currentY = doc.lastAutoTable.finalY + 12;

  // Summary Metrics KPIs
  const skillsList = report?.report || [];
  const extractedSkills = report?.extracted_skills || [];
  const totalEvaluated = skillsList.length;
  const totalDetected = extractedSkills.length;
  const totalGaps = skillsList.filter(s => (s.gap || 0) > 0).length;
  const totalMet = totalEvaluated - totalGaps;
  const fitRate = totalEvaluated > 0 ? Math.round((totalMet / totalEvaluated) * 100) : 0;

  const kpiRows = [
    [
      { content: `${totalDetected}\nSkills in Resume`, styles: { halign: "center", fontStyle: "bold", textColor: [37, 99, 235] } },
      { content: `${totalEvaluated}\nSkills Evaluated`, styles: { halign: "center", fontStyle: "bold", textColor: [15, 23, 42] } },
      { content: `${totalGaps}\nSkills to Improve`, styles: { halign: "center", fontStyle: "bold", textColor: [234, 88, 12] } },
      { content: `${fitRate}%\nRole Readiness Fit`, styles: { halign: "center", fontStyle: "bold", textColor: [22, 163, 74] } }
    ]
  ];

  autoTable(doc, {
    startY: currentY,
    margin: { left: margin, right: margin },
    body: kpiRows,
    theme: "grid",
    styles: {
      fontSize: 9,
      cellPadding: 6,
      fillColor: [241, 245, 249],
      lineColor: [203, 213, 225],
      lineWidth: 0.5
    }
  });

  currentY = doc.lastAutoTable.finalY + 14;

  // Section 1: Detailed Skill Gap Table
  doc.setFont("helvetica", "bold");
  doc.setFontSize(11);
  doc.setTextColor(30, 41, 59);
  doc.text("1. Current vs. Required Skill Gap Breakdown", margin, currentY);
  currentY += 6;

  const tableData = skillsList.map(item => {
    const isMet = (item.gap || 0) === 0;
    return [
      item.skill || "",
      item.category || "General",
      `${item.current || 0}%`,
      `${item.required || 0}%`,
      `${item.gap || 0}`,
      `${item.score || 0}`,
      isMet ? "Met" : `Gap (-${item.gap})`
    ];
  });

  autoTable(doc, {
    startY: currentY,
    margin: { left: margin, right: margin },
    head: [["Skill Name", "Category", "Current", "Required", "Gap", "Priority", "Status"]],
    body: tableData,
    theme: "striped",
    headStyles: {
      fillColor: [30, 58, 138],
      textColor: 255,
      fontStyle: "bold",
      fontSize: 8,
      cellPadding: 4.5
    },
    styles: {
      fontSize: 7.5,
      cellPadding: 4,
      lineColor: [226, 232, 240],
      lineWidth: 0.5
    },
    alternateRowStyles: {
      fillColor: [248, 250, 252]
    },
    columnStyles: {
      0: { cellWidth: 130, fontStyle: "bold", textColor: [15, 23, 42] },
      1: { cellWidth: 105, textColor: [71, 85, 105] },
      2: { cellWidth: 48, halign: "center" },
      3: { cellWidth: 48, halign: "center" },
      4: { cellWidth: 40, halign: "center" },
      5: { cellWidth: 48, halign: "center" },
      6: { cellWidth: 63, halign: "center", fontStyle: "bold" }
    },
    didParseCell: function (data) {
      if (data.section === "body" && data.column.index === 6) {
        if (data.cell.raw === "Met") {
          data.cell.styles.textColor = [21, 128, 61]; // green
        } else {
          data.cell.styles.textColor = [185, 28, 28]; // red
        }
      }
    }
  });

  currentY = doc.lastAutoTable.finalY + 14;

  // Section 2: Top Priority Learning Areas
  const gapSkills = skillsList.filter(s => (s.gap || 0) > 0);
  if (gapSkills.length > 0) {
    // Check if we need page break
    if (currentY > pageHeight - 120) {
      doc.addPage();
      currentY = 46;
    }

    doc.setFont("helvetica", "bold");
    doc.setFontSize(11);
    doc.setTextColor(30, 41, 59);
    doc.text("2. Top Priority Learning Areas", margin, currentY);
    currentY += 6;

    const priorityData = gapSkills.slice(0, 5).map((s, idx) => [
      `#${idx + 1}`,
      `${s.skill} (${s.category || "General"})`,
      `${s.current || 0}%`,
      `${s.required || 0}%`,
      `${s.gap || 0}`,
      `${s.score || 0} pts`
    ]);

    autoTable(doc, {
      startY: currentY,
      margin: { left: margin, right: margin },
      head: [["Rank", "Priority Skill", "Current", "Target", "Gap", "Impact Score"]],
      body: priorityData,
      theme: "striped",
      headStyles: {
        fillColor: [37, 99, 235],
        textColor: 255,
        fontStyle: "bold",
        fontSize: 8,
        cellPadding: 4.5
      },
      styles: {
        fontSize: 7.5,
        cellPadding: 4,
        lineColor: [226, 232, 240],
        lineWidth: 0.5
      },
      alternateRowStyles: {
        fillColor: [248, 250, 252]
      },
      columnStyles: {
        0: { cellWidth: 35, halign: "center", fontStyle: "bold" },
        1: { cellWidth: 200, fontStyle: "bold" },
        2: { cellWidth: 55, halign: "center" },
        3: { cellWidth: 55, halign: "center" },
        4: { cellWidth: 50, halign: "center" },
        5: { cellWidth: 80, halign: "center", fontStyle: "bold", textColor: [37, 99, 235] }
      }
    });

    currentY = doc.lastAutoTable.finalY + 14;
  }

  // Section 3: Recommended Learning Resources
  const recommendations = report?.recommendations || [];
  if (recommendations.length > 0) {
    if (currentY > pageHeight - 130) {
      doc.addPage();
      currentY = 46;
    }

    doc.setFont("helvetica", "bold");
    doc.setFontSize(11);
    doc.setTextColor(30, 41, 59);
    doc.text("3. Recommended Learning Resources & Courses", margin, currentY);
    currentY += 6;

    const recData = recommendations.map(c => [
      c.title || "",
      c.provider || "Online",
      c.level || "All Levels",
      c.url || "Available Online"
    ]);

    autoTable(doc, {
      startY: currentY,
      margin: { left: margin, right: margin },
      head: [["Course / Resource Title", "Provider", "Level", "Link / URL"]],
      body: recData,
      theme: "striped",
      headStyles: {
        fillColor: [15, 118, 110],
        textColor: 255,
        fontStyle: "bold",
        fontSize: 8,
        cellPadding: 4.5
      },
      styles: {
        fontSize: 7.5,
        cellPadding: 4,
        lineColor: [226, 232, 240],
        lineWidth: 0.5
      },
      alternateRowStyles: {
        fillColor: [248, 250, 252]
      },
      columnStyles: {
        0: { cellWidth: 220, fontStyle: "bold" },
        1: { cellWidth: 100 },
        2: { cellWidth: 70, halign: "center" },
        3: { cellWidth: 142, textColor: [37, 99, 235] }
      }
    });

    currentY = doc.lastAutoTable.finalY + 14;
  }

  // Guidance / Disclaimer note
  if (currentY > pageHeight - 70) {
    doc.addPage();
    currentY = 46;
  }

  const noteMsg = report?.note || "Resume detection indicates skill presence only. Review and adjust self-ratings for a more accurate proficiency estimate.";
  autoTable(doc, {
    startY: currentY,
    margin: { left: margin, right: margin },
    body: [[`Assessment Advisory: ${noteMsg}`]],
    theme: "plain",
    styles: {
      fontSize: 7.5,
      textColor: [71, 85, 105],
      fontStyle: "italic",
      cellPadding: 6,
      fillColor: [239, 246, 255],
      lineColor: [191, 219, 254],
      lineWidth: 0.5
    }
  });

  // Footer & Page numbers across all pages
  const totalPages = doc.getNumberOfPages();
  for (let i = 1; i <= totalPages; i++) {
    doc.setPage(i);

    // Footer divider line
    doc.setDrawColor(226, 232, 240);
    doc.setLineWidth(0.75);
    doc.line(margin, pageHeight - 34, pageWidth - margin, pageHeight - 34);

    doc.setFont("helvetica", "bold");
    doc.setFontSize(7.5);
    doc.setTextColor(37, 99, 235);
    doc.text("SkillPath AI", margin, pageHeight - 22);

    doc.setFont("helvetica", "normal");
    doc.setTextColor(100, 116, 139);
    doc.text("· Confidential Career Readiness & Skill Gap Report", margin + 48, pageHeight - 22);

    doc.text(`Page ${i} of ${totalPages}`, pageWidth - margin, pageHeight - 22, { align: "right" });
  }

  // Trigger download in browser
  const roleSlug = (roleName || "Career").replace(/[^a-zA-Z0-9]/g, "_");
  doc.save(`SkillGapReport_${roleSlug}.pdf`);
}
