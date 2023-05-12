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



def Average(lst):

    return sum(lst) / len(lst)


class LPF_OT_PingPongOp(bpy.types.Operator):
    """Looping repeated or ping pong animation on selected fcurves"""
    bl_idname = "loopify.ping_pong"
    bl_label = "Repeat/Ping Pong"
    bl_options = {'REGISTER', 'UNDO'}
    
    loops: bpy.props.IntProperty(name = "Number of Loops", default = 3,min = 1)
    amp: bpy.props.FloatProperty(name = "Amplitude",default = 1)
    offset: bpy.props.FloatProperty(name = "Offset",default = 0)
    frame_offset: bpy.props.IntProperty(name = "Frame Offset", default = 0)
    repeat_ping_pong: bpy.props.BoolProperty(name = "Repeat/Ping Pong", default = False)
    
    # average: bpy.props.FloatProperty(options = '')
    def execute(self, context):
  
        scene = context.scene
        start_frame = scene.frame_start
        end_frame = scene.frame_end

        fcu = context.active_editable_fcurve
        fcurves = context.selected_editable_fcurves

        ping_pong  = self.repeat_ping_pong
        loops = self.loops
        if ping_pong:
            loops *= 2
        frame_offset = self.frame_offset
        
        

        for fcu in fcurves:
            vals = []
            for key in fcu.keyframe_points:
                vals.append(key.co[1])
            average = Average(vals)
            
           
            mod_exists = False
            for mod in fcu.modifiers:
                if mod.type == 'CYCLES':
                    mod_exists = True
            if not mod_exists:
                pass
                fcu.modifiers.new("CYCLES")
            
            for mod in fcu.modifiers:
                if mod.type == 'CYCLES':
                    if ping_pong:
                        mod.mode_before = 'MIRROR'
                        mod.mode_after = 'MIRROR'
                    else:
                        mod.mode_before = 'REPEAT'
                        mod.mode_after = 'REPEAT'
        
            for i in reversed(range(len(fcu.keyframe_points))):
                if i == 0:
                    fcu.keyframe_points[i].co[0] = start_frame
                    break
                p = fcu.keyframe_points[i]
                fcu.keyframe_points.remove(p)



            
            
            anim_len = (end_frame+1) - start_frame
            step = anim_len/loops
            amp = self.amp
            offset = self.offset
            

            offs = step
            
            cur_frame = start_frame + offs
            # cur_frame = int(cur_frame)

            fcu.keyframe_points.insert(cur_frame,0)
            min = average - amp/2
            max = average + amp/2
            min += offset
            max += offset
           

            for i,key in enumerate(fcu.keyframe_points):
                pass
                key.handle_left_type = 'AUTO_CLAMPED'
                key.handle_right_type = 'AUTO_CLAMPED'

                if i%2 == 0:
                    key.co[1] = min
                else:
                    key.co[1] = max
                key.co[0]+= frame_offset

            fcu.update()         
            


        return {'FINISHED'}


  

