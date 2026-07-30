import bpy
from bpy.types import Panel


class JPTHB_PT_main(Panel):
    bl_label = "JP Timber House Builder"
    bl_idname = "JPTHB_PT_main"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "JP House"

    def draw(self, context):
        layout = self.layout
        props = context.scene.jp_thb

        box = layout.box()
        box.label(text="Building")
        box.prop(props, "building_width_mm")
        box.prop(props, "building_depth_mm")
        box.prop(props, "foundation_height_mm")
        box.prop(props, "slab_thickness_mm")
        box.prop(props, "wall_thickness_mm")
        box.prop(props, "first_story_height_mm")
        box.prop(props, "second_story_height_mm")
        box.prop(props, "include_second_story")

        roof = layout.box()
        roof.label(text="Single-slope Roof")
        roof.prop(props, "roof_slope_percent")
        roof.prop(props, "roof_thickness_mm")
        roof.prop(props, "roof_overhang_mm")
        roof.prop(props, "slope_along_y")

        layout.operator("jp_thb.generate", icon="MOD_BUILD")
        layout.operator("jp_thb.clear", icon="TRASH")


CLASSES = (JPTHB_PT_main,)


def register():
    for cls in CLASSES:
        bpy.utils.register_class(cls)


def unregister():
    for cls in reversed(CLASSES):
        bpy.utils.unregister_class(cls)
