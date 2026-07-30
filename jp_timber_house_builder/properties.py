import bpy
from bpy.props import BoolProperty, FloatProperty, PointerProperty
from bpy.types import PropertyGroup


class JPTHBProperties(PropertyGroup):
    building_width_mm: FloatProperty(
        name="Width",
        description="Building width in millimeters",
        default=9100.0,
        min=1000.0,
    )
    building_depth_mm: FloatProperty(
        name="Depth",
        description="Building depth in millimeters",
        default=6370.0,
        min=1000.0,
    )
    foundation_height_mm: FloatProperty(name="Foundation", default=600.0, min=0.0)
    slab_thickness_mm: FloatProperty(name="Slab thickness", default=150.0, min=20.0)
    wall_thickness_mm: FloatProperty(name="Wall thickness", default=125.0, min=40.0)
    first_story_height_mm: FloatProperty(name="First story", default=2735.0, min=1800.0)
    second_story_height_mm: FloatProperty(name="Second story", default=3200.0, min=1800.0)
    roof_slope_percent: FloatProperty(name="Roof slope %", default=2.5, min=-30.0, max=30.0)
    roof_thickness_mm: FloatProperty(name="Roof thickness", default=120.0, min=20.0)
    roof_overhang_mm: FloatProperty(name="Roof overhang", default=450.0, min=0.0)
    slope_along_y: BoolProperty(
        name="Slope along Y",
        description="When enabled, roof rises from negative Y to positive Y",
        default=True,
    )
    include_second_story: BoolProperty(name="Second story", default=True)


def register():
    bpy.utils.register_class(JPTHBProperties)
    bpy.types.Scene.jp_thb = PointerProperty(type=JPTHBProperties)


def unregister():
    del bpy.types.Scene.jp_thb
    bpy.utils.unregister_class(JPTHBProperties)
