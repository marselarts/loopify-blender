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



class LPF_OT_SetKeyframesValueOp(bpy.types.Operator):
    """Sets exact value to all selected keyframes"""
    bl_idname = "loopify.set_keyframes_value"
    bl_label = "Set Value"
    bl_options = {'REGISTER', 'UNDO'}
    
    
    value: bpy.props.FloatProperty(default = 0.0)
    
    def execute(self, context):
        keyframes = context.selected_editable_keyframes
        value = self.value
        for key in keyframes:
            co = key.co[1]
            h_l_co = co - key.handle_left[1]
            h_r_co = co - key.handle_right[1]

            key.co[1] = value
            key.handle_left[1] = value - h_l_co
            key.handle_right[1] = value - h_r_co
        return {'FINISHED'}
    
    def invoke(self, context, event):
        keyframes = context.selected_editable_keyframes
        self.value = keyframes[0].co[1]      

        return self.execute(context)