import bpy
from bpy.types import Operator, Panel
from .utils import *
from bpy.app.handlers import persistent


@persistent
def validate_material(dummy):
    if bpy.context.object is None:
        return
    if bpy.context.object.active_material is None:
        return
    mat = bpy.context.object.active_material
    if mat.enable_visualization:
        if 'FS22_colorMask' not in mat.node_tree.nodes:
            mat.enable_visualization = False


def real_time_update(dummy):
    if not bpy.context.scene.real_time_update:
        return

    if check_material(bpy.context):
        get_data_i3dio(bpy.context)


bpy.app.handlers.depsgraph_update_post.append(validate_material)
bpy.app.handlers.depsgraph_update_post.append(real_time_update)


class MATVIS_OT_GetData(Operator):
    bl_idname = "matvis.get"
    bl_label = "Get data from visualizer"
    bl_description = "Get data from visualizer into shader that will be exported"
    bl_options = {'REGISTER', 'UNDO'}

    @classmethod
    def poll(cls, context):
        return check_material(context)

    def execute(self, context):
        get_data_i3dio(context)
        return {'FINISHED'}


class MATVIS_OT_SetData(Operator):
    bl_idname = "matvis.set"
    bl_label = "Set data to visualizer"
    bl_description = "Set data to visualizer from shader that will be exported"
    bl_options = {'REGISTER', 'UNDO'}

    @classmethod
    def poll(cls, context):
        return check_material(context)

    def execute(self, context):
        set_data_i3dio(context)
        return {'FINISHED'}


class MATVIS_PT_I3DioPanel(Panel):
    bl_idname = "MATVIS_PT_I3DioPanel"
    bl_label = "Material Visualizer"
    bl_space_type = 'PROPERTIES'
    bl_region_type = 'WINDOW'
    bl_category = 'Material'
    bl_context = 'material'

    @classmethod
    def poll(cls, context):
        return context.object is not None and context.object.active_material is not None

    def draw(self, context):
        layout = self.layout
        row = layout.row(align=True)
        row.prop(context.material, 'enable_visualization', text="Enable Visualization", icon='SHADING_SOLID' if context.material.enable_visualization else 'SHADING_RENDERED', toggle=True)
        row.prop(context.scene, 'real_time_update', text="", toggle=True, icon='PAUSE' if context.scene.real_time_update else 'PLAY')

        row = layout.row(align=True)
        row.operator("matvis.get", text="Get", icon='IMPORT')
        row.operator("matvis.set", text="Set", icon='EXPORT')
