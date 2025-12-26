"""
PDF Generator untuk SPK Pemilihan Jurusan
Menggunakan ReportLab untuk generate PDF report
"""

from reportlab.lib.pagesizes import A4, letter
from reportlab.lib import colors
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, PageBreak, Image
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_JUSTIFY
from reportlab.pdfgen import canvas
from io import BytesIO
from datetime import datetime
import pandas as pd

def generate_pdf_report(nama, nilai_akademik, minat, ekonomi, prospek_kerja, 
                       hasil, detail, bobot_kriteria):
    """
    Generate PDF report untuk hasil rekomendasi SPK
    
    Args:
        nama (str): Nama siswa
        nilai_akademik (float): Nilai akademik
        minat (str): Minat bidang studi
        ekonomi (str): Kemampuan ekonomi
        prospek_kerja (float): Prioritas prospek kerja
        hasil (list): List hasil ranking
        detail (list): List detail perhitungan
        bobot_kriteria (dict): Dictionary bobot kriteria
    
    Returns:
        BytesIO: PDF file dalam bentuk bytes
    """
    
    # Buat buffer untuk PDF
    buffer = BytesIO()
    
    # Setup document
    doc = SimpleDocTemplate(
        buffer,
        pagesize=A4,
        rightMargin=0.75*inch,
        leftMargin=0.75*inch,
        topMargin=1*inch,
        bottomMargin=0.75*inch
    )
    
    # Container untuk elements
    elements = []
    
    # Styles
    styles = getSampleStyleSheet()
    
    # Custom styles
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=18,
        textColor=colors.HexColor('#1e40af'),
        spaceAfter=10,
        alignment=TA_CENTER,
        fontName='Helvetica-Bold'
    )
    
    subtitle_style = ParagraphStyle(
        'CustomSubtitle',
        parent=styles['Normal'],
        fontSize=12,
        textColor=colors.HexColor('#6b7280'),
        spaceAfter=20,
        alignment=TA_CENTER,
        fontName='Helvetica'
    )
    
    heading_style = ParagraphStyle(
        'CustomHeading',
        parent=styles['Heading2'],
        fontSize=14,
        textColor=colors.HexColor('#1f2937'),
        spaceAfter=12,
        spaceBefore=12,
        fontName='Helvetica-Bold'
    )
    
    normal_style = ParagraphStyle(
        'CustomNormal',
        parent=styles['Normal'],
        fontSize=10,
        textColor=colors.HexColor('#374151'),
        spaceAfter=6,
        fontName='Helvetica'
    )
    
    # ========================================
    # HEADER
    # ========================================
    elements.append(Paragraph("🎓 SISTEM PENDUKUNG KEPUTUSAN", title_style))
    elements.append(Paragraph("PEMILIHAN JURUSAN KULIAH", title_style))
    elements.append(Paragraph("Metode SAW (Simple Additive Weighting)", subtitle_style))
    elements.append(Spacer(1, 0.3*inch))
    
    # ========================================
    # INFO SISWA
    # ========================================
    elements.append(Paragraph("📋 DATA SISWA", heading_style))
    
    data_siswa = [
        ['Nama Lengkap', ':', nama],
        ['Nilai Akademik', ':', f'{nilai_akademik:.1f}'],
        ['Minat Bidang Studi', ':', minat],
        ['Kemampuan Ekonomi', ':', ekonomi],
        ['Prioritas Prospek Kerja', ':', f'{prospek_kerja}/100'],
        ['Tanggal Analisis', ':', datetime.now().strftime('%d %B %Y, %H:%M')]
    ]
    
    table_siswa = Table(data_siswa, colWidths=[2*inch, 0.3*inch, 3*inch])
    table_siswa.setStyle(TableStyle([
        ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 0), (-1, -1), 10),
        ('TEXTCOLOR', (0, 0), (0, -1), colors.HexColor('#1f2937')),
        ('TEXTCOLOR', (2, 0), (2, -1), colors.HexColor('#059669')),
        ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
        ('FONTNAME', (2, 0), (2, -1), 'Helvetica-Bold'),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('LEFTPADDING', (0, 0), (-1, -1), 0),
        ('RIGHTPADDING', (0, 0), (-1, -1), 0),
    ]))
    
    elements.append(table_siswa)
    elements.append(Spacer(1, 0.3*inch))
    
    # ========================================
    # REKOMENDASI TERBAIK
    # ========================================
    best = hasil[0]
    
    elements.append(Paragraph("🏆 REKOMENDASI TERBAIK", heading_style))
    
    # Box untuk rekomendasi
    rekomendasi_data = [
        [Paragraph(f"<b>{best['Jurusan']}</b>", ParagraphStyle('Bold', fontSize=14, textColor=colors.HexColor('#059669')))],
        [f"Kode: {best['Kode']}"],
        [f"Nilai SAW: {best['Nilai SAW']:.4f}"],
        ['Ranking: #1']
    ]
    
    table_rekomendasi = Table(rekomendasi_data, colWidths=[5.5*inch])
    table_rekomendasi.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor('#d1fae5')),
        ('TEXTCOLOR', (0, 0), (-1, -1), colors.HexColor('#047857')),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 1), (-1, -1), 11),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('INNERGRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#10b981')),
        ('BOX', (0, 0), (-1, -1), 2, colors.HexColor('#10b981')),
        ('TOPPADDING', (0, 0), (-1, -1), 10),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 10),
    ]))
    
    elements.append(table_rekomendasi)
    elements.append(Spacer(1, 0.3*inch))
    
    # ========================================
    # RANKING LENGKAP
    # ========================================
    elements.append(Paragraph("📊 RANKING LENGKAP SEMUA JURUSAN", heading_style))
    
    # Prepare data untuk tabel
    ranking_data = [['Rank', 'Kode', 'Nama Jurusan', 'Nilai SAW']]
    
    for i, h in enumerate(hasil, 1):
        ranking_data.append([
            str(i),
            h['Kode'],
            h['Jurusan'],
            f"{h['Nilai SAW']:.4f}"
        ])
    
    table_ranking = Table(ranking_data, colWidths=[0.7*inch, 0.7*inch, 2.8*inch, 1.3*inch])
    table_ranking.setStyle(TableStyle([
        # Header
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#3b82f6')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 11),
        ('ALIGN', (0, 0), (-1, 0), 'CENTER'),
        
        # Body
        ('BACKGROUND', (0, 1), (-1, 1), colors.HexColor('#d1fae5')),  # Rank 1
        ('TEXTCOLOR', (0, 1), (-1, 1), colors.HexColor('#047857')),
        ('FONTNAME', (0, 1), (-1, 1), 'Helvetica-Bold'),
        
        ('BACKGROUND', (0, 2), (-1, -1), colors.white),
        ('TEXTCOLOR', (0, 2), (-1, -1), colors.black),
        ('FONTNAME', (0, 2), (-1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 1), (-1, -1), 10),
        ('ALIGN', (0, 1), (-1, -1), 'CENTER'),
        ('ALIGN', (2, 1), (2, -1), 'LEFT'),
        
        # Grid
        ('INNERGRID', (0, 0), (-1, -1), 0.5, colors.grey),
        ('BOX', (0, 0), (-1, -1), 1, colors.HexColor('#3b82f6')),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('TOPPADDING', (0, 0), (-1, -1), 8),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
    ]))
    
    elements.append(table_ranking)
    elements.append(Spacer(1, 0.3*inch))
    
    # ========================================
    # BOBOT KRITERIA
    # ========================================
    elements.append(Paragraph("⚖️ BOBOT KRITERIA PENILAIAN", heading_style))
    
    bobot_data = [['Kriteria', 'Bobot', 'Persentase']]
    for key, value in bobot_kriteria.items():
        bobot_data.append([
            key.replace('_', ' ').title(),
            f'{value:.2f}',
            f'{value*100:.0f}%'
        ])
    
    table_bobot = Table(bobot_data, colWidths=[2.5*inch, 1.5*inch, 1.5*inch])
    table_bobot.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#f59e0b')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 11),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        
        ('BACKGROUND', (0, 1), (-1, -1), colors.white),
        ('TEXTCOLOR', (0, 1), (-1, -1), colors.black),
        ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 1), (-1, -1), 10),
        
        ('INNERGRID', (0, 0), (-1, -1), 0.5, colors.grey),
        ('BOX', (0, 0), (-1, -1), 1, colors.HexColor('#f59e0b')),
        ('TOPPADDING', (0, 0), (-1, -1), 6),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
    ]))
    
    elements.append(table_bobot)
    elements.append(PageBreak())
    
    # ========================================
    # DETAIL PERHITUNGAN (Page 2)
    # ========================================
    elements.append(Paragraph("🔢 DETAIL PERHITUNGAN NORMALISASI", heading_style))
    elements.append(Paragraph("Tabel berikut menampilkan nilai normalisasi (R) untuk setiap kriteria:", normal_style))
    elements.append(Spacer(1, 0.1*inch))
    
    # Prepare detail data
    detail_data = [['Kode', 'Jurusan', 'R1', 'R2', 'R3', 'R4', 'Total']]
    
    for d in detail:
        detail_data.append([
            d['Kode'],
            d['Jurusan'][:15],  # Trim nama kalau kepanjangan
            f"{d['R1']:.3f}",
            f"{d['R2']:.3f}",
            f"{d['R3']:.3f}",
            f"{d['R4']:.3f}",
            f"{d['Total']:.4f}"
        ])
    
    table_detail = Table(detail_data, colWidths=[0.5*inch, 1.8*inch, 0.6*inch, 0.6*inch, 0.6*inch, 0.6*inch, 0.8*inch])
    table_detail.setStyle(TableStyle([
        # Header
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#6366f1')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 9),
        ('ALIGN', (0, 0), (-1, 0), 'CENTER'),
        
        # Rank 1 row
        ('BACKGROUND', (0, 1), (-1, 1), colors.HexColor('#d1fae5')),
        ('FONTNAME', (0, 1), (-1, 1), 'Helvetica-Bold'),
        
        # Body
        ('BACKGROUND', (0, 2), (-1, -1), colors.white),
        ('FONTNAME', (0, 2), (-1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 1), (-1, -1), 8),
        ('ALIGN', (0, 1), (-1, -1), 'CENTER'),
        ('ALIGN', (1, 1), (1, -1), 'LEFT'),
        
        ('INNERGRID', (0, 0), (-1, -1), 0.5, colors.grey),
        ('BOX', (0, 0), (-1, -1), 1, colors.HexColor('#6366f1')),
        ('TOPPADDING', (0, 0), (-1, -1), 5),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 5),
    ]))
    
    elements.append(table_detail)
    elements.append(Spacer(1, 0.2*inch))
    
    # ========================================
    # KETERANGAN
    # ========================================
    elements.append(Paragraph("📖 KETERANGAN", heading_style))
    
    keterangan_text = """
    <b>R1 - Nilai Akademik (Benefit):</b> Normalisasi berdasarkan nilai standar jurusan<br/>
    <b>R2 - Minat (Benefit):</b> Nilai 1.0 jika minat cocok, 0.6 jika tidak cocok<br/>
    <b>R3 - Ekonomi (Cost):</b> Normalisasi biaya kuliah vs kemampuan ekonomi<br/>
    <b>R4 - Prospek Kerja (Benefit):</b> Normalisasi prioritas prospek kerja<br/>
    <br/>
    <b>Formula SAW:</b> Vi = Σ(Wj × Rij)<br/>
    Di mana:<br/>
    • Vi = Nilai preferensi alternatif ke-i<br/>
    • Wj = Bobot kriteria ke-j<br/>
    • Rij = Rating kinerja ternormalisasi<br/>
    <br/>
    <b>Kesimpulan:</b><br/>
    Semakin tinggi nilai Total (Vi), semakin cocok jurusan tersebut dengan profil siswa.
    """
    
    elements.append(Paragraph(keterangan_text, normal_style))
    elements.append(Spacer(1, 0.3*inch))
    
    # ========================================
    # FOOTER
    # ========================================
    footer_style = ParagraphStyle(
        'Footer',
        parent=styles['Normal'],
        fontSize=8,
        textColor=colors.HexColor('#9ca3af'),
        alignment=TA_CENTER
    )
    
    elements.append(Spacer(1, 0.5*inch))
    elements.append(Paragraph("─" * 80, footer_style))
    elements.append(Paragraph("Sistem Pendukung Keputusan Pemilihan Jurusan", footer_style))
    elements.append(Paragraph("Metode SAW (Simple Additive Weighting)", footer_style))
    elements.append(Paragraph(f"Generated on {datetime.now().strftime('%d %B %Y, %H:%M:%S')}", footer_style))
    elements.append(Paragraph("© 2024 SPK Jurusan v1.0", footer_style))
    
    # Build PDF
    doc.build(elements)
    
    # Get PDF bytes
    pdf_bytes = buffer.getvalue()
    buffer.close()
    
    return pdf_bytes


def generate_simple_pdf(nama, best_jurusan, nilai_saw):
    """
    Generate PDF simple (backup jika reportlab gagal)
    Hanya menampilkan hasil utama
    """
    buffer = BytesIO()
    
    doc = SimpleDocTemplate(buffer, pagesize=A4)
    elements = []
    styles = getSampleStyleSheet()
    
    elements.append(Paragraph("HASIL REKOMENDASI JURUSAN", styles['Title']))
    elements.append(Spacer(1, 0.3*inch))
    elements.append(Paragraph(f"Nama: {nama}", styles['Normal']))
    elements.append(Paragraph(f"Jurusan Terbaik: {best_jurusan}", styles['Heading2']))
    elements.append(Paragraph(f"Nilai SAW: {nilai_saw:.4f}", styles['Normal']))
    
    doc.build(elements)
    
    pdf_bytes = buffer.getvalue()
    buffer.close()
    
    return pdf_bytes