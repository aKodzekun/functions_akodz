import cv2
import mediapipe as mp
# Хүний нүүрэнд маск тавина.

mp_face_mesh = mp.solutions.face_mesh
mp_drawing = mp.solutions.drawing_utils

with mp_face_mesh.FaceMesh(
    static_image_mode=True,
    max_num_faces=10,
    min_detection_confidence=0.5
) as face_mesh :
    image = cv2.imread("datas/face's/manFace.jpg")

    height, width, _ = image.shape
    image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    result = face_mesh.process(image_rgb)
    print(result.multi_face_landmarks)

    if result.multi_face_landmarks is not None :
        for face_landmarks in result.multi_face_landmarks :
            mp_drawing.draw_landmarks(
                image,
                face_landmarks,
                mp_face_mesh.FACEMESH_CONTOURS,
                mp_drawing.DrawingSpec(
                    color=(0,255,255),
                    thickness=1,
                    circle_radius=1
                ),
                mp_drawing.DrawingSpec(
                    color=(255,0,255),
                    thickness=1
                )
            )

    cv2.imshow("Image",image)
    cv2.waitKey(0)

cv2.destroyAllWindows()