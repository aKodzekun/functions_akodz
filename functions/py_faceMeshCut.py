import cv2
import mediapipe
import numpy as np
import pandas as pd

# Хүний нүүрэн хэсгийн тасдаж авах хэсэг
# img = cv2.imread("datas/face's/manFace.jpg")

def meshCut(img, dates) :
    # Нүүрний тэмдэглэгээ илрүүлэгчийг барих
    # Нүүрний тэмдэглэгээ илрүүлэгч загвар нь шийдлийн модулийн нүүрний торон объекттой ирдэг.
    # Илрүүлэгчийн объектыг бүтээсний дараа бид дүрсийг оролт болгон өгөх боломжтой.

    mp_face_mesh = mediapipe.solutions.face_mesh
    face_mesh = mp_face_mesh.FaceMesh(static_image_mode=True)

    # Илрүүлэгчийг ажиллуулах
    results = face_mesh.process(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
    landmarks = results.multi_face_landmarks[0]

    # Зууван нүүрэнд анхаарлаа хандуулна
    # MediaPipe нь 469 чухал цэгийг олдог боловч бид энэ судалгаанд зөвхөн нүүрний зууван цэгүүдэд анхаарлаа хандуулах болно.
    # Нүүрний торон объект нь тэмдэглэгээний цэгийн ангиллыг мөн хадгалдна
    face_oval = mp_face_mesh.FACEMESH_FACE_OVAL
    df = pd.DataFrame(list(face_oval), columns=["p1", "p2"])

    # Нүүрний зууван зураас захиалах
    # Харамсалтай нь нүүрний зууван шугамыг эрэмбэлдэггүй.
    # Бидэнд opencv-тэй зураг дээрх хэсгийг задлахад дараалсан шугамууд хэрэгтэй.
    routes_idx = []

    p1 = df.iloc[0]["p1"]
    p2 = df.iloc[0]["p2"]

    for i in range(0, df.shape[0]):
        # print(p1, p2)

        obj = df[df["p1"] == p2]
        p1 = obj["p1"].values[0]
        p2 = obj["p2"].values[0]

        route_idx = []
        route_idx.append(p1)
        route_idx.append(p2)
        routes_idx.append(route_idx)

    for route_idx in routes_idx:
        print(f"Draw a line between {route_idx[0]}th landmark point to {route_idx[1]}th landmark point")

    # Цэгүүдийн координатыг олно
    # Бид өмнөх хэсэгт урьдчилан тодорхойлсон маршрутуудыг захиалсан.
    # Цэг бүрийн координатыг олъё. Харьцангуй эх үүсвэр ба зорилт нь хэвийн бус координатуудыг хадгалах болно гэдгийг анхаарна
    routes = []

    for source_idx, target_idx in routes_idx:
        source = landmarks.landmark[source_idx]
        target = landmarks.landmark[target_idx]

        relative_source = (int(img.shape[1] * source.x), int(img.shape[0] * source.y))
        relative_target = (int(img.shape[1] * target.x), int(img.shape[0] * target.y))

        # cv2.line(img, relative_source, relative_target, (255, 255, 255), thickness = 2)

        routes.append(relative_source)
        routes.append(relative_target)

    # Нүүрний зууван хэлбэрийг гаргаж авах
    # Opencv-ийн дүүргэлтийн олон гишүүнт функц нь шугамын маршрутыг хүлээнэ
    # Бид үүнийг маршрутын жагсаалтад аль хэдийн хадгална
    # Нэмж дурдахад, тэг пиксел нь хар, 255 нь цагаан гэсэн утгатай тул бид маск объектод хар дүрсийг өгнө
    mask = np.zeros((img.shape[0], img.shape[1]))
    mask = cv2.fillConvexPoly(mask, np.array(routes), 1)
    mask = mask.astype(bool)

    out = np.zeros_like(img)
    out[mask] = img[mask]

    filename = f"datas/faces/face-cut-{dates}-mesh.jpg"
    cv2.imwrite(filename, out)

# cv2.imshow("Image",out)
# cv2.waitKey(0)
#
# cv2.destroyAllWindows()