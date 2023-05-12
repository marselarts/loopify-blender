# ====================== BEGIN LICENSE BLOCK ======================
# Copyright (C) 2023 Marsel Rashitov
# This program is distributed under the terms of the GNU General Public License v3.0.
# You should have received a copy of the GNU General Public License v3.0
# along with this program; if not, visit https://www.gnu.org/licenses/gpl-3.0.html
# to obtain a copy of the license.
# If you would like to use this program under a different license,
# please contact Marsel Rashitov at marsellarts@gmail.com
# ======================= END LICENSE BLOCK =======================

bl_info = {
    "name": "Loopify" ,
}
import bpy
import math
import re

import os
import addon_utils
import importlib.util

def import_mod(dir,mod_name):
    spec = importlib.util.spec_from_file_location(mod_name, os.path.join(dir,mod_name+".py"))
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod

def get_addon_path(addon_name):
    for mod in addon_utils.modules():
        if mod.bl_info['name'] == addon_name:
            filepath = mod.__file__
            return filepath
        else:
            pass
        
def ImportFromAddonDir(module_name,sub_path):
    addon_path = get_addon_path(bl_info["name"])
    addon_dir = os.path.dirname(addon_path)
    path = os.path.join(addon_dir,sub_path)
    mod = import_mod(path,module_name)
    return mod

LPFinstances = ImportFromAddonDir('lpf_instances','instancing').LPFinstances

class LPF_OT_CopyOffsetsOp(bpy.types.Operator):
    """Copies first frames of selected fcurves"""
    bl_idname = "loopify.copy_offsets"
    bl_label = "Copy Offsets"
    bl_options = {'REGISTER', 'UNDO'}
    
    

    def execute(self, context):
        scene = context.scene
        props = scene.loopify_props
        frames_list = props.frames_list
        frames_list.clear()

        for fcu in context.selected_editable_fcurves:
            key = fcu.keyframe_points[0]
            copy_key = frames_list.add()
            copy_key.key = key.co
            copy_key.handle_left = key.handle_left
            copy_key.handle_right = key.handle_right
            



        return {'FINISHED'}

  
