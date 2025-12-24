"""
Data Master Jurusan dan Bobot Kriteria
File ini berisi semua data statis yang digunakan dalam aplikasi SPK
"""

# ========================================
# DATA JURUSAN (ALTERNATIF)
# ========================================
JURUSAN_DATA = {
    'A1': {
        'nama': 'Teknik Informatika',
        'nilai_standar': 85,      # Nilai akademik minimal ideal
        'minat': 'IPA',           # Minat yang paling cocok
        'biaya': 'Tinggi',        # Kategori biaya kuliah
        'prospek': 95             # Prospek kerja (0-100)
    },
    'A2': {
        'nama': 'Manajemen',
        'nilai_standar': 75,
        'minat': 'IPS',
        'biaya': 'Sedang',
        'prospek': 80
    },
    'A3': {
        'nama': 'Akuntansi',
        'nilai_standar': 78,
        'minat': 'IPS',
        'biaya': 'Sedang',
        'prospek': 85
    },
    'A4': {
        'nama': 'Teknik Sipil',
        'nilai_standar': 80,
        'minat': 'IPA',
        'biaya': 'Tinggi',
        'prospek': 82
    },
    'A5': {
        'nama': 'Psikologi',
        'nilai_standar': 76,
        'minat': 'Seni',
        'biaya': 'Sedang',
        'prospek': 78
    }
}

# ========================================
# BOBOT KRITERIA
# ========================================
# Total harus = 1.0 (100%)
BOBOT_KRITERIA = {
    'nilai_akademik': 0.30,   # 30%
    'minat': 0.35,            # 35%
    'ekonomi': 0.20,          # 20%
    'prospek_kerja': 0.15     # 15%
}

# ========================================
# MAPPING NILAI EKONOMI
# ========================================
# Mapping kemampuan ekonomi siswa ke nilai numerik
# Nilai lebih tinggi = kemampuan lebih baik
EKONOMI_SISWA_MAP = {
    'Rendah': 100,   # Butuh biaya rendah
    'Sedang': 70,    # Biaya sedang OK
    'Tinggi': 40     # Bisa bayar biaya tinggi
}

# ========================================
# MAPPING BIAYA JURUSAN
# ========================================
# Mapping kategori biaya jurusan ke nilai numerik
# Nilai lebih tinggi = biaya lebih mahal
BIAYA_JURUSAN_MAP = {
    'Rendah': 40,
    'Sedang': 70,
    'Tinggi': 100
}

# ========================================
# VALIDASI DATA
# ========================================
def validasi_bobot():
    """
    Fungsi untuk memvalidasi total bobot kriteria
    Total bobot harus = 1.0 (100%)
    """
    total = sum(BOBOT_KRITERIA.values())
    if abs(total - 1.0) > 0.001:  # Toleransi error floating point
        raise ValueError(f"Total bobot kriteria harus 1.0, saat ini: {total}")
    return True

def get_info_jurusan(kode_jurusan):
    """
    Mendapatkan informasi lengkap suatu jurusan berdasarkan kode
    
    Args:
        kode_jurusan (str): Kode jurusan (contoh: 'A1')
    
    Returns:
        dict: Informasi lengkap jurusan atau None jika tidak ditemukan
    """
    return JURUSAN_DATA.get(kode_jurusan, None)

def get_semua_nama_jurusan():
    """
    Mendapatkan list semua nama jurusan yang tersedia
    
    Returns:
        list: List nama jurusan
    """
    return [data['nama'] for data in JURUSAN_DATA.values()]

# ========================================
# INFORMASI KRITERIA
# ========================================
KETERANGAN_KRITERIA = {
    'nilai_akademik': {
        'nama': 'Nilai Akademik',
        'deskripsi': 'Rata-rata nilai rapor atau ijazah siswa',
        'tipe': 'benefit',  # Semakin tinggi semakin baik
        'satuan': 'poin (0-100)'
    },
    'minat': {
        'nama': 'Minat Bidang Studi',
        'deskripsi': 'Kesesuaian minat siswa dengan bidang jurusan',
        'tipe': 'benefit',
        'pilihan': ['IPA', 'IPS', 'Seni']
    },
    'ekonomi': {
        'nama': 'Kemampuan Ekonomi',
        'deskripsi': 'Kemampuan keluarga dalam membiayai kuliah',
        'tipe': 'cost',  # Semakin rendah biaya semakin baik
        'pilihan': ['Rendah', 'Sedang', 'Tinggi']
    },
    'prospek_kerja': {
        'nama': 'Prospek Kerja',
        'deskripsi': 'Seberapa penting prospek kerja dalam memilih jurusan',
        'tipe': 'benefit',
        'satuan': 'poin (0-100)'
    }
}

# ========================================
# CONTOH DATA TESTING
# ========================================
CONTOH_DATA_SISWA = [
    {
        'nama': 'Ahmad Rizki',
        'nilai_akademik': 85,
        'minat': 'IPA',
        'ekonomi': 'Sedang',
        'prospek_kerja': 90
    },
    {
        'nama': 'Siti Nurhaliza',
        'nilai_akademik': 78,
        'minat': 'IPS',
        'ekonomi': 'Rendah',
        'prospek_kerja': 85
    },
    {
        'nama': 'Budi Santoso',
        'nilai_akademik': 82,
        'minat': 'IPA',
        'ekonomi': 'Tinggi',
        'prospek_kerja': 75
    }
]

# Validasi saat import
if __name__ != "__main__":
    try:
        validasi_bobot()
    except ValueError as e:
        print(f"ERROR: {e}")