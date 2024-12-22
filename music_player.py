import pygame

class MusicPlayer:
    """Kelas untuk memutar musik menggunakan pygame."""
    def __init__(self):
        self.song_list = ["GGMU.mp3", "tanahair.mp3", "simpanrasa.mp3"]
        self.current_song_index = 0
        pygame.mixer.init()

    def play_current_song(self):
        """Putar lagu saat ini."""
        if self.song_list:
            pygame.mixer.music.load(self.song_list[self.current_song_index])
            pygame.mixer.music.play(-1)

    def next_song(self):
        """Pindah ke lagu berikutnya."""
        self.current_song_index = (self.current_song_index + 1) % len(self.song_list)
        self.play_current_song()

    def previous_song(self):
        """Pindah ke lagu sebelumnya."""
        self.current_song_index = (self.current_song_index - 1) % len(self.song_list)
        self.play_current_song()