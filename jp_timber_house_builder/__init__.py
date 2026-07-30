bl_info = {
    "name": "JP Timber House Builder",
    "author": "OpenAI + Project Owner",
    "version": (0, 4, 0),
    "blender": (5, 0, 0),
    "location": "View3D > Sidebar > JP House",
    "description": "Parameterized Japanese timber-house massing generator",
    "category": "Add Mesh",
}

from . import operators, panel, properties


def register():
    properties.register()
    operators.register()
    panel.register()


def unregister():
    panel.unregister()
    operators.unregister()
    properties.unregister()
