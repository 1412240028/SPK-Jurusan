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
# CSS STYLING
# ========================================
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        color: #1e40af;
        text-align: center;
        margin-bottom: 10px;
    }
    .sub-header {
        text-align: center;
        color: #6b7280;
        margin-bottom: 30px;
    }
    .result-card {
        padding: 20px;
        border-radius: 10px;
        background-color: #f0fdf4;
        border-left: 5px solid #10b981;
        margin: 20px 0;
    }
    .info-box {
        padding: 15px;
        border-radius: 8px;
        background-color: #eff6ff;
        border-left: 4px solid #3b82f6;
        margin: 15px 0;
    }
    .stButton>button {
        width: 100%;
        background-color: #4f46e5;
        color: white;
        font-weight: bold;
        padding: 12px;
        border-radius: 8px;
        border: none;
        font-size: 1rem;
    }
    .stButton>button:hover {
        background-color: #4338ca;
    }
    div[data-testid="stMetricValue"] {
        font-size: 1.5rem;
        color: #059669;
    }
</style>
""", unsafe_allow_html=True)

# ========================================
# SIDEBAR - INFO APLIKASI
# ========================================
with st.sidebar:
    st.image("https://via.placeholder.com/150x150.png?text=SPK", width=150)
    st.title("📚 Informasi")
    
    st.markdown("""
    ### Tentang Aplikasi
    Aplikasi ini membantu siswa memilih jurusan kuliah yang tepat menggunakan metode SAW.
    
    ### Metode SAW
    Simple Additive Weighting adalah metode penjumlahan terbobot yang mencari penjumlahan terbobot dari rating kinerja pada setiap alternatif.
    
    ### Kriteria Penilaian
    """)
    
    for key, value in BOBOT_KRITERIA.items():
        st.write(f"- **{key.replace('_', ' ').title()}:** {value*100}%")
    
    st.markdown("---")
    st.markdown("""
    ### 📞 Bantuan
    Jika ada pertanyaan, hubungi:
    - Email: admin@spk.ac.id
    - Telp: 0812-3456-7890
    """)

# ========================================
# HEADER UTAMA
# ========================================
st.markdown('<p class="main-header">🎓 Sistem Pendukung Keputusan Pemilihan Jurusan</p>', unsafe_allow_html=True)
st.markdown('<p class="sub-header">Metode SAW (Simple Additive Weighting)</p>', unsafe_allow_html=True)

# Info box
st.markdown("""
<div class="info-box">
    <strong>ℹ️ Cara Penggunaan:</strong><br>
    1. Isi semua data siswa di form sebelah kiri<br>
    2. Klik tombol "Hitung Rekomendasi"<br>
    3. Lihat hasil rekomendasi dan ranking jurusan<br>
    4. Ekspor hasil jika diperlukan
</div>
""", unsafe_allow_html=True)

# ========================================
# LAYOUT 2 KOLOM
# ========================================
col1, col2 = st.columns([1, 1.2])

# ========================================
# KOLOM 1: FORM INPUT
# ========================================
with col1:
    st.subheader("📝 Input Data Siswa")
    
    with st.form("form_siswa"):
        # Nama
        nama = st.text_input(
            "Nama Lengkap *", 
            placeholder="Contoh: Budi Santoso",
            help="Masukkan nama lengkap siswa"
        )
        
        # Nilai Akademik
        nilai_akademik = st.number_input(
            "Nilai Akademik (0-100) *", 
            min_value=0.0, 
            max_value=100.0, 
            value=0.0,
            step=0.1,
            help="Rata-rata nilai rapor atau ijazah siswa"
        )
        
        # Minat
        minat = st.selectbox(
            "Minat Bidang Studi *",
            ["", "IPA", "IPS", "Seni"],
            help="Pilih bidang studi yang diminati siswa"
        )
        
        # Ekonomi
        ekonomi = st.selectbox(
            "Kemampuan Ekonomi *",
            ["", "Rendah", "Sedang", "Tinggi"],
            help="Kemampuan keluarga dalam membiayai kuliah"
        )
        
        st.markdown("**Keterangan Kemampuan Ekonomi:**")
        st.caption("• Rendah: Lebih memilih biaya kuliah terjangkau")
        st.caption("• Sedang: Biaya kuliah standar")
        st.caption("• Tinggi: Biaya bukan masalah utama")
        
        # Prospek Kerja
        prospek_kerja = st.slider(
            "Prioritas Prospek Kerja (0-100) *",
            0, 100, 50,
            help="Seberapa penting prospek kerja dalam memilih jurusan? (0=tidak penting, 100=sangat penting)"
        )
        
        st.markdown("---")
        
        # Tombol Submit
        submit_button = st.form_submit_button(
            "🔍 Hitung Rekomendasi",
            use_container_width=True
        )
    
    # Info Jurusan Tersedia
    with st.expander("📋 Lihat Daftar Jurusan Tersedia"):
        for kode, data in JURUSAN_DATA.items():
            st.write(f"**{kode}:** {data['nama']}")
            st.caption(f"└─ Minat: {data['minat']} | Biaya: {data['biaya']} | Prospek: {data['prospek']}/100")

# ========================================
# KOLOM 2: HASIL & VISUALISASI
# ========================================
with col2:
    st.subheader("📊 Hasil Rekomendasi")
    
    if submit_button:
        # Validasi input
        if not nama or not minat or not ekonomi or nilai_akademik == 0:
            st.error("⚠️ **Mohon lengkapi semua data yang bertanda (*)**")
        else:
            # Hitung SAW
            with st.spinner("⏳ Sedang menghitung..."):
                hasil, detail = hitung_saw(
                    nilai_akademik, 
                    minat, 
                    ekonomi, 
                    prospek_kerja,
                    JURUSAN_DATA,
                    BOBOT_KRITERIA
                )
            
            # ===== REKOMENDASI TERBAIK =====
            st.success("✅ Perhitungan selesai!")
            
            best = hasil[0]
            st.markdown(f"""
            <div class="result-card">
                <h3 style="margin:0; color:#059669;">🏆 Rekomendasi Terbaik</h3>
                <p style="margin:10px 0 5px 0;"><strong>Nama Siswa:</strong> {nama}</p>
                <p style="margin:5px 0; font-size:1.4rem; color:#047857; font-weight:bold;">
                    {best['Jurusan']}
                </p>
                <p style="margin:5px 0; color:#6b7280; font-size:1.1rem;">
                    Nilai SAW: <strong style="color:#059669;">{best['Nilai SAW']:.4f}</strong>
                </p>
            </div>
            """, unsafe_allow_html=True)
            
            # ===== METRICS =====
            met_col1, met_col2, met_col3 = st.columns(3)
            with met_col1:
                st.metric("Ranking", "#1", delta="Terbaik")
            with met_col2:
                st.metric("Kode Jurusan", best['Kode'])
            with met_col3:
                gap = best['Nilai SAW'] - hasil[1]['Nilai SAW']
                st.metric("Selisih Rank #2", f"{gap:.4f}")
            
            st.markdown("---")
            
            # ===== TABEL RANKING =====
            st.write("### 📋 Ranking Lengkap Semua Jurusan")
            
            df_hasil = pd.DataFrame(hasil)
            df_hasil['Ranking'] = range(1, len(df_hasil) + 1)
            df_hasil['Nilai SAW'] = df_hasil['Nilai SAW'].apply(lambda x: f"{x:.4f}")
            
            # Styling dataframe
            st.dataframe(
                df_hasil[['Ranking', 'Kode', 'Jurusan', 'Nilai SAW']],
                use_container_width=True,
                hide_index=True,
                height=220
            )
            
            # ===== VISUALISASI BAR CHART =====
            st.write("### 📈 Visualisasi Perbandingan")
            
            fig, ax = plt.subplots(figsize=(10, 5))
            colors = ['#10b981', '#3b82f6', '#f59e0b', '#ef4444', '#6b7280']
            
            jurusan_names = [h['Jurusan'] for h in hasil]
            nilai_saw = [h['Nilai SAW'] for h in hasil]
            
            bars = ax.barh(jurusan_names, nilai_saw, color=colors)
            
            ax.set_xlabel('Nilai SAW', fontsize=12, fontweight='bold')
            ax.set_title('Perbandingan Nilai SAW Semua Jurusan', 
                        fontsize=14, fontweight='bold', pad=20)
            ax.grid(axis='x', alpha=0.3, linestyle='--')
            
            # Tambahkan nilai di ujung bar
            for i, (bar, nilai) in enumerate(zip(bars, nilai_saw)):
                width = bar.get_width()
                ax.text(width + 0.01, bar.get_y() + bar.get_height()/2, 
                       f'{nilai:.4f}',
                       ha='left', va='center', fontsize=10, fontweight='bold')
            
            plt.tight_layout()
            st.pyplot(fig)
            
            # ===== DETAIL PERHITUNGAN =====
            with st.expander("🔢 Lihat Detail Perhitungan Lengkap"):
                st.write("**Tabel Nilai Normalisasi (R) dan Hasil Akhir:**")
                
                df_detail = pd.DataFrame(detail)
                df_detail = df_detail.round(4)
                
                st.dataframe(df_detail, use_container_width=True, hide_index=True)
                
                st.markdown("""
                **Keterangan Kolom:**
                - **R1:** Normalisasi Nilai Akademik (Benefit)
                - **R2:** Normalisasi Minat (1.0 = cocok, 0.6 = tidak cocok)
                - **R3:** Normalisasi Ekonomi (Cost - biaya kuliah)
                - **R4:** Normalisasi Prospek Kerja (Benefit)
                - **Total:** Hasil penjumlahan terbobot = (0.30×R1) + (0.35×R2) + (0.20×R3) + (0.15×R4)
                
                **Rumus SAW:**
                ```
                Vi = Σ(Wj × Rij)
                ```
                Di mana:
                - Vi = Nilai preferensi alternatif ke-i
                - Wj = Bobot kriteria ke-j
                - Rij = Rating kinerja ternormalisasi
                """)
            
            # ===== TOMBOL EXPORT =====
            st.markdown("---")
            exp_col1, exp_col2 = st.columns(2)
            
            with exp_col1:
                # Export ke CSV
                csv = df_hasil.to_csv(index=False).encode('utf-8')
                st.download_button(
                    label="📥 Download Hasil (CSV)",
                    data=csv,
                    file_name=f"hasil_spk_{nama.replace(' ', '_')}.csv",
                    mime="text/csv",
                    use_container_width=True
                )
            
            with exp_col2:
                # Export detail perhitungan
                csv_detail = pd.DataFrame(detail).to_csv(index=False).encode('utf-8')
                st.download_button(
                    label="📥 Download Detail (CSV)",
                    data=csv_detail,
                    file_name=f"detail_perhitungan_{nama.replace(' ', '_')}.csv",
                    mime="text/csv",
                    use_container_width=True
                )
    
    else:
        # Tampilan default sebelum hitung
        st.info("👈 Silakan isi form di sebelah kiri dan klik tombol 'Hitung Rekomendasi'")
        
        st.markdown("""
        ### 🎯 Kriteria Penilaian
        
        Sistem ini menggunakan 4 kriteria utama:
        
        1. **Nilai Akademik (30%)** - Kemampuan akademis siswa
        2. **Minat (35%)** - Kesesuaian minat dengan jurusan
        3. **Ekonomi (20%)** - Kemampuan biaya kuliah
        4. **Prospek Kerja (15%)** - Peluang karir setelah lulus
        
        Semakin tinggi nilai SAW yang dihasilkan, semakin cocok jurusan tersebut dengan profil siswa.
        """)

# ========================================
# FOOTER
# ========================================
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #6b7280; font-size: 0.9rem; padding: 20px;">
    <p style="margin: 5px 0;"><strong>📚 Sistem Pendukung Keputusan Pemilihan Jurusan</strong></p>
    <p style="margin: 5px 0;">Menggunakan Metode SAW (Simple Additive Weighting)</p>
    <p style="margin: 5px 0;">Dibuat untuk keperluan pembelajaran Mata Kuliah Sistem Pendukung Keputusan</p>
    <p style="margin: 15px 0 5px 0; color: #9ca3af;">© 2024 - SPK Jurusan v1.0</p>
</div>
""", unsafe_allow_html=True)