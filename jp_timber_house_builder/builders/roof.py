from ..utils.geometry import create_mesh_object, mm


def _roof_plane(props, width, depth, overhang, base_z):
    slope = props.roof_slope_percent / 100.0
    x0 = -(width / 2.0 + overhang)
    x1 = +(width / 2.0 + overhang)
    y0 = -(depth / 2.0 + overhang)
    y1 = +(depth / 2.0 + overhang)

    if props.slope_along_y:
        dz = (y1 - y0) * slope
        top = [(x0, y0, base_z), (x1, y0, base_z), (x1, y1, base_z + dz), (x0, y1, base_z + dz)]
        return top, (y0, y1), slope
    dz = (x1 - x0) * slope
    top = [(x0, y0, base_z), (x1, y0, base_z + dz), (x1, y1, base_z + dz), (x0, y1, base_z)]
    return top, (x0, x1), slope


def _build_roof_fill(props, collections, width, depth, overhang, thickness, base_z):
    """Fill the wedge between the flat wall top and the roof underside.

    This is deliberately a solid envelope rather than a thin visual panel: it
    prevents daylight gaps in section/elevation views and gives the next door
    and window stages a closed building shell.
    """
    slope = props.roof_slope_percent / 100.0
    x0, x1 = -width / 2.0, width / 2.0
    y0, y1 = -depth / 2.0, depth / 2.0

    if props.slope_along_y:
        roof_y0 = -(depth / 2.0 + overhang)
        z0 = base_z + (y0 - roof_y0) * slope - thickness
        z1 = base_z + (y1 - roof_y0) * slope - thickness
        base = min(z0, z1)
        vertices = [
            (x0, y0, base), (x1, y0, base), (x1, y1, base), (x0, y1, base),
            (x0, y0, z0), (x1, y0, z0), (x1, y1, z1), (x0, y1, z1),
        ]
    else:
        roof_x0 = -(width / 2.0 + overhang)
        z0 = base_z + (x0 - roof_x0) * slope - thickness
        z1 = base_z + (x1 - roof_x0) * slope - thickness
        base = min(z0, z1)
        vertices = [
            (x0, y0, base), (x1, y0, base), (x1, y1, base), (x0, y1, base),
            (x0, y0, z0), (x1, y0, z1), (x1, y1, z1), (x0, y1, z0),
        ]

    faces = [
        (0, 1, 2, 3), (7, 6, 5, 4),
        (0, 4, 5, 1), (1, 5, 6, 2),
        (2, 6, 7, 3), (3, 7, 4, 0),
    ]
    return create_mesh_object("Roof_Wall_Infill", vertices, faces, collections["walls"])


def build_roof(props, collections):
    width = mm(props.building_width_mm)
    depth = mm(props.building_depth_mm)
    overhang = mm(props.roof_overhang_mm)
    thickness = mm(props.roof_thickness_mm)

    foundation = mm(props.foundation_height_mm)
    slab = mm(props.slab_thickness_mm)
    h1 = mm(props.first_story_height_mm)
    h2 = mm(props.second_story_height_mm if props.include_second_story else 0.0)
    story_slabs = slab * (2.0 if props.include_second_story else 1.0)
    base_z = foundation + story_slabs + h1 + h2

    top, _, _ = _roof_plane(props, width, depth, overhang, base_z)
    bottom = [(x, y, z - thickness) for x, y, z in top]
    faces = [
        (0, 1, 2, 3), (7, 6, 5, 4),
        (0, 4, 5, 1), (1, 5, 6, 2),
        (2, 6, 7, 3), (3, 7, 4, 0),
    ]

    roof = create_mesh_object("Single_Slope_Roof", top + bottom, faces, collections["roof"])
    roof["slope_percent"] = props.roof_slope_percent
    roof["overhang_mm"] = props.roof_overhang_mm
    roof["thickness_mm"] = props.roof_thickness_mm
    _build_roof_fill(props, collections, width, depth, overhang, thickness, base_z)
    return roof
