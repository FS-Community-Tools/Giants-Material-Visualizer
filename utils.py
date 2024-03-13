import logging
import bpy
from os import path


def print(*args):
    msg = ' '.join(map(str, args))
    logging.log(logging.WARNING, msg)


def get_i3dio():
    if 'i3dio' in bpy.context.preferences.addons:
        return True
    return False


def get_giants():
    if 'io_export_i3d_9_1_0' or 'io_export_i3d' in bpy.context.preferences.addons:
        return True
    return False


def import_shader():
    library = path.abspath(path.join(path.dirname(__file__), 'shader.blend'))
    filepath = path.join(library, 'NodeTree', 'FS22_colorMask')
    directory = path.join(library, 'NodeTree')
    bpy.ops.wm.append(
        filepath=filepath,
        filename='FS22_colorMask',
        directory=directory
    )


def update_material(self, context):
    if 'FS22_colorMask' not in bpy.data.node_groups:
        if context.active_object is not None:
            if context.active_object.mode == 'EDIT':
                bpy.ops.object.mode_set(mode='OBJECT')
                import_shader()
                bpy.ops.object.mode_set(mode='EDIT')
            else:
                import_shader()

    mat = context.material
    node_tree = mat.node_tree
    mat_output = node_tree.nodes.get('Material Output')
    principled = node_tree.nodes.get('Principled BSDF')
    if not principled or not mat_output:
        print('Material does not have Principled BSDF or Material Output node')
        return

    if self.enable_visualization:
        node = node_tree.nodes.new('ShaderNodeGroup')
        node.name = 'FS22_colorMask'
        node.label = 'FS22_colorMask'
        node.location = (750, 300)
        node.node_tree = bpy.data.node_groups.get('FS22_colorMask')

        node_tree.links.new(node.outputs[0], mat_output.inputs[0])

        principled = node_tree.nodes.get('Principled BSDF')
        if principled:
            diffuse = principled.inputs.get('Base Color')
            if diffuse.links:
                node_tree.links.new(node.inputs['Diffuse'], diffuse.links[0].from_socket)
                node.inputs['Use Diffuse Color'].default_value = False

            alpha = principled.inputs.get('Alpha')
            if alpha.links:
                node_tree.links.new(node.inputs['Alpha'], alpha.links[0].from_socket)

            normal = node_tree.nodes.get('Normal Map')
            if normal:
                normal_color = normal.inputs.get('Color')
                if normal_color.links:
                    node_tree.links.new(node.inputs['Normal'], normal_color.links[0].from_socket)

            glossmap = node_tree.nodes.get('Glossmap')
            if glossmap:
                node_tree.links.new(node.inputs['AO'], glossmap.outputs['Green'])

    else:
        node = node_tree.nodes.get('FS22_colorMask')
        if node:
            node_tree.nodes.remove(node)

        node_tree.links.new(principled.outputs[0], mat_output.inputs[0])


def check_material(context):
    if ((context.object is None
         and context.object.active_material is None)
            or not context.object.active_material.enable_visualization
            or not get_i3dio()):
        return False
    else:
        if context.object.active_material.i3d_attributes.source != '':
            valid_shader_variations = ('colorMask', 'Light')
            return any(variation in context.object.active_material.i3d_attributes.variation for variation in valid_shader_variations)
        return False


def set_data_i3dio(context):
    mat = context.object.active_material
    shader = mat.node_tree.nodes.get('FS22_colorMask')
    shader_parameters = mat.i3d_attributes.shader_parameters

    for i in range(2, 9):
        shader.inputs[f'colorMat{i - 2}'].default_value[:3] = shader_parameters[i].data_float_4[:3]
        shader.inputs[f'mat{i - 2}'].default_value = shader_parameters[i].data_float_4[3]


def get_data_i3dio(context):
    mat = context.object.active_material
    shader = mat.node_tree.nodes.get('FS22_colorMask')
    shader_parameters = mat.i3d_attributes.shader_parameters

    for i in range(2, 9):
        shader_parameters[i].data_float_4[:3] = shader.inputs[f'colorMat{i - 2}'].default_value[:3]
        shader_parameters[i].data_float_4[3] = shader.inputs[f'mat{i - 2}'].default_value
