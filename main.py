#LECUN - CNN => Josh Starmer
# Livro : https://d2l.ai/index.html - Dive into Deep Learning


import cv2
import mediapipe as mp

mp_drawing = mp.solutions.drawing_utils
mp_hands = mp.solutions.hands

cap = cv2.VideoCapture(0)

with mp_hands.Hands(min_detection_confidence=0.5, min_tracking_confidence=0.5) as hands:
    while cap.isOpened():
        success, image = cap.read()
        if not success:
            continue

        # Inverte a imagem para visualização de selfie e converte BGR para RGB
        image = cv2.cvtColor(cv2.flip(image, 1), cv2.COLOR_BGR2RGB)
        results = hands.process(image)
        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

        # Definindo a linha a 3/4 da altura da imagem
        linha_y = int(image.shape[0] * 0.75)
        cv2.line(image, (0, linha_y), (image.shape[1], linha_y), (255, 0, 0), 2)

        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                mp_drawing.draw_landmarks(image, hand_landmarks, mp_hands.HAND_CONNECTIONS)

                # Verificar cada ponto de referência dos dedos
                for landmark in hand_landmarks.landmark:
                    ponto_y = int(landmark.y * image.shape[0])
                    if ponto_y > linha_y:  # Verifica se o ponto passou da linha
                        print("Dedo passou da linha!")
                        break  # Opcional: interrompe o loop após a primeira detecção

        # Exibe a imagem processada
        cv2.imshow('Hand Recognition', image)
        if cv2.waitKey(5) & 0xFF == 27:
            break

cap.release()
cv2.destroyAllWindows()




