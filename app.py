"""
Sistem Pendukung Keputusan Pemilihan Jurusan
Metode: SAW (Simple Additive Weighting)
Author: [Dhoni Prasetya]
"""

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from data.jurusan_data import JURUSAN_DATA, BOBOT_KRITERIA
from utils.saw_calculator import hitung_saw, format_hasil
from utils.pdf_generator import generate_pdf_report

# ========================================
# KONFIGURASI HALAMAN
# ========================================
st.set_page_config(
    page_title="SPK Pemilihan Jurusan",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ========================================
# CSS STYLING - MOBILE FIRST APPROACH
# ========================================
st.markdown("""
<style>
    /* Import Google Fonts */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');
    
    /* Global Reset & Base Styling */
    * {
        font-family: 'Inter', sans-serif;
    }
    
    /* Hide Streamlit Branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    
    /* MOBILE FIRST: Base Styles for Mobile */
    
    /* Main Container - Mobile Default */
    .main {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 0.5rem;
    }
    
    .block-container {
        background: white;
        border-radius: 12px;
        padding: 1rem;
        box-shadow: 0 4px 15px rgba(0,0,0,0.2);
        max-width: 100%;
    }
    
    /* Sidebar - Mobile */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #1e3a8a 0%, #1e40af 100%);
        padding: 1rem 0.5rem;
    }
    
    [data-testid="stSidebar"] * {
        color: white !important;
    }
    
    [data-testid="stSidebar"] h1 {
        font-size: 1.2rem;
        margin-top: 0.5rem;
    }
    
    [data-testid="stSidebar"] h3 {
        font-size: 1rem;
        margin-top: 1rem;
    }
    
    [data-testid="stSidebar"] hr {
        border-color: rgba(255,255,255,0.2);
        margin: 1rem 0;
    }
    
    /* Header - Mobile First */
    .main-header {
        font-size: 1.5rem;
        font-weight: 800;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        text-align: center;
        margin-bottom: 0.5rem;
        line-height: 1.3;
    }
    
    .sub-header {
        text-align: center;
        color: #6b7280;
        font-size: 0.85rem;
        margin-bottom: 1rem;
        font-weight: 500;
    }
    
    /* Info Box - Mobile Optimized */
    .info-box {
        padding: 0.8rem;
        border-radius: 10px;
        background: linear-gradient(135deg, #e0e7ff 0%, #e0f2fe 100%);
        border-left: 4px solid #3b82f6;
        margin: 1rem 0;
        box-shadow: 0 2px 8px rgba(59, 130, 246, 0.1);
        font-size: 0.85rem;
        line-height: 1.6;
    }
    
    .info-box strong {
        color: #1e40af;
        font-size: 0.95rem;
        display: block;
        margin-bottom: 0.3rem;
    }
    
    /* Result Card - Mobile */
    .result-card {
        padding: 1rem;
        border-radius: 12px;
        background: linear-gradient(135deg, #d1fae5 0%, #a7f3d0 100%);
        border: 2px solid #10b981;
        margin: 1rem 0;
        box-shadow: 0 4px 15px rgba(16, 185, 129, 0.2);
    }
    
    .result-card h3 {
        margin: 0 0 0.5rem 0;
        color: #059669;
        font-size: 1.1rem;
    }
    
    .result-card p {
        margin: 0.3rem 0;
        font-size: 0.9rem;
    }
    
    .result-card .jurusan-name {
        font-size: 1.3rem !important;
        color: #047857;
        font-weight: 800;
        margin: 0.5rem 0 !important;
    }
    
    .result-card .nilai-saw {
        font-size: 1.1rem !important;
        color: #059669;
        font-weight: 700;
    }
    
    /* Button - Mobile Touch Friendly */
    .stButton>button {
        width: 100%;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        font-weight: 700;
        padding: 0.8rem;
        border-radius: 10px;
        border: none;
        font-size: 0.95rem;
        box-shadow: 0 4px 12px rgba(102, 126, 234, 0.3);
        transition: all 0.2s ease;
        text-transform: uppercase;
        letter-spacing: 0.5px;
        min-height: 48px; /* Touch target size */
    }
    
    .stButton>button:active {
        transform: scale(0.98);
        box-shadow: 0 2px 8px rgba(102, 126, 234, 0.4);
    }
    
    /* Form - Mobile Optimized */
    .stTextInput>div>div>input,
    .stNumberInput>div>div>input,
    .stSelectbox>div>div>select {
        border-radius: 8px;
        border: 2px solid #e5e7eb;
        padding: 0.6rem;
        font-size: 0.95rem;
        min-height: 44px; /* Touch friendly */
    }
    
    .stTextInput>div>div>input:focus,
    .stNumberInput>div>div>input:focus,
    .stSelectbox>div>div>select:focus {
        border-color: #667eea;
        box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
    }
    
    /* Slider - Mobile */
    .stSlider {
        padding: 0.5rem 0;
    }
    
    /* Metrics - Mobile */
    div[data-testid="stMetric"] {
        background: #f9fafb;
        padding: 0.8rem;
        border-radius: 8px;
        border: 1px solid #e5e7eb;
    }
    
    div[data-testid="stMetricValue"] {
        font-size: 1.3rem;
        font-weight: 800;
        background: linear-gradient(135deg, #10b981 0%, #059669 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
    }
    
    div[data-testid="stMetricLabel"] {
        font-weight: 600;
        color: #374151;
        font-size: 0.8rem;
    }
    
    /* Dataframe - Mobile */
    .dataframe {
        font-size: 0.85rem;
        border-radius: 8px;
        overflow-x: auto;
    }
    
    /* Expander - Mobile */
    .streamlit-expanderHeader {
        background: linear-gradient(135deg, #f3f4f6 0%, #e5e7eb 100%);
        border-radius: 8px;
        font-weight: 600;
        color: #1f2937;
        padding: 0.8rem;
        font-size: 0.9rem;
    }
    
    /* Download Button - Mobile */
    .stDownloadButton>button {
        background: linear-gradient(135deg, #10b981 0%, #059669 100%);
        color: white;
        font-weight: 600;
        border-radius: 8px;
        padding: 0.6rem;
        border: none;
        box-shadow: 0 4px 12px rgba(16, 185, 129, 0.3);
        font-size: 0.85rem;
        min-height: 44px;
        width: 100%;
    }
    
    .stDownloadButton>button:active {
        transform: scale(0.98);
    }
    
    /* Subheaders - Mobile */
    h2 {
        color: #1f2937;
        font-weight: 700;
        font-size: 1.2rem;
        margin: 1rem 0 0.5rem 0;
    }
    
    h3 {
        color: #1f2937;
        font-weight: 700;
        font-size: 1rem;
        margin: 0.8rem 0 0.4rem 0;
    }
    
    /* Messages - Mobile */
    .stSuccess, .stError, .stWarning, .stInfo {
        border-radius: 10px;
        padding: 0.8rem;
        font-weight: 500;
        font-size: 0.9rem;
    }
    
    /* Caption - Mobile */
    .stCaptionContainer {
        color: #6b7280;
        font-size: 0.8rem;
        line-height: 1.5;
    }
    
    /* Chart - Mobile */
    .element-container:has(canvas) {
        margin: 1rem 0;
        border-radius: 10px;
        overflow: hidden;
    }
    
    /* Spinner */
    .stSpinner > div {
        border-top-color: #667eea !important;
    }
    
    /* ==========================================
       TABLET & DESKTOP IMPROVEMENTS
       ========================================== */
    
    /* Tablet (min-width: 768px) */
    @media (min-width: 768px) {
        .main {
            padding: 1.5rem;
        }
        
        .block-container {
            padding: 2rem;
            border-radius: 15px;
        }
        
        .main-header {
            font-size: 2.5rem;
        }
        
        .sub-header {
            font-size: 1rem;
            margin-bottom: 1.5rem;
        }
        
        .info-box {
            padding: 1.2rem;
            font-size: 0.95rem;
        }
        
        .result-card {
            padding: 1.5rem;
        }
        
        .result-card h3 {
            font-size: 1.3rem;
        }
        
        .result-card .jurusan-name {
            font-size: 1.5rem !important;
        }
        
        .stButton>button {
            font-size: 1rem;
            padding: 0.8rem 1.5rem;
        }
        
        div[data-testid="stMetricValue"] {
            font-size: 1.8rem;
        }
        
        h2 {
            font-size: 1.5rem;
        }
        
        h3 {
            font-size: 1.2rem;
        }
        
        [data-testid="stSidebar"] {
            padding: 1.5rem 1rem;
        }
        
        [data-testid="stSidebar"] h1 {
            font-size: 1.5rem;
        }
        
        [data-testid="stSidebar"] h3 {
            font-size: 1.1rem;
        }
    }
    
    /* Desktop (min-width: 1024px) */
    @media (min-width: 1024px) {
        .main {
            padding: 2rem;
        }
        
        .block-container {
            padding: 2.5rem 3rem;
            border-radius: 20px;
            box-shadow: 0 20px 60px rgba(0,0,0,0.3);
        }
        
        .main-header {
            font-size: 3rem;
            letter-spacing: -1px;
        }
        
        .sub-header {
            font-size: 1.1rem;
            margin-bottom: 2rem;
        }
        
        .info-box {
            padding: 1.5rem;
            font-size: 1rem;
            border-radius: 15px;
        }
        
        .result-card {
            padding: 2rem;
            border-radius: 20px;
            transition: transform 0.3s ease;
        }
        
        .result-card:hover {
            transform: translateY(-5px);
            box-shadow: 0 15px 40px rgba(16, 185, 129, 0.3);
        }
        
        .result-card h3 {
            font-size: 1.5rem;
        }
        
        .result-card .jurusan-name {
            font-size: 1.6rem !important;
        }
        
        .result-card .nilai-saw {
            font-size: 1.3rem !important;
        }
        
        .stButton>button {
            font-size: 1.1rem;
            padding: 0.8rem 1.5rem;
        }
        
        .stButton>button:hover {
            background: linear-gradient(135deg, #764ba2 0%, #667eea 100%);
            transform: translateY(-2px);
            box-shadow: 0 12px 30px rgba(102, 126, 234, 0.4);
        }
        
        .stDownloadButton>button:hover {
            background: linear-gradient(135deg, #059669 0%, #047857 100%);
            transform: translateY(-2px);
            box-shadow: 0 8px 20px rgba(16, 185, 129, 0.4);
        }
        
        div[data-testid="stMetricValue"] {
            font-size: 2rem;
        }
        
        div[data-testid="stMetricLabel"] {
            font-size: 0.95rem;
        }
        
        h2 {
            font-size: 1.8rem;
        }
        
        h3 {
            font-size: 1.4rem;
        }
        
        [data-testid="stSidebar"] {
            padding: 2rem 1rem;
        }
        
        [data-testid="stSidebar"] h1 {
            font-size: 1.5rem;
        }
    }
    
    /* Large Desktop (min-width: 1440px) */
    @media (min-width: 1440px) {
        .block-container {
            max-width: 1400px;
            margin: 0 auto;
        }
    }
    
    /* Landscape Optimization */
    @media (max-height: 600px) and (orientation: landscape) {
        .main {
            padding: 0.5rem;
        }
        
        .block-container {
            padding: 1rem;
        }
        
        .main-header {
            font-size: 1.3rem;
            margin-bottom: 0.3rem;
        }
        
        .sub-header {
            font-size: 0.8rem;
            margin-bottom: 0.5rem;
        }
        
        .info-box {
            padding: 0.6rem;
            margin: 0.5rem 0;
        }
        
        .result-card {
            padding: 0.8rem;
            margin: 0.5rem 0;
        }
        
        .stButton>button {
            padding: 0.5rem;
            min-height: 40px;
        }
    }
    
    /* Animations - Only on Desktop */
    @media (min-width: 1024px) {
        @keyframes fadeInDown {
            from {
                opacity: 0;
                transform: translateY(-30px);
            }
            to {
                opacity: 1;
                transform: translateY(0);
            }
        }
        
        @keyframes fadeInUp {
            from {
                opacity: 0;
                transform: translateY(30px);
            }
            to {
                opacity: 1;
                transform: translateY(0);
            }
        }
        
        @keyframes slideInLeft {
            from {
                opacity: 0;
                transform: translateX(-30px);
            }
            to {
                opacity: 1;
                transform: translateX(0);
            }
        }
        
        .main-header {
            animation: fadeInDown 0.8s ease-out;
        }
        
        .sub-header {
            animation: fadeInUp 0.8s ease-out;
        }
        
        .info-box {
            animation: slideInLeft 0.6s ease-out;
        }
    }
</style>
""", unsafe_allow_html=True)

# ========================================
# SIDEBAR - INFO APLIKASI
# ========================================
with st.sidebar:
    try:
        st.image("assets/Logo.png", width=120)  # Smaller on mobile
    except:
        st.markdown("# 🎓")
    
    st.title("📚 Informasi")
    
    st.markdown("""
    ### Tentang Aplikasi
    Aplikasi ini membantu siswa memilih jurusan kuliah yang tepat menggunakan metode SAW.
    
    ### Metode SAW
    Simple Additive Weighting adalah metode penjumlahan terbobot.
    
    ### Kriteria Penilaian
    """)
    
    for key, value in BOBOT_KRITERIA.items():
        st.write(f"• **{key.replace('_', ' ').title()}:** {value*100}%")
    
    st.markdown("---")
    st.markdown("""
    ### 📞 Bantuan
    Email: dhoniprasetya3@gmail.com  
    GitHub: @14112240028
    """)

# ========================================
# HEADER UTAMA
# ========================================
st.markdown('<p class="main-header">🎓 Sistem Pendukung Keputusan Pemilihan Jurusan</p>', unsafe_allow_html=True)
st.markdown('<p class="sub-header">Metode SAW (Simple Additive Weighting)</p>', unsafe_allow_html=True)

# Info box
st.markdown("""
<div class="info-box">
    <strong>ℹ️ Cara Penggunaan</strong>
    1. Isi data siswa di form<br>
    2. Klik "Hitung Rekomendasi"<br>
    3. Lihat hasil & ranking<br>
    4. Download PDF Report
</div>
""", unsafe_allow_html=True)

# ========================================
# LAYOUT 2 KOLOM (AUTO STACK ON MOBILE)
# ========================================
col1, col2 = st.columns([1, 1.2])

# ========================================
# KOLOM 1: FORM INPUT
# ========================================
with col1:
    st.subheader("📝 Input Data")
    
    with st.form("form_siswa"):
        # Nama
        nama = st.text_input(
            "Nama Lengkap *", 
            placeholder="Contoh: Budi Santoso"
        )
        
        # Nilai Akademik
        nilai_akademik = st.number_input(
            "Nilai Akademik (0-100) *", 
            min_value=0.0, 
            max_value=100.0, 
            value=0.0,
            step=0.1
        )
        
        # Minat
        minat = st.selectbox(
            "Minat Bidang *",
            ["", "IPA", "IPS", "Seni"]
        )
        
        # Ekonomi
        ekonomi = st.selectbox(
            "Kemampuan Ekonomi *",
            ["", "Rendah", "Sedang", "Tinggi"]
        )
        
        st.caption("• Rendah: Biaya terjangkau")
        st.caption("• Sedang: Biaya standar")
        st.caption("• Tinggi: Biaya tidak masalah")
        
        # Prospek Kerja
        prospek_kerja = st.slider(
            "Prioritas Prospek Kerja *",
            0, 100, 50
        )
        
        st.markdown("---")
        
        # Tombol Submit
        submit_button = st.form_submit_button(
            "🔍 Hitung",
            use_container_width=True
        )
    
    # Info Jurusan Tersedia
    with st.expander("📋 Daftar Jurusan"):
        for kode, data in JURUSAN_DATA.items():
            st.write(f"**{kode}:** {data['nama']}")
            st.caption(f"Minat: {data['minat']} | Biaya: {data['biaya']}")

# ========================================
# KOLOM 2: HASIL & VISUALISASI
# ========================================
with col2:
    st.subheader("📊 Hasil")
    
    if submit_button:
        # Validasi input
        if not nama or not minat or not ekonomi or nilai_akademik == 0:
            st.error("⚠️ Mohon lengkapi semua data!")
        else:
            # Hitung SAW
            with st.spinner("⏳ Menghitung..."):
                hasil, detail = hitung_saw(
                    nilai_akademik, 
                    minat, 
                    ekonomi, 
                    prospek_kerja,
                    JURUSAN_DATA,
                    BOBOT_KRITERIA
                )
            
            # ===== REKOMENDASI TERBAIK =====
            st.success("✅ Selesai!")
            
            best = hasil[0]
            st.markdown(f"""
            <div class="result-card">
                <h3>🏆 Rekomendasi Terbaik</h3>
                <p><strong>Nama:</strong> {nama}</p>
                <p class="jurusan-name">{best['Jurusan']}</p>
                <p>Nilai SAW: <span class="nilai-saw">{best['Nilai SAW']:.4f}</span></p>
            </div>
            """, unsafe_allow_html=True)
            
            # ===== METRICS =====
            met_col1, met_col2, met_col3 = st.columns(3)
            with met_col1:
                st.metric("Ranking", "#1", delta="Top")
            with met_col2:
                st.metric("Kode", best['Kode'])
            with met_col3:
                gap = best['Nilai SAW'] - hasil[1]['Nilai SAW']
                st.metric("Gap", f"{gap:.3f}")
            
            st.markdown("---")
            
            # ===== TABEL RANKING =====
            st.write("### 📋 Ranking Lengkap")
            
            df_hasil = pd.DataFrame(hasil)
            df_hasil['Ranking'] = range(1, len(df_hasil) + 1)
            df_hasil['Nilai SAW'] = df_hasil['Nilai SAW'].apply(lambda x: f"{x:.4f}")
            
            st.dataframe(
                df_hasil[['Ranking', 'Kode', 'Jurusan', 'Nilai SAW']],
                use_container_width=True,
                hide_index=True,
                height=200
            )
            
            # ===== VISUALISASI =====
            st.write("### 📈 Grafik")
            
            fig, ax = plt.subplots(figsize=(10, 4))
            colors = ['#10b981', '#3b82f6', '#f59e0b', '#ef4444', '#6b7280']
            
            jurusan_names = [h['Jurusan'] for h in hasil]
            nilai_saw = [h['Nilai SAW'] for h in hasil]
            
            bars = ax.barh(jurusan_names, nilai_saw, color=colors, height=0.6)
            
            ax.set_xlabel('Nilai SAW', fontsize=11, fontweight='bold')
            ax.set_title('Perbandingan Nilai SAW', fontsize=12, fontweight='bold', pad=15)
            ax.grid(axis='x', alpha=0.3, linestyle='--')
            
            for i, (bar, nilai) in enumerate(zip(bars, nilai_saw)):
                width = bar.get_width()
                ax.text(width + 0.01, bar.get_y() + bar.get_height()/2, 
                       f'{nilai:.3f}',
                       ha='left', va='center', fontsize=9, fontweight='bold')
            
            plt.tight_layout()
            st.pyplot(fig)
            
            # ===== DETAIL =====
            with st.expander("🔢 Detail Perhitungan"):
                st.write("**Nilai Normalisasi (R):**")
                
                df_detail = pd.DataFrame(detail)
                df_detail = df_detail.round(4)
                
                st.dataframe(df_detail, use_container_width=True, hide_index=True)
                
                st.caption("""
                **Rumus:** Vi = Σ(Wj × Rij)
                
                • R1: Nilai Akademik (30%)
                • R2: Minat (35%)
                • R3: Ekonomi (20%)
                • R4: Prospek (15%)
                """)
            
            # ===== EXPORT =====
            st.markdown("---")
            st.write("### 💾 Export Data")
            exp_col1, exp_col2, exp_col3 = st.columns(3)
            
            with exp_col1:
            # Export CSV
                csv = df_hasil.to_csv(index=False).encode('utf-8')
                st.download_button(
                    label="📥 Hasil",
                    data=csv,
                    file_name=f"hasil_{nama.replace(' ', '_')}.csv",
                    mime="text/csv",
                    use_container_width=True
                )
            # Export Detail Perhitungan
            with exp_col2:
                csv_detail = pd.DataFrame(detail).to_csv(index=False).encode('utf-8')
                st.download_button(
                    label="📥 Detail",
                    data=csv_detail,
                    file_name=f"detail_{nama.replace(' ', '_')}.csv",
                    mime="text/csv",
                    use_container_width=True
                )
            with exp_col3:
            # Export PDF Report
                pdf_bytes = generate_pdf_report(
                    nama = nama,
                    nilai_akademik = nilai_akademik,
                    minat = minat,
                    ekonomi = ekonomi,
                    prospek_kerja = prospek_kerja,
                    hasil = hasil,
                    detail = detail,
                    bobot_kriteria = BOBOT_KRITERIA
                )
                st.download_button(
                    label="📄 PDF Report",
                    data=pdf_bytes,
                    file_name=f"report_{nama.replace(' ', '_')}.pdf",
                    mime="application/pdf",
                    use_container_width=True
                )
    else:
        st.info("👈 Isi form dan klik tombol hitung")
        
        st.markdown("""
        ### 🎯 Kriteria
        
        Sistem menggunakan 4 kriteria:
        
        1. **Nilai Akademik (30%)**
        2. **Minat (35%)**
        3. **Ekonomi (20%)**
        4. **Prospek Kerja (15%)**
        """)

# ========================================
# FOOTER
# ========================================
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #6b7280; font-size: 0.85rem; padding: 1rem;">
    <p style="margin: 3px 0;"><strong>📚 SPK Pemilihan Jurusan</strong></p>
    <p style="margin: 3px 0;">Metode SAW</p>
    <p style="margin: 8px 0 3px 0; color: #9ca3af;">© 2024 v1.0</p>
</div>
""", unsafe_allow_html=True)