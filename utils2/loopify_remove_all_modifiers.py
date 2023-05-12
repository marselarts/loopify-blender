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


class LPF_OT_RemoveAllModifiersOp(bpy.types.Operator):
    """Removes all modifiers on selected fcurves"""
    bl_idname = "loopify.remove_all_modifiers"
    bl_label = "Remove All Modifiers"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
 
        fcurves = bpy.context.selected_editable_fcurves


        for i,fcu in enumerate(fcurves):
            for mod in fcu.modifiers:
                fcu.modifiers.remove(mod)

        return {'FINISHED'}
    
   