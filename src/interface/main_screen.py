import tkinter as tk
from service.recognition import RecognitionHand

class MainScreen:
    def __init__(self):
        # Janela principal
        self._root = tk.Tk()
        self._root.title("CENTRO 4.0 - FIEMG")
        self._root.geometry("1600x900")

        # Frame principal
        self._main_frame = tk.Frame(self._root)
        self._main_frame.pack(fill=tk.BOTH, expand=True)

        # Frame de vídeo (esquerdo)
        self.video_frame = tk.Frame(self._main_frame)
        self.video_frame.pack(side=tk.LEFT, padx=10, pady=10)

        # Label para exibir o vídeo
        self.video_label = tk.Label(self.video_frame)
        self.video_label.pack()

        # Frame de controles (direito)
        self.controls_frame = tk.Frame(self._main_frame, width=300, height=500)
        self.controls_frame.pack(side=tk.RIGHT, padx=10, pady=10, fill=tk.Y)

        # Instancia o reconhecimento de mãos
        self.recognizer = RecognitionHand(self.video_label)

        # Controles de tamanho da área segura
        self.controller_width()
        self.controller_height()
        self.starter_button()

    def controller_width(self):
        """Controlador para a largura da área segura."""
        tk.Label(self.controls_frame, text="Largura (%)", font=("Arial", 18, "bold")).pack()
        width_slider = tk.Scale(
            self.controls_frame, from_=10, to=100, orient=tk.HORIZONTAL,
            command=lambda value: self.recognizer.set_width_secure_area(int(value)),
            width=20,       # Aumenta a espessura do slider
            length=200 
        )
        width_slider.set(50)
        width_slider.pack()

    def controller_height(self):
        """Controlador para a altura da área segura."""
        tk.Label(self.controls_frame, text="Altura (%)", font=("Arial", 18, "bold")).pack()
        height_slider = tk.Scale(
            self.controls_frame, from_=10, to=100, orient=tk.HORIZONTAL,
            command=lambda value: self.recognizer.set_height_secure_area(int(value)),
            width=20,       # Aumenta a espessura do slider
            length=200 )
        
        height_slider.set(40)
        height_slider.pack()

    def start_capture(self):
        """Inicia a captura de vídeo.""" 
        self.recognizer.start_capture()

    def starter_button(self):
        """Botão para iniciar a captura."""
        start_button = tk.Button(self.controls_frame, text="Iniciar Captura", 
                                 command=self.start_capture, 
                                 font=("Arial", 18, "bold"),
                                 bg="white",
                                 fg="black")
        start_button.pack(pady=10)

    def run(self):
        """Inicia o loop principal."""
        self._root.mainloop()

    def __del__(self):
        """Libera a câmera ao fechar o programa."""
        self.recognizer.release()



