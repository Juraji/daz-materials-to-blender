def register():
    from .actions import register as register_actions
    from .debug import register as register_debug
    from .preferences import register as register_preferences

    register_actions()
    register_debug()
    register_preferences()


def unregister():
    from .actions import unregister as unregister_actions
    from .debug import unregister as unregister_debug
    from .preferences import unregister as unregister_preferences

    unregister_actions()
    unregister_debug()
    unregister_preferences()
