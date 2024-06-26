import cv2
import mediapipe as mp
import time
import py_faceMeshCut as fmc

mp_face_mesh = mp.solutions.face_mesh
mp_drawing = mp.solutions.drawing_utils

cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)

fourcc = cv2.VideoWriter_fourcc(*'XVID')
timestamp = time.strftime("%Y%m%d-%H%M%S")
root = f"datas/face-records/{timestamp}-facemesh.avi"
out = cv2.VideoWriter(root, fourcc, 20.0, (640, 480))

with mp_face_mesh.FaceMesh(
    static_image_mode=False,
    max_num_faces=10,
    min_detection_confidence=0.5) as face_mesh:
    while True:
        ret, frame = cap.read()
        old = frame
        if ret == False:
            break
        frame = cv2.flip(frame, 1)
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = face_mesh.process(frame_rgb)

        if results.multi_face_landmarks is not None:
            for face_landmarks in results.multi_face_landmarks:
                mp_drawing.draw_landmarks(
                    frame,
                    face_landmarks,
                    mp_face_mesh.FACEMESH_RIGHT_EYE,
                    mp_drawing.DrawingSpec(
                        color=(0,255,255),
                        thickness=1,
                        circle_radius=1
                    ),
                    mp_drawing.DrawingSpec(
                        color=(255,0,255),
                        thickness=1
                    ))

        out.write(frame)
        cv2.imshow("Frame", frame)
        f = cv2.waitKey(1) & 0xFF
        if f == ord('q') :
            timestamp = time.strftime("%Y%m%d-%H%M%S")
            filename = f"datas/face's/screen-vi-{timestamp}.jpg"
            filename1 = f"datas/face's/screen-vi-{timestamp}-mesh.jpg"
            cv2.imwrite(filename, frame)
            cv2.imwrite(filename1, old)
            fmc.meshCut(old,timestamp)
        if f == ord('w') :
            break

out.release()
cap.release()
cv2.destroyAllWindows()