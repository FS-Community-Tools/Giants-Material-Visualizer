import bpy
from bpy.types import Operator, Panel
from .utils import *


class MatVis_OT_GetData(Operator):
    bl_idname = "matvis.get"
    bl_label = "Get data from visualizer"
    bl_description = "Get data from visualizer into shader that will be exported"
    bl_options = {'REGISTER', 'UNDO'}

    @classmethod
    def poll(cls, context):
        if (context.object is not None
                and context.object.active_material is not None
                and context.material.enable_visualization
                and get_i3dio()):
            return 'colorMask' in context.object.active_material.i3d_attributes.variation
        return False

    def execute(self, context):
        return {'FINISHED'}


class MatVis_OT_SetData(Operator):
    bl_idname = "matvis.set"
    bl_label = "Set data to visualizer"
    bl_description = "Set data to visualizer from shader that will be exported"
    bl_options = {'REGISTER', 'UNDO'}

    @classmethod
    def poll(cls, context):
        if (context.object is not None
                and context.object.active_material is not None
                and context.material.enable_visualization
                and get_i3dio()):
            return 'colorMask' in context.object.active_material.i3d_attributes.variation
        return False

    def execute(self, context):
        return {'FINISHED'}


class MatVis_PT_I3DioPanel(Panel):
    bl_idname = "MatVis_PT_I3DioPanel"
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
        mat = context.material
        row = layout.row(align=True)
        row.prop(context.material, 'enable_visualization', text="Enable Visualization", icon='SHADING_SOLID' if context.material.enable_visualization else 'SHADING_RENDERED', toggle=True)
        row.prop(context.scene, 'real_time_visualization', text="", toggle=True, icon='PAUSE' if context.scene.real_time_visualization else 'PLAY')

        row = layout.row(align=True)
        row.operator("matvis.get", text="Get", icon='IMPORT')
        row.operator("matvis.set", text="Set", icon='EXPORT')
