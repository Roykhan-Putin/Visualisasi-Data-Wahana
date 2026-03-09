import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns

# ==========================================
# 0. KONFIGURASI HALAMAN STREAMLIT
# ==========================================
st.set_page_config(page_title="Dufan Queue Simulator", layout="wide", page_icon="🎢")

st.title("🎢 Dashboard Analisis Simulasi Dufan")
st.markdown("Bandingkan performa simulasi **Dengan Strategi (Hierarchical + PWT)** dan **Tanpa Strategi (Baseline)** secara interaktif.")

# Pengaturan Tema Grafik (Aesthetic)
sns.set_theme(style="whitegrid")
plt.rcParams['font.family'] = 'sans-serif'
color_hier = '#38bdf8'  # Biru (Strategi)
color_base = '#818cf8'  # Ungu (Tanpa Strategi)

# ==========================================
# 1. SIDEBAR: UPLOAD DATA
# ==========================================
st.sidebar.header("📂 1. Upload Data Simulasi (1 Run)")

st.sidebar.markdown("**A. Skenario Dengan Strategi**")
f_p_hier = st.sidebar.file_uploader("Data Pengunjung (Strategi)", type="csv", key="p_h")
f_w_hier = st.sidebar.file_uploader("Data Wahana (Strategi)", type="csv", key="w_h")
f_m_hier = st.sidebar.file_uploader("Data Meta (Strategi)", type="csv", key="m_h")

st.sidebar.markdown("**B. Skenario Tanpa Strategi**")
f_p_base = st.sidebar.file_uploader("Data Pengunjung (Baseline)", type="csv", key="p_b")
f_w_base = st.sidebar.file_uploader("Data Wahana (Baseline)", type="csv", key="w_b")
f_m_base = st.sidebar.file_uploader("Data Meta (Baseline)", type="csv", key="m_b")

st.sidebar.markdown("---")
st.sidebar.header("📈 2. Analisis Sensitivitas (Beragam N)")
st.sidebar.info("Upload BANYAK file 'Data Meta' dari simulasi dengan jumlah N yang berbeda-beda ke dalam kotak di bawah ini.")

f_meta_multi_hier = st.sidebar.file_uploader("Kumpulan Data Meta (Strategi)", type="csv", accept_multiple_files=True, key="mm_h")
f_meta_multi_base = st.sidebar.file_uploader("Kumpulan Data Meta (Baseline)", type="csv", accept_multiple_files=True, key="mm_b")

# ==========================================
# 2. PROSES & VISUALISASI JIKA FILE LENGKAP
# ==========================================
if all([f_p_hier, f_w_hier, f_m_hier, f_p_base, f_w_base, f_m_base]):
    
    with st.spinner('Memproses data dan merender grafik...'):
        # Load Data
        df_p_hier = pd.read_csv(f_p_hier)
        df_w_hier = pd.read_csv(f_w_hier)
        df_m_hier = pd.read_csv(f_m_hier)
        
        df_p_base = pd.read_csv(f_p_base)
        df_w_base = pd.read_csv(f_w_base)
        df_m_base = pd.read_csv(f_m_base)

        # Fungsi Pembantu Plot Wahana
        def create_wahana_plot(col_name, title, ylabel):
            fig, ax = plt.subplots(figsize=(10, 5))
            wahana_names = df_w_hier['Nama Wahana'].values
            x = np.arange(len(wahana_names))
            width = 0.35  

            val_hier = df_w_hier[col_name].values
            val_base = df_w_base[col_name].values

            ax.bar(x - width/2, val_hier, width, label='Hierarchical (Strategi)', color=color_hier)
            ax.bar(x + width/2, val_base, width, label='No Hierarchical (Baseline)', color=color_base)

            ax.set_title(title, fontsize=12, fontweight='bold')
            ax.set_ylabel(ylabel, fontsize=10)
            ax.set_xticks(x)
            ax.set_xticklabels(wahana_names, rotation=45, ha='right', fontsize=8)
            ax.legend()
            plt.tight_layout()
            return fig

        # --- TAMPILAN DASHBOARD ---
        
        st.markdown("---")
        st.subheader("📌 1. Ringkasan Performa (KPI Dashboard)")
        
        kpi_columns = [
            ('Total Pengunjung', 'Jumlah Orang'),
            ('Avg Rides', 'Jumlah Wahana'),
            ('Avg Queue Global (m)', 'Menit'),
            ('Satisfaction Score (%)', 'Persentase (%)'),
            ('Global Rho', 'Skala Util (0.0 - 1.0+)')
        ]

        fig_meta, axes = plt.subplots(2, 3, figsize=(15, 8))
        axes = axes.flatten()

        for i, (col, ylabel) in enumerate(kpi_columns):
            val_h = float(df_m_hier[col].values[0])
            val_b = float(df_m_base[col].values[0])
            
            labels_bar = ['Strategi (Hier)', 'Tanpa Strategi (Base)']
            values_bar = [val_h, val_b]
            
            bars = axes[i].bar(labels_bar, values_bar, color=[color_hier, color_base], width=0.6)
            
            axes[i].set_title(col.upper(), fontsize=12, fontweight='bold')
            axes[i].set_ylabel(ylabel)
            
            for bar, val in zip(bars, values_bar):
                text_val = f'{val:.2f}' if val % 1 != 0 else f'{int(val)}'
                axes[i].text(bar.get_x() + bar.get_width()/2, val, text_val, 
                             ha='center', va='bottom', fontweight='bold', fontsize=11)
        axes[5].axis('off')
        plt.tight_layout()
        st.pyplot(fig_meta)
        plt.close(fig_meta)

        st.markdown("---")
        st.subheader("🎢 2. Analisis Antrean per Wahana")
        col1, col2 = st.columns(2)
        
        with col1:
            fig_q = create_wahana_plot('Avg Antre (m)', 'Rata-Rata Waktu Tunggu per Wahana', 'Waktu (Menit)')
            st.pyplot(fig_q)
            plt.close(fig_q)
            
            fig_tn = create_wahana_plot('Total Pengunjung Naik', 'Total Pengunjung per Wahana', 'Jumlah Orang')
            st.pyplot(fig_tn)
            plt.close(fig_tn)

        with col2:
            fig_rho = create_wahana_plot('rho', 'Utilisasi Wahana (ρ)', 'Persentase Utilisasi (0 - 1.5+)')
            st.pyplot(fig_rho)
            plt.close(fig_rho)
            
            fig_lq = create_wahana_plot('Lq', 'Panjang Antrean Rata-rata (Lq)', 'Jumlah Orang di Antrean')
            st.pyplot(fig_lq)
            plt.close(fig_lq)

        st.markdown("---")
        st.subheader("🚶 3. Perilaku & Pola Kedatangan Pengunjung")
        col3, col4 = st.columns(2)

        with col3:
            bins = [0, 2, 5, 9, 14, 20, 25]
            labels = ['1-2', '3-5', '6-9', '10-14', '15-20', '21+']

            out_hier = pd.cut(df_p_hier['Total Naik'], bins=bins, labels=labels, include_lowest=True).value_counts(sort=False)
            out_base = pd.cut(df_p_base['Total Naik'], bins=bins, labels=labels, include_lowest=True).value_counts(sort=False)

            x = np.arange(len(labels))
            width = 0.35

            fig_dist, ax_dist = plt.subplots(figsize=(8, 5))
            ax_dist.bar(x - width/2, out_hier.values, width, label='Hierarchical', color=color_hier)
            ax_dist.bar(x + width/2, out_base.values, width, label='No Hierarchical', color=color_base)

            ax_dist.set_title('Distribusi Jumlah Wahana yang Dinaiki Pengunjung', fontweight='bold')
            ax_dist.set_ylabel('Jumlah Pengunjung')
            ax_dist.set_xticks(x)
            ax_dist.set_xticklabels(labels)
            ax_dist.legend()
            plt.tight_layout()
            
            st.pyplot(fig_dist)
            plt.close(fig_dist)

        with col4:
            fig_arr, ax_arr = plt.subplots(figsize=(8, 5))
            jam_hier = df_p_hier['Jam Masuk'].str.split(':').str[0].astype(int).value_counts().sort_index()
            jam_base = df_p_base['Jam Masuk'].str.split(':').str[0].astype(int).value_counts().sort_index()

            ax_arr.plot(jam_hier.index, jam_hier.values, marker='o', color=color_hier, linewidth=2, label='Hierarchical')
            ax_arr.plot(jam_base.index, jam_base.values, marker='o', color=color_base, linewidth=2, label='No Hierarchical')
            ax_arr.fill_between(jam_hier.index, jam_hier.values, alpha=0.1, color=color_hier)
            ax_arr.fill_between(jam_base.index, jam_base.values, alpha=0.1, color=color_base)

            ax_arr.set_title('Pola Kedatangan Pengunjung per Jam', fontweight='bold')
            ax_arr.set_xlabel('Jam')
            ax_arr.set_ylabel('Jumlah Kedatangan')
            ax_arr.set_xticks(np.arange(10, 21, 1))
            ax_arr.legend()
            plt.tight_layout()
            
            st.pyplot(fig_arr)
            plt.close(fig_arr)

    st.success('Visualisasi 1 Run berhasil dimuat! Lanjutkan ke bagian Analisis Sensitivitas di bawah jika Anda mengunggah file multi-meta.')

# ==========================================
# 3. ANALISIS SENSITIVITAS (MULTIPLE FILES)
# ==========================================
if f_meta_multi_hier and f_meta_multi_base:
    st.markdown("---")
    st.subheader("📈 4. Analisis Sensitivitas Kapasitas Pengunjung (N)")
    
    with st.spinner('Membangun Kurva Sensitivitas...'):
        # Fungsi untuk menggabungkan file multi menjadi 1 dataframe
        def combine_meta_files(uploaded_files):
            df_list = []
            for file in uploaded_files:
                df = pd.read_csv(file)
                df_list.append(df)
            combined_df = pd.concat(df_list, ignore_index=True)
            # Sortir berdasarkan kolom N (Total Pengunjung) dari terkecil ke terbesar
            combined_df = combined_df.sort_values(by='Total Pengunjung').reset_index(drop=True)
            return combined_df
            
        df_multi_h = combine_meta_files(f_meta_multi_hier)
        df_multi_b = combine_meta_files(f_meta_multi_base)

        # Fungsi Pembantu Plot Line Sensitivitas
        def create_sensitivity_plot(col_name, title, ylabel):
            fig, ax = plt.subplots(figsize=(8, 5))
            
            ax.plot(df_multi_h['Total Pengunjung'], df_multi_h[col_name], 
                    marker='o', color=color_hier, linewidth=2.5, label='Strategi (Hierarchical)')
            ax.plot(df_multi_b['Total Pengunjung'], df_multi_b[col_name], 
                    marker='o', color=color_base, linewidth=2.5, linestyle='--', label='Baseline (Tanpa Strategi)')
            
            ax.set_title(title, fontsize=12, fontweight='bold')
            ax.set_xlabel('Total Pengunjung (N)', fontsize=10)
            ax.set_ylabel(ylabel, fontsize=10)
            ax.legend()
            ax.grid(True, linestyle=':', alpha=0.6)
            plt.tight_layout()
            return fig

        # Membuat 4 Plot sesuai request
        col5, col6 = st.columns(2)
        
        with col5:
            # Grafik 1: Waktu Tunggu vs N
            fig_q_sens = create_sensitivity_plot('Avg Queue Global (m)', 'Trade-off: Waktu Tunggu vs Kapasitas Pengunjung', 'Global Avg Queue (Menit)')
            st.pyplot(fig_q_sens)
            plt.close(fig_q_sens)
            
            # Grafik 2: Global Rho vs N
            fig_rho_sens = create_sensitivity_plot('Global Rho', 'Beban Mesin Wahana (Utilisasi) vs Kapasitas Pengunjung', 'Global Rho (ρ)')
            st.pyplot(fig_rho_sens)
            plt.close(fig_rho_sens)

        with col6:
            # Grafik 3: Rata-rata Wahana vs N
            fig_rides_sens = create_sensitivity_plot('Avg Rides', 'Kemampuan Jelajah Wahana vs Kapasitas Pengunjung', 'Rata-rata Wahana per Orang')
            st.pyplot(fig_rides_sens)
            plt.close(fig_rides_sens)
            
            # Grafik 4: Satisfaction vs N
            fig_sat_sens = create_sensitivity_plot('Satisfaction Score (%)', 'Tingkat Kepuasan vs Kapasitas Pengunjung', 'Satisfaction Score (%)')
            st.pyplot(fig_sat_sens)
            plt.close(fig_sat_sens)

elif (f_meta_multi_hier and not f_meta_multi_base) or (f_meta_multi_base and not f_meta_multi_hier):
    st.warning("⚠️ Untuk menampilkan Analisis Sensitivitas, harap upload Kumpulan Data Meta untuk KEDUA Skenario (Strategi & Baseline) di sidebar.")

elif not all([f_p_hier, f_w_hier, f_m_hier, f_p_base, f_w_base, f_m_base]):
    # Tampilan awal jika belum ada file yang diupload sama sekali
    st.info("👈 Silakan upload file CSV di panel sebelah kiri untuk mulai melihat visualisasi.")
    
    st.image("https://www.ancol.com/shared/images/logo-dufan.png", width=200)
    st.markdown("*Aplikasi ini memproses log Agent-Based Simulation tanpa mengirimkan data ke server eksternal.*")