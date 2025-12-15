# File: jump_search.py (Logika Algoritma)

import math

# List global untuk menyimpan riwayat langkah
HISTORY = []

def jump_search(data_list, target):
    """
    Mengimplementasikan Jump Search dan mencatat setiap langkah di HISTORY.
    Mengembalikan index jika ditemukan, atau -1 jika tidak ditemukan.
    """
    global HISTORY
    HISTORY = []
    
    # Prasyarat: Array harus terurut! Kita asumsikan array input sudah terurut.
    arr = sorted(data_list[:]) 
    n = len(arr)
    
    # Tentukan ukuran lompatan (m = sqrt(n))
    m = int(math.sqrt(n))
    prev = 0
    
    # Catat status awal
    HISTORY.append({
        'array': arr[:],
        'target': target,
        'prev': -1, 
        'curr': 0,
        'm': m,
        'status': 'Mulai',
        'action': f'Memulai Jump Search. Ukuran lompatan (m) = {m}.'
    })

    # --- FASE 1: Lompatan (Jumping) ---
    while arr[min(m, n) - 1] < target:
        # Catat blok yang dilewati
        HISTORY.append({
            'array': arr[:],
            'target': target,
            'prev': prev, 
            'curr': min(m, n) - 1,
            'm': m,
            'status': 'Melompat',
            'action': f'Nilai {arr[min(m, n) - 1]} < {target}. Lewati blok dari {prev} ke {min(m, n) - 1}.'
        })
        
        prev = m
        m += int(math.sqrt(n))
        
        if prev >= n:
            # Jika batas bawah (prev) sudah di luar array, target tidak ada
            HISTORY.append({
                'array': arr[:],
                'target': target,
                'prev': prev, 
                'curr': -1,
                'm': m,
                'status': 'Selesai',
                'action': f'Batas bawah melewati akhir array. Nilai {target} tidak ditemukan.'
            })
            return -1, HISTORY

    # Catat akhir fase lompatan
    HISTORY.append({
        'array': arr[:],
        'target': target,
        'prev': prev, 
        'curr': min(m, n) - 1,
        'm': m,
        'status': 'Blok Ditemukan',
        'action': f'Nilai {target} mungkin berada di blok ini (antara Indeks {prev} dan {min(m, n) - 1}).'
    })
    
    # --- FASE 2: Pencarian Linear (Linear Search) ---
    curr = prev # Mulai linear search dari batas bawah blok
    
    while arr[curr] < target:
        HISTORY.append({
            'array': arr[:],
            'target': target,
            'prev': prev, 
            'curr': curr,
            'm': m,
            'status': 'Linear Mencari',
            'action': f'Pencarian Linear: Mengecek Indeks {curr} (Nilai: {arr[curr]}).'
        })
        curr += 1
        
        # Jika curr mencapai batas atas blok atau akhir array
        if curr == min(m, n):
            HISTORY.append({
                'array': arr[:],
                'target': target,
                'prev': prev, 
                'curr': curr,
                'm': m,
                'status': 'Selesai',
                'action': f'Pencarian Linear melampaui batas blok. Nilai {target} tidak ditemukan.'
            })
            return -1, HISTORY
            
    # Catat langkah pengecekan terakhir (sebelum perbandingan sukses atau gagal)
    HISTORY.append({
        'array': arr[:],
        'target': target,
        'prev': prev, 
        'curr': curr,
        'm': m,
        'status': 'Cek Akhir',
        'action': f'Pencarian Linear: Melakukan pengecekan terakhir di Indeks {curr}.'
    })
    
    # --- FASE 3: Hasil ---
    if arr[curr] == target:
        # Ditemukan
        HISTORY.append({
            'array': arr[:],
            'target': target,
            'prev': prev, 
            'curr': curr,
            'm': m,
            'status': 'Ditemukan',
            'action': f'Nilai {target} DITEMUKAN pada Indeks {curr}!'
        })
        return curr, HISTORY
    else:
        # Tidak Ditemukan
        HISTORY.append({
            'array': arr[:],
            'target': target,
            'prev': prev, 
            'curr': curr,
            'm': m,
            'status': 'Selesai',
            'action': f'Nilai pada Indeks {curr} ({arr[curr]}) bukan {target}. Tidak ditemukan.'
        })
        return -1, HISTORY
