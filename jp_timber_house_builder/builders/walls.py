from ..utils.geometry import create_box, mm


def _box(name, width, depth, height, location, collection):
    if width <= 0.0 or depth <= 0.0 or height <= 0.0:
        return None
    return create_box(name, width, depth, height, location, collection)


def _south_wall_with_door(prefix, width, thickness, height, z_base, door_width, door_height, collection):
    """Build a south wall in three pieces, leaving a centered door opening."""
    y = -0.5 * width * 0.0  # keeps location construction below visually clear
    del y
    door_width = min(door_width, width - 2.0 * thickness)
    door_height = min(door_height, height - thickness)
    side = 0.5 * (width - door_width)
    wall_y = -0.5

    _box(f"{prefix}_South_West", side, thickness, height,
         (-0.5 * (width - side), wall_y, z_base + 0.5 * height), collection)
    _box(f"{prefix}_South_East", side, thickness, height,
         (+0.5 * (width - side), wall_y, z_base + 0.5 * height), collection)
    _box(f"{prefix}_South_Header", door_width, thickness, height - door_height,
         (0.0, wall_y, z_base + door_height + 0.5 * (height - door_height)), collection)


def _perimeter_walls(prefix, width, depth, thickness, height, z_base, collection, props, first_story=False):
    z = z_base + height / 2.0
    south_y = -depth / 2.0 + thickness / 2.0
    north_y = depth / 2.0 - thickness / 2.0

    if first_story and props.use_openings:
        door_width = mm(props.front_door_width_mm)
        door_height = mm(props.front_door_height_mm)
        door_width = min(door_width, width - 2.0 * thickness)
        door_height = min(door_height, height - thickness)
        side = (width - door_width) / 2.0
        _box(f"{prefix}_South_West", side, thickness, height,
             (-(door_width + side) / 2.0, south_y, z), collection)
        _box(f"{prefix}_South_East", side, thickness, height,
             (+(door_width + side) / 2.0, south_y, z), collection)
        _box(f"{prefix}_South_Header", door_width, thickness, height - door_height,
             (0.0, south_y, z_base + door_height + (height - door_height) / 2.0), collection)

        window_width = min(mm(props.north_window_width_mm), width - 2.0 * thickness)
        window_height = min(mm(props.north_window_height_mm), height - thickness)
        sill = min(mm(props.north_window_sill_mm), height - window_height - thickness)
        side = (width - window_width) / 2.0
        _box(f"{prefix}_North_West", side, thickness, height,
             (-(window_width + side) / 2.0, north_y, z), collection)
        _box(f"{prefix}_North_East", side, thickness, height,
             (+(window_width + side) / 2.0, north_y, z), collection)
        _box(f"{prefix}_North_Sill", window_width, thickness, sill,
             (0.0, north_y, z_base + sill / 2.0), collection)
        top_height = height - sill - window_height
        _box(f"{prefix}_North_Header", window_width, thickness, top_height,
             (0.0, north_y, z_base + sill + window_height + top_height / 2.0), collection)
    else:
        _box(f"{prefix}_South", width, thickness, height, (0.0, south_y, z), collection)
        _box(f"{prefix}_North", width, thickness, height, (0.0, north_y, z), collection)

    _box(f"{prefix}_West", thickness, depth - 2.0 * thickness, height,
         (-width / 2.0 + thickness / 2.0, 0.0, z), collection)
    _box(f"{prefix}_East", thickness, depth - 2.0 * thickness, height,
         (width / 2.0 - thickness / 2.0, 0.0, z), collection)


def build_walls(props, collections):
    width = mm(props.building_width_mm)
    depth = mm(props.building_depth_mm)
    t = mm(props.wall_thickness_mm)
    foundation = mm(props.foundation_height_mm)
    slab = mm(props.slab_thickness_mm)
    h1 = mm(props.first_story_height_mm)
    h2 = mm(props.second_story_height_mm)

    first_base = foundation + slab
    _perimeter_walls("L1", width, depth, t, h1, first_base, collections["walls"], props, first_story=True)

    if props.include_second_story:
        second_base = first_base + h1 + slab
        _perimeter_walls("L2", width, depth, t, h2, second_base, collections["walls"], props)
