import bpy


class ALX_OT_Mesh_Shapekey_FlipDeformation(bpy.types.Operator):
    """"""

    bl_label = ""
    bl_idname = "alx.operator_mesh_shapekey_flip_deformation"
    bl_options = {"REGISTER", "UNDO"}

    @classmethod
    def poll(cls, context):
        return True

    def execute(self, context):
        shapekey_object = context.active_object

        if shapekey_object is not None and shapekey_object.type == "MESH":
            # noinspection PyTypeChecker
            mesh_data: bpy.types.Mesh = shapekey_object.data

            if hasattr(mesh_data, "shape_keys") and mesh_data.shape_keys is not None:
                active_shapekey = shapekey_object.active_shape_key
                if active_shapekey is not None:
                    base_co = []
                    shapekey_co = []

                    # get
                    mesh_data.vertices.foreach_get("co", base_co)
                    active_shapekey.points.foreach_get("co", shapekey_co)

                    # set
                    mesh_data.vertices.foreach_set("co", shapekey_co)
                    active_shapekey.points.foreach_set("co", base_co)

        return {"FINISHED"}
