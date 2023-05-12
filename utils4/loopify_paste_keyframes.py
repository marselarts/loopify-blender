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


class LPF_OT_PasteKeyframesOp(bpy.types.Operator):
    """Paste all keyframes to selected fcurves"""
    bl_idname = "loopify.paste_keyframes"
    bl_label = "Paste Keyframes"
    bl_options = {'REGISTER', 'UNDO'}
    
    
    def execute(self, context):
        
        json_path = FileFromAddonDir('keyframe_lists.json',r'data')
        print(json_path)

        fcurves = context.selected_editable_fcurves
        with open(json_path, "r") as f:
            json_str = f.read()
            data = json.loads(json_str)

        if len(data) > 1:
            for i,fcurve_data in enumerate(data):
                try:
                    fcurve = fcurves[i]
                except:
                    pass
            #    if fcurve is None:
            #        fcurve = context.object.animation_data.action.fcurves.new(fcurve_data["data_path"], index=fcurve_data["array_index"])

                fcurve.keyframe_points.clear()
                for keyframe_data in fcurve_data["keyframe_points"]:
                    keyframe = fcurve.keyframe_points.insert(keyframe_data["co"][0], keyframe_data["co"][1])
                    keyframe.interpolation = keyframe_data["interpolation"]
                    
                    keyframe.handle_left = keyframe_data["handle_left"]
                    keyframe.handle_right = keyframe_data["handle_right"]
                    keyframe.handle_left_type = keyframe_data["handle_left_type"] 
                    keyframe.handle_right_type = keyframe_data["handle_right_type"] 
        else:
            fcurve_data = data[0]
            for fcurve in fcurves:
                fcurve.keyframe_points.clear()
                for keyframe_data in fcurve_data["keyframe_points"]:
                    keyframe = fcurve.keyframe_points.insert(keyframe_data["co"][0], keyframe_data["co"][1])
                    keyframe.interpolation = keyframe_data["interpolation"]
                    
                    keyframe.handle_left = keyframe_data["handle_left"]
                    keyframe.handle_right = keyframe_data["handle_right"]
                    keyframe.handle_left_type = keyframe_data["handle_left_type"] 
                    keyframe.handle_right_type = keyframe_data["handle_right_type"]                

        return {'FINISHED'}

  
