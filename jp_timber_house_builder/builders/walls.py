from ..utils.geometry import create_box, mm


def _perimeter_walls(prefix, width, depth, thickness, height, z_base, collection):
    z = z_base + height / 2.0
    create_box(f"{prefix}_South", width, thickness, height, (0.0, -depth / 2.0 + thickness / 2.0, z), collection)
    create_box(f"{prefix}_North", width, thickness, height, (0.0, depth / 2.0 - thickness / 2.0, z), collection)
    create_box(f"{prefix}_West", thickness, depth - 2.0 * thickness, height, (-width / 2.0 + thickness / 2.0, 0.0, z), collection)
    create_box(f"{prefix}_East", thickness, depth - 2.0 * thickness, height, (width / 2.0 - thickness / 2.0, 0.0, z), collection)


def build_walls(props, collections):
    width = mm(props.building_width_mm)
    depth = mm(props.building_depth_mm)
    t = mm(props.wall_thickness_mm)
    foundation = mm(props.foundation_height_mm)
    slab = mm(props.slab_thickness_mm)
    h1 = mm(props.first_story_height_mm)
    h2 = mm(props.second_story_height_mm)

    first_base = foundation + slab
    _perimeter_walls("L1", width, depth, t, h1, first_base, collections["walls"])

    if props.include_second_story:
        second_base = first_base + h1 + slab
        _perimeter_walls("L2", width, depth, t, h2, second_base, collections["walls"])
