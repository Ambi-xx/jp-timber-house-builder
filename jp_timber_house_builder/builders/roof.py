from ..utils.geometry import create_mesh_object, mm


def build_roof(props, collections):
    width = mm(props.building_width_mm)
    depth = mm(props.building_depth_mm)
    overhang = mm(props.roof_overhang_mm)
    thickness = mm(props.roof_thickness_mm)
    slope = props.roof_slope_percent / 100.0

    foundation = mm(props.foundation_height_mm)
    slab = mm(props.slab_thickness_mm)
    h1 = mm(props.first_story_height_mm)
    h2 = mm(props.second_story_height_mm if props.include_second_story else 0.0)
    story_slabs = slab * (2.0 if props.include_second_story else 1.0)
    base_z = foundation + story_slabs + h1 + h2

    x0 = -(width / 2.0 + overhang)
    x1 = +(width / 2.0 + overhang)
    y0 = -(depth / 2.0 + overhang)
    y1 = +(depth / 2.0 + overhang)

    if props.slope_along_y:
        run = y1 - y0
        dz = run * slope
        z00 = base_z
        z01 = base_z + dz
        top = [
            (x0, y0, z00),
            (x1, y0, z00),
            (x1, y1, z01),
            (x0, y1, z01),
        ]
    else:
        run = x1 - x0
        dz = run * slope
        z00 = base_z
        z10 = base_z + dz
        top = [
            (x0, y0, z00),
            (x1, y0, z10),
            (x1, y1, z10),
            (x0, y1, z00),
        ]

    bottom = [(x, y, z - thickness) for x, y, z in top]
    vertices = top + bottom
    faces = [
        (0, 1, 2, 3),
        (7, 6, 5, 4),
        (0, 4, 5, 1),
        (1, 5, 6, 2),
        (2, 6, 7, 3),
        (3, 7, 4, 0),
    ]

    roof = create_mesh_object("Single_Slope_Roof", vertices, faces, collections["roof"])
    roof["slope_percent"] = props.roof_slope_percent
    roof["overhang_mm"] = props.roof_overhang_mm
    roof["thickness_mm"] = props.roof_thickness_mm
    return roof
