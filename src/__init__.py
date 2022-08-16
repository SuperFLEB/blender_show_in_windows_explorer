from typing import Callable
import bpy
from . import operator
from . import lib

if "_LOADED" in locals():
    import importlib

    for mod in (operator,):  # list all imports here
        importlib.reload(mod)
_LOADED = True

package_name = __package__

bl_info = {
    "name": "Show in Windows Explorer",
    "description": "Show the currently-open file in Windows Explorer. Requires Microsoft Windows.",
    "author": "FLEB (a.k.a. SuperFLEB)",
    "version": (0, 1, 1),
    "blender": (3, 1, 0),
    "location": "View3D > Object",
    "warning": "Requires Microsoft Windows",
    "doc_url": "https://github.com/SuperFLEB/blender_show_in_windows_explorer",
    "tracker_url": "https://github.com/SuperFLEB/blender_show_in_windows_explorer/issues",
    "support": "COMMUNITY",
    "category": "User Interface",
}


def menuitem(cls: bpy.types.Operator | bpy.types.Menu, operator_context: str = "EXEC_DEFAULT") -> Callable:
    def operator_fn(self, context):
        self.layout.operator_context = operator_context
        self.layout.operator(cls.bl_idname)

    return operator_fn


# Registerable modules have a REGISTER_CLASSES list that lists all registerable classes in the module
registerable_modules = [
    operator,
]

classes = []

menus = {
    "explore": menuitem(operator.ExploreToCurrentDocument),
}


def get_classes() -> list:
    # Uses a set to prevent doubles, and a list to preserve order
    all_classes = classes.copy()
    known_classes = set(classes)
    for module in [m for m in registerable_modules if hasattr(m, "REGISTER_CLASSES")]:
        for cls in [c for c in module.REGISTER_CLASSES if c not in known_classes]:
            all_classes.append(cls)
            known_classes.add(cls)
    return all_classes


def register() -> None:
    all_classes = get_classes()

    for c in all_classes:
        # Attempt to clean up if the addon broke during registration.
        try:
            bpy.utils.unregister_class(c)
        except RuntimeError:
            pass
        bpy.utils.register_class(c)
    bpy.types.TOPBAR_MT_file.prepend(menus["explore"])


def unregister() -> None:
    all_classes = get_classes()
    bpy.types.TOPBAR_MT_file.remove(menus["explore"])
    for c in all_classes[::-1]:
        try:
            bpy.utils.unregister_class(c)
        except RuntimeError:
            pass


if __name__ == "__main__":
    register()
