import streamlit as st
import pandas as pd
import numpy as np
import joblib
import os

# ─── PAGE CONFIG ─────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Jaya Jaya Institut — Student Dropout Predictor",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ─── LOAD MODEL ──────────────────────────────────────────────────────────────
@st.cache_resource
def load_model():
    pipeline    = joblib.load('model/random_forest_pipeline.joblib')
    le_target   = joblib.load('model/label_encoder.joblib')
    feature_names = joblib.load('model/feature_names.joblib')
    return pipeline, le_target, feature_names

try:
    pipeline, le_target, FEATURES = load_model()
    model_loaded = True
except Exception as e:
    model_loaded = False
    st.error(f"⚠️ Model belum tersedia. Jalankan notebook terlebih dahulu untuk melatih model.\n\nError: {e}")

# ─── STYLE ───────────────────────────────────────────────────────────────────
st.markdown("""
<style>
    .main-title {
        font-size: 2.2rem; font-weight: 800;
        background: linear-gradient(90deg, #1a237e, #0288d1);
        -webkit-background-clip: text; -webkit-text-fill-color: transparent;
    }
    .predict-box {
        padding: 1.5rem; border-radius: 12px;
        border: 2px solid #e0e0e0; margin-top: 1rem;
    }
    .dropout-box   { background: #fdecea; border-color: #e53935; }
    .enrolled-box  { background: #e3f2fd; border-color: #1e88e5; }
    .graduate-box  { background: #e8f5e9; border-color: #43a047; }
    .metric-card {
        background: #f8f9fa; border-radius: 10px;
        padding: 1rem; text-align: center;
    }
</style>
""", unsafe_allow_html=True)

# ─── HEADER ──────────────────────────────────────────────────────────────────
st.markdown('<p class="main-title">🎓 Jaya Jaya Institut</p>', unsafe_allow_html=True)
st.markdown("### Student Dropout Early Warning System")
st.markdown("Masukkan data mahasiswa untuk memprediksi kemungkinan status akhir mereka: **Dropout**, **Enrolled**, atau **Graduate**.")
st.divider()

# ─── SIDEBAR ─────────────────────────────────────────────────────────────────
with st.sidebar:
    st.image("https://img.icons8.com/color/96/000000/university.png", width=80)
    st.title("Panduan Penggunaan")
    st.info("""
    1. Isi data akademik dan demografi mahasiswa di form utama.
    2. Klik tombol **🔍 Prediksi Status** untuk mendapatkan hasil.
    3. Sistem akan menampilkan prediksi beserta probabilitas untuk setiap kelas.
    """)
    st.divider()
    st.markdown("**Model:** Random Forest Classifier")
    st.markdown("**Kelas Target:** Dropout | Enrolled | Graduate")
    st.caption("Jaya Jaya Institut © 2024")

# ─── FORM INPUT ──────────────────────────────────────────────────────────────
if model_loaded:
    with st.form("input_form"):
        st.subheader("📋 Data Akademik Mahasiswa")

        col1, col2, col3 = st.columns(3)

        with col1:
            st.markdown("**Informasi Pribadi**")
            gender = st.selectbox("Jenis Kelamin", options=[1, 0], format_func=lambda x: "Laki-laki" if x == 1 else "Perempuan")
            age = st.number_input("Usia Saat Pendaftaran", min_value=17, max_value=60, value=20)
            marital_status = st.selectbox("Status Pernikahan", options=[1,2,3,4,5,6],
                format_func=lambda x: {1:"Single",2:"Menikah",3:"Janda/Duda",4:"Cerai",5:"Kumpul Kebo",6:"Pisah Hukum"}[x])
            nationality = st.selectbox("Kewarganegaraan", options=[1, 41, 6, 2, 14],
                format_func=lambda x: {1:"Portugis",41:"Brasil",6:"Spanyol",2:"Jerman",14:"Inggris"}[x])
            international = st.selectbox("Mahasiswa Internasional", options=[0, 1], format_func=lambda x: "Ya" if x == 1 else "Tidak")

        with col2:
            st.markdown("**Informasi Akademik**")
            application_mode = st.selectbox("Mode Aplikasi", options=[1,17,18,39,42,43], format_func=lambda x: {
                1:"1st phase - general",17:"2nd phase",18:"3rd phase",
                39:"Over 23 tahun",42:"Transfer",43:"Ganti jurusan"}[x])
            application_order = st.slider("Urutan Pilihan (0=pilihan 1)", 0, 9, 0)
            course = st.selectbox("Program Studi", options=[9147, 9119, 9500, 9085, 9254, 9670, 9853],
                format_func=lambda x: {9147:"Manajemen",9119:"Informatika",9500:"Keperawatan",
                    9085:"Keperawatan Hewan",9254:"Pariwisata",9670:"Advertising & Marketing",9853:"Pendidikan Dasar"}[x])
            attendance = st.selectbox("Jadwal Perkuliahan", options=[1, 0], format_func=lambda x: "Siang" if x == 1 else "Malam")
            prev_qualification = st.selectbox("Kualifikasi Sebelumnya", options=[1, 2, 3, 6, 9],
                format_func=lambda x: {1:"SMA/Sederajat",2:"D3",3:"S1",6:"Sedang kuliah",9:"SMA Tidak Lulus"}[x])
            prev_grade = st.slider("Nilai Kualifikasi Sebelumnya (0-200)", 0, 200, 130)
            admission_grade = st.slider("Nilai Masuk (0-200)", 0, 200, 130)

        with col3:
            st.markdown("**Status Keuangan & Sosial**")
            displaced = st.selectbox("Mahasiswa Pindahan", options=[0, 1], format_func=lambda x: "Ya" if x == 1 else "Tidak")
            special_needs = st.selectbox("Kebutuhan Khusus", options=[0, 1], format_func=lambda x: "Ya" if x == 1 else "Tidak")
            debtor = st.selectbox("Memiliki Hutang", options=[0, 1], format_func=lambda x: "Ya" if x == 1 else "Tidak")
            tuition_uptodate = st.selectbox("Biaya Kuliah Tepat Waktu", options=[1, 0], format_func=lambda x: "Ya" if x == 1 else "Tidak")
            scholarship = st.selectbox("Pemegang Beasiswa", options=[0, 1], format_func=lambda x: "Ya" if x == 1 else "Tidak")

        st.divider()
        st.subheader("📊 Performa Akademik")

        col4, col5 = st.columns(2)
        with col4:
            st.markdown("**Semester 1**")
            cu1_credited   = st.number_input("Mata Kuliah Dikreditkan (Sem 1)", 0, 20, 0)
            cu1_enrolled   = st.number_input("Mata Kuliah Diambil (Sem 1)", 0, 20, 6)
            cu1_evaluations= st.number_input("Jumlah Evaluasi (Sem 1)", 0, 45, 8)
            cu1_approved   = st.number_input("Mata Kuliah Lulus (Sem 1)", 0, 20, 5)
            cu1_grade      = st.slider("Nilai Rata-rata Semester 1 (0-20)", 0.0, 20.0, 12.0, 0.5)
            cu1_no_eval    = st.number_input("Tanpa Evaluasi (Sem 1)", 0, 20, 0)

        with col5:
            st.markdown("**Semester 2**")
            cu2_credited   = st.number_input("Mata Kuliah Dikreditkan (Sem 2)", 0, 20, 0)
            cu2_enrolled   = st.number_input("Mata Kuliah Diambil (Sem 2)", 0, 20, 6)
            cu2_evaluations= st.number_input("Jumlah Evaluasi (Sem 2)", 0, 45, 8)
            cu2_approved   = st.number_input("Mata Kuliah Lulus (Sem 2)", 0, 20, 5)
            cu2_grade      = st.slider("Nilai Rata-rata Semester 2 (0-20)", 0.0, 20.0, 12.0, 0.5)
            cu2_no_eval    = st.number_input("Tanpa Evaluasi (Sem 2)", 0, 20, 0)

        st.divider()
        st.subheader("🌍 Kondisi Makroekonomi")
        col6, col7, col8 = st.columns(3)
        with col6: unemployment = st.number_input("Tingkat Pengangguran (%)", 0.0, 25.0, 10.8, 0.1)
        with col7: inflation    = st.number_input("Tingkat Inflasi (%)", -5.0, 15.0, 1.4, 0.1)
        with col8: gdp          = st.number_input("GDP", -5.0, 5.0, 1.74, 0.01)

        # Untuk fitur orang tua (pakai nilai default umum)
        mother_qual = 19; father_qual = 19
        mother_occ  = 9;  father_occ  = 9

        submitted = st.form_submit_button("🔍 Prediksi Status Mahasiswa", use_container_width=True, type="primary")

    # ─── PREDIKSI ────────────────────────────────────────────────────────────
    if submitted:
        input_data = {
            'Marital_status': marital_status,
            'Application_mode': application_mode,
            'Application_order': application_order,
            'Course': course,
            'Daytime_evening_attendance': attendance,
            'Previous_qualification': prev_qualification,
            'Previous_qualification_grade': prev_grade,
            'Nacionality': nationality,
            'Mothers_qualification': mother_qual,
            'Fathers_qualification': father_qual,
            'Mothers_occupation': mother_occ,
            'Fathers_occupation': father_occ,
            'Admission_grade': admission_grade,
            'Displaced': displaced,
            'Educational_special_needs': special_needs,
            'Debtor': debtor,
            'Tuition_fees_up_to_date': tuition_uptodate,
            'Gender': gender,
            'Scholarship_holder': scholarship,
            'Age_at_enrollment': age,
            'International': international,
            'Curricular_units_1st_sem_credited': cu1_credited,
            'Curricular_units_1st_sem_enrolled': cu1_enrolled,
            'Curricular_units_1st_sem_evaluations': cu1_evaluations,
            'Curricular_units_1st_sem_approved': cu1_approved,
            'Curricular_units_1st_sem_grade': cu1_grade,
            'Curricular_units_1st_sem_without_evaluations': cu1_no_eval,
            'Curricular_units_2nd_sem_credited': cu2_credited,
            'Curricular_units_2nd_sem_enrolled': cu2_enrolled,
            'Curricular_units_2nd_sem_evaluations': cu2_evaluations,
            'Curricular_units_2nd_sem_approved': cu2_approved,
            'Curricular_units_2nd_sem_grade': cu2_grade,
            'Curricular_units_2nd_sem_without_evaluations': cu2_no_eval,
            'Unemployment_rate': unemployment,
            'Inflation_rate': inflation,
            'GDP': gdp,
        }

        df_input = pd.DataFrame([input_data])

        # Pastikan urutan fitur sesuai model
        for f in FEATURES:
            if f not in df_input.columns:
                df_input[f] = 0
        df_input = df_input[FEATURES]

        pred_class = pipeline.predict(df_input)[0]
        pred_proba = pipeline.predict_proba(df_input)[0]
        pred_label = le_target.inverse_transform([pred_class])[0]

        st.divider()
        st.subheader("📈 Hasil Prediksi")

        # Tampilkan hasil utama
        css_class = {"Dropout": "dropout-box", "Enrolled": "enrolled-box", "Graduate": "graduate-box"}
        icon = {"Dropout": "🚨", "Enrolled": "📚", "Graduate": "🎓"}

        st.markdown(f"""
        <div class="predict-box {css_class[pred_label]}">
            <h2 style="margin:0">{icon[pred_label]} Prediksi: <strong>{pred_label}</strong></h2>
            <p style="margin:0.5rem 0 0 0; font-size:1rem;">
                Berdasarkan data yang dimasukkan, mahasiswa ini diprediksi akan <strong>{pred_label}</strong>.
            </p>
        </div>
        """, unsafe_allow_html=True)

        st.write("Input Data:")
        st.write(df_input)

        st.write("Prediction Probabilities:")
        st.write(pred_proba)

        # Tampilkan probabilitas
        st.markdown("#### Probabilitas Per Kelas")
        prob_cols = st.columns(len(le_target.classes_))
        icons_map = {"Dropout": "🚨", "Enrolled": "📚", "Graduate": "🎓"}
        colors_map = {"Dropout": "#e53935", "Enrolled": "#1e88e5", "Graduate": "#43a047"}

        for col_ui, (cls, prob) in zip(prob_cols, zip(le_target.classes_, pred_proba)):
            with col_ui:
                st.metric(
                    label=f"{icons_map[cls]} {cls}",
                    value=f"{prob*100:.1f}%"
                )
                st.progress(float(prob))

        # Rekomendasi
        st.markdown("#### 💡 Rekomendasi Tindakan")
        if pred_label == "Dropout":
            st.error("""
            **⚠️ Mahasiswa ini berisiko tinggi dropout!** Tindakan yang disarankan:
            - Segera jadwalkan sesi konseling akademik
            - Evaluasi kondisi finansial dan tawarkan program cicilan/beasiswa
            - Pantau kehadiran dan performa di semester berikutnya secara intensif
            """)
        elif pred_label == "Enrolled":
            st.warning("""
            **📌 Mahasiswa masih dalam proses studi.** Tindakan yang disarankan:
            - Berikan motivasi dan dukungan akademik rutin
            - Pastikan mahasiswa memiliki akses ke sumber daya belajar yang memadai
            - Monitor tren nilai semester demi semester
            """)
        else:
            st.success("""
            **✅ Mahasiswa diprediksi akan lulus!** Tindakan yang disarankan:
            - Pastikan mahasiswa tetap terlibat dalam kegiatan akademik
            - Pertimbangkan program mentoring atau magang untuk mempersiapkan karir
            """)
