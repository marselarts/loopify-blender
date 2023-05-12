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
from mathutils import *
import math


def align_left_handle_to_right(key):
    v = key.handle_right-key.co
    v_norm = v.normalized()
    length = (key.co - key.handle_left).length

    key.handle_left = key.co+v_norm * -length


def get_key_handles(key):
    key_co = key.co
    handle_left = key_co - key.handle_left
    handle_right = key_co - key.handle_right
    return key_co,handle_left,handle_right

def set_key_handles(key,co,frame,handle_left,handle_right):
    key.co[1] = co[1]
    key.co[0] = frame
    key.handle_left =   key.co -handle_left
    key.handle_right  = key.co -handle_right
    
    
class LPF_OT_MakeLoopOutToInOp(bpy.types.Operator):
    """Sets the value of last keyframe same as first keyframe on selected fcurves"""
    
    bl_idname = "loopify.make_loop_out_to_in"
    bl_label = "Make Loop/Out to In"
    bl_options = {'REGISTER', 'UNDO'}
    def execute(self, context):
        
        scene = context.scene

        start_frame = scene.frame_start
        end_frame = scene.frame_end


   
        fcurves =context.selected_editable_fcurves
        
        for fcu in fcurves:
            keys = fcu.keyframe_points
            first_key = keys[0]
            end_key = keys[-1]
            
            key_co,handle_left,handle_right = get_key_handles(first_key)
            
            
            
            set_key_handles(end_key,key_co,end_frame,handle_left,handle_right)
        return {'FINISHED'}

