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



class LPF_OT_FixCycleLoopOp(bpy.types.Operator):
    """Fix Repeater/Ping Pong looping"""
    bl_idname = "loopify.fix_cycle_loop"
    bl_label = "Fix Cycle Loop"
    bl_options = {'REGISTER', 'UNDO'}

    loops: bpy.props.IntProperty(name = "Number of Loops", default = 3,min = 1)  

    def execute(self, context):
        loops = self.loops

    
        scene = context.scene
        start_frame = scene.frame_start
        end_frame = scene.frame_end  
        anim_len = (end_frame+1) - start_frame
        

        
        fcurves = context.selected_editable_fcurves

        for fcu in fcurves:
            cycles = False
            mirror = False
            for mod in fcu.modifiers:
                if mod.type != 'CYCLES':
                    continue
                cycles = True
                if mod.mode_after == 'MIRROR':
                    mirror = True
            if not cycles:
                continue

            fcu_step = fcu.keyframe_points[-1].co[0]-fcu.keyframe_points[0].co[0]

            num_cycles = loops
            # if len(fcurves) > 1:
            #     num_cycles_ = int(anim_len/fcu_step)
            #     num_cycles += num_cycles_

            if mirror:
                # pass
                num_cycles *= 2

            new_step = anim_len/num_cycles 
            ratio = new_step/fcu_step
            ratio = round(ratio, 4)

            first_point = fcu.keyframe_points[0].co[0]
            first_point_mult = first_point*ratio
            diff = first_point_mult-first_point
            for key in fcu.keyframe_points:
                key.co[0] *= ratio
                key.handle_left[0] *= ratio
                key.handle_right[0] *= ratio   
                key.co[0] -= diff
                key.handle_left[0] -= diff
                key.handle_right[0] -= diff

      

        return {'FINISHED'}
    
    def invoke(self, context, event):
        scene = context.scene
        start_frame = scene.frame_start
        end_frame = scene.frame_end  
        anim_len = (end_frame+1) - start_frame
        

        
        fcurves = context.selected_editable_fcurves

        for fcu in fcurves:
            cycles = False
            mirror = False
            for mod in fcu.modifiers:
                if mod.type != 'CYCLES':
                    continue
                cycles = True
                if mod.mode_after == 'MIRROR':
                    mirror = True
            if not cycles:
                continue

            fcu_step = fcu.keyframe_points[-1].co[0]-fcu.keyframe_points[0].co[0]
            if mirror:
                fcu_step *= 2
            num_cycles = int(anim_len/fcu_step)
        
        self.loops = num_cycles
        return self.execute(context)

