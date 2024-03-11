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
        import_shader()

    mat = context.material
    node_tree = mat.node_tree
    mat_output = node_tree.nodes.get('Material Output')
    principled = node_tree.nodes.get('Principled BSDF')
    if not principled or not mat_output:
        print('Material does not have Principled BSDF or Material Output node')
        return

    if self.enable_visualisation:
        node = node_tree.nodes.new('ShaderNodeGroup')
        node.name = 'FS22_colorMask'
        node.label = 'FS22_colorMask'
        node.location = (0, 0)
        node.node_tree = bpy.data.node_groups.get('FS22_colorMask')

        node_tree.links.new(node.outputs[0], mat_output.inputs[0])

        principled = node_tree.nodes.get('Principled BSDF')
        if principled:
            diffuse = principled.inputs.get('Base Color')
            if diffuse.links:
                node_tree.links.new(node.inputs['Diffuse'], diffuse.links[0].from_socket)
                node.inputs['Use Diffuse Color'].default_value = True

            alpha = principled.inputs.get('Alpha')
            if alpha.links:
                node_tree.links.new(node.inputs['Alpha'], alpha.links[0].from_socket)

            normal = principled.inputs.get('Normal')
            if normal.links:
                node_tree.links.new(node.inputs['Normal'], normal.links[0].from_socket)

            glossmap = node_tree.nodes.get('Glossmap')
            if glossmap:
                node_tree.links.new(node.inputs['AO'], glossmap.outputs['Green'])

    else:
        node = node_tree.nodes.get('FS22_colorMask')
        if node:
            node_tree.nodes.remove(node)

        node_tree.links.new(principled.outputs[0], mat_output.inputs[0])
