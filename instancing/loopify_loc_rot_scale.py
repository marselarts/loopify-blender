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

LPFinstancesNoAnim = ImportFromAddonDir('lpf_instances','instancing').LPFinstancesNoAnim

class LPF_OT_LocRotScaleOp(bpy.types.Operator):
    """Offset selected objects or bones transforms. 
Bones option works only with one armature object with selected bones"""
    bl_idname = "loopify.loc_rot_scale"
    bl_label = "Shift Loc/Rot/Scale"
    bl_options = {'REGISTER', 'UNDO'}
    
   
    add_to_existing : bpy.props.BoolProperty(default = False,name = 'Add to Existing')

    loc: bpy.props.FloatVectorProperty(
            default=(0, 0, 0), 
            name = 'Location'
            )    

    rot: bpy.props.FloatVectorProperty(
            default=(0, 0, 0,), 
            subtype = 'EULER',
            name = 'Rotation'
            )    
    
    scl_min: bpy.props.FloatProperty(
            default=1, 
            name = 'Scale Min'
            )    

    scl_max: bpy.props.FloatProperty(
            default=1, 
            name = 'Scale Max'
            )    
    def execute(self, context):
        scene = context.scene
        props = scene.loopify_props
     

        add_to_existing = self.add_to_existing
        loc = self.loc
        rot = self.rot
        scl_min = self.scl_min
        scl_max = self.scl_max

        objs = context.selected_objects


        instances = LPFinstancesNoAnim(context,objs)
        if instances.message != 'Good':
            self.report({'ERROR'}, instances.message )
            return {'CANCELLED'}   
      
     
     
        instances.loc_rot_scale(add_to_existing,loc,rot,scl_min,scl_max)

        
        

        return {'FINISHED'}

    def invoke(self, context, event):
       
     
        return self.execute(context)

