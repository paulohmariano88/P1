import tkinter as tk
from src.service.recognition import RecognitionHand

class MainScreen:
    def __init__(self):
        # Janela principal
        self._root = tk.Tk()
        self._root.title("CENTRO 4.0 - FIEMG: INTELIGENCIA ARTIFICIAL DE PROTEÇÃO A MÃOS E PULSOS - PROJETO ERGONOMIA")
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

        # Campo de senha e botão de verificação
        self.add_password_field()

        # Controles de tamanho da área segura (iniciam bloqueados)
        self.controller_width()
        self.controller_height()
        self.starter_button()

    def add_password_field(self):
        """Adiciona um campo de senha para desbloquear os controles."""
        password_label = tk.Label(self.controls_frame, text="Digite a senha:", font=("Arial", 14))
        password_label.pack(pady=5)

        self.password_entry = tk.Entry(self.controls_frame, show="*", font=("Arial", 14))
        self.password_entry.pack(pady=5)

        # Frame para os botões "Desbloquear" e "Travar"
        button_frame = tk.Frame(self.controls_frame)
        button_frame.pack(pady=10)

        unlock_button = tk.Button(button_frame, text="Desbloquear", command=self.check_password, font=("Arial", 14, "bold"))
        unlock_button.pack(side=tk.LEFT, padx=5)

        lock_button = tk.Button(button_frame, text="Travar", command=self.lock_controls, font=("Arial", 14, "bold"))
        lock_button.pack(side=tk.LEFT, padx=5)

        # Label para mensagens de feedback
        self.message_label = tk.Label(self.controls_frame, font=("Arial", 14))
        self.message_label.pack(pady=5)

    def display_message(self, message, color):
        """Exibe uma mensagem e limpa a anterior."""
        self.message_label.config(text=message, fg=color)

    def check_password(self):
        """Verifica a senha e desbloqueia os controles se estiver correta."""
        password = self.password_entry.get()
        if password == "1234":  # Substitua "1234" pela senha desejada
            self.unlock_controls()
            self.display_message("Controles desbloqueados!", "green")
        else:
            self.display_message("Senha incorreta!", "red")

    def unlock_controls(self):
        """Desbloqueia os controles."""
        self.width_slider.config(state="normal", bg="white")
        self.height_slider.config(state="normal", bg="white")

    def lock_controls(self):
        """Trava os controles novamente."""
        self.width_slider.config(state="disabled", bg="#d3d3d3")  # Esmaece
        self.height_slider.config(state="disabled", bg="#d3d3d3")  # Esmaece
        self.display_message("Controles travados!", "red")

    def controller_width(self):
        """Controlador para a largura da área segura."""
        tk.Label(self.controls_frame, text="Largura (%)", font=("Arial", 14, "bold")).pack()
        self.width_slider = tk.Scale(
            self.controls_frame, from_=10, to=100, orient=tk.HORIZONTAL,
            command=lambda value: self.recognizer.set_width_secure_area(int(value)),
            width=20,
            length=200,
            state="disabled"  # Inicia bloqueado
        )
        self.width_slider.set(50)
        self.width_slider.pack()

    def controller_height(self):
        """Controlador para a altura da área segura."""
        tk.Label(self.controls_frame, text="Altura (%)", font=("Arial", 14, "bold")).pack()
        self.height_slider = tk.Scale(
            self.controls_frame, from_=10, to=100, orient=tk.HORIZONTAL,
            command=lambda value: self.recognizer.set_height_secure_area(int(value)),
            width=20,
            length=200,
            state="disabled"  # Inicia bloqueado
        )
        self.height_slider.set(40)
        self.height_slider.pack()

    def start_capture(self):
        """Inicia a captura de vídeo."""
        self.recognizer.start_capture()

    def starter_button(self):
        """Botão para iniciar a captura."""
        start_button = tk.Button(self.controls_frame, text="Iniciar Captura",
                                 command=self.start_capture,
                                 font=("Arial", 14, "bold"),
                                 bg="white",
                                 fg="black")
        start_button.pack(pady=10)

    def run(self):
        """Inicia o loop principal."""
        self._root.mainloop()

    def __del__(self):
        """Libera a câmera ao fechar o programa."""
        self.recognizer.release()








