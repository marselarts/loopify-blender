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



class LPF_OT_LoopNoiseOp(bpy.types.Operator):
    """Loop Noise modifier. Works only with one noise modifier on selected fcurves"""
    bl_idname = "loopify.loop_noise"
    bl_label = "Loop Noise"
    bl_options = {'REGISTER', 'UNDO'}

    

    def execute(self, context):
       

        scene = context.scene
        frame_start = scene.frame_start
        frame_end = scene.frame_end
        duration = frame_end - frame_start


      
        fcurves = context.selected_editable_fcurves
        for fcu in fcurves:

            fcu.select = True
            modifiers = fcu.modifiers
            noise_mods = []
            for mod in modifiers:
                if mod.type == 'NOISE':
                     noise_mods.append(mod)
            for i,mod in enumerate(noise_mods):
                if i>0:
                    modifiers.remove(mod)

            if len(noise_mods) == 0:
                continue
            noise = noise_mods[0]
            
            
            blend_length=abs(noise.scale)
            blend_out = blend_length/2


            noise.use_restricted_range = True
            noise.frame_start = frame_start
            noise.frame_end = frame_start + (duration/2) + blend_length
            noise.blend_out = blend_out

            new_noise = modifiers.new('NOISE')

            new_noise.scale = noise.scale
            new_noise.strength = noise.strength

            new_noise.offset = noise.offset+duration+1
            new_noise.phase = noise.phase
            new_noise.depth = noise.depth
            new_noise.influence = noise.influence
            new_noise.use_restricted_range = True
            new_noise.frame_start = frame_start + (duration/2) - blend_length
            new_noise.frame_end = frame_end
            new_noise.blend_in = blend_out

        return {'FINISHED'}
    
   