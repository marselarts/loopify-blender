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


class LPF_OT_RandomizeNoiseSeedOp(bpy.types.Operator):
    """Randomize the seed of the noise modifier on selected fcurves"""
    bl_idname = "loopify.randomize_noise_seed"
    bl_label = "Randomize Noise Seed"
    bl_options = {'REGISTER', 'UNDO'}

    offset: bpy.props.FloatProperty(default = 10)
    global_offset: bpy.props.FloatProperty(default = 0)
    def execute(self, context):
 
        fcurves = bpy.context.selected_editable_fcurves

        offset = self.offset
        global_offset = self.global_offset

        for i,fcu in enumerate(fcurves):
            for mod in fcu.modifiers:
                if mod.type == 'NOISE':
                    phase = i * offset
                    phase += global_offset
                    mod.phase = phase
            
        return {'FINISHED'}
    
   