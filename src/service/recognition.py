#LECUN - CNN => Josh Starmer
# Livro : https://d2l.ai/index.html - Dive into Deep Learning
import cv2
import mediapipe as mp
from PIL import Image, ImageTk
import threading
from config.config import Config
from playsound import playsound
from src.service.sender import ModBusSender

class RecognitionHand:
    def __init__(self, video_label):
        self.video_label = video_label  # Label para exibir o vídeo
        self.mp_drawing = mp.solutions.drawing_utils
        self.mp_hands = mp.solutions.hands.Hands(min_detection_confidence=0.5, min_tracking_confidence=0.5)
        self.hand_in_danger_zone = False
        self.cap = self.initialize_camera()
        self._width_secure_area = 0.50
        self._height_secure_area = 0.40
        self.capturing = False
        self.sender = ModBusSender()  # Reutiliza a mesma instância de ModBusSender
        self.alarm_thread = None  # Thread do alarme
        self.alarm_active = False  # Flag para indicar se o alarme está ativo
        self.stop_alarm = threading.Event()  # Evento para parar o alarme

    def start_capture(self):
        if not self.capturing:
            self.capturing = True
            self.update_video_frame()

    def initialize_camera(self):
        """Configura a câmera."""
        cap = cv2.VideoCapture(1)
        cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
        cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)
        return cap

    def set_width_secure_area(self, size):
        """Define a largura da área segura."""
        self._width_secure_area = size / 100

    def set_height_secure_area(self, size):
        """Define a altura da área segura."""
        self._height_secure_area = size / 100

    def play_alert_sound(self):
        """Toca o som continuamente enquanto a mão estiver na área de perigo."""
        while not self.stop_alarm.is_set():
            try:
                playsound(Config.ALERT_SOUND.value)
            except Exception as e:
                print(f"Erro ao tocar som: {e}")

    def start_alarm(self):
        """Inicia o alarme em uma thread separada."""
        if not self.alarm_active:
            self.alarm_active = True
            self.stop_alarm.clear()
            self.alarm_thread = threading.Thread(target=self.play_alert_sound, daemon=True)
            self.alarm_thread.start()

    def stop_alarm_sound(self):
        """Para o alarme."""
        if self.alarm_active:
            self.stop_alarm.set()
            self.alarm_active = False

    def start_modbus_signal(self, signal: bool):
        """Envia um sinal Modbus."""
        try:
            self.sender.send_signal(signal)  # Usa a mesma instância de ModBusSender
        except Exception as e:
            print("Error Modbus", e)

    def get_rectangle_coordinates(self, image):
        """Calcula as coordenadas da área segura."""
        image_height, image_width = image.shape[:2]
        rect_width = int(image_width * self._width_secure_area)
        rect_height = int(image_height * self._height_secure_area)
        center_x, center_y = image_width // 2, image_height // 2
        top_left = (center_x - rect_width // 2, center_y - rect_height // 2)
        bottom_right = (center_x + rect_width // 2, center_y + rect_height // 2)
        return top_left, bottom_right

    def is_hand_in_danger_zone(self, hand_landmarks, top_left, bottom_right, image):
        """Verifica se a mão está na área de perigo."""
        image_width, image_height = image.shape[1], image.shape[0]
        for landmark in hand_landmarks.landmark:
            x = int(landmark.x * image_width)
            y = int(landmark.y * image_height)
            if top_left[0] < x < bottom_right[0] and top_left[1] < y < bottom_right[1]:
                return True
        return False

    def update_video_frame(self):
        """Captura e atualiza o frame de vídeo no Label."""
        success, image = self.cap.read()
        if success:
            image = cv2.flip(image, 1)
            image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
            top_left, bottom_right = self.get_rectangle_coordinates(image)
            rect_color = (0, 0, 255)
            landmark_color = (0, 0, 255)  # Cor padrão (azul)

            results = self.mp_hands.process(image)
            if results.multi_hand_landmarks:
                for hand_landmarks in results.multi_hand_landmarks:
                    if self.is_hand_in_danger_zone(hand_landmarks, top_left, bottom_right, image):
                        rect_color = (255, 0, 0)  # Muda o retângulo para vermelho
                        landmark_color = (255, 0, 0)  # Muda a cor das landmarks para vermelho
                        self.start_alarm()
                        self.start_modbus_signal(True)
                    else:
                        self.stop_alarm_sound()
                        self.start_modbus_signal(False)

                    # Desenha as landmarks com a cor correspondente
                    self.mp_drawing.draw_landmarks(
                        image,
                        hand_landmarks,
                        mp.solutions.hands.HAND_CONNECTIONS,
                        self.mp_drawing.DrawingSpec(color=landmark_color, thickness=2, circle_radius=2),
                        self.mp_drawing.DrawingSpec(color=landmark_color, thickness=2),
                    )

            cv2.rectangle(image, top_left, bottom_right, rect_color, 2)
            img = Image.fromarray(image)
            imgtk = ImageTk.PhotoImage(image=img)
            self.video_label.imgtk = imgtk
            self.video_label.config(image=imgtk)

        if self.capturing:
            self.video_label.after(10, self.update_video_frame)

    def stop_capture(self):
        self.capturing = False

    def release(self):
        """Libera a câmera."""
        self.stop_capture()
        self.stop_alarm_sound()  # Garante que o alarme pare ao liberar a câmera
        if self.cap.isOpened():
            self.cap.release()













