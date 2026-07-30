import bpy
from bpy.types import Operator

from .builders.floors import build_floors
from .builders.roof import build_roof
from .builders.walls import build_walls
from .utils.collections import clear_generated, ensure_collections


class JPTHB_OT_generate(Operator):
    bl_idname = "jp_thb.generate"
    bl_label = "Generate v0.4 House"
    bl_options = {"REGISTER", "UNDO"}

    def execute(self, context):
        clear_generated()
        collections = ensure_collections()
        props = context.scene.jp_thb
        build_floors(props, collections)
        build_walls(props, collections)
        build_roof(props, collections)
        self.report({"INFO"}, "JP Timber House v0.4 generated")
        return {"FINISHED"}


class JPTHB_OT_clear(Operator):
    bl_idname = "jp_thb.clear"
    bl_label = "Clear Generated House"
    bl_options = {"REGISTER", "UNDO"}

    def execute(self, context):
        clear_generated()
        return {"FINISHED"}


CLASSES = (JPTHB_OT_generate, JPTHB_OT_clear)


def register():
    for cls in CLASSES:
        bpy.utils.register_class(cls)


def unregister():
    for cls in reversed(CLASSES):
        bpy.utils.unregister_class(cls)
