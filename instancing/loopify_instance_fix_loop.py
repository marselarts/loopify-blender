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
class LPF_OT_InstanceFixLoopOp(bpy.types.Operator):
    """Fixes animation looping of instances. 
Works better with uniform offset"""
    bl_idname = "loopify.instance_fix_loop"
    bl_label = "loopify instance fix loop"
    bl_options = {'REGISTER', 'UNDO'}
    
    
    not_linear: bpy.props.BoolProperty(name = 'Not even offset', default = False)
    
    def execute(self, context):
        print("fix looping")

        scene = context.scene
        props = scene.loopify_props
        only_selected_curves = props.selected_only

        objs = context.selected_objects
        instances = LPFinstances(context,objs,only_selected_curves)


        if instances.message != 'Good':
            self.report({'ERROR'}, instances.message )
            return {'CANCELLED'}                 

        
        instances.fix_looping(context)
        if self.not_linear:
            instances.fix_fcurves_start_end(context)

        if instances.message != 'Good':
            self.report({'ERROR'}, instances.message )
            return {'CANCELLED'}           
   
        
        return {'FINISHED'}


classes = [
LPF_OT_InstanceFixLoopOp, 
]
def register():
    for cls in classes:
        bpy.utils.register_class(cls)
def unregister():
    for cls in classes:
        bpy.utils.unregister_class(cls)
if __name__ == '__main__':
    register()
