bl_info = {
    "name": "JP Timber House Builder",
    "author": "OpenAI + Project Owner",
    "version": (0, 6, 0),
    "blender": (5, 0, 0),
    "location": "View3D > Sidebar > JP House",
    "description": "Japanese timber-house massing with DXF-ready plans and openings",
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
