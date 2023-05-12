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

def FileFromAddonDir(file_name,sub_path):
    addon_path = get_addon_path(bl_info["name"])
    addon_dir = os.path.dirname(addon_path)
    path = os.path.join(addon_dir,sub_path)
    file_path = os.path.join(path,file_name)
    return file_path

LPFinstances = ImportFromAddonDir('lpf_instances','instancing').LPFinstances

import json
import bpy
def to_dict(fcurve):
    data = {
        "data_path": fcurve.data_path,
        "array_index": fcurve.array_index,
        "keyframe_points": [],
    }

    for keyframe in fcurve.keyframe_points:
        data["keyframe_points"].append({
            "co": tuple(keyframe.co),
            "handle_left": tuple(keyframe.handle_left),
            "handle_right": tuple(keyframe.handle_right),
            "handle_left_type": keyframe.handle_left_type,
            "handle_right_type": keyframe.handle_right_type,
            "interpolation": keyframe.interpolation,
        })

    return data
def to_json(fcurves):
    data = []
    for fcurve in fcurves:
        data.append(to_dict(fcurve))
    return json.dumps(data)

class LPF_OT_CopyKeyframesOp(bpy.types.Operator):
    """Copies all keyframes of selected fcurves"""
    bl_idname = "loopify.copy_keyframes"
    bl_label = "Copy Keyframes"
    bl_options = {'REGISTER', 'UNDO'}
    
    

    def execute(self, context):
        
        json_path = FileFromAddonDir('keyframe_lists.json',r'data')
        print(json_path)

        fcurves = context.selected_editable_fcurves



        json_str = to_json(fcurves)
            

        with open(json_path, "w") as f:
            f.write(json_str)
            

        return {'FINISHED'}

  
