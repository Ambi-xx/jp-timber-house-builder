from ..utils.geometry import create_box, mm


def build_floors(props, collections):
    width = mm(props.building_width_mm)
    depth = mm(props.building_depth_mm)
    foundation = mm(props.foundation_height_mm)
    slab = mm(props.slab_thickness_mm)
    h1 = mm(props.first_story_height_mm)

    create_box(
        "Foundation_Slab",
        width,
        depth,
        foundation,
        (0.0, 0.0, foundation / 2.0),
        collections["floors"],
    )

    create_box(
        "Floor_1_Slab",
        width,
        depth,
        slab,
        (0.0, 0.0, foundation + slab / 2.0),
        collections["floors"],
    )

    if props.include_second_story:
        z = foundation + slab + h1
        create_box(
            "Floor_2_Slab",
            width,
            depth,
            slab,
            (0.0, 0.0, z + slab / 2.0),
            collections["floors"],
        )
