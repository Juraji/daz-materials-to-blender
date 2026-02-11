from bpy.types import Context, Mesh, Object


def deselect_all_geometry(context: Context, obj: Object):
    if context.mode != 'OBJECT' or not obj or obj.type != 'MESH':
        raise Exception("Context should be in OBJECT mode")

    mesh = obj.data

    for f in mesh.polygons:
        f.select = False
    for e in mesh.edges:
        e.select = False
    for v in mesh.vertices:
        v.select = False
