from src.signal.signal import Signal
import pygame
from config.config import Config

class SoundSignal(Signal):
    
    def __init__(self):
        try:
            pygame.mixer.init()
            print("Mixer inicializado com sucesso!")
        except Exception as e:
            print(f"Erro ao inicializar o mixer: {e}")

    def start(self):
        """Carrega e toca o som definido na configuração."""
        try:
            pygame.mixer.music.load(Config.ALERT_SOUND)
            pygame.mixer.music.play()
            print(f"Reproduzindo som: {Config.ALERT_SOUND}")
        except Exception as e:
            print(f"Erro ao carregar o som: {e}")

    def stop(self):
        """Para a reprodução do som."""
        try:
            pygame.mixer.music.stop()
            print("Som interrompido.")
        except Exception as e:
            print(f"Erro ao parar o som: {e}")