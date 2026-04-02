# Proyek Akhir: Menyelesaikan Permasalahan Institusi Pendidikan Jaya Jaya Institut

## Business Understanding

Jaya Jaya Institut adalah sebuah institusi pendidikan tinggi yang telah berdiri sejak tahun 2000 dan telah mencetak banyak lulusan berkualitas. Meskipun memiliki reputasi yang baik, institusi ini menghadapi tantangan serius terkait tingginya angka *dropout* (putus studi) di kalangan mahasiswanya. Tingginya angka dropout tidak hanya berdampak pada reputasi institusi, tetapi juga pada efisiensi operasional dan pendapatan institusi secara keseluruhan.

Untuk mengatasi permasalahan ini, Jaya Jaya Institut ingin memanfaatkan pendekatan berbasis data (*data-driven*) guna mengidentifikasi mahasiswa yang berpotensi dropout sedini mungkin, sehingga pihak institusi dapat memberikan bimbingan dan intervensi yang tepat sebelum mahasiswa tersebut benar-benar meninggalkan studi mereka.

### Permasalahan Bisnis

Berdasarkan konteks di atas, berikut adalah permasalahan bisnis yang akan diselesaikan:

1. **Tingginya angka dropout mahasiswa** — Institusi belum memiliki sistem yang dapat mendeteksi mahasiswa berisiko tinggi dropout secara dini dan otomatis.
2. **Kurangnya visibilitas data performa mahasiswa** — Manajemen kesulitan memantau tren dan pola performa mahasiswa secara menyeluruh dan real-time.
3. **Tidak adanya alat prediksi yang dapat digunakan staf** — Konselor dan staf akademik tidak memiliki tools yang mudah digunakan untuk memprediksi status akhir seorang mahasiswa (dropout atau graduate).

### Cakupan Proyek

Proyek ini mencakup tahapan-tahapan berikut:

1. **Business Understanding** — Memahami konteks bisnis dan merumuskan permasalahan.
2. **Data Understanding** — Eksplorasi dan pemahaman dataset mahasiswa Jaya Jaya Institut.
3. **Data Preparation** — Pembersihan data, encoding, dan feature engineering.
4. **Modeling** — Membangun model klasifikasi Machine Learning (Random Forest) untuk memprediksi status mahasiswa.
5. **Evaluation** — Mengevaluasi performa model menggunakan metrik yang relevan.
6. **Deployment** — Membuat prototype berbasis Streamlit dan dashboard monitoring menggunakan Metabase.

### Persiapan

**Sumber data:**
Dataset yang digunakan bersumber dari repositori GitHub Dicoding Academy yang mencakup data demografis, akademik, dan sosial-ekonomi mahasiswa.

Dataset dapat diakses di: [Students Performance Dataset](https://raw.githubusercontent.com/dicodingacademy/dicoding_dataset/main/students_performance/data.csv)

Setup environment:

```
pip install -r requirements.txt
```

Atau dapat menggunakan virtual environment bawaan Python (venv):

```
python -m venv dropout-env
dropout-env\Scripts\activate
pip install -r requirements.txt
```

## Business Dashboard

Dashboard monitoring dibuat menggunakan **Metabase** yang dihubungkan dengan database SQLite hasil ekspor dari proses analisis data. Dashboard ini dirancang untuk membantu manajemen Jaya Jaya Institut dalam:

- Memantau **distribusi status mahasiswa** (Dropout, Enrolled, Graduate) secara keseluruhan.
- Menganalisis **faktor-faktor utama** yang berkontribusi terhadap dropout (nilai semester, status beasiswa, utang biaya kuliah, dsb.).
- Memonitor **tren performa akademik** mahasiswa per semester.
- Membandingkan performa berdasarkan **jurusan, jenis kelamin, dan status keuangan**.

**Cara mengakses dashboard Metabase (lokal):**

```bash
# Jalankan Metabase via Docker
docker run -d -p 3000:3000 \
  -v $(pwd)/metabase-data:/metabase-data \
  --name metabase metabase/metabase

# Akses di browser: http://localhost:3000
```

| Kredensial | Detail |
|---|---|
| Email | `root@mail.com` |
| Password | `root123` |

> File database Metabase telah diekspor dan tersedia di repository: `metabase.db.mv.db`
>
> Untuk mengimpor, salin file tersebut ke dalam container:
> ```bash
> docker cp metabase.db.mv.db metabase:/metabase.db/metabase.db.mv.db
> ```

---

## Menjalankan Sistem Machine Learning

Prototype sistem Machine Learning dibuat menggunakan **Streamlit** dan dapat dijalankan secara lokal maupun diakses secara online melalui Streamlit Community Cloud.

**Cara menjalankan secara lokal:**

```bash
# Pastikan sudah berada di direktori project dan virtual environment aktif
streamlit run app.py
```

**Akses prototype online:**

> 🔗 **[https://student-dropout-prediction-m7mut4z7t5qgqpwjpgxszq.streamlit.app/](https://student-dropout-prediction-m7mut4z7t5qgqpwjpgxszq.streamlit.app/)**

**Fitur prototype:**
- Input data mahasiswa secara manual melalui form interaktif.
- Prediksi status mahasiswa: **Dropout** atau **Graduate**.
- Menampilkan probabilitas prediksi untuk setiap kelas.
- Menampilkan faktor-faktor paling berpengaruh terhadap prediksi (*feature importance*).

---

## Conclusion

Berdasarkan hasil analisis data dan pemodelan Machine Learning yang telah dilakukan, diperoleh beberapa kesimpulan utama:

1. **Model Random Forest** berhasil memprediksi status mahasiswa (Dropout, Enrolled, Graduate) dengan akurasi yang baik (90.63%), menggunakan fitur akademik semester 1 dan 2 sebagai prediktor terkuat.

2. **Faktor-faktor paling berpengaruh** terhadap risiko dropout mahasiswa adalah:
   - Jumlah mata kuliah yang **disetujui (approved)** di semester 1 dan 2.
   - **Nilai rata-rata** di semester 1 dan 2.
   - Status **pembayaran biaya kuliah** (apakah tepat waktu atau tidak).
   - Status **pemegang beasiswa**.
   - **Usia saat pendaftaran**.

3. Mahasiswa yang **tidak membayar biaya kuliah tepat waktu**, **tidak memiliki beasiswa**, dan memiliki **performa akademik rendah** di semester pertama memiliki risiko dropout tertinggi.

4. Intervensi dini pada semester pertama terbukti krusial — performa mahasiswa di semester awal sangat menentukan status akhir mereka.

### Rekomendasi Action Items

Berdasarkan hasil analisis, berikut adalah rekomendasi tindakan yang dapat dilakukan:

- **Action Item 1 — Sistem Early Warning Otomatis:** Implementasikan prototype machine learning yang telah dibuat ke dalam sistem informasi akademik, sehingga staf konselor mendapatkan notifikasi otomatis ketika seorang mahasiswa teridentifikasi berisiko tinggi dropout.

- **Action Item 2 — Program Intervensi Semester Pertama:** Fokuskan program bimbingan akademik intensif pada mahasiswa semester 1 yang menunjukkan performa rendah (nilai di bawah rata-rata dan jumlah mata kuliah yang disetujui rendah).

- **Action Item 3 — Kebijakan Fleksibilitas Pembayaran:** Buat program cicilan atau keringanan biaya kuliah yang lebih fleksibel untuk mahasiswa dengan kesulitan finansial, mengingat status pembayaran biaya kuliah adalah salah satu faktor prediksi dropout terkuat.

- **Action Item 4 — Perluasan Program Beasiswa:** Tingkatkan cakupan program beasiswa, karena mahasiswa pemegang beasiswa terbukti memiliki tingkat dropout yang jauh lebih rendah.

- **Action Item 5 — Dashboard Monitoring Berkala:** Gunakan dashboard Metabase yang telah dibuat untuk melakukan review performa mahasiswa secara berkala (minimal per akhir semester), sehingga tren dropout dapat dideteksi lebih awal.
