# ------------------------------------------------------------------------
#    Setup
# ------------------------------------------------------------------------

bl_info = {
    "name": "Vertex Insert",
    "description": "Inserts a vertex or vertices between an even number of selected vertices",
    "author": "storme",
    "version": (1),
    "blender": (3, 2, 1),
    "warning": "arrays do not exist within blender and so the code is not effecient - this is highly annoying"
}

import bpy
import bmesh

from bpy.props import (StringProperty,
                       BoolProperty,
                       IntProperty,
                       FloatProperty,
                       FloatVectorProperty,
                       EnumProperty,
                       PointerProperty,
                       )
                       
from bpy.types import (Panel,
                       Menu,
                       Operator,
                       PropertyGroup,
                       )

from math import sqrt

def verticesDefine():
    
    bpy.ops.object.mode_set(mode='OBJECT') 
    bpy.ops.object.mode_set(mode='EDIT')
    
    count = 0

    verts = bpy.context.active_object.data.vertices 

    for i in verts:
        if (i.select == True):
            count = count + 1
               
    return(count)

# ------------------------------------------------------------------------
#    Properties
# ------------------------------------------------------------------------

class Property(PropertyGroup):

    distance : FloatProperty(
        name = "distance",
        description = "The distance from a selected vertex that a new vertex will be created",
        default = 23.7,
        )
        
# ------------------------------------------------------------------------
#    Operators
# ------------------------------------------------------------------------

#First operator.
class OBJECT_OT_one_vertex(Operator):
    bl_label = "Create from one vertex"
    bl_idname = "object.one_vertex"

# Check that I am in edit mode:
    @classmethod
    def poll(cls, context):
        return (bpy.context.active_object.mode == 'EDIT') 
    
# Check that I am in vertex mode:
    @classmethod
    def poll(cls, context):
        return (bpy.context.tool_settings.mesh_select_mode[:][0] == True)

# Insert vertices if 2 vertices are selected:
    def execute(self, context):
        check = verticesDefine()
        
        if (check == 2):
                        
#Remove mesh data of deleted objects.            
            for block in bpy.data.meshes:
                if block.users == 0:
                    bpy.data.meshes.remove(block)

#Remember name of selected object.            
            selected_name = bpy.context.selected_objects
 
#Create list of coordinates of selected points.
            ob = bpy.context.active_object
            bm = bmesh.from_edit_mesh(ob.data)

            points = []
            
            for v in bm.verts:
                if (v.select == True):
                    obMat = ob.matrix_world
                    points.append(obMat @ v.co)

#Save the distance property.            
            scene = context.scene
            mytool = scene.my_tool
                        
            a = mytool.distance

#Direction vector.            
            V = points[1] - points[0]

            bpy.ops.object.mode_set(mode='OBJECT') 

#Position of vertex to be created.            
            new_point = points[0] + (a/sqrt((V[0])**2+(V[1])**2+(V[2])**2))*V
            
#Create new vertex.             
            mesh = bpy.data.meshes.new("newMesh")  # add the new mesh
            obj = bpy.data.objects.new(mesh.name, mesh)
            col = bpy.data.collections.get("Collection")
            col.objects.link(obj)
            bpy.context.view_layer.objects.active = obj

            verts = [(new_point[0], new_point[1], new_point[2])]  # 4 verts made with XYZ coords
            edges = []
            faces = []

            mesh.from_pydata(verts, edges, faces)

#Deselect all objects.            
            bpy.ops.object.select_all(action='DESELECT')
 
#Select initially selected object.            
            bpy.data.objects[selected_name[0].name].select_set(True)

#Join the created vertex and the initially selected object.            
            q = [bpy.context.selected_objects[0], bpy.data.objects['newMesh']]

            ctx = bpy.context.copy()

            ctx['active_object'] = q[0]

            ctx['selected_editable_objects'] = q 

            bpy.ops.object.join(ctx)            

        else:
            print("Select 2 vertices")
        return {"FINISHED"}

#Second operator.        
class OBJECT_OT_other_vertex(Operator):
    bl_label = "Create from other vertex"
    bl_idname = "object.other_vertex"
        
# Check that I am in edit mode:

    @classmethod
    def poll(cls, context):
        return (bpy.context.active_object.mode == 'EDIT') 
    
# Check that I am in vertex mode:

    @classmethod
    def poll(cls, context):
        return (bpy.context.tool_settings.mesh_select_mode[:][0] == True)

# Insert vertices if 2 vertices are selected:

    def execute(self, context):
        check = verticesDefine()
        
        if (check == 2):
            
            
#Remove mesh data of deleted objects.            
            for block in bpy.data.meshes:
                if block.users == 0:
                    bpy.data.meshes.remove(block)

#Remember name of selected object.            
            selected_name = bpy.context.selected_objects
 
#Create list of coordinates of selected points.
            ob = bpy.context.active_object
            bm = bmesh.from_edit_mesh(ob.data)

            points = []
            
            for v in bm.verts:
                if (v.select == True):
                    obMat = ob.matrix_world
                    points.append(obMat @ v.co)

#Save the distance property.            
            scene = context.scene
            mytool = scene.my_tool
                        
            a = mytool.distance

#Direction vector.            
            V = points[0] - points[1]

            bpy.ops.object.mode_set(mode='OBJECT') 

#Position of vertex to be created.            
            new_point = points[1] + (a/sqrt((V[0])**2+(V[1])**2+(V[2])**2))*V
            
#Create new vertex.             
            mesh = bpy.data.meshes.new("newMesh")  # add the new mesh
            obj = bpy.data.objects.new(mesh.name, mesh)
            col = bpy.data.collections.get("Collection")
            col.objects.link(obj)
            bpy.context.view_layer.objects.active = obj

            verts = [(new_point[0], new_point[1], new_point[2])]  # 4 verts made with XYZ coords
            edges = []
            faces = []

            mesh.from_pydata(verts, edges, faces)

#Deselect all objects.            
            bpy.ops.object.select_all(action='DESELECT')
 
#Select initially selected object.            
            bpy.data.objects[selected_name[0].name].select_set(True)

#Join the created vertex and the initially selected object.            
            q = [bpy.context.selected_objects[0], bpy.data.objects['newMesh']]

            ctx = bpy.context.copy()

            ctx['active_object'] = q[0]

            ctx['selected_editable_objects'] = q 

            bpy.ops.object.join(ctx) 

        else:
            print("Select 2 vertices")
        return {"FINISHED"}
                
#Third operator.        
class OBJECT_OT_both_vertices(Operator):
    bl_label = "Create 2 vertices"
    bl_idname = "object.both_vertices"

# Check that I am in edit mode:

    @classmethod
    def poll(cls, context):
        return (bpy.context.active_object.mode == 'EDIT') 
    
# Check that I am in vertex mode:

    @classmethod
    def poll(cls, context):
        return (bpy.context.tool_settings.mesh_select_mode[:][0] == True)

# Insert vertices if 2 vertices are selected:

    def execute(self, context):
        check = verticesDefine()
        
        if (check == 2):
            
            
#Remove mesh data of deleted objects.            
            for block in bpy.data.meshes:
                if block.users == 0:
                    bpy.data.meshes.remove(block)

#Remember name of selected object.            
            selected_name = bpy.context.selected_objects
 
#Create list of coordinates of selected points.
            ob = bpy.context.active_object
            bm = bmesh.from_edit_mesh(ob.data)

            points = []
            
            for v in bm.verts:
                if (v.select == True):
                    obMat = ob.matrix_world
                    points.append(obMat @ v.co)

#Save the distance property.            
            scene = context.scene
            mytool = scene.my_tool
                        
            a = mytool.distance

#Direction vector.            
            V0 = points[1] - points[0]
            V1 = points[0] - points[1]

            bpy.ops.object.mode_set(mode='OBJECT') 

#Position of vertex to be created.            
            new_point_0 = points[0] + (a/sqrt((V0[0])**2+(V0[1])**2+(V0[2])**2))*V0
            new_point_1 = points[1] + (a/sqrt((V1[0])**2+(V1[1])**2+(V1[2])**2))*V1            
            
#Create new vertex.             
            mesh = bpy.data.meshes.new("newMesh")  # add the new mesh
            obj = bpy.data.objects.new(mesh.name, mesh)
            col = bpy.data.collections.get("Collection")
            col.objects.link(obj)
            bpy.context.view_layer.objects.active = obj

            verts = [(new_point_0[0], new_point_0[1], new_point_0[2]), (new_point_1[0], new_point_1[1], new_point_1[2])]
            edges = []
            faces = []

            mesh.from_pydata(verts, edges, faces)

#Deselect all objects.            
            bpy.ops.object.select_all(action='DESELECT')
 
#Select initially selected object.            
            bpy.data.objects[selected_name[0].name].select_set(True)

#Join the created vertex and the initially selected object.            
            q = [bpy.context.selected_objects[0], bpy.data.objects['newMesh']]

            ctx = bpy.context.copy()

            ctx['active_object'] = q[0]

            ctx['selected_editable_objects'] = q 

            bpy.ops.object.join(ctx)

        else:
            print("Select 2 vertices")
        return {"FINISHED"}
        
# ------------------------------------------------------------------------
#    Panel in Object Mode
# ------------------------------------------------------------------------

class PANEL_PT_main_panel(Panel):
    bl_label = "Tool"
    bl_idname = "PANEL_PT_main_panel"
    bl_space_type = "VIEW_3D"   
    bl_region_type = "UI"
    bl_category = "Insert"   


    def draw(self, context):
        layout = self.layout
        scene = context.scene
        mytool = scene.my_tool

        layout.prop(mytool, "distance")
        layout.operator("object.one_vertex")
        layout.operator("object.other_vertex")
        layout.operator("object.both_vertices")

# ------------------------------------------------------------------------
#    Registration
# ------------------------------------------------------------------------

classes = (
    Property,
    OBJECT_OT_one_vertex,
    OBJECT_OT_other_vertex,
    OBJECT_OT_both_vertices,
    PANEL_PT_main_panel   
)

def register():
    from bpy.utils import register_class
    for cls in classes:
        register_class(cls)

    bpy.types.Scene.my_tool = PointerProperty(type=Property)

def unregister():
    from bpy.utils import unregister_class
    for cls in reversed(classes):
        unregister_class(cls)
    del bpy.types.Scene.my_tool


if __name__ == "__main__":
    register()