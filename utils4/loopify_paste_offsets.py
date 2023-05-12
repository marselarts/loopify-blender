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

class LPF_OT_PasteOffsetsOp(bpy.types.Operator):
    """Pastes offsets to selected fcurves"""
    bl_idname = "loopify.paste_offsets"
    bl_label = "Paste Offsets"
    bl_options = {'REGISTER', 'UNDO'}
    
    

    def execute(self, context):
        scene = context.scene
        props = scene.loopify_props
        frames_list = props.frames_list
        # frames_list.clear()
        fcurves = context.selected_editable_fcurves
        for i,copy_key in enumerate(frames_list):
            frame = copy_key.key[0]
            try:
                fcu = fcurves[i]
            except:
                pass
            first_key = fcu.keyframe_points[0].co[0]
            dist = frame - first_key
            for key in fcu.keyframe_points:
                key.co[0] += dist
                key.handle_left[0] += dist
                key.handle_right[0] += dist


            



        return {'FINISHED'}

  
