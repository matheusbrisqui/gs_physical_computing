## BlackOutCare – Reconhecimento Corporal para Situações de Apagão

Guilherme Rezende Bezerra RM: 95808 ||
Gustavo Brisqui Martinez RM: 97969 ||
Matheus Brisqui Martinez RM: 97892 ||

## 🧠 Descrição do Problema

Durante apagões, muitas pessoas enfrentam dificuldades para pedir ajuda ou se locomover com segurança, principalmente em hospitais, centros de comando, residências com idosos ou pessoas com deficiência. Nessas situações, a falta de iluminação torna os métodos tradicionais de comunicação (voz, botão, telefone) menos acessíveis. Por isso, é necessário desenvolver uma alternativa tecnológica acessível, de fácil uso e sem dependência de hardware externo.

---

## 💡 Visão Geral da Solução

O **BlackOutCare** é um sistema de detecção de gestos de emergência com **MediaPipe Pose**, que utiliza a **webcam em tempo real** para identificar se o usuário levanta o braço acima do ombro — gesto que indica um pedido de ajuda.

Ao detectar esse gesto, o sistema dispara um **som de alerta**, permitindo que o usuário chame atenção em ambientes escuros ou em situações críticas durante uma falha de energia. A interface exibe o corpo com landmarks desenhados (pontos e conexões) em tempo real, facilitando a visualização da detecção.

Essa solução não requer sensores físicos como Arduino ou ESP32 — funciona apenas com software Python, uma webcam e luz ambiente mínima.

---

## 🧰 Tecnologias Utilizadas

- Python 3.11+
- OpenCV (processamento de vídeo)
- MediaPipe Pose (reconhecimento de pontos do corpo)
- Playsound (reprodução de som de alerta)

---

## Link do vídeo

 - https://youtu.be/BEhALLhySb0
---

## Código fonte
import cv2
import mediapipe as mp
from playsound import playsound
import threading

mp_pose = mp.solutions.pose
mp_drawing = mp.solutions.drawing_utils

def tocar_alerta():
    playsound('alerta.mp3')

def detectar_pose():
    cap = cv2.VideoCapture(0)

    with mp_pose.Pose(min_detection_confidence=0.7, min_tracking_confidence=0.7) as pose:
        alerta_disparado = False

        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                break

            dark_frame = cv2.convertScaleAbs(frame, alpha=0.6, beta=0)
            rgb = cv2.cvtColor(dark_frame, cv2.COLOR_BGR2RGB)
            result = pose.process(rgb)

            if result.pose_landmarks:
                mp_drawing.draw_landmarks(
                    dark_frame, result.pose_landmarks, mp_pose.POSE_CONNECTIONS
                )

                landmarks = result.pose_landmarks.landmark
                ombro_direito = landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER]
                mao_direita = landmarks[mp_pose.PoseLandmark.RIGHT_WRIST]

                # Verifica se os pontos estão confiáveis (visibilidade e valores válidos)
                if (ombro_direito.visibility > 0.5 and mao_direita.visibility > 0.5):
                    if mao_direita.y < ombro_direito.y:
                        if not alerta_disparado:
                            print("🚨 Gesto de emergência detectado (braço levantado)!")
                            threading.Thread(target=tocar_alerta).start()
                            alerta_disparado = True
                    else:
                        alerta_disparado = False

            cv2.imshow('SafeSign - Pose Estimation', dark_frame)
            if cv2.waitKey(10) & 0xFF == 27:
                break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    detectar_pose()
