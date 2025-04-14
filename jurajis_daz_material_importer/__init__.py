def register():
    from .properties import register as register_properties
    from .operators import register as register_operators
    from .ui import register as register_ui

    register_properties()
    register_operators()
    register_ui()


def unregister():
    from .properties import unregister as unregister_properties
    from .operators import unregister as unregister_operators
    from .ui import unregister as unregister_ui

    unregister_properties()
    unregister_operators()
    unregister_ui()
