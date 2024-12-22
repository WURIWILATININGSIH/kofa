import pyaudio
import numpy as np
import cv2
import pygame
import tkinter as tk
from tkinter import filedialog
import threading
from PIL import Image, ImageTk

# Fungsi untuk merekam audio
class AudioRecorder:
    def __init__(self, chunk_size, rate):
        self.chunk_size = chunk_size
        self.rate = rate
        self.p = pyaudio.PyAudio()
        self.stream = self.p.open(format=pyaudio.paInt16, channels=1, rate=self.rate, input=True, frames_per_buffer=self.chunk_size)

    def record_audio(self):
        data = self.stream.read(self.chunk_size, exception_on_overflow=False)
        audio_data = np.frombuffer(data, dtype=np.int16)
        return audio_data

    def close(self):
        self.stream.stop_stream()
        self.stream.close()
        self.p.terminate()

# Fungsi untuk mengganti lagu
class MusicPlayer:
    def __init__(self):
        self.song_list = ["GGMU.mp3", "tanahair.mp3", "simpanrasa.mp3"]
        self.current_song_index = 0
        pygame.mixer.init()

    def play_current_song(self):
        if self.song_list:
            pygame.mixer.music.load(self.song_list[self.current_song_index])
            pygame.mixer.music.play(-1)

    def next_song(self):
        if self.song_list:
            self.current_song_index = (self.current_song_index + 1) % len(self.song_list)
            self.play_current_song()

    def previous_song(self):
        if self.song_list:
            self.current_song_index = (self.current_song_index - 1) % len(self.song_list)
            self.play_current_song()

# Fungsi untuk animasi wajah
def animate_face(frame, face_coords):
    x, y, w, h = face_coords
    face_center = (x + w // 2, y + h // 2)

    # Gambar wajah (lingkaran biru muda)
    cv2.circle(frame, face_center, w // 2, (240, 240, 255), -1)

    # Gambar mata (dua lingkaran hitam)
    eye_radius = w // 10
    eye_offset_x = w // 5
    eye_offset_y = h // 5
    cv2.circle(frame, (face_center[0] - eye_offset_x, face_center[1] - eye_offset_y), eye_radius, (0, 0, 0), -1)
    cv2.circle(frame, (face_center[0] + eye_offset_x, face_center[1] - eye_offset_y), eye_radius, (0, 0, 0), -1)

    # Gambar mulut (lingkaran merah kecil di tengah)
    mouth_radius = w // 8
    cv2.circle(frame, (face_center[0], face_center[1] + h // 8), mouth_radius, (0, 0, 255), -1)

    # Gambar kumis (garis di kiri dan kanan mulut)
    whisker_length = w // 3
    whisker_thickness = 2
    cv2.line(frame, (face_center[0] - w // 4, face_center[1] + h // 8),
             (face_center[0] - w // 4 - whisker_length, face_center[1] + h // 10), (0, 0, 0), whisker_thickness)
    cv2.line(frame, (face_center[0] + w // 4, face_center[1] + h // 8),
             (face_center[0] + w // 4 + whisker_length, face_center[1] + h // 10), (0, 0, 0), whisker_thickness)

    return frame

# Fungsi utama
def main():
    # Konfigurasi audio dan video
    CHUNK = 1024
    RATE = 44100
    audio_recorder = AudioRecorder(CHUNK, RATE)
    cap = cv2.VideoCapture(0)
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")

    music_player = MusicPlayer()

    # Status rekaman
    recording = threading.Event()

    # Fungsi untuk merekam video
    def start_recording():
        recording.set()
        fourcc = cv2.VideoWriter_fourcc(*'XVID')
        out = cv2.VideoWriter('output.avi', fourcc, 20.0, (640, 480))

        while recording.is_set():
            ret, frame = cap.read()
            if not ret:
                break

            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(100, 100))

            for (x, y, w, h) in faces:
                frame = animate_face(frame, (x, y, w, h))

            out.write(frame)
            update_video(frame)

        out.release()

    def stop_recording():
        recording.clear()

    # Fungsi untuk memperbarui tampilan video di Canvas
    def update_video(frame):
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        img = Image.fromarray(rgb_frame)
        imgtk = ImageTk.PhotoImage(image=img)
        video_label.imgtk = imgtk
        video_label.configure(image=imgtk)

    # GUI Tkinter
    root = tk.Tk()
    root.title("Karaoke Face Animation")

    video_label = tk.Label(root)
    video_label.pack()

    # Tombol kontrol
    control_frame = tk.Frame(root)
    control_frame.pack()

    start_button = tk.Button(control_frame, text="Start Recording", command=lambda: threading.Thread(target=start_recording).start(), bg="red", fg="white")
    start_button.grid(row=0, column=0, padx=10, pady=10)

    stop_button = tk.Button(control_frame, text="Stop Recording", command=stop_recording, bg="red", fg="white")
    stop_button.grid(row=0, column=1, padx=10, pady=10)

    prev_song_button = tk.Button(control_frame, text="Previous Song", command=music_player.previous_song, bg="blue", fg="white")
    prev_song_button.grid(row=0, column=2, padx=10, pady=10)

    next_song_button = tk.Button(control_frame, text="Next Song", command=music_player.next_song, bg="blue", fg="white")
    next_song_button.grid(row=0, column=3, padx=10, pady=10)

    # Loop untuk memperbarui video secara real-time
    def video_loop():
        while True:
            ret, frame = cap.read()
            if ret:
                gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(100, 100))
                for (x, y, w, h) in faces:
                    frame = animate_face(frame, (x, y, w, h))
                update_video(frame)

    threading.Thread(target=video_loop, daemon=True).start()

    root.mainloop()

    audio_recorder.close()
    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
