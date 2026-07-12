import bpy

from ..MeshTools.ALX_shapekey import (
    ALX_OT_ShapeKey_MergeShapeKeys,
    ALX_OT_Shapekey_RemoveUnlockedShapekey,
)


class ALX_MT_ShapeKeyToolset(bpy.types.Menu):
    """"""

    bl_label = ""
    bl_idname = "ALX_MT_menu_shapekey_toolset"

    @classmethod
    def poll(cls, context: bpy.types.Context):
        return True

    def draw(self, context: bpy.types.Context):
        layout: bpy.types.UILayout = self.layout

        box = layout.box()

        row = box.row(align=True)
        row.scale_x = 0.75
        operator = row.operator(
            ALX_OT_Shapekey_RemoveUnlockedShapekey.bl_idname,
            text="",
            icon="UNLOCKED",
            emboss=False,
        )
        label = row.label(icon="REMOVE")

        row = box.row(align=True)
        row.scale_x = 0.75
        row.operator(
            ALX_OT_ShapeKey_MergeShapeKeys.bl_idname,
            text="",
            icon="AUTOMERGE_OFF",
            emboss=False,
        )
        label = row.label(icon="TRIA_DOWN")
