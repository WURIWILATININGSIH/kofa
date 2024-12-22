import numpy as np
import pyaudio


class AudioRecorder:
    """Kelas untuk merekam audio, mendeteksi pitch, dan memproses data audio."""

    def __init__(self, chunk, rate, input_device_index=None):
        """
        Inisialisasi AudioRecorder.
        :param chunk: Ukuran buffer audio.
        :param rate: Frekuensi sampling audio.
        :param input_device_index: Indeks perangkat input audio (opsional).
        """
        self.chunk = chunk
        self.rate = rate
        self.audio_interface = pyaudio.PyAudio()

        # Validasi perangkat input audio
        if input_device_index is None:
            input_device_index = self._get_default_input_device()
        self.stream = self.audio_interface.open(
            format=pyaudio.paInt16,
            channels=1,
            rate=self.rate,
            input=True,
            input_device_index=1,
            frames_per_buffer=self.chunk
        )

    def _get_default_input_device(self):
        """
        Dapatkan indeks perangkat input audio default.
        :return: Indeks perangkat input audio.
        """
        for i in range(self.audio_interface.get_device_count()):
            device_info = self.audio_interface.get_device_info_by_index(i)
            if device_info["maxInputChannels"] > 0:
                print(f"Default input device: {device_info['name']} (index: {i})")
                return i
        raise ValueError("No input device found!")

    def record_audio(self):
        """
        Rekam audio dari mikrofon.
        :return: Data audio dalam bentuk numpy array.
        """
        try:
            audio_data = self.stream.read(self.chunk, exception_on_overflow=False)
            audio_array = np.frombuffer(audio_data, dtype=np.int16)  # Pastikan tipe data adalah int16
            print(f"Audio data recorded: {audio_array[:10]}")  # Log 10 sampel pertama
            return audio_array
        except Exception as e:
            print(f"Error recording audio: {e}")
            return np.zeros(self.chunk, dtype=np.int16)

    def noise_suppression(self, audio_data, threshold=0):
        """Kurangi noise latar belakang."""
        return np.where(np.abs(audio_data) > threshold, audio_data, 0)
    
    def normalize_audio(self, audio_data):
        """
        Normalisasi level audio secara manual tanpa menggunakan pydub.
        :param audio_data: Array numpy berisi data audio.
        :return: Audio yang dinormalisasi.
        """
        try:
            # Normalisasi manual: skala data audio ke rentang maksimum
            max_val = np.max(np.abs(audio_data))
            if max_val == 0:
                return audio_data
            normalized_audio = (audio_data / max_val) * 32767  # Skala ke int16
            # Tambahkan penguatan (amplifikasi)
            amplification_factor = 2.0  # Sesuaikan faktor amplifikasi
            amplified_audio = normalized_audio * amplification_factor
            amplified_audio = np.clip(amplified_audio, -32768, 32767)  # Hindari overflow
            return normalized_audio.astype(np.int16)
        except Exception as e:
            print(f"Error normalizing audio: {e}")
            return audio_data

    def detect_pitch(self, audio_data, threshold=30):
        """
        Deteksi pitch dari sinyal audio, hanya fokus pada frekuensi suara manusia.
        :param audio_data: Array numpy berisi data audio.
        :param threshold: Ambang batas magnitudo untuk mengabaikan noise.
        :return: Pitch yang terdeteksi dalam Hertz (Hz).
        """
        if len(audio_data) == 0:
            return 0

        # Transformasi Fourier Cepat (FFT)
        fft_result = np.fft.fft(audio_data)
        frequencies = np.fft.fftfreq(len(fft_result), 1 / self.rate)

        # Filter hanya frekuensi positif
        magnitudes = np.abs(fft_result)
        positive_frequencies = frequencies[:len(frequencies) // 2]
        positive_magnitudes = magnitudes[:len(magnitudes) // 2]

        # Fokus pada frekuensi suara manusia
        valid_range = (positive_frequencies >= 30) & (positive_frequencies <= 1900)
        filtered_magnitudes = positive_magnitudes[valid_range]
        filtered_frequencies = positive_frequencies[valid_range]

        # Abaikan jika tidak ada suara signifikan
        if len(filtered_frequencies) == 0 or max(filtered_magnitudes) < threshold:
            return 0

        # Ambil frekuensi dengan magnitudo tertinggi
        peak_index = np.argmax(filtered_magnitudes)
        pitch = abs(filtered_frequencies[peak_index])

        # Abaikan pitch di luar rentang manusia
        return pitch if 20 <= pitch <= 2000 else 0

    def close(self):
        """Tutup stream audio dan interface."""
        self.stream.stop_stream()
        self.stream.close()
        self.audio_interface.terminate()