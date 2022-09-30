import numpy as np
import bpy
filepath = r'C:/Users/ladyb/python/shellmag/result/np_save.npy'
xyzval = np.load(filepath)
ver_count = len(xyzval[0])
frame_count = len(xyzval)


def generate_ver(ver_count):
    print(ver_count)
    bpy.data.meshes.new(name='shellmag_Mesh')
    bpy.data.objects.new(name='shellmag_Obj', object_data=bpy.data.meshes['shellmag_Mesh'])
    bpy.context.scene.collection.objects.link(bpy.data.objects['shellmag_Obj'])
    Obj = bpy.data.objects['shellmag_Obj'].data
    Obj.vertices.add(ver_count)    
    return

def move_ver_anyframe(xyzval, frame_count):
    ob = bpy.data.objects['shellmag_Obj']
    for frame_num in range(frame_count):
        i = 0
        for p in xyzval[frame_num]:
            X = p[0]
            Y = p[1]
            Z = p[2]
            ver = ob.data.vertices[i]
            ver.co.x = X
            ver.co.y = Y
            ver.co.z = Z
            i += 1
            ver.keyframe_insert('co',index = -1,frame = frame_num)
            
    return

generate_ver(ver_count)
move_ver_anyframe(xyzval, frame_count)
