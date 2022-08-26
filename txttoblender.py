# オブジェクトモードでrun
import bpy
import os
import glob

valtxt_dir = r'D:/blender/Make_addon/tech'  # テキストデータを保存したフォルダのpathを指定する
txtfile_list = glob.glob(os.path.join(valtxt_dir, "*.txt"))

for txtfile_path in txtfile_list:

    # 生成する頂点の個数を取得
    f = open(txtfile_path, 'r', encoding='utf-8')
    count = 1
    line = f.readline()
    while line:
        line = f.readline().replace('\n', '')
        count += 1
    f.close()

    # オブジェクト名の指定と頂点群の生成
    file_path = os.path.splitext(txtfile_path)[0]
    face_name = file_path.split('/')[-1]
    bpy.data.meshes.new(name=face_name+'Mesh')
    bpy.data.objects.new(name=face_name+'Obj', object_data=bpy.data.meshes[face_name+'Mesh'])
    bpy.context.scene.collection.objects.link(bpy.data.objects[face_name+'Obj'])
    Obj = bpy.data.objects[face_name+'Obj'].data
    Obj.vertices.add(count)

    # 取得した座標に頂点群を移動
    i = 0
    f = open(txtfile_path)
    line = f.readline()
    while line:
        d = line.split(',')
        X = float(d[1])
        Y = float(d[2])
        Z = float(d[3])
        Obj.vertices[i].co.x = X
        Obj.vertices[i].co.y = Y
        Obj.vertices[i].co.z = Z
        line = f.readline().replace('\n', '')
        i += 1
    f.close()