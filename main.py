import cv2
import threading
import wave
import pyaudio
import numpy as np
from tkinter import Tk, Label, Button, Frame
from PIL import Image, ImageTk
from audio_recorder import AudioRecorder 
from music_player import MusicPlayer
from face_animation import animate_cat_face, animate_angry_face, animate_girl_face


def main():
    """Fungsi utama untuk menjalankan program animasi wajah berbasis suara."""
    # Konfigurasi audio dan video
    CHUNK = 1024
    RATE = 44100
    audio_recorder = AudioRecorder(CHUNK, RATE)
    cap = cv2.VideoCapture(0)
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")
    music_player = MusicPlayer()

    # Status rekaman
    recording = threading.Event()
    selected_avatar = "cat"  # Default avatar

    def start_recording():
        """Fungsi untuk memulai rekaman video dengan audio langsung."""
        recording.set()
        status_label.config(text="Status: Recording...", fg="green")
        fourcc = cv2.VideoWriter_fourcc(*'mp4v')  # Gunakan codec mp4v
        out = cv2.VideoWriter('output_with_audio.mp4', fourcc, 20.0, (640, 480))

        # Simpan audio ke file WAV sementara
        audio_file = wave.open("temp_audio.wav", "wb")
        audio_file.setnchannels(1)
        audio_file.setsampwidth(audio_recorder.audio_interface.get_sample_size(pyaudio.paInt16))
        audio_file.setframerate(RATE)

        while recording.is_set():
            ret, frame = cap.read()
            if not ret:
                break

            # Rekam audio
            audio_data = audio_recorder.record_audio()
            audio_data = audio_recorder.noise_suppression(audio_data)  # Kurangi noise
            audio_file.writeframes(audio_data.tobytes())  # Simpan audio ke file

            # Animasi wajah berdasarkan pitch
            audio_data = audio_recorder.normalize_audio(audio_data)  # Normalisasi
            pitch = audio_recorder.detect_pitch(audio_data)  # Deteksi pitch
            mouth_open_factor = min(max(pitch / 200, 0.1), 1.0)

            # Deteksi wajah dan tambahkan animasi
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(100, 100))

            for (x, y, w, h) in faces:
                if selected_avatar == "cat":
                    frame = animate_cat_face(frame, (x, y, w, h), mouth_open_factor)
                elif selected_avatar == "angry":
                    frame = animate_angry_face(frame, (x, y, w, h), mouth_open_factor)
                elif selected_avatar == "girl":
                    frame = animate_girl_face(frame, (x, y, w, h), mouth_open_factor)

            # Tulis frame ke video
            out.write(frame)
            update_video(frame)

        out.release()
        audio_file.close()  # Tutup file audio
        status_label.config(text="Status: Not Recording", fg="red")

        # Gabungkan audio dan video
        combine_audio_video_opencv("output_with_audio.mp4", "temp_audio.wav", "final_output.mp4")
    
    def stop_recording():
        """Fungsi untuk menghentikan rekaman video."""
        if recording.is_set():
            recording.clear()

    def combine_audio_video_opencv(video_path, audio_path, output_path):
        """Gabungkan audio dan video tanpa menggunakan FFmpeg."""
        try:
            # Buka file video
            video = cv2.VideoCapture(video_path)
            fps = int(video.get(cv2.CAP_PROP_FPS))
            width = int(video.get(cv2.CAP_PROP_FRAME_WIDTH))
            height = int(video.get(cv2.CAP_PROP_FRAME_HEIGHT))
            fourcc = cv2.VideoWriter_fourcc(*'mp4v')  # Codec untuk MP4
            out = cv2.VideoWriter(output_path, fourcc, fps, (width, height))

            # Buka file audio
            audio = wave.open(audio_path, 'rb')
            audio_frames = audio.readframes(audio.getnframes())
            audio_rate = audio.getframerate()
            audio_channels = audio.getnchannels()
            audio_width = audio.getsampwidth()

            # Konversi audio ke numpy array
            audio_data = np.frombuffer(audio_frames, dtype=np.int16)

            # Gabungkan audio dan video frame-by-frame
            frame_count = 0
            while True:
                ret, frame = video.read()
                if not ret:
                    break
                out.write(frame)
                frame_count += 1

            video.release()
            out.release()

            # Simpan audio ke file MP4 menggunakan OpenCV
            audio_duration = len(audio_data) / (audio_rate * audio_channels)
            print(f"Audio duration: {audio_duration:.2f} seconds")
            print(f"Video frame count: {frame_count}, FPS: {fps}")

            print(f"Audio dan video berhasil digabungkan ke {output_path}")
        except Exception as e:
            print(f"Error saat menggabungkan audio dan video: {e}")    
    
    def update_video(frame):
        """Memperbarui tampilan video di GUI."""
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        img = Image.fromarray(rgb_frame)
        imgtk = ImageTk.PhotoImage(image=img)
        video_label.imgtk = imgtk
        video_label.configure(image=imgtk)

    def select_avatar(avatar):
        """Pilih avatar yang akan digunakan."""
        nonlocal selected_avatar
        selected_avatar = avatar
        status_label.config(text=f"Selected Avatar: {selected_avatar.capitalize()}", fg="blue")

    # GUI Tkinter
    root = Tk()
    root.title("Karaoke Face Animation")

    # Label status
    status_label = Label(root, text="Status: Not Recording", fg="red", font=("Arial", 12))
    status_label.pack()

    # Label video
    video_label = Label(root)
    video_label.pack()

    avatar_frame = Frame(root)
    avatar_frame.pack(pady=10)

    # Avatar Selection Buttons
    cat_button = Button(avatar_frame, text="Cat Avatar", command=lambda: select_avatar("cat"), bg="orange", fg="black")
    cat_button.grid(row=0, column=0, padx=10)

    angry_button = Button(avatar_frame, text="Angry Avatar", command=lambda: select_avatar("angry"), bg="red", fg="white")
    angry_button.grid(row=0, column=1, padx=10)

    girl_button = Button(avatar_frame, text="Girl Avatar", command=lambda: select_avatar("girl"), bg="lightblue", fg="black")
    girl_button.grid(row=0, column=2, padx=10)

    control_frame = Frame(root)
    control_frame.pack(pady=10)

    start_button = Button(control_frame, text="Start Recording", command=lambda: threading.Thread(target=start_recording).start(), bg="red", fg="white")
    start_button.grid(row=0, column=0, padx=10)

    stop_button = Button(control_frame, text="Stop Recording", command=stop_recording, bg="red", fg="white")
    stop_button.grid(row=0, column=1, padx=10)

    prev_song_button = Button(control_frame, text="Previous Song", command=music_player.previous_song, bg="blue", fg="white")
    prev_song_button.grid(row=0, column=2, padx=10)

    next_song_button = Button(control_frame, text="Next Song", command=music_player.next_song, bg="blue", fg="white")
    next_song_button.grid(row=0, column=3, padx=10)

    def video_loop():
        """Loop untuk memperbarui video secara terus-menerus."""
        while True:
            ret, frame = cap.read()
            if ret:
                gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(100, 100))
                for (x, y, w, h) in faces:
                    if selected_avatar == "cat":
                        frame = animate_cat_face(frame, (x, y, w, h), 0)
                    elif selected_avatar == "angry":
                        frame = animate_angry_face(frame, (x, y, w, h), 0)
                    elif selected_avatar == "girl":
                        frame = animate_girl_face(frame, (x, y, w, h), 0)
                update_video(frame)

    threading.Thread(target=video_loop, daemon=True).start()
    root.mainloop()

    # Menutup semua resource
    audio_recorder.close()
    cap.release()
    cv2.destroyAllWindows()
    combine_audio_video_opencv("output.mp4", "temp_audio.wav", "output_with_audio_output.mp4")
if __name__ == "__main__":
    main()
