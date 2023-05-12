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




class LPF_OT_NLA_Loop_Op(bpy.types.Operator):
    """Looping active nla strip"""
    bl_idname = "loopify.nla_loop"
    bl_label = "Loop strips"
    bl_options = {'REGISTER', 'UNDO'}
    
    # repeat: 
    # offset: bpy.props.FloatProperty(name = 'Offset', default = 0)
    # global_offset: bpy.props.IntProperty(name = 'Global Offset', default = 0)

    def execute(self, context):
        scene = bpy.context.scene
        start_frame = scene.frame_start
        end_frame = scene.frame_end

        frame_range = end_frame - start_frame +1


        strips =  bpy.context.selected_nla_strips

        
        props = context.scene.loopify_props
        repeat = props.nla_repeat
        # offset = props.nla_offset
        # global_offset = props.nla_global_offset

        for i,strip in enumerate(strips):
            strip_range = strip.action_frame_end-strip.action_frame_start

            # num_cycles = floor(strip.repeat)
            num_cycles = repeat
            new_strip_range = frame_range/num_cycles

            ratio = new_strip_range/ strip_range


            print(ratio)
            strip.scale = ratio 
            strip.repeat = num_cycles
            print(new_strip_range,strip_range)
            strip.frame_start_ui = start_frame #+ (i*offset)
            strip.frame_end_ui = end_frame #+ (i*offset)
        
        return {'FINISHED'}


  

