import bpy

bl_info = {
    "name": "FS Material Visualizer",
    "author": "LKAMinco",
    "description": "Addon provide visualisation for the Farming Simulator 22 UDIM system",
    "blender": (2, 80, 0),
    "location": "View3D",
    "warning": "",
    "category": "Generic"
}

classes = (
)

register, unregister = bpy.utils.register_classes_factory(classes)
