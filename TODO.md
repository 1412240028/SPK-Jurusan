# TODO: Testing Plan for SPK Jurusan Application

This TODO list outlines the testing plan for the SPK (Sistem Pendukung Keputusan) application using the SAW method, based on the SETUP_GUIDE.txt.

## Prerequisites
- [x] Ensure Python 3.8+ is installed
- [x] Install dependencies: `pip install -r requirements.txt`
- [x] Verify installations: streamlit, pandas, matplotlib
- [x] Run the application: `streamlit run app.py`
- [x] Application accessible at http://localhost:8501

## Test Cases
### Test Case 1: Ahmad Rizki
- [x] Input: Nama: Ahmad Rizki, Nilai Akademik: 85, Minat: IPA, Ekonomi: Sedang, Prospek Kerja: 90
- [x] Expected: Rekomendasi: Teknik Informatika, Nilai SAW: 0.92-0.93
- [x] Verify recommendation appears correctly

### Test Case 2: Siti Nurhaliza
- [ ] Input: Nama: Siti Nurhaliza, Nilai Akademik: 78, Minat: IPS, Ekonomi: Rendah, Prospek Kerja: 85
- [ ] Expected: Rekomendasi: Manajemen atau Akuntansi, Nilai SAW: 0.85-0.90
- [ ] Verify recommendation appears correctly

### Test Case 3: Budi Santoso
- [ ] Input: Nama: Budi Santoso, Nilai Akademik: 82, Minat: IPA, Ekonomi: Tinggi, Prospek Kerja: 75
- [ ] Expected: Rekomendasi: Teknik Informatika atau Teknik Sipil, Nilai SAW: 0.88-0.92
- [ ] Verify recommendation appears correctly

## Functional Testing Checklist
- [x] Form input functions properly (all fields accept input)
- [x] "Hitung Rekomendasi" button functions
- [x] Recommendation results display correctly
- [x] Ranking table displays completely
- [x] Bar chart graph appears
- [x] Calculation details can be opened
- [x] Download CSV button functions
- [x] No errors in console

## Additional Testing
- [ ] Test with invalid inputs (e.g., nilai > 100, empty fields)
- [ ] Test on different browsers
- [ ] Test responsiveness (if applicable)
- [ ] Verify SAW calculations manually for accuracy

## Pre-Presentation Checklist
- [ ] All files created
- [ ] Dependencies installed
- [ ] Application runs without errors
- [ ] Testing with 3 example data successful
- [ ] Screenshots of results for documentation
- [ ] Understand SAW algorithm
- [ ] Able to explain each criteria & weight
- [ ] Able to demo all features
- [ ] README.md complete
- [ ] Code backed up to USB/cloud

## Notes
- Run tests in order listed
- Document any failures and resolutions
- Update this TODO as tests are completed
