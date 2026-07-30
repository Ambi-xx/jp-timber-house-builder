import bpy

ROOT_NAME = "JPTHB_House"


def get_or_create_collection(name, parent=None):
    collection = bpy.data.collections.get(name)
    if collection is None:
        collection = bpy.data.collections.new(name)
        if parent is None:
            bpy.context.scene.collection.children.link(collection)
        else:
            parent.children.link(collection)
    return collection


def ensure_collections():
    root = get_or_create_collection(ROOT_NAME)
    return {
        "root": root,
        "levels": get_or_create_collection("01_Levels", root),
        "floors": get_or_create_collection("02_Floors", root),
        "walls": get_or_create_collection("03_Walls", root),
        "roof": get_or_create_collection("04_Roof", root),
    }


def clear_generated():
    root = bpy.data.collections.get(ROOT_NAME)
    if root is None:
        return

    for obj in list(root.all_objects):
        bpy.data.objects.remove(obj, do_unlink=True)

    def remove_children(collection):
        for child in list(collection.children):
            remove_children(child)
            bpy.data.collections.remove(child)

    remove_children(root)
    bpy.data.collections.remove(root)
