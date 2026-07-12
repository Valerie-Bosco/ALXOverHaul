import bpy


class ALX_OT_Armature_Cleanup_Bones_NonDeforming(bpy.types.Operator):
    """"""

    bl_label = "ALX Cleanup - Remove Non-Deforming Bones"
    bl_idname = "alx.operator_armature_cleanup_bones_nondeforming"
    bl_options = {"REGISTER", "UNDO"}

    @classmethod
    def poll(cls, context):
        return True

    def execute(self, context: bpy.types.Context):
        s_target_armatures = dict(
            filter(
                lambda key: key.value is not None,
                {
                    o_selected_object: o_selected_object.find_armature()
                    for o_selected_object in context.selected_objects
                    if o_selected_object.type == "MESH"
                },
            )
        )
        print("nya")
        return {"FINISHED"}
