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
    
    
class LPF_OT_MakeLoopOp(bpy.types.Operator):
    """Sets the values and positions of the last pair of keyframes on selected fcurves, relative to the first pair of keyframes
Minimum 4 keyframes needed"""
    bl_idname = "loopify.make_loop"
    bl_label = "Make Loop"
    bl_options = {'REGISTER', 'UNDO'}
    def execute(self, context):
        
        def get_first_end_points(keys):
            scene = context.scene
            start_frame = scene.frame_start
            end_frame = scene.frame_end
            
            key_pair_start = None
            for i,key in enumerate(keys):
                if i < len(keys)-1:
                    next_key = keys[i+1]
                    if next_key.co[0] > start_frame:
                        key_pair_start = [key,next_key]
                        break

            key_pair_end = None

            for i in reversed(range(len(keys))):
                key = keys[i]
                if i > 0:
                    prev_key = keys[i-1]
                    if prev_key.co[0] <= end_frame+1:
                        key_pair_end = [prev_key,key]
                        break
            return key_pair_start,key_pair_end

 
        scene = context.scene

        start_frame = scene.frame_start
        end_frame = scene.frame_end


        fcurves =context.selected_editable_fcurves
        
        for fcu in fcurves:
            keys = fcu.keyframe_points
            if len(keys)<4:
                continue

            key_pair_start,key_pair_end = get_first_end_points(keys)
            
            first_key = key_pair_start[0]
            first_end_key = key_pair_end[0]

            second_key = key_pair_start[1]
            second_end_key = key_pair_end[1]
            
            if first_key.co[0] <= start_frame:
                offs = start_frame - first_key.co[0]
            else:
                offs = 0
            
            co,l,r = get_key_handles(first_key)
#            set_key_handles(first_end_key,co,end_frame-offs+1,l,r)
            

            first_end_key.co[1] = first_key.co[1]
            first_end_key.co[0] = end_frame-offs+1
            first_end_key.handle_right = first_end_key.co - r
            align_left_handle_to_right(first_end_key)
            
            offs1 = start_frame - second_key.co[0]
            co1,l1,r1 = get_key_handles(second_key)
            set_key_handles(second_end_key,co1,end_frame-offs1+1,l1,r1)
        
      
        
        return {'FINISHED'}

