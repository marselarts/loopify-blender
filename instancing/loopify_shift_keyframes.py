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

class LPF_OT_ShiftKeyframesOp(bpy.types.Operator):
    """Offset selected animated objects or bones keyframes. 
Bones option works only with one armature object with selected bones"""
    bl_idname = "loopify.shift_keyframes"
    bl_label = "Shift Keyframes X"
    bl_options = {'REGISTER', 'UNDO'}
    
    add_to_existing : bpy.props.BoolProperty(default = False,name = 'Add to Existing')
    offset : bpy.props.IntProperty(default =  25, min = 1, name = 'Offset')
    global_offset: bpy.props.IntProperty(default =  0, name = 'Global Offset')
    fix_looping: bpy.props.BoolProperty(default = False, name = 'Fix Looping')

    def execute(self, context):
        scene = context.scene
        props = scene.loopify_props
        # props.add_to_existing = self.add_to_existing 
        # props.offset = self.offset 
        # props.global_offset = self.global_offset
        
        
        
        add_to_existing = self.add_to_existing
        offset = self.offset
        global_offset = self.global_offset
        fix_looping = self.fix_looping

        selected_only = props.selected_only

        objs = context.selected_objects


        instances = LPFinstances(context,objs,selected_only)
        if instances.message != 'Good':
            self.report({'ERROR'}, instances.message )
            return {'CANCELLED'}   
      
     
        reset_curves = not add_to_existing
        instances.offset(offset,global_offset,reset_curves)
        
                        
        if fix_looping:
            instances.fix_looping(context)

        return {'FINISHED'}

    def invoke(self, context, event):
       
        # scene = context.scene
        # props = scene.loopify_props
        # self.add_to_existing = props.add_to_existing
        # self.offset = props.offset
        # self.global_offset = props.global_offset

        return self.execute(context)

