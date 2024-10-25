#LECUN - CNN => Josh Starmer
# Livro : https://d2l.ai/index.html - Dive into Deep Learning
import cv2
import mediapipe as mp
# from sender import ModBusSender

class RecognitionHand:

    def __init__(self):
        self.mp_drawing = mp.solutions.drawing_utils
        self.mp_hands = mp.solutions.hands
   
    def recoginitionInitialize(self):
        cap = cv2.VideoCapture(1)
        cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1360)  # Define a largura para 1920 pixels
        cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 768)  # Define a altura para 1080 pixels

        with self.mp_hands.Hands(min_detection_confidence=0.5, min_tracking_confidence=0.5) as hands:
            while cap.isOpened():
                success, image = cap.read()
                if not success:
                    continue
                # Inverte a imagem para visualização de selfie e converte BGR para RGB
                image = cv2.cvtColor(cv2.flip(image, 1), cv2.COLOR_BGR2RGB)
                results = hands.process(image)
                image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

                # Dimensões da imagem
                image_height, image_width = image.shape[0], image.shape[1]

                # Definindo o tamanho do retângulo
                rect_width = int(image_width * 0.40)  # 5% da largura da imagem
                rect_height = int(image_height * 0.50)  # 80% da altura da imagem

                # Calculando as coordenadas do retângulo centralizado
                center_x, center_y = image_width // 2, image_height // 2
                top_left = (center_x - rect_width // 2, center_y - rect_height // 2)
                bottom_right = (center_x + rect_width // 2, center_y + rect_height // 2)

                # Definir a cor do retângulo
                rect_color = (255, 0, 0)  # Azul padrão

                # Variável para verificar se algum ponto está dentro do retângulo (zona perigosa)
                hand_in_danger_zone = False

                if results.multi_hand_landmarks:
                    for hand_landmarks in results.multi_hand_landmarks:
                        try:
                            self.mp_drawing.draw_landmarks(image, hand_landmarks, self.mp_hands.HAND_CONNECTIONS)
                            
                            # Verificar cada ponto de referência dos dedos
                            for landmark in hand_landmarks.landmark:
                                # Convertendo as coordenadas normalizadas dos landmarks para pixels
                                ponto_x = int(landmark.x * image.shape[1])
                                ponto_y = int(landmark.y * image.shape[0])

                                # Verifica se o ponto está dentro do retângulo (zona de perigo)
                                if top_left[0] < ponto_x < bottom_right[0] and top_left[1] < ponto_y < bottom_right[1]:
                                    hand_in_danger_zone = True
                                    break  # Se um ponto estiver dentro, não precisa verificar mais

                        except Exception as e:
                            print("Falha: ", e)

                # Se algum ponto entrou na zona de perigo, altera a cor do retângulo para vermelho
                if hand_in_danger_zone:
                    rect_color = (0, 0, 255)  # Vermelho

                # Desenha o retângulo com a cor apropriada
                cv2.rectangle(image, top_left, bottom_right, rect_color, 2)

                # Exibe a imagem processada
                cv2.imshow('Hand Recognition', image)

                if cv2.waitKey(5) & 0xFF == 27:
                    break

            cap.release()
            cv2.destroyAllWindows()

        
        # # Calcula a média de tempo de detecção
        # if detection_times:
        #     avg_detection_time = sum(detection_times) / len(detection_times)
        #     print(f'Tempo médio de detecção da ultrapassagem da linha: {avg_detection_time:.4f} segundos')
        # else:
        #     print('Nenhuma ultrapassagem de linha detectada.')







