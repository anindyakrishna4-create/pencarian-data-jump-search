# File: app.py (Aplikasi Streamlit dengan Matplotlib)

import streamlit as st
import pandas as pd
import time
from jump_search import jump_search 
import matplotlib.pyplot as plt
import numpy as np
import math

# --- Konfigurasi Halaman ---
st.set_page_config(
    page_title="Virtual Lab: Jump Search",
    layout="wide"
)

st.title("🦘 Virtual Lab: Jump Search Interaktif (Matplotlib)")
st.markdown("### Visualisasi Algoritma Pencarian Blok ($O(\sqrt{n})$)")

st.sidebar.header("Konfigurasi Data dan Target")

# --- Input Data (Tanpa Batas Input) ---
default_data = "1, 5, 8, 10, 15, 22, 34, 45, 50, 60, 75, 88, 90, 95, 100, 110"
input_data_str = st.sidebar.text_input(
    "Masukkan data terurut (pisahkan dengan koma):", 
    default_data
)
target_value_str = st.sidebar.text_input("Masukkan Nilai Target yang Dicari:", "60")
speed = st.sidebar.slider("Kecepatan Simulasi (detik)", 0.1, 2.0, 0.5)

# --- Proses Data Input ---
try:
    data_list = [int(x.strip()) for x in input_data_str.split(',') if x.strip()]
    if not data_list:
        st.error("Masukkan setidaknya satu angka untuk array.")
        st.stop()
    target_value = int(target_value_str.strip())
    # Prasyarat: Array harus terurut
    initial_data_sorted = sorted(list(data_list))
except ValueError:
    st.error("Pastikan semua input data dan target adalah angka (integer) yang dipisahkan oleh koma.")
    st.stop()

# --- Penjelasan Pewarnaan ---
st.markdown("""
#### Pewarnaan Bar:
* **Hijau:** Indeks **Saat Ini (curr)** yang sedang diperiksa (saat lompatan atau linear search).
* **Kuning:** Batas **Blok yang Dipilih** (antara `prev` dan `curr` blok lompatan).
* **Merah:** Blok array yang sudah **dilewati** atau **dibuang**.
* **Ungu:** Indeks di mana nilai **ditemukan**.
""")

st.write(f"**Array Terurut (Prasyarat):** {initial_data_sorted}")
st.write(f"**Nilai Target:** **{target_value}**")
st.write(f"**Ukuran Lompatan (m):** **{int(math.sqrt(len(initial_data_sorted)))}**")


# --- Fungsi Plot Matplotlib ---
def plot_array(arr, target, prev, curr, found_index, max_val, status):
    fig, ax = plt.subplots(figsize=(12, 4))
    n = len(arr)
    x_pos = np.arange(n)
    
    # Inisialisasi warna: Merah (#CC0000 - Dibuang)
    colors = ['#CC0000'] * n 
    
    # 1. Kuning (#F1C232): Blok Aktif
    if prev != -1:
        # Tentukan batas atas pencarian linear
        block_end = min(prev + int(math.sqrt(n)), n) 
        
        # Warnai blok yang sedang diperiksa/dilompati
        for i in range(prev, block_end):
             colors[i] = '#F1C232'
    
    # 2. Hijau (#6AA84F): Posisi Current (curr)
    if curr != -1 and curr < n:
        colors[curr] = '#6AA84F'

    # 3. Ungu (#8E44AD): Ditemukan
    if found_index != -1:
        colors[found_index] = '#8E44AD'
        
    # Membuat Bar Plot
    ax.bar(x_pos, arr, color=colors)
    
    # Menambahkan Label Angka di Atas Bar
    for i, height in enumerate(arr):
        ax.text(x_pos[i], height + max_val * 0.02, str(height), ha='center', va='bottom', fontsize=10)
        
    # Menambahkan label prev dan curr jika relevan
    if status not in ('Selesai', 'Mulai'):
        if prev != -1 and prev < n and prev != curr:
            ax.text(prev, max_val * 1.05, f'PREV ({prev})', color='darkblue', ha='center', fontsize=10, weight='bold')
        if curr != -1 and curr < n:
             # Pindahkan label curr sedikit ke bawah agar tidak bertabrakan dengan prev
             y_pos_curr = max_val * 0.95 if prev != curr else max_val * 1.05
             ax.text(curr, y_pos_curr, f'CURR ({curr})', color='darkgreen', ha='center', fontsize=10, weight='bold')

    # Konfigurasi Grafik
    ax.set_ylim(0, max_val * 1.1)
    ax.set_xticks(x_pos)
    ax.set_xticklabels([f'I: {i}' for i in range(n)], rotation=0) 
    ax.set_ylabel('Nilai')
    ax.set_title(f"Pencarian Nilai: {target}", fontsize=14)
    
    plt.close(fig) 
    return fig


# --- Visualisasi Utama ---
if st.button("Mulai Simulasi Jump Search"):
    
    found_index, history = jump_search(list(data_list), target_value)
    max_data_value = max(initial_data_sorted) if initial_data_sorted else 10 
    
    st.markdown("---")
    st.subheader("Visualisasi Langkah Demi Langkah")
    
    col1, col2 = st.columns([3, 1])
    
    with col1:
        vis_placeholder = st.empty()
        status_placeholder = st.empty() 
    with col2:
        table_placeholder = st.empty()
    
    final_found_index = -1
    
    # --- Loop Simulasi ---
    for step, state in enumerate(history):
        current_array = state['array']
        prev = state['prev']
        curr = state['curr']
        status = state['status']
        action = state['action']

        if status == 'Ditemukan':
            final_found_index = curr 
        
        # --- Tampilkan Grafik (Matplotlib) ---
        fig_mpl = plot_array(
            current_array, 
            state['target'], 
            prev, 
            curr, 
            final_found_index, 
            max_data_value, 
            status
        )

        with vis_placeholder.container():
            st.pyplot(fig_mpl, clear_figure=True)
        
        # --- TABEL DATA PENDUKUNG ---
        with table_placeholder.container():
             df_table = pd.DataFrame({'Index': range(len(current_array)), 'Nilai': current_array})
             st.markdown("##### Data Array (Index & Nilai)")
             st.dataframe(df_table.T, hide_index=True)

        with status_placeholder.container():
            if status == 'Ditemukan':
                st.success(f"**Langkah ke-{step}** | **Status:** {status}")
            elif status == 'Selesai':
                st.error(f"**Langkah ke-{step}** | **Status:** {status}")
            else:
                 st.info(f"**Langkah ke-{step+1}** | **Status:** {status}")
            st.caption(action)

        # Jeda untuk simulasi
        time.sleep(speed)

    # --- Hasil Akhir Final (Tampil Setelah Loop Selesai) ---
    st.markdown("---")
    if final_found_index != -1:
        st.balloons()
        st.success(f"**Pencarian Tuntas!**")
        st.write(f"Nilai **{target_value}** DITEMUKAN pada Indeks **{final_found_index}**.")
    else:
        st.error(f"**Pencarian Tuntas!**")
        st.write(f"Nilai **{target_value}** TIDAK DITEMUKAN dalam array.")
    
    st.info(f"Algoritma Jump Search selesai dalam **{len(history)-1}** langkah pengecekan.")
