**Karaoke Face Animation**

Karaoke Face Animation adalah sebuah inovasi dalam teknologi augmented reality (AR) yang memadukan animasi wajah dengan elemen karaoke.Teknologi ini memungkinkan pengguna untuk merasakan pengalaman bernyanyi secara interaktif dengan memanfaatkan fitur pelacakan wajah
dan sinkronisasi audio-visual

**fitur utama**

1. Deteksi Wajah Real-Time:

Menggunakan teknologi Haar Cascade untuk mendeteksi wajah pengguna melalui kamera secara real-time.
Animasi Avatar Berbasis Wajah:

2. Aplikasi menyediakan tiga pilihan avatar:
Wajah kucing (dengan kumis dan animasi mata/mulut).
Wajah marah (dengan alis menurun dan ekspresi sesuai suara).
Wajah feminin (dengan pipi merah muda dan bibir berwarna).
Sinkronisasi Audio-Visual:

3. Animasi wajah, terutama gerakan mulut, disinkronisasi dengan pitch suara pengguna yang dianalisis secara real-time.
Rekaman Video dan Audio:

4. Aplikasi dapat merekam video dengan animasi wajah dan audio secara bersamaan, menghasilkan output berupa file video MP4.
Antarmuka Pengguna Interaktif:

5. Dibangun menggunakan Tkinter, antarmuka menyediakan tombol untuk memilih avatar, memutar lagu, serta memulai dan menghentikan perekaman.
Pengolahan dan Penggabungan Audio-Video:

6. Video dan audio digabungkan tanpa menggunakan alat eksternal seperti FFmpeg, tetapi menggunakan pendekatan internal dengan OpenCV.
Dukungan Multithreading:

7. Proses berat, seperti perekaman dan rendering animasi, dilakukan secara paralel untuk menjaga performa aplikasi.

**cara menjalankan**

1. clone ropository git clone:
   https://github.com/WURIWILATININGSIH/kofa.git

2. install requirements.txt menggunakan terminal:
    pip install -r requirements.txt

3. lalu pastikan berikut terinstall :
        - openCV
        - numpy
        - pyaudio
        - pygame

4.  jalankan program menggunakan terminal :
    python main.py