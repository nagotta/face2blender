import cv2 as cv
import mediapipe as mp
import os
import glob

# face landmarksを画像上に出力するための準備
mp_drawing = mp.solutions.drawing_utils
drawing_spec = mp_drawing.DrawingSpec(thickness=1, circle_radius=1)
# face landmarksを取得するための準備
mp_face_mesh = mp.solutions.face_mesh
face_mesh = mp_face_mesh.FaceMesh(
    static_image_mode=True,
    max_num_faces=1,
    min_detection_confidence=0.5)

# 使用する画像のpathを取得してリスト化
resource_dir = r'./data'
file_list = glob.glob(os.path.join(resource_dir, "*.jpg"))  # 任意でjpg → pngに変更

# 保存先のディレクトリの作成
result_image_dir = 'result/image'
os.makedirs(result_image_dir, exist_ok=True)
result_txt_dir = 'result/txt'
os.makedirs(result_txt_dir, exist_ok=True)


for file_path in file_list:
    # 画像を読み込む
    image = cv.imread(file_path)
    height, width = image.shape[:2]
    # BGRをRGBに変える
    rgb_image = cv.cvtColor(image, cv.COLOR_BGR2RGB)
    # LandMark検出
    results = face_mesh.process(rgb_image)
    # 検出した点を出力した画像を作るためのコピーを保存
    annotated_image = image.copy()
    
    # 顔が検出されなければcontinue
    if not results.multi_face_landmarks:
        continue

    face_landmarks = results.multi_face_landmarks[0]

    file_path = os.path.splitext(file_path)[0]
    file_name = file_path.split('/')[-1]
    txtfile_path = result_txt_dir+'/'+file_name+'.txt'
    # テキストファイルにLandMarkを書き込む
    f = open(txtfile_path, 'w')
    f.write(str(face_landmarks))
    f.close()
    # LandMarkを出力した画像を生成
    mp_drawing.draw_landmarks(
        image=annotated_image,
        landmark_list=face_landmarks,
        connections=mp_face_mesh.FACEMESH_TESSELATION,
        landmark_drawing_spec=drawing_spec,
        connection_drawing_spec=drawing_spec)
    cv.imwrite(result_image_dir+'/'+file_name+'.png', annotated_image)

    #  以下よりデータ整合
    xyz_val_dir = 'result/val'
    os.makedirs(xyz_val_dir, exist_ok=True)
    i = 0
    count = 0
    fv = open(xyz_val_dir+'/'+file_name+'.txt', 'w')

    with open(txtfile_path) as ft:
        lines = ft.read()
        for l in lines.split("\n"):
            if i%5 == 0 or i%5 == 4:
                i += 1
                continue
            elif i%5 == 1:
                # x行の処理
                tmp = l.split()  # tmp[0]='x:' tmp[1]='0.…'(←LandMarkのx座標)
                x = f'{float(tmp[1]) *width:.5f}'
                count += 1
                fv.write(str(count)+','+str(x))
                
            elif i%5 == 2:
                # y行の処理
                tmp = l.split()
                y = f'{float(tmp[1]) *height:.5f}'
                fv.write(','+str(y))
                
            else:
                # z行の処理
                tmp = l.split()
                z = f'{float(tmp[1]) *width:.5f}'
                fv.write(','+str(z)+'\n')   
            i += 1
        fv.close()

face_mesh.close()