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