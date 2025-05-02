"""
Polling functions
"""
from bpy.types import Context, Object


### Editor modes

def mode_is_object(context: Context):
    """
    Checks of the current editor mode is set to "OBJECT"
    :param context:
    :return:
    """
    return context.mode == 'OBJECT'


### Object

def object_is_mesh(context: Context, obj: Object = None, check_linked=False):
    """
    Checks whether the given or active object is an object of type "MESH"
    :param context:
    :param obj:
    :param check_linked:
    :return:
    """
    obj = obj or context.active_object

    if obj is None:
        return False
    if obj.type != 'MESH':
        return False
    return not (check_linked and object_is_linked(context, obj))


def object_is_linked(context: Context, obj: Object = None) -> bool:
    """
    Checks if the current object is linked from the library or other blend file
    :param context:
    :param obj:
    :return:
    """
    obj = obj or context.active_object

    return obj not in context.editable_objects or obj.library or obj.override_library


### Selected objects

def selected_objects_has_selection(context: Context):
    """
    Checks whether any objects are selected within the given context
    :param context:
    :return:
    """
    return len(context.selected_objects) != 0


def selected_objects_all_is_mesh(context: Context):
    """
    Checks if all selected objects in the given context are of type MESH.
    Note, if no objects are selected, this method returns False.

    :param context:
    :return:
    """
    return (selected_objects_has_selection(context) and
            all(object_is_mesh(context, o) for o in context.selected_objects))
