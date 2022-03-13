bl_info = {
    "name": "convex_hull2D",
    "author": "your_name",
    "blender": (2, 80, 0),
    "location": "View3D > Sidebar > My own addon",
    "description": "whats this?",
    "warning": "",
    "wiki_url": "",
    "category": "3D View"}
#------------------------------------------------------------#

import bpy
import bmesh
import random 
import enum
import numpy as np

def get_mesh():
    obj = bpy.context.object.data
    if bpy.context.mode == 'EDIT_MESH':
        bm = bmesh.from_edit_mesh(obj)

    else:
        # Get a BMesh representation
        bm = bmesh.new()   # create an empty BMesh
        bm.from_mesh(obj)   # fill it in from a Mesh
        bm.verts.ensure_lookup_table()
    return bm,obj       
def update_mesh(bm,obj):
    bm.verts.ensure_lookup_table()

    if bpy.context.mode == 'EDIT_MESH':
        bmesh.update_edit_mesh(obj)
    
    else:
        # Finish up, write the bmesh back to the mesh
        bm.to_mesh(obj)
        bm.free()  # free and prevent further access         
    
    obj.update()

class Ori(enum.Enum):
   cw = -1
   lin = 0
   ccw = 1

class Point:
    def __init__(self,v:bmesh.types.BMVert):
        self.v:bmesh.types.BMVert = v
        self.cw = None
        self.ccw = None

    def __eq__(self, p):
            return self.v.co.x == p.v.co.x and self.v.co.y == p.v.co.y

    @staticmethod
    def orientation(p1,p2,p3):
        diff = (p2.v.co.y - p1.v.co.y) * (p3.v.co.x - p2.v.co.x) - (p2.v.co.x - p1.v.co.x) * (p3.v.co.y - p2.v.co.y) 
        return Ori(np.sign(diff))


class ConvexHull(bpy.types.Operator):
    bl_idname = "myaddon.convex2d"
    bl_label = "CH"
    bl_description = ""

    def execute(self, context):

        bm,obj=get_mesh()
        #change mesh here
        bm.verts.sort(key= lambda p:p.co.x)
        bm.verts.index_update()
        bm.verts.ensure_lookup_table()

        points = []
        for v in bm.verts:
            points.append(Point(v)) 
            self.report({'INFO'}, f"vv:{v.index}" )  

        indices = self.process(points)
        self.report({'INFO'}, f"{indices}" )               

        self.connect_points(indices,bm)

        update_mesh(bm,obj)
        self.report({'INFO'}, "Done" )               
        return {'FINISHED'}
    
    def connect_points(self,indices,bm:bmesh.types.BMesh):
        for e in bm.edges:
            bm.edges.remove(e)
        v_start = bm.verts[indices[0].v.index]
        v_last = bm.verts[indices[-1].v.index]
        bm.edges.new([v_start,v_last])

        for i in range(len(indices)-1):
            p = bm.verts[indices[i].v.index]
            q = bm.verts[indices[i+1].v.index]
            bm.edges.new([p,q])

    
    def process(self,points):
        return points
    
    #left and right is an array of type Point defined above
    def merge(self,left,right):
        # hint: to access actual cordinates of a vertex:
        # Point has a attribute v and v has atribute co and in there you can find x,y
        # so like this: p.v.co.x
        pass


class RandomPoints(bpy.types.Operator):
    bl_idname = "myaddon.randompoints"
    bl_label = "Randomize"
    bl_description = ""

    def clear_mesh(self,bm):
        for item in bm.verts:
            bm.verts.remove(item)
        
    
    def randomize(self,bm,size):
        for i in range(size):
            x , y = random.uniform(-10,10) , random.uniform(-10,10)
            bm.verts.new( [x,y,0] ) 
           
    def execute(self, context):            
        scene = context.scene
        my_prop_tool = scene.my_tool
        size = my_prop_tool.int_value

        bm,obj=get_mesh()
        self.report({'INFO'}, f"{size}" ) 
        
        self.clear_mesh(bm)
        
        self.randomize(bm,size)        

        update_mesh(bm,obj)
        return {'FINISHED'}

class MyPanel(bpy.types.Panel):
    bl_label = "Buttons"
    bl_category = "convex hull"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
   
    def draw(self, context):
        layout = self.layout
        scene = context.scene
        my_prop_tool = scene.my_tool
        
        row = layout.row()
        row.scale_y = 2
        row.operator(RandomPoints.bl_idname,text="Randomize")   
        
        row = layout.row()
        row.prop(my_prop_tool,"int_value")
        
        row = layout.row()
        row.operator(ConvexHull.bl_idname,text="Process")
        
        
         
        
class MyProperty(bpy.types.PropertyGroup):
    int_value:bpy.props.IntProperty(name="points",min=2,max=200,default=4)
    


#----------------registration----------------#

classes = (MyProperty,ConvexHull,RandomPoints, MyPanel)


def register():
    for cls in classes:
        bpy.utils.register_class(cls)
        
        bpy.types.Scene.my_tool = bpy.props.PointerProperty(type=MyProperty)

def unregister():
    for cls in classes:
        bpy.utils.unregister_class(cls)
    
    del bpy.types.Scene.my_tool
        
if __name__ == "__main__":
     register()
     
#https://github.com/Korchy/blender_autocomplete