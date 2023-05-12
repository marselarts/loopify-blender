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

class LPF_OT_RemoveNoiseLoopOp(bpy.types.Operator):
    """Removes created noise loop on selected fcurves"""
    bl_idname = "loopify.remove_noise_loop"
    bl_label = "Remove Noise Loop"
    bl_options = {'REGISTER', 'UNDO'}
    def execute(self, context):
 

        fcurves = context.selected_editable_fcurves
        for fcu in fcurves:
            modifiers = fcu.modifiers
            noise_mods = []
            for mod in modifiers:
                if mod.type == 'NOISE':
                     noise_mods.append(mod)
            for i,mod in enumerate(noise_mods):
                if i>0:
                    modifiers.remove(mod)


            noise = noise_mods[0]
            noise.use_restricted_range = False


        return {'FINISHED'}