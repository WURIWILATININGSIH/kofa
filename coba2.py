import pyaudio
import numpy as np
import cv2
import pygame

# 1. Konfigurasi Input Audio
def record_audio(stream, chunk_size, rate):
    data = stream.read(chunk_size, exception_on_overflow=False)
    audio_data = np.frombuffer(data, dtype=np.int16)
    return audio_data

# 2. Analisis Audio
def analyze_audio(audio_data, rate):
    # FFT untuk analisis frekuensi
    fft_data = np.fft.fft(audio_data)
    frequencies = np.fft.fftfreq(len(fft_data), 1 / rate)
    magnitude = np.abs(fft_data)

    # Identifikasi pitch (frekuensi dominan)
    peak_idx = np.argmax(magnitude)
    pitch = abs(frequencies[peak_idx])
    
    # Normalisasi magnitude untuk menentukan intensitas
    intensity = np.log10(np.max(magnitude) + 1)

    return pitch, intensity

# 3. Animasi Wajah dengan Kumis Kucing
def animate_face(frame, face_coords, pitch, intensity):
    x, y, w, h = face_coords
    center = (x + w // 2, y + h // 2)
    face_radius = w // 2

    # Gambar wajah
    cv2.circle(frame, center, face_radius, (255, 224, 189), -1)  # Wajah
    cv2.circle(frame, (center[0] - w // 5, center[1] - h // 5), w // 10, (0, 0, 0), -1)  # Mata kiri
    cv2.circle(frame, (center[0] + w // 5, center[1] - h // 5), w // 10, (0, 0, 0), -1)  # Mata kanan

    # Gambar kumis kucing
    whisker_length = w // 3
    whisker_thickness = 2
    # Kumis kiri
    cv2.line(frame, (center[0] - w // 4, center[1] + h // 8),
             (center[0] - w // 4 - whisker_length, center[1] + h // 10), (0, 0, 0), whisker_thickness)
    cv2.line(frame, (center[0] - w // 4, center[1] + h // 8),
             (center[0] - w // 4 - whisker_length, center[1] + h // 5), (0, 0, 0), whisker_thickness)
    # Kumis kanan
    cv2.line(frame, (center[0] + w // 4, center[1] + h // 8),
             (center[0] + w // 4 + whisker_length, center[1] + h // 10), (0, 0, 0), whisker_thickness)
    cv2.line(frame, (center[0] + w // 4, center[1] + h // 8),
             (center[0] + w // 4 + whisker_length, center[1] + h // 5), (0, 0, 0), whisker_thickness)

    # Gambar mulut
    mouth_open = int(10 + 20 * (pitch / 1000))  # Skala pitch
    mouth_open = max(5, min(mouth_open, h // 4))   # Batasan ukuran
    intensity_factor = int(5 * intensity)      # Skala intensitas
    mouth_height = mouth_open + intensity_factor
    cv2.ellipse(frame, (center[0], center[1] + h // 4), (w // 6, mouth_height), 0, 0, 360, (0, 0, 255), -1)

    return frame

# 4. Alur Kerja Utama
def main():
    # Konfigurasi Audio
    CHUNK = 1024
    RATE = 44100
    p = pyaudio.PyAudio()
    stream = p.open(format=pyaudio.paInt16, channels=1, rate=RATE, input=True, frames_per_buffer=CHUNK)

    # Konfigurasi Video dan Face Detector
    cap = cv2.VideoCapture(0)
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")

    # Konfigurasi Musik Latar
    pygame.mixer.init()
    pygame.mixer.music.load("GGMU.mp3")  # Ganti dengan path lagu Anda
    pygame.mixer.music.play(-1)  # Putar berulang

    try:
        while True:
            # Input Audio
            audio_data = record_audio(stream, CHUNK, RATE)
            
            # Analisis Audio
            pitch, intensity = analyze_audio(audio_data, RATE)
            
            # Input Video
            ret, frame = cap.read()
            if not ret:
                break
            
            # Deteksi Wajah
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(100, 100))

            # Jika ada wajah, tambahkan animasi
            for (x, y, w, h) in faces:
                frame = animate_face(frame, (x, y, w, h), pitch, intensity)
            
            # Tampilkan Animasi
            cv2.imshow("Karaoke Face Animation", frame)
            
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
    finally:
        # Tutup Stream
        stream.stop_stream()
        stream.close()
        p.terminate()
        cap.release()
        cv2.destroyAllWindows()
        pygame.mixer.music.stop()

if __name__ == "__main__":
    main()
