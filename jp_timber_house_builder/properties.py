import bpy
from bpy.props import BoolProperty, FloatProperty, PointerProperty, StringProperty
from bpy.types import PropertyGroup


class JPTHBProperties(PropertyGroup):
    building_width_mm: FloatProperty(name="Width", default=9100.0, min=1000.0)
    building_depth_mm: FloatProperty(name="Depth", default=6370.0, min=1000.0)
    foundation_height_mm: FloatProperty(name="Foundation", default=600.0, min=0.0)
    slab_thickness_mm: FloatProperty(name="Slab thickness", default=150.0, min=20.0)
    wall_thickness_mm: FloatProperty(name="Wall thickness", default=125.0, min=40.0)
    first_story_height_mm: FloatProperty(name="First story", default=2735.0, min=1800.0)
    second_story_height_mm: FloatProperty(name="Second story", default=3200.0, min=1800.0)
    roof_slope_percent: FloatProperty(name="Roof slope %", default=2.5, min=-30.0, max=30.0)
    roof_thickness_mm: FloatProperty(name="Roof thickness", default=120.0, min=20.0)
    roof_overhang_mm: FloatProperty(name="Roof overhang", default=450.0, min=0.0)
    slope_along_y: BoolProperty(name="Slope along Y", default=True)
    include_second_story: BoolProperty(name="Second story", default=True)

    use_openings: BoolProperty(
        name="Create door and window openings",
        description="Split perimeter walls to leave real, empty openings",
        default=True,
    )
    front_door_width_mm: FloatProperty(name="South door width", default=910.0, min=400.0)
    front_door_height_mm: FloatProperty(name="South door height", default=2100.0, min=1500.0)
    north_window_width_mm: FloatProperty(name="North window width", default=1640.0, min=300.0)
    north_window_height_mm: FloatProperty(name="North window height", default=1100.0, min=300.0)
    north_window_sill_mm: FloatProperty(name="North window sill", default=900.0, min=0.0)

    use_dxf_plans: BoolProperty(
        name="Build walls from DXF",
        description="Generate plan walls from ASCII DXF linework",
        default=False,
    )
    first_floor_dxf: StringProperty(name="1F DXF", subtype="FILE_PATH")
    second_floor_dxf: StringProperty(name="2F DXF", subtype="FILE_PATH")
    dxf_layer_filter: StringProperty(
        name="Wall layer filter",
        description="Comma-separated layer name fragments; empty imports all eligible segments",
        default="wall,壁,間仕切",
    )
    dxf_units_to_mm: FloatProperty(
        name="DXF unit to mm",
        description="Multiplier converting one drawing unit to millimeters",
        default=1.0,
        min=0.000001,
    )
    dxf_min_segment_mm: FloatProperty(
        name="Minimum wall length",
        description="Ignore shorter segments to reduce symbols and annotation noise",
        default=200.0,
        min=1.0,
    )
    dxf_center_plans: BoolProperty(
        name="Center imported plans",
        description="Move imported linework bounding-box center to the Blender origin",
        default=True,
    )


def register():
    bpy.utils.register_class(JPTHBProperties)
    bpy.types.Scene.jp_thb = PointerProperty(type=JPTHBProperties)


def unregister():
    del bpy.types.Scene.jp_thb
    bpy.utils.unregister_class(JPTHBProperties)
