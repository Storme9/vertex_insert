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
import mathutils

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
        default = 1,
        )
        
# ------------------------------------------------------------------------
#    Operators
# ------------------------------------------------------------------------

#First operator.
class OBJECT_OT_first_vertices(Operator):
    bl_label = "From first selected vertices"
    bl_idname = "object.first_vertices"

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
        check = int
        check = verticesDefine()
        count = check
        
        if (check >= 2 and check%2 ==0):            
                        
#Remove mesh data of deleted objects.            
            for block in bpy.data.meshes:
                if block.users == 0:
                    bpy.data.meshes.remove(block)

#Remember selected object's name.
            selected_name = bpy.context.selected_objects

#Create an object with the initially selected object's name (to remember).
            ob_name = bpy.context.scene.objects[selected_name[0].name]   

#Save world values.
            ob_x_scale = bpy.context.object.scale[0]
            ob_y_scale = bpy.context.object.scale[1]
            ob_z_scale = bpy.context.object.scale[2]

            location_x = bpy.context.object.location[0]
            location_y = bpy.context.object.location[1]
            location_z = bpy.context.object.location[2]
            
#Create list of coordinates of selected points.
            obj = bpy.context.object
            data = obj.data
            bm = bmesh.from_edit_mesh(data)

            z = [s.co for s in bm.select_history if isinstance(s, bmesh.types.BMVert)]
            
            v = []          
            for x in z:
                v.append(mathutils.Vector((((x[0]*ob_x_scale) + location_x),((x[1]*ob_y_scale) + location_y),((x[2]*ob_z_scale) + location_z))))
            print(v)
                                  
#Save the distance property.            
            scene = context.scene
            mytool = scene.my_tool
                        
            a = mytool.distance

#Direction vectors. 
            Directional_Vectors = []
            i = 0
            
            while (i < check):
                V = v[i + 1] - v[i]
                Directional_Vectors.append(V)
                i = i + 2
                  
#Position of vertex to be created.
            positions = []
            i = 0
            j = 0
            
            while (count > 0):
                b = v[j] + ((a / sqrt(Directional_Vectors[i][0]**2 + Directional_Vectors[i][1]**2 + Directional_Vectors[i][2]**2)) * Directional_Vectors[i])
                positions.append(b)
                i = i + 1
                j = j + 2
                count = count - 2
                           
#Create new vertex.             
            bpy.ops.object.mode_set(mode='OBJECT') 
            mesh = bpy.data.meshes.new("newMesh")  # add the new mesh
            obj = bpy.data.objects.new(mesh.name, mesh)
            col = bpy.data.collections.get("Collection")
            col.objects.link(obj)
            bpy.context.view_layer.objects.active = obj

            verts = []            
            for x in positions:
                verts.append((x[0],x[1],x[2]))
            edges = []
            faces = []

            mesh.from_pydata(verts, edges, faces)

#Deselect all objects.            
            bpy.ops.object.select_all(action='DESELECT')

#Select initially selected object.            
            bpy.data.objects[selected_name[0].name].select_set(True)

#Join the created vertex and the initially selected object.    
            
            q = [bpy.context.selected_objects[0], bpy.data.objects['newMesh']]
            
            q[0].select_set(True)
            q[1].select_set(True)
            
            bpy.context.view_layer.objects.active = q[0]
            
            bpy.ops.object.join()          

#Make the initially selected object active, select it and enter edit mode.
            bpy.ops.object.select_all(action='DESELECT')
            bpy.context.view_layer.objects.active = ob_name   # Make the cube the active object 
            ob_name.select_set(True)  
            bpy.ops.object.editmode_toggle()

        else:
            print("Select 2 vertices")
        return {"FINISHED"}

#Second operator.        
class OBJECT_OT_both_vertices(Operator):
    bl_label = "From both selected vertices"
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
        check = int
        check = verticesDefine()
        count = check
        
        if (check >= 2 and check%2 ==0):            
                        
#Remove mesh data of deleted objects.            
            for block in bpy.data.meshes:
                if block.users == 0:
                    bpy.data.meshes.remove(block)

#Remember selected object's name.
            selected_name = bpy.context.selected_objects

#Create an object with the initially selected object's name (to remember).
            ob_name = bpy.context.scene.objects[selected_name[0].name]   

#Save world values.
            ob_x_scale = bpy.context.object.scale[0]
            ob_y_scale = bpy.context.object.scale[1]
            ob_z_scale = bpy.context.object.scale[2]

            location_x = bpy.context.object.location[0]
            location_y = bpy.context.object.location[1]
            location_z = bpy.context.object.location[2]
            
#Create list of coordinates of selected points.
            obj = bpy.context.object
            data = obj.data
            bm = bmesh.from_edit_mesh(data)

            z = [s.co for s in bm.select_history if isinstance(s, bmesh.types.BMVert)]
            print(z)
            v = []          
            for x in z:
                v.append(mathutils.Vector((((x[0]*ob_x_scale) + location_x),((x[1]*ob_y_scale) + location_y),((x[2]*ob_z_scale) + location_z))))
                       
#Save the distance property.            
            scene = context.scene
            mytool = scene.my_tool
                        
            a = mytool.distance

#Direction vectors. 
            Directional_Vectors_0 = []
            Directional_Vectors_1 = []
            i = 0
            
            while (i < check):
                V0 = v[i + 1] - v[i]
                V1 = v[i] - v[i + 1]
                Directional_Vectors_0.append(V0)
                Directional_Vectors_1.append(V1)
                i = i + 2
                  
#Position of vertex to be created.
            positions = []
            i = 0
            j = 0
            
            while (count > 0):
                new_point_0 = v[j] + ((a / sqrt(Directional_Vectors_0[i][0]**2 + Directional_Vectors_0[i][1]**2 + Directional_Vectors_0[i][2]**2)) * Directional_Vectors_0[i])
                new_point_1 = v[j+1] + ((a / sqrt(Directional_Vectors_1[i][0]**2 + Directional_Vectors_1[i][1]**2 + Directional_Vectors_1[i][2]**2)) * Directional_Vectors_1[i])

                positions.append(new_point_0)
                positions.append(new_point_1)
                i = i + 1
                j = j + 2
                count = count - 2
                           
#Create new vertex.             
            bpy.ops.object.mode_set(mode='OBJECT') 
            mesh = bpy.data.meshes.new("newMesh")  # add the new mesh
            obj = bpy.data.objects.new(mesh.name, mesh)
            col = bpy.data.collections.get("Collection")
            col.objects.link(obj)
            bpy.context.view_layer.objects.active = obj

            verts = []            
            for x in positions:
                verts.append((x[0],x[1],x[2]))
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

#Make the initially selected object active, select it and enter edit mode.
            bpy.ops.object.select_all(action='DESELECT')
            bpy.context.view_layer.objects.active = ob_name   # Make the cube the active object 
            ob_name.select_set(True)  
            bpy.ops.object.editmode_toggle()

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
        layout.operator("object.first_vertices")
        layout.operator("object.both_vertices")

# ------------------------------------------------------------------------
#    Registration
# ------------------------------------------------------------------------

classes = (
    Property,
    OBJECT_OT_first_vertices,
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