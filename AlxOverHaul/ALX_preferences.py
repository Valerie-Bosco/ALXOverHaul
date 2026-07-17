import os

import bpy
import rna_keymap_ui

from . import ALX_keymaps
from .modules.ALXAddonUpdater.ALXAddonUpdater.ALX_AddonUpdaterUI import (
    update_settings_ui,
)
from .modules.ALXModuleManager.ALXModuleManager import module_manager


class ALXOverHaul_AddonPreferences(bpy.types.AddonPreferences):
    """"""

    bl_idname = __package__

    addon_preference_tabs: bpy.props.EnumProperty(
        name="",
        default="HOME",
        items=[
            ("HOME", "home", "", "HOME", 1),
            ("KEYBINDS", "keybinds", "", "EVENT_K", 1 << 1),
            ("SETTINGS", "settings", "", "PREFERENCES", 1 << 2),
        ],
    )  # type: ignore

    def GET_debug(self):
        return self.DEBUG

    def SET_transform_debug(self: bpy.types.bpy_struct, new_value: bool, curr_value: bool, is_set: bool) -> bool:

        self: ALXOverHaul_AddonPreferences
        if (mm := module_manager.GET_module_manager()) is not None:
            mm.mute = not self.DEBUG

        return new_value

    DEBUG: bpy.props.BoolProperty(default=False, set_transform=SET_transform_debug)

    # region ADD-ON UPDATER
    auto_check_update: bpy.props.BoolProperty(
        name="Auto-check for Update",
        description="If enabled, auto-check for updates using an interval",
        default=False,
    )  # type: ignore

    updater_interval_months: bpy.props.IntProperty(
        name="Months",
        description="Number of months between checking for updates",
        default=0,
        min=0,
    )  # type: ignore
    updater_interval_days: bpy.props.IntProperty(
        name="Days",
        description="Number of days between checking for updates",
        default=7,
        min=0,
        max=31,
    )  # type: ignore
    updater_interval_hours: bpy.props.IntProperty(
        name="Hours",
        description="Number of hours between checking for updates",
        default=0,
        min=0,
        max=23,
    )  # type: ignore
    updater_interval_minutes: bpy.props.IntProperty(
        name="Minutes",
        description="Number of minutes between checking for updates",
        default=0,
        min=0,
        max=59,
    )  # type: ignore

    # endregion ADD-ON UPDATER

    # region CUSTOM KEYBINDS
    def UPDATE_View3d_Pan_Use_Shift_GRLess(self, context):
        if self.View3d_Pan_Use_Shift_GRLess:
            ALX_keymaps.AlxEditKeymaps(
                KeyconfigSource="Blender",
                ConfigSpaceName="3D View",
                ItemidName="view3d.move",
                MapType="KEYBOARD",
                Key="GRLESS",
                UseShift=True,
                Active=True,
            )
        else:
            ALX_keymaps.AlxEditKeymaps(
                KeyconfigSource="Blender",
                ConfigSpaceName="3D View",
                ItemidName="view3d.move",
                MapType="MOUSE",
                Key="MIDDLEMOUSE",
                UseShift=True,
                Active=True,
            )

    def UPDATE_View3d_Rotate_Use_GRLess(self, context):
        if self.View3d_Rotate_Use_GRLess:
            ALX_keymaps.AlxEditKeymaps(
                KeyconfigSource="Blender",
                ConfigSpaceName="3D View",
                ItemidName="view3d.rotate",
                MapType="KEYBOARD",
                Key="GRLESS",
                Active=True,
            )
        else:
            ALX_keymaps.AlxEditKeymaps(
                KeyconfigSource="Blender",
                ConfigSpaceName="3D View",
                ItemidName="view3d.rotate",
                MapType="MOUSE",
                Key="MIDDLEMOUSE",
                Active=True,
            )

    def UPDATE_View3d_Zoom_Use_GRLess(self, context):
        if self.View3d_Zoom_Use_GRLess:
            ALX_keymaps.AlxEditKeymaps(
                KeyconfigSource="Blender",
                ConfigSpaceName="3D View",
                ItemidName="view3d.zoom",
                MapType="KEYBOARD",
                Key="GRLESS",
                UseCtrl=True,
                Active=True,
            )
        else:
            ALX_keymaps.AlxEditKeymaps(
                KeyconfigSource="Blender",
                ConfigSpaceName="3D View",
                ItemidName="view3d.zoom",
                MapType="MOUSE",
                Key="MIDDLEMOUSE",
                UseCtrl=True,
                Active=True,
            )

    View3d_Pan_Use_Shift_GRLess: bpy.props.BoolProperty(
        name="Alx Optional Keybind: Change View3D Pan",
        description="Replace [Shift + Middle-Mouse] with [shift + GRLess] for 3D View Pan",
        update=UPDATE_View3d_Pan_Use_Shift_GRLess,
    )  # type: ignore
    View3d_Rotate_Use_GRLess: bpy.props.BoolProperty(
        name="Alx Optional Keybind: Change View3D Rotate",
        description="Replace [Middle-Mouse] with [GRLess] for 3D View Rotation",
        update=UPDATE_View3d_Rotate_Use_GRLess,
    )  # type: ignore
    View3d_Zoom_Use_GRLess: bpy.props.BoolProperty(
        name="Alx Optional Keybind: Change View3D Zoom",
        description="Replace [Ctrl + Middle-Mouse] with [Ctrl + GRLess] for 3D View Zoom",
        update=UPDATE_View3d_Zoom_Use_GRLess,
    )  # type: ignore

    # endregion CUSTOM KEYBINDS

    # region MACHINE
    registration_debug: bpy.props.BoolProperty(
        name="Addon Terminal Registration Output", default=True
    )

    def update_switchmatcap1(self, context):
        if self.avoid_update:
            self.avoid_update = False
            return

        matcaps = [
            mc.name
            for mc in context.preferences.studio_lights
            if os.path.basename(os.path.dirname(mc.path)) == "matcap"
        ]
        if self.switchmatcap1 not in matcaps:
            self.avoid_update = True
            self.switchmatcap1 = "NOT FOUND"

    def update_switchmatcap2(self, context):
        if self.avoid_update:
            self.avoid_update = False
            return

        matcaps = [
            mc.name
            for mc in context.preferences.studio_lights
            if os.path.basename(os.path.dirname(mc.path)) == "matcap"
        ]
        if self.switchmatcap2 not in matcaps:
            self.avoid_update = True
            self.switchmatcap2 = "NOT FOUND"

    def update_custom_preferences_keymap(self, context):

        if self.custom_preferences_keymap:
            kc = context.window_manager.keyconfigs.user

            for km in kc.keymaps:
                if km.is_user_modified:
                    self.custom_preferences_keymap = False
                    self.dirty_keymaps = True
                    return

            self.dirty_keymaps = False

    focus_show: bpy.props.BoolProperty(name="Show Focus Preferences", default=False)

    focus_view_transition: bpy.props.BoolProperty(
        name="Viewport Tweening", default=True
    )
    focus_lights: bpy.props.BoolProperty(
        name="Ignore Lights (keep them always visible)", default=False
    )

    group_show: bpy.props.BoolProperty(name="Show Group Preferences", default=False)

    group_auto_name: bpy.props.BoolProperty(
        name="Auto Name Groups",
        description="Automatically add a Prefix and/or Suffix to any user-set Group Name",
        default=True,
    )
    group_basename: bpy.props.StringProperty(name="Group Basename", default="GROUP")
    group_prefix: bpy.props.StringProperty(
        name="Prefix to add to Group Names", default="_"
    )
    group_suffix: bpy.props.StringProperty(
        name="Suffix to add to Group Names", default="_grp"
    )
    group_size: bpy.props.FloatProperty(
        name="Group Empty Draw Size", description="Default Group Size", default=0.2
    )
    group_fade_sizes: bpy.props.BoolProperty(
        name="Fade Group Empty Sizes",
        description="Make Sub Group's Emtpies smaller than their Parents",
        default=True,
    )
    group_fade_factor: bpy.props.FloatProperty(
        name="Fade Group Size Factor",
        description="Factor by which to decrease each Group Empty's Size",
        default=0.8,
        min=0.1,
        max=0.9,
    )
    group_remove_empty: bpy.props.BoolProperty(
        name="Remove Empty Groups",
        description="Automatically remove Empty Groups in each Cleanup Pass",
        default=True,
    )

    assetbrowser_show: bpy.props.BoolProperty(
        name="Show Asset Browser Tools Preferences", default=False
    )

    preferred_default_catalog: bpy.props.StringProperty(
        name="Preferred Default Catalog", default="Model"
    )
    preferred_assetbrowser_workspace_name: bpy.props.StringProperty(
        name="Preferred Workspace for Assembly Asset Creation", default="General.alt"
    )
    show_assembly_asset_creation_in_save_pie: bpy.props.BoolProperty(
        name="Show Assembly Asset Creation in Save Pie", default=True
    )
    show_instance_collection_assembly_in_modes_pie: bpy.props.BoolProperty(
        name="Show Collection Instance Assembly in Modes Pie", default=True
    )
    hide_wire_objects_when_creating_assembly_asset: bpy.props.BoolProperty(
        name="Hide Wire Objects when creating Assembly Asset", default=True
    )
    hide_wire_objects_when_assembling_instance_collection: bpy.props.BoolProperty(
        name="Hide Wire Objects when assembling Collection Instance", default=True
    )

    region_show: bpy.props.BoolProperty(name="Show Region Preferences", default=False)

    region_prefer_left_right: bpy.props.BoolProperty(
        name="Prefer Left/Right over Bottom/Top", default=True
    )
    region_close_range: bpy.props.FloatProperty(
        name="Close Range", subtype="PERCENTAGE", default=30, min=1, max=50
    )

    region_toggle_assetshelf: bpy.props.BoolProperty(
        name="Toggle the Asset Shelf, instead of the Browser", default=False
    )
    region_toggle_assetbrowser_top: bpy.props.BoolProperty(
        name="Toggle the Asset Browser at the Top", default=True
    )
    region_toggle_assetbrowser_bottom: bpy.props.BoolProperty(
        name="Toggle the Asset Browser at the Bottom", default=True
    )

    region_warp_mouse_to_asset_border: bpy.props.BoolProperty(
        name="Warp Mouse to Asset Browser Border", default=False
    )

    render_show: bpy.props.BoolProperty(name="Show Render Preferences", default=False)

    render_folder_name: bpy.props.StringProperty(
        name="Render Folder Name",
        description="Folder used to stored rended images relative to the Location of the .blend file",
        default="out",
    )
    render_seed_count: bpy.props.IntProperty(
        name="Seed Render Count",
        description="Set the Amount of Seed Renderings used to remove Fireflies",
        default=3,
        min=2,
        max=9,
    )
    render_keep_seed_renderings: bpy.props.BoolProperty(
        name="Keep Individual Renderings",
        description="Keep the individual Seed Renderings, after they've been combined into a single Image",
        default=False,
    )
    render_use_clownmatte_naming: bpy.props.BoolProperty(
        name="Use Clownmatte Name",
        description="""It's a better name than "Cryptomatte", believe me""",
        default=True,
    )
    render_show_buttons_in_light_properties: bpy.props.BoolProperty(
        name="Show Render Buttons in Light Properties Panel",
        description="Show Render Buttons in Light Properties Panel",
        default=True,
    )
    render_sync_light_visibility: bpy.props.BoolProperty(
        name="Sync Light visibility/renderability",
        description="Sync Light hide_render props based on hide_viewport props",
        default=True,
    )
    render_adjust_lights_on_render: bpy.props.BoolProperty(
        name="Ajust Area Lights when Rendering in Cycles",
        description="Adjust Area Lights when Rendering, to better match Eevee and Cycles",
        default=True,
    )
    render_enforce_hide_render: bpy.props.BoolProperty(
        name="Enforce hide_render setting when Viewport Rendering",
        description="Hide Objects based on their hide_render props, when Viewport Rendering with Cyclces",
        default=True,
    )
    render_use_bevel_shader: bpy.props.BoolProperty(
        name="Automatically set up Bevel Shader when Cycles Rendering",
        description="Set up Bevel Shader on all visible Materials when Cycles Renderings",
        default=True,
    )

    matpick_show: bpy.props.BoolProperty(
        name="Show Material Picker Preferences", default=False
    )

    matpick_workspace_names: bpy.props.StringProperty(
        name="Workspaces the Material Picker should appear on",
        default="Shading, Material",
    )
    matpick_shading_type_material: bpy.props.BoolProperty(
        name="Show Material Picker in all Material Shading Viewports", default=True
    )
    matpick_shading_type_render: bpy.props.BoolProperty(
        name="Show Material Picker in all Render Shading Viewports", default=False
    )
    matpick_spacing_obj: bpy.props.FloatProperty(
        name="Object Mode Spacing", min=0, default=20
    )
    matpick_spacing_edit: bpy.props.FloatProperty(
        name="Edit Mode Spacing", min=0, default=5
    )

    customize_show: bpy.props.BoolProperty(
        name="Show Customize Preferences", default=False
    )

    custom_startup: bpy.props.BoolProperty(name="Startup Scene", default=False)
    custom_theme: bpy.props.BoolProperty(name="Theme", default=True)
    custom_matcaps: bpy.props.BoolProperty(name="Matcaps", default=True)
    custom_shading: bpy.props.BoolProperty(name="Shading", default=False)
    custom_overlays: bpy.props.BoolProperty(name="Overlays", default=False)
    custom_outliner: bpy.props.BoolProperty(name="Outliner", default=False)
    custom_preferences_interface: bpy.props.BoolProperty(
        name="Preferences: Interface", default=False
    )
    custom_preferences_viewport: bpy.props.BoolProperty(
        name="Preferences: Viewport", default=False
    )
    custom_preferences_input_navigation: bpy.props.BoolProperty(
        name="Preferences: Input & Navigation", default=False
    )
    custom_preferences_keymap: bpy.props.BoolProperty(
        name="Preferences: Keymap",
        default=False,
        update=update_custom_preferences_keymap,
    )
    custom_preferences_system: bpy.props.BoolProperty(
        name="Preferences: System", default=False
    )
    custom_preferences_save: bpy.props.BoolProperty(
        name="Preferences: Save & Load", default=False
    )

    modes_pie_show: bpy.props.BoolProperty(
        name="Show Modes Pie Preferences", default=False
    )

    toggle_cavity: bpy.props.BoolProperty(
        name="Toggle Cavity/Curvature OFF in Edit Mode, ON in Object Mode", default=True
    )
    toggle_xray: bpy.props.BoolProperty(
        name="Toggle X-Ray ON in Edit Mode, OFF in Object Mode, if Pass Through or Wireframe was enabled in Edit Mode",
        default=True,
    )
    sync_tools: bpy.props.BoolProperty(
        name="Sync Tool if possible, when switching Modes", default=True
    )

    save_pie_show: bpy.props.BoolProperty(name="Show Save Pie", default=False)

    save_pie_show_obj_export: bpy.props.BoolProperty(
        name="Show .obj Export", default=True
    )
    save_pie_show_plasticity_export: bpy.props.BoolProperty(
        name="Show Plasticity Export", default=True
    )
    save_pie_show_fbx_export: bpy.props.BoolProperty(
        name="Show .fbx Export", default=True
    )
    save_pie_show_usd_export: bpy.props.BoolProperty(
        name="Show .usd Export", default=True
    )
    save_pie_show_stl_export: bpy.props.BoolProperty(
        name="Show .stl Export", default=False
    )

    fbx_export_apply_scale_all: bpy.props.BoolProperty(
        name="Use 'Fbx All' for Applying Scale",
        description="This is useful for Unity, but bad for Unreal Engine",
        default=False,
    )

    show_screencast: bpy.props.BoolProperty(
        name="Show Screencast in Save Pie",
        description="Show Screencast in Save Pie",
        default=True,
    )
    screencast_operator_count: bpy.props.IntProperty(
        name="Operator Count",
        description="Maximum number of Operators displayed when Screen Casting",
        default=12,
        min=1,
        max=100,
    )
    screencast_fontsize: bpy.props.IntProperty(name="Font Size", default=12, min=2)
    screencast_highlight_machin3: bpy.props.BoolProperty(
        name="Highlight MACHIN3 operators",
        description="Highlight Operators from MACHIN3 addons",
        default=True,
    )
    screencast_show_addon: bpy.props.BoolProperty(
        name="Display Operator's Addons",
        description="Display Operator's Addon",
        default=True,
    )
    screencast_show_idname: bpy.props.BoolProperty(
        name="Display Operator's idnames",
        description="Display Operator's bl_idname",
        default=False,
    )

    screencast_use_skribe: bpy.props.BoolProperty(
        name="Use SKRIBE (dedicated, preferred)", default=True
    )
    screencast_use_screencast_keys: bpy.props.BoolProperty(
        name="Use Screencast Keys (addon)", default=True
    )

    save_pie_use_undo_save: bpy.props.BoolProperty(
        name="Make Pre-Undo Saving available in the Pie", default=False
    )

    shading_pie_show: bpy.props.BoolProperty(name="Show Shading Pie", default=False)

    overlay_solid: bpy.props.BoolProperty(
        name="Show Overlays in Solid Shading by default",
        description="For a newly created scene, or a .blend file where where it wasn't set before, show Overlays for Solid shaded 3D views",
        default=True,
    )
    overlay_material: bpy.props.BoolProperty(
        name="Show Overlays in Material Shading by default",
        description="For a newly created scene, or a .blend file where where it wasn't set before, show Overlays for Material shaded 3D views",
        default=False,
    )
    overlay_rendered: bpy.props.BoolProperty(
        name="Show Overlays in Rendered Shading by default",
        description="For a newly created scene, or a .blend file where where it wasn't set before, show Overlays for Rendered shaded 3D views",
        default=False,
    )
    overlay_wire: bpy.props.BoolProperty(
        name="Show Overlays in Wire Shading by default",
        description="For a newly created scene, or a .blend file where where it wasn't set before, show Overlays for Wire shaded 3D views",
        default=True,
    )

    switchmatcap1: bpy.props.StringProperty(
        name="Matcap 1", update=update_switchmatcap1
    )
    switchmatcap2: bpy.props.StringProperty(
        name="Matcap 2", update=update_switchmatcap2
    )
    matcap2_force_single: bpy.props.BoolProperty(
        name="Force Single Color Shading for Matcap 2", default=True
    )
    matcap2_disable_overlays: bpy.props.BoolProperty(
        name="Disable Overlays for Matcap 2", default=True
    )

    matcap_switch_background: bpy.props.BoolProperty(
        name="Switch Background too", default=False
    )

    matcap1_switch_background_viewport_color: bpy.props.FloatVectorProperty(
        name="Matcap 1 Background Color",
        subtype="COLOR",
        default=[0.05, 0.05, 0.05],
        size=3,
        min=0,
        max=1,
    )

    matcap2_switch_background_viewport_color: bpy.props.FloatVectorProperty(
        name="Matcap 2 Background Color",
        subtype="COLOR",
        default=[0.05, 0.05, 0.05],
        size=3,
        min=0,
        max=1,
    )

    views_pie_show: bpy.props.BoolProperty(
        name="Show Views Pie Preferences", default=False
    )

    obj_mode_rotate_around_active: bpy.props.BoolProperty(
        name="Rotate Around Selection, but only in Object Mode", default=False
    )
    custom_views_use_trackball: bpy.props.BoolProperty(
        name="Force Trackball Navigation when using Custom Views", default=True
    )
    custom_views_set_transform_preset: bpy.props.BoolProperty(
        name="Set Transform Preset when using Custom Views", default=False
    )
    show_orbit_selection: bpy.props.BoolProperty(
        name="Show Orbit around Active", default=True
    )
    show_orbit_method: bpy.props.BoolProperty(
        name="Show Orbit Method Selection", default=True
    )

    cursor_pie_show: bpy.props.BoolProperty(
        name="Show Cursor and Origin Pie Preferences", default=False
    )

    cursor_show_to_grid: bpy.props.BoolProperty(
        name="Show Cursor and Selected to Grid", default=False
    )
    cursor_set_transform_preset: bpy.props.BoolProperty(
        name="Set Transform Preset when Setting Cursor", default=False
    )

    snapping_pie_show: bpy.props.BoolProperty(
        name="Show Snapping Pie Preferences", default=False
    )

    snap_show_absolute_grid: bpy.props.BoolProperty(
        name="Show Absolute Grid Snapping", default=False
    )
    snap_show_volume: bpy.props.BoolProperty(name="Show Volume Snapping", default=False)

    workspace_pie_show: bpy.props.BoolProperty(
        name="Show Workspace Pie Preferences", default=False
    )

    pie_workspace_left_name: bpy.props.StringProperty(
        name="Left Workspace Name", default="Layout"
    )
    pie_workspace_left_text: bpy.props.StringProperty(
        name="Left Workspace Custom Label", default="MACHIN3"
    )
    pie_workspace_left_icon: bpy.props.StringProperty(
        name="Left Workspace Icon", default="VIEW3D"
    )

    pie_workspace_top_left_name: bpy.props.StringProperty(
        name="Top-Left Workspace Name", default="UV Editing"
    )
    pie_workspace_top_left_text: bpy.props.StringProperty(
        name="Top-Left Workspace Custom Label", default="UVs"
    )
    pie_workspace_top_left_icon: bpy.props.StringProperty(
        name="Top-Left Workspace Icon", default="GROUP_UVS"
    )

    pie_workspace_top_name: bpy.props.StringProperty(
        name="Top Workspace Name", default="Shading"
    )
    pie_workspace_top_text: bpy.props.StringProperty(
        name="Top Workspace Custom Label", default="Materials"
    )
    pie_workspace_top_icon: bpy.props.StringProperty(
        name="Top Workspace Icon", default="MATERIAL_DATA"
    )

    pie_workspace_top_right_name: bpy.props.StringProperty(
        name="Top-Right Workspace Name", default=""
    )
    pie_workspace_top_right_text: bpy.props.StringProperty(
        name="Top-Right Workspace Custom Label", default=""
    )
    pie_workspace_top_right_icon: bpy.props.StringProperty(
        name="Top-Right Workspace Icon", default=""
    )

    pie_workspace_right_name: bpy.props.StringProperty(
        name="Right Workspace Name", default="Rendering"
    )
    pie_workspace_right_text: bpy.props.StringProperty(
        name="Right Workspace Custom Label", default=""
    )
    pie_workspace_right_icon: bpy.props.StringProperty(
        name="Right Workspace Icon", default=""
    )

    pie_workspace_bottom_right_name: bpy.props.StringProperty(
        name="Bottom-Right Workspace Name", default=""
    )
    pie_workspace_bottom_right_text: bpy.props.StringProperty(
        name="Bottom-Right Workspace Custom Label", default=""
    )
    pie_workspace_bottom_right_icon: bpy.props.StringProperty(
        name="Bottom-Right Workspace Icon", default=""
    )

    pie_workspace_bottom_name: bpy.props.StringProperty(
        name="Bottom Workspace Name", default="Scripting"
    )
    pie_workspace_bottom_text: bpy.props.StringProperty(
        name="Bottom Workspace Custom Label", default=""
    )
    pie_workspace_bottom_icon: bpy.props.StringProperty(
        name="Bottom Workspace Icon", default="CONSOLE"
    )

    pie_workspace_bottom_left_name: bpy.props.StringProperty(
        name="Bottom-Left Workspace Name", default=""
    )
    pie_workspace_bottom_left_text: bpy.props.StringProperty(
        name="Bottom-Left Workspace Custom Label", default=""
    )
    pie_workspace_bottom_left_icon: bpy.props.StringProperty(
        name="Bottom-Left Workspace Icon", default=""
    )

    tools_pie_show: bpy.props.BoolProperty(
        name="Show Tools Pie Preferences", default=False
    )

    tools_show_boxcutter_presets: bpy.props.BoolProperty(
        name="Show BoxCutter Presets", default=True
    )
    tools_show_hardops_menu: bpy.props.BoolProperty(
        name="Show Hard Ops Menu", default=True
    )
    tools_show_quick_favorites: bpy.props.BoolProperty(
        name="Show Quick Favorites", default=False
    )
    tools_show_tool_bar: bpy.props.BoolProperty(name="Show Tool Bar", default=False)

    use_group_sub_menu: bpy.props.BoolProperty(name="Use Group Sub-Menu", default=False)
    use_group_outliner_toggles: bpy.props.BoolProperty(
        name="Show Group Outliner Toggles", default=True
    )

    show_sidebar_panel: bpy.props.BoolProperty(
        name="Show Sidebar Panel",
        description="Show MACHIN3tools Panel in 3D View's Sidebar",
        default=True,
    )

    modal_hud_scale: bpy.props.FloatProperty(
        name="HUD Scale", description="Scale of HUD elements", default=1, min=0.1
    )
    modal_hud_timeout: bpy.props.FloatProperty(
        name="HUD timeout",
        description="Global Timeout Modulation (not exposed in MACHIN3tools)",
        default=1,
        min=0.1,
    )

    HUD_fade_clean_up: bpy.props.FloatProperty(
        name="Clean Up HUD Fade Time (seconds)", default=1, min=0.1
    )
    HUD_fade_clipping_toggle: bpy.props.FloatProperty(
        name="Clipping Toggle HUD Fade Time (seconds)", default=1, min=0.1
    )
    HUD_fade_group: bpy.props.FloatProperty(
        name="Group HUD Fade Time (seconds)", default=1, min=0.1
    )
    HUD_fade_tools_pie: bpy.props.FloatProperty(
        name="Tools Pie HUD Fade Time (seconds)", default=0.75, min=0.1
    )

    mirror_flick_distance: bpy.props.IntProperty(
        name="Flick Distance", default=75, min=20, max=1000
    )

    avoid_update: bpy.props.BoolProperty(default=False)
    dirty_keymaps: bpy.props.BoolProperty(default=False)

    # endregion MACHINE

    def draw(self, context: bpy.types.Context):
        preference_box = self.layout
        preference_box.grid_flow(row_major=True, align=True).prop(
            self, "addon_preference_tabs", expand=True
        )

        keymap_configs = (
            context.window_manager.keyconfigs.user
            if context.window_manager is not None
            else None
        )

        if self.addon_preference_tabs == "KEYBINDS":
            keybinds_column = preference_box.column()

            keybinds_column.prop(self, "View3d_Pan_Use_Shift_GRLess")
            keybinds_column.prop(self, "View3d_Rotate_Use_GRLess")
            keybinds_column.prop(self, "View3d_Zoom_Use_GRLess")

            for keymap, keymap_item in ALX_keymaps.AlxAddonKeymaps:
                rna_keymap_ui.draw_kmi(
                    [], keymap_configs, keymap, keymap_item, keybinds_column, 0
                )

        if self.addon_preference_tabs == "SETTINGS":
            developer_options = preference_box.split()
            developer_options.prop(
                self, "DEBUG", text="Enable Debug Mode", toggle=True, icon="ERROR"
            )

            developer_options.separator_spacer()

            addon_updater_column = preference_box.column()
            update_settings_ui(context, addon_updater_column)


def GET_preferences() -> bpy.types.AddonPreferences | None:
    if bpy.context.preferences is not None:
        addon: bpy.types.Addon | list[bpy.types.Addon] = bpy.context.preferences.addons[
            __package__
        ]

        addon: bpy.types.Addon
        if addon is not None and type(addon) == bpy.types.Addon:
            return addon.preferences
    return None
