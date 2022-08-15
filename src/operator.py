from typing import Set
import bpy
from bpy.types import Operator
from . import lib

if "_LOADED" in locals():
    import importlib

    for mod in (lib,):  # list all imports here
        importlib.reload(mod)
_LOADED = True


class ExploreToCurrentDocument(Operator):
    """Show the currently-open file in Windows Explorer"""
    bl_idname = "show_in_windows_explorer.show_in_windows_explorer"
    bl_label = "Show in Windows Explorer"
    bl_options = {'REGISTER'}

    @classmethod
    def poll(cls, context) -> bool:
        if not lib.can_find_explorer():
            cls.poll_message_set("Requires Microsoft Windows and Windows Explorer")
            return False
        if not bpy.data.filepath:
            cls.poll_message_set("The working document has not been saved")
            return False
        return True

    def execute(self, context) -> Set[str]:
        lib.explore_to_file(bpy.data.filepath)
        return {'FINISHED'}


REGISTER_CLASSES = [ExploreToCurrentDocument]
