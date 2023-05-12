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

class LPF_OT_FixBoneFollowPathOp(bpy.types.Operator):
    """Fix bone offset, when creating 'Follow Path' constraint"""
    bl_idname = "loopify.fix_bone_follow_path_offset"
    bl_label = "Fix Offset"
    bl_options = {'REGISTER', 'UNDO'}
    
    @classmethod
    def poll(cls, context):
        return context.mode == 'POSE'
    
    def execute(self, context):
            #LPF_fix_bone_follow_path


        ob = context.object
        bones = context.selected_pose_bones

        for b in bones:
            try:
                c = [c for c in b.constraints if c.type == "FOLLOW_PATH"][0]
            except:
                continue    
            b.location = [0,0,0]
            b.matrix = ob.matrix_world.inverted()
            b.rotation_euler = [0,0,0]
            b.rotation_quaternion = [1,0,0,0]

        return {'FINISHED'}

