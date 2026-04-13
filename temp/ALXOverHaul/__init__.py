import bpy

from . import handlers
from .UnlockedTools import AlxUnlockedModeling
from .interface import ALX_Alexandria_General_Panel, ALX_Shapeky_Toolset
from .interface.ALX_Alexandria_Layouts import UIPreset_ObjectTabUIWrapper
from .modules.ALXAddonUpdater.ALXAddonUpdater.ALX_AddonUpdater import Alx_Addon_Updater
from .modules.ALXModuleManager.ALXModuleManager.ALX_ModuleManager import (
    Alx_Module_Manager,
)
from .properties import register_properties, unregister_properties
from .reorganize_later import AlxProperties
from .weight_paint_tools import Alx_weightpaint_bucket_fill

bl_info = {
    "name": "ALXOverHaul",
    "author": "Valerie Bosco",
    "description": "",
    "warning": "",
    "version": (1, 0, 0),
    "blender": (3, 6, 0),
    "category": "3D View",
    "location": "[Ctrl Alt A] General Menu, [Shift Alt S] Pivot Menu, [Tab] Auto Mode Pie Menu",
    "doc_url": "https://github.com/Valerie-Bosco/AlxOverHaul/wiki",
    "tracker_url": "https://github.com/Valerie-Bosco/AlxOverHaul/issues",
}

module_loader = Alx_Module_Manager(path=__path__, globals=globals(), mute=True)
addon_updater = Alx_Addon_Updater(
    path=__path__,
    bl_info=bl_info,
    engine="Github",
    engine_user_name="Valerie-Bosco",
    engine_repo_name="AlxOverHaul",
    manual_download_website="https://github.com/Valerie-Bosco/AlxOverHaul/releases/tag/main_branch_latest",
)


def RegisterHandlers():
    bpy.app.handlers.load_post.append(handlers.AlxMain_load_post)
    bpy.app.handlers.save_post.append(handlers.ALX_MainSavePost)

    bpy.app.handlers.load_post.append(handlers.AlxAddonKeymapHandler)
    bpy.app.handlers.load_post.append(handlers.AlxUpdateSceneSelectionObjectList)
    # bpy.app.handlers.depsgraph_update_post.append(
    #     handlers.AlxUpdateSceneSelectionObjectList
    # )


def UnRegisterHandlers():
    bpy.app.handlers.load_post.remove(handlers.AlxMain_load_post)
    bpy.app.handlers.save_post.remove(handlers.ALX_MainSavePost)

    bpy.app.handlers.load_post.remove(handlers.AlxAddonKeymapHandler)
    bpy.app.handlers.load_post.remove(handlers.AlxUpdateSceneSelectionObjectList)
    # bpy.app.handlers.depsgraph_update_post.remove(
    #     handlers.AlxUpdateSceneSelectionObjectList
    # )


def register():
    module_loader.developer_register_modules()
    addon_updater.register_addon_updater(mute=True)

    bpy.types.OBJECT_PT_context_object.prepend(UIPreset_ObjectTabUIWrapper)
    bpy.types.DATA_PT_shape_keys.prepend(
        ALX_Shapeky_Toolset.ALX_MT_ShapeKeyToolset.draw
    )

    register_properties()
    RegisterHandlers()

    bpy.context.preferences.use_preferences_save = True


def unregister():
    module_loader.developer_unregister_modules()
    addon_updater.unregister_addon_updater()

    bpy.types.OBJECT_PT_context_object.remove(UIPreset_ObjectTabUIWrapper)
    bpy.types.DATA_PT_shape_keys.remove(ALX_Shapeky_Toolset.ALX_MT_ShapeKeyToolset.draw)

    unregister_properties()
    UnRegisterHandlers()


if __name__ == "__main__":
    register()
