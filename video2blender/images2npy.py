import cv2 as cv
import mediapipe as mp
import os
import glob
import numpy as np

def get_landmark(image, file_path):
    # face landmarksを取得するための準備
    mp_face_mesh = mp.solutions.face_mesh
    face_mesh = mp_face_mesh.FaceMesh(
        static_image_mode=True,
        max_num_faces=1,
        min_detection_confidence=0.5)
    rgb_image = cv.cvtColor(image, cv.COLOR_BGR2RGB)
    # LandMark検出
    results = face_mesh.process(rgb_image)
    # 顔が検出されなければcontinue
    if not results.multi_face_landmarks:
        exit()
    face_landmarks = results.multi_face_landmarks[0]
    file_path = os.path.splitext(file_path)[0]
    file_name = file_path.split('/')[-1]
    # 保存先のフォルダ作成
    result_txt_dir = 'result/txt'
    os.makedirs(result_txt_dir, exist_ok=True)
    txtfile_path = result_txt_dir+'/'+file_name+'.txt'
    # テキストファイルにLandMarkを書き込む
    f = open(txtfile_path, 'w')
    f.write(str(face_landmarks))
    f.close()
    make_landmarkimg(image, face_landmarks, file_name, mp_face_mesh)
    face_mesh.close()
    return get_original_scalexyz(image, txtfile_path)

def make_landmarkimg(image, face_landmarks, file_name, mp_face_mesh):
    result_image_dir = 'result/image'
    os.makedirs(result_image_dir, exist_ok=True)
    # face landmarksを画像上に出力するための準備
    mp_drawing = mp.solutions.drawing_utils
    drawing_spec = mp_drawing.DrawingSpec(thickness=1, circle_radius=3)
    # 検出した点を出力した画像を作るためのコピーを保存
    annotated_image = image.copy()
    # LandMarkを出力した画像を生成
    mp_drawing.draw_landmarks(
        image=annotated_image,
        landmark_list=face_landmarks,
        connections=mp_face_mesh.FACEMESH_TESSELATION,
        landmark_drawing_spec=drawing_spec,
        connection_drawing_spec=drawing_spec)
    cv.imwrite(result_image_dir+'/'+file_name+'.png', annotated_image)

def get_original_scalexyz(image, txtfile_path):
    height, width = image.shape[:2]
    vers = []
    i = 0
    with open(txtfile_path) as ft:
        lines = ft.read()
        for l in lines.split("\n"):
            if i%5 == 0 or i%5 == 4:
                i += 1
                continue
            elif i%5 == 1:
                tmp = l.split()  
                x = f'{float(tmp[1]) *width:.5f}'
            elif i%5 == 2:
                tmp = l.split()
                y = f'{float(tmp[1]) *height:.5f}'
            else:
                tmp = l.split()
                z = f'{float(tmp[1]) *width:.5f}'
                vers.append([float(x), float(y), float(z)])
            i += 1
    return vers

# 使用する画像のpathを取得してリスト化
resource_dir = r'./image'
file_list = glob.glob(os.path.join(resource_dir, "*.jpg"))
xyzval = []
for file_path in file_list:
    # 画像を読み込む
    image = cv.imread(file_path)
    xyzval.append(get_landmark(image, file_path))
np.save('result/np_save', xyzval)
