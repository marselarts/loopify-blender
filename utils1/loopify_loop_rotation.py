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
    "name": "LPF" ,
}
import bpy
from mathutils import *
import math


class LPF_OT_LoopRotationOp(bpy.types.Operator):
    """Loop rotation on selected fcurves"""
    bl_idname = "loopify.loop_rotation"
    bl_label = "Loop Rotation"
    bl_options = {'REGISTER', 'UNDO'}
    
    number_of_rotations: bpy.props.IntProperty(name = 'Turns',default = 1)
    offset: bpy.props.IntProperty(name = 'Offset',default = 0)
        
    def execute(self, context):


        number_of_rotations = float(self.number_of_rotations)
        offset = float(self.offset)

        offset = offset*(math.pi/180)

        scene = context.scene
        start_frame = scene.frame_start
        end_frame = scene.frame_end

        fcurves = context.selected_editable_fcurves
        fcu = context.active_editable_fcurve

        for fcu in fcurves:
            try:
                fcu.modifiers.new("CYCLES")
            except:
                pass
            for mod in fcu.modifiers:
                if mod.type == 'CYCLES':
                    # print(mod.mode_before)
                    mod.mode_before = 'REPEAT_OFFSET'
                    mod.mode_after = 'REPEAT_OFFSET'

        for fcu in fcurves:

            for i in reversed(range(len(fcu.keyframe_points))):
                if i == 0:
                    break
                p = fcu.keyframe_points[i]
                fcu.keyframe_points.remove(p)
                
            
            rot_amp = math.pi*2
            rot_amp = number_of_rotations*rot_amp

            start = offset
            end = rot_amp+offset
                        
            fcu.keyframe_points.insert(end_frame+1,end)
            
            first_key = fcu.keyframe_points[0]
            last_key = fcu.keyframe_points[-1]

            first_key.interpolation = 'LINEAR'
            last_key.interpolation = 'LINEAR'

            first_key.co[0] = start_frame
            first_key.co[1] = start



        return {'FINISHED'}
