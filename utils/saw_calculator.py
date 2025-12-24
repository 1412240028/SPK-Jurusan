"""
Modul untuk perhitungan SAW (Simple Additive Weighting)
Berisi semua fungsi logic untuk menghitung rekomendasi jurusan
"""

from data.jurusan_data import EKONOMI_SISWA_MAP, BIAYA_JURUSAN_MAP


def normalisasi_benefit(nilai, nilai_max):
    """
    Normalisasi untuk kriteria benefit (semakin besar semakin baik)
    
    Formula: Rij = Xij / Max(Xij)
    
    Args:
        nilai (float): Nilai yang akan dinormalisasi
        nilai_max (float): Nilai maksimum dari kriteria
    
    Returns:
        float: Nilai ternormalisasi (0-1)
    """
    if nilai_max == 0:
        return 0
    return nilai / nilai_max


def normalisasi_cost(nilai_min, nilai):
    """
    Normalisasi untuk kriteria cost (semakin kecil semakin baik)
    
    Formula: Rij = Min(Xij) / Xij
    
    Args:
        nilai_min (float): Nilai minimum dari kriteria
        nilai (float): Nilai yang akan dinormalisasi
    
    Returns:
        float: Nilai ternormalisasi (0-1)
    """
    if nilai == 0:
        return 0
    return nilai_min / nilai


def hitung_r1_nilai_akademik(nilai_siswa, nilai_standar_jurusan):
    """
    Hitung normalisasi R1 untuk kriteria Nilai Akademik
    
    Args:
        nilai_siswa (float): Nilai akademik siswa (0-100)
        nilai_standar_jurusan (float): Nilai standar jurusan
    
    Returns:
        float: Nilai R1 ternormalisasi
    """
    return normalisasi_benefit(nilai_siswa, nilai_standar_jurusan)


def hitung_r2_minat(minat_siswa, minat_jurusan):
    """
    Hitung normalisasi R2 untuk kriteria Minat
    
    Args:
        minat_siswa (str): Minat siswa ('IPA', 'IPS', 'Seni')
        minat_jurusan (str): Minat yang cocok untuk jurusan
    
    Returns:
        float: Nilai R2 (1.0 jika cocok, 0.6 jika tidak cocok)
    """
    if minat_siswa == minat_jurusan:
        return 1.0  # Minat cocok
    else:
        return 0.6  # Minat tidak cocok, tapi masih bisa


def hitung_r3_ekonomi(kemampuan_ekonomi_siswa, biaya_jurusan):
    """
    Hitung normalisasi R3 untuk kriteria Ekonomi (COST)
    
    Args:
        kemampuan_ekonomi_siswa (str): 'Rendah', 'Sedang', 'Tinggi'
        biaya_jurusan (str): 'Rendah', 'Sedang', 'Tinggi'
    
    Returns:
        float: Nilai R3 ternormalisasi
    """
    # Convert ke nilai numerik
    ekonomi_nilai = EKONOMI_SISWA_MAP[kemampuan_ekonomi_siswa]
    biaya_nilai = BIAYA_JURUSAN_MAP[biaya_jurusan]
    
    # Normalisasi cost (ekonomi siswa / biaya jurusan)
    # Jika biaya rendah & ekonomi siswa rendah = cocok (nilai tinggi)
    # Jika biaya tinggi & ekonomi siswa rendah = tidak cocok (nilai rendah)
    return normalisasi_cost(ekonomi_nilai, biaya_nilai)


def hitung_r4_prospek_kerja(prioritas_siswa, prospek_jurusan):
    """
    Hitung normalisasi R4 untuk kriteria Prospek Kerja
    
    Args:
        prioritas_siswa (float): Seberapa penting prospek kerja (0-100)
        prospek_jurusan (float): Prospek kerja jurusan (0-100)
    
    Returns:
        float: Nilai R4 ternormalisasi
    """
    # Jika siswa tidak peduli prospek (0), return 0.5 (netral)
    if prioritas_siswa == 0:
        return 0.5
    
    # Normalisasi berdasarkan prioritas siswa
    return normalisasi_benefit(prioritas_siswa * (prospek_jurusan / 100), 100)


def hitung_nilai_preferensi(r1, r2, r3, r4, bobot):
    """
    Hitung nilai preferensi (Vi) menggunakan metode SAW
    
    Formula: Vi = Σ(Wj × Rij)
    
    Args:
        r1 (float): Nilai R1 (Nilai Akademik)
        r2 (float): Nilai R2 (Minat)
        r3 (float): Nilai R3 (Ekonomi)
        r4 (float): Nilai R4 (Prospek Kerja)
        bobot (dict): Dictionary berisi bobot setiap kriteria
    
    Returns:
        float: Nilai preferensi total
    """
    nilai_preferensi = (
        (bobot['nilai_akademik'] * r1) +
        (bobot['minat'] * r2) +
        (bobot['ekonomi'] * r3) +
        (bobot['prospek_kerja'] * r4)
    )
    return nilai_preferensi


def hitung_saw(nilai_akademik, minat, ekonomi, prospek_kerja, 
               jurusan_data, bobot_kriteria):
    """
    Fungsi utama untuk menghitung SAW untuk semua alternatif jurusan
    
    Args:
        nilai_akademik (float): Nilai akademik siswa (0-100)
        minat (str): Minat siswa ('IPA', 'IPS', 'Seni')
        ekonomi (str): Kemampuan ekonomi ('Rendah', 'Sedang', 'Tinggi')
        prospek_kerja (float): Prioritas prospek kerja (0-100)
        jurusan_data (dict): Data semua jurusan
        bobot_kriteria (dict): Bobot untuk setiap kriteria
    
    Returns:
        tuple: (hasil_ranking, detail_perhitungan)
            - hasil_ranking: List dictionary berisi ranking jurusan
            - detail_perhitungan: List dictionary berisi detail normalisasi
    """
    hasil = []
    detail = []
    
    # Hitung untuk setiap jurusan
    for kode, data in jurusan_data.items():
        # Hitung masing-masing R (normalisasi)
        r1 = hitung_r1_nilai_akademik(nilai_akademik, data['nilai_standar'])
        r2 = hitung_r2_minat(minat, data['minat'])
        r3 = hitung_r3_ekonomi(ekonomi, data['biaya'])
        r4 = hitung_r4_prospek_kerja(prospek_kerja, data['prospek'])
        
        # Hitung nilai preferensi (V)
        nilai_preferensi = hitung_nilai_preferensi(r1, r2, r3, r4, bobot_kriteria)
        
        # Simpan hasil
        hasil.append({
            'Kode': kode,
            'Jurusan': data['nama'],
            'Nilai SAW': nilai_preferensi
        })
        
        # Simpan detail untuk tabel
        detail.append({
            'Kode': kode,
            'Jurusan': data['nama'],
            'R1': r1,
            'R2': r2,
            'R3': r3,
            'R4': r4,
            'Total': nilai_preferensi
        })
    
    # Sort hasil berdasarkan nilai SAW (descending)
    hasil.sort(key=lambda x: x['Nilai SAW'], reverse=True)
    detail.sort(key=lambda x: x['Total'], reverse=True)
    
    return hasil, detail


def format_hasil(hasil, nama_siswa):
    """
    Format hasil perhitungan menjadi string yang readable
    
    Args:
        hasil (list): List hasil perhitungan SAW
        nama_siswa (str): Nama siswa
    
    Returns:
        str: String berisi hasil terformat
    """
    output = f"\n{'='*60}\n"
    output += f"HASIL REKOMENDASI JURUSAN UNTUK: {nama_siswa}\n"
    output += f"{'='*60}\n\n"
    
    output += "REKOMENDASI TERBAIK:\n"
    output += f"  🏆 {hasil[0]['Jurusan']}\n"
    output += f"     Nilai SAW: {hasil[0]['Nilai SAW']:.4f}\n\n"
    
    output += "RANKING LENGKAP:\n"
    for i, item in enumerate(hasil, 1):
        output += f"  {i}. {item['Jurusan']:<25} | Nilai: {item['Nilai SAW']:.4f}\n"
    
    output += f"\n{'='*60}\n"
    return output


def validasi_input(nilai_akademik, minat, ekonomi, prospek_kerja):
    """
    Validasi input dari user
    
    Args:
        nilai_akademik (float): Nilai akademik (harus 0-100)
        minat (str): Minat (harus 'IPA', 'IPS', atau 'Seni')
        ekonomi (str): Ekonomi (harus 'Rendah', 'Sedang', 'Tinggi')
        prospek_kerja (float): Prospek kerja (harus 0-100)
    
    Returns:
        tuple: (is_valid, error_message)
    """
    errors = []
    
    # Validasi nilai akademik
    if not (0 <= nilai_akademik <= 100):
        errors.append("Nilai akademik harus antara 0-100")
    
    # Validasi minat
    if minat not in ['IPA', 'IPS', 'Seni']:
        errors.append("Minat harus 'IPA', 'IPS', atau 'Seni'")
    
    # Validasi ekonomi
    if ekonomi not in ['Rendah', 'Sedang', 'Tinggi']:
        errors.append("Ekonomi harus 'Rendah', 'Sedang', atau 'Tinggi'")
    
    # Validasi prospek kerja
    if not (0 <= prospek_kerja <= 100):
        errors.append("Prospek kerja harus antara 0-100")
    
    if errors:
        return False, " | ".join(errors)
    
    return True, ""


# ========================================
# TESTING FUNGSI (jika file dijalankan langsung)
# ========================================
if __name__ == "__main__":
    from jurusan_data import JURUSAN_DATA, BOBOT_KRITERIA
    
    print("="*60)
    print("TESTING MODUL SAW CALCULATOR")
    print("="*60)
    
    # Data testing
    test_data = {
        'nilai_akademik': 85,
        'minat': 'IPA',
        'ekonomi': 'Sedang',
        'prospek_kerja': 90
    }
    
    print("\nData Input:")
    for key, value in test_data.items():
        print(f"  - {key}: {value}")
    
    # Validasi
    is_valid, error_msg = validasi_input(
        test_data['nilai_akademik'],
        test_data['minat'],
        test_data['ekonomi'],
        test_data['prospek_kerja']
    )
    
    if not is_valid:
        print(f"\n❌ ERROR: {error_msg}")
    else:
        print("\n✅ Input valid, menghitung...")
        
        # Hitung SAW
        hasil, detail = hitung_saw(
            test_data['nilai_akademik'],
            test_data['minat'],
            test_data['ekonomi'],
            test_data['prospek_kerja'],
            JURUSAN_DATA,
            BOBOT_KRITERIA
        )
        
        # Tampilkan hasil
        print(format_hasil(hasil, "Test User"))
        
        print("\nDetail Perhitungan:")
        print(f"{'Jurusan':<20} | {'R1':>6} | {'R2':>6} | {'R3':>6} | {'R4':>6} | {'Total':>8}")
        print("-" * 70)
        for row in detail:
            print(f"{row['Jurusan']:<20} | {row['R1']:>6.3f} | {row['R2']:>6.3f} | "
                  f"{row['R3']:>6.3f} | {row['R4']:>6.3f} | {row['Total']:>8.4f}")
    
    print("\n" + "="*60)