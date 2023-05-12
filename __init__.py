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
    "author": "Marsel Rashitov",
    "version": (1, 0),
    "blender": (3, 3, 0),
    "location": "Graph Editor",
    "description": "A set of tools for making perfect animation loops",
    "category": "Animation",
}

import bpy

import os
import addon_utils
import importlib.util

def import_mod(dir,mod_name):
    spec = importlib.util.spec_from_file_location(mod_name, os.path.join(dir,mod_name+".py"))
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod

def get_addon_path(addon_name):
    for mod in addon_utils.modules():
        if mod.bl_info['name'] == addon_name:
            filepath = mod.__file__
            return filepath
        else:
            pass
        
def ImportFromAddonDir(module_name,sub_path):
    addon_path = get_addon_path(bl_info["name"])
    addon_dir = os.path.dirname(addon_path)
    path = os.path.join(addon_dir,sub_path)
    mod = import_mod(path,module_name)
    return mod

LPF_OT_MakeLoopOp = ImportFromAddonDir('loopify_make_loop','utils1').LPF_OT_MakeLoopOp
LPF_OT_MakeLoopOutToInOp = ImportFromAddonDir('loopify_make_loop_out_to_in','utils1').LPF_OT_MakeLoopOutToInOp
LPF_OT_LoopRotationOp = ImportFromAddonDir('loopify_loop_rotation','utils1').LPF_OT_LoopRotationOp
LPF_OT_PingPongOp = ImportFromAddonDir('loopify_ping_pong','utils1').LPF_OT_PingPongOp
LPF_OT_LoopNoiseOp = ImportFromAddonDir('loopify_loop_noise','utils2').LPF_OT_LoopNoiseOp
LPF_OT_RemoveNoiseLoopOp = ImportFromAddonDir('loopify_remove_noise_loop','utils2').LPF_OT_RemoveNoiseLoopOp
LPF_OT_FixCycleLoopOp = ImportFromAddonDir('loopify_fix_loop_cycle','utils2').LPF_OT_FixCycleLoopOp
LPF_OT_InstantiateOp = ImportFromAddonDir('loopify_instantiate','instancing').LPF_OT_InstantiateOp
LPF_OT_InstantiateCollectionOp = ImportFromAddonDir('loopify_instantiate_collection','instancing').LPF_OT_InstantiateCollectionOp
LPF_OT_InstanceFixLoopOp = ImportFromAddonDir('loopify_instance_fix_loop','instancing').LPF_OT_InstanceFixLoopOp
LPF_OT_ShiftKeyframesOp = ImportFromAddonDir('loopify_shift_keyframes','instancing').LPF_OT_ShiftKeyframesOp
LPF_OT_ShiftFcurveValuesOp = ImportFromAddonDir('loopify_shift_values','instancing').LPF_OT_ShiftFcurveValuesOp
LPF_OT_LocRotScaleOp = ImportFromAddonDir('loopify_loc_rot_scale','instancing').LPF_OT_LocRotScaleOp
LPF_OT_FixBoneFollowPathOp = ImportFromAddonDir('loopify_fix_bone_follow_path','utils3').LPF_OT_FixBoneFollowPathOp
LPF_OT_CopyOffsetsOp = ImportFromAddonDir('loopify_copy_offsets','utils4').LPF_OT_CopyOffsetsOp
LPF_OT_PasteOffsetsOp = ImportFromAddonDir('loopify_paste_offsets','utils4').LPF_OT_PasteOffsetsOp
LPF_OT_CopyKeyframesOp = ImportFromAddonDir('loopify_copy_keyframes','utils4').LPF_OT_CopyKeyframesOp
LPF_OT_PasteKeyframesOp = ImportFromAddonDir('loopify_paste_keyframes','utils4').LPF_OT_PasteKeyframesOp
LPF_OT_SetKeyframesValueOp = ImportFromAddonDir('loopify_set_keyframes_value','utils4').LPF_OT_SetKeyframesValueOp
LPF_OT_NLA_Loop_Op =  ImportFromAddonDir('loopify_nla_loop','utils_nla').LPF_OT_NLA_Loop_Op
LPF_OT_RandomizeNoiseSeedOp =  ImportFromAddonDir('loopify_noise_seed','utils2').LPF_OT_RandomizeNoiseSeedOp
LPF_OT_RemoveAllModifiersOp =  ImportFromAddonDir('loopify_remove_all_modifiers','utils2').LPF_OT_RemoveAllModifiersOp

class LoopifyPanelBase:
    bl_idname = "LPF_PT_panel_base"
    bl_space_type = "GRAPH_EDITOR"
    bl_category = 'Loopify'
    bl_label = "Loopify"
    bl_region_type = 'UI'

class LPF_PT_PanelInstanceOperations(LoopifyPanelBase, bpy.types.Panel):
    bl_idname = "LPF_PT_PanelInstanceOperations"
    bl_label = "Instancing Operations"
    def draw(self, context):
        layout = self.layout
        scene = context.scene
        props = scene.loopify_props
        layout.prop(props,'selected_only',text = 'Affect Only Selected Fcurves')
    

class LPF_PT_PanelInstanceBase(LoopifyPanelBase, bpy.types.Panel):
    bl_idname = "LPF_PT_panel_instance"
    bl_label = "Instancing"
    bl_parent_id = 'LPF_PT_PanelInstanceOperations'
    bl_options = {'DEFAULT_CLOSED'}

    def draw(self, context):
        layout = self.layout

        scene = context.scene
        props = scene.loopify_props

 
        layout.prop(props,'duplicate_linked', text = 'Duplicate Linked')  
        box = layout.box()
        
        box.prop(props, "fit_timeline", text = 'Fit Timeline')
        row = box.row()
        if not props.fit_timeline:
            row.enabled = True
        else:
            row.enabled = False
        row.prop(props, "num_instances", text = 'Number of Objects')
      


        op = box.operator(LPF_OT_InstantiateOp.bl_idname, text = 'Instantiate Object')
        op.offset = props.offset
        op.num_instances = props.num_instances
        op.fit_timeline = props.fit_timeline       
        layout.separator()
        box = layout.box()
        box.prop(props,'num_instances',text ='Number of Collections')    
         
        op = box.operator(LPF_OT_InstantiateCollectionOp.bl_idname, text = 'Instantiate Collection')


class LPF_PT_PanelInstanceTweak(LoopifyPanelBase,bpy.types.Panel):

    bl_label = "Instances Tweaking"
    bl_parent_id = 'LPF_PT_PanelInstanceOperations'
    bl_options = {'DEFAULT_CLOSED'}
    def draw(self, context):
        layout = self.layout   
        box = layout.box()   
  
        box.operator(LPF_OT_InstanceFixLoopOp.bl_idname, text = 'Fix Instances Looping')







class LPF_PT_PanelCopyPaste(LoopifyPanelBase, bpy.types.Panel):
    bl_idname = "LPF_PT_PanelCopyPaste"
    bl_label = 'Copy/Past/Tweak'
    
    def draw(self, context):
        layout = self.layout
        
        box = layout.box()  
   
        row = box.row()
        row.operator(LPF_OT_CopyKeyframesOp.bl_idname)
        row.operator(LPF_OT_PasteKeyframesOp.bl_idname)
        row = box.row()
     
        row.operator(LPF_OT_CopyOffsetsOp.bl_idname)
        row.operator(LPF_OT_PasteOffsetsOp.bl_idname)

        row = box.row()
        row.operator(LPF_OT_SetKeyframesValueOp.bl_idname, text = "Set Value")  


class LPF_PT_PanelCopyPaste(LoopifyPanelBase, bpy.types.Panel):
    bl_idname = "LPF_PT_PanelCopyPaste"
    bl_label = 'Copy/Paste/Tweak'
    bl_options = {'DEFAULT_CLOSED'}
    def draw(self, context):
        layout = self.layout
        
        box = layout.box()  
   
        row = box.row()
        row.operator(LPF_OT_CopyKeyframesOp.bl_idname)
        row.operator(LPF_OT_PasteKeyframesOp.bl_idname)
        row = box.row()
        row.operator(LPF_OT_CopyOffsetsOp.bl_idname)
        row.operator(LPF_OT_PasteOffsetsOp.bl_idname)
        row = box.row()
        row.operator(LPF_OT_SetKeyframesValueOp.bl_idname, text = "Set Value")  

class LPF_PT_PanelMatchStartEnd(LoopifyPanelBase, bpy.types.Panel):
    bl_idname = "LPF_PT_PanelMatchStartEnd"
    bl_label = 'Match Start/End Keyframes'
    bl_options = {'DEFAULT_CLOSED'}
    def draw(self, context):
        layout = self.layout
        box = layout.box()
        row = box.row()
        row.operator(LPF_OT_MakeLoopOp.bl_idname, text = 'Match Start/End 1')
        row.operator(LPF_OT_MakeLoopOutToInOp.bl_idname, text = "Match Start/End 2")

class LPF_PT_PanelNoise(LoopifyPanelBase, bpy.types.Panel):
    bl_idname = "LPF_PT_PanelNoise"
    bl_label = 'Noise Modifier'
    bl_options = {'DEFAULT_CLOSED'}
    
    def draw(self, context):
        layout = self.layout
        box = layout.box()              
        
        row = box.row()
        row.operator(LPF_OT_LoopNoiseOp.bl_idname, text = "Loop Noise")
        row.operator(LPF_OT_RemoveNoiseLoopOp.bl_idname, text = "Remove Noise Loop")
        row = box.row()
        row.operator(LPF_OT_RandomizeNoiseSeedOp.bl_idname, text = "Randomize Noise Seed")
        row = box.row()
        row.operator(LPF_OT_RemoveAllModifiersOp.bl_idname, text = "Remove All Modifiers")

class LPF_PT_PanelRotation(LoopifyPanelBase, bpy.types.Panel):
    bl_idname = "LPF_PT_PanelRotation"
    bl_label = 'Rotation'
    bl_options = {'DEFAULT_CLOSED'}
    
    def draw(self, context):
        layout = self.layout
        box = layout.box()              
     
        box.operator(LPF_OT_LoopRotationOp.bl_idname, text = "Loop Rotation")   

class LPF_PT_PanelRepeater(LoopifyPanelBase, bpy.types.Panel):
    bl_idname = "LPF_PT_PanelRepeater"
    bl_label = 'Repeater'
    bl_options = {'DEFAULT_CLOSED'}
    
    def draw(self, context):
        layout = self.layout
        box = layout.box()              

        box.operator(LPF_OT_PingPongOp.bl_idname, text = "Repeater/Ping Pong")  

        box.operator(LPF_OT_FixCycleLoopOp.bl_idname, text = "Fix Repeater Looping") 



########################################################################################### SHIFT KEYFRAMES
class LPF_PT_PanelShiftKeyframesBase(LoopifyPanelBase, bpy.types.Panel):
    bl_idname = "LPF_PT_panel_utils2"
    bl_label = "Shift"
    bl_parent_id = 'LPF_PT_PanelInstanceOperations'
    bl_options = {'DEFAULT_CLOSED'}
    def draw(self, context):
        

        layout = self.layout  
        box = layout.box()
        box.operator(LPF_OT_ShiftKeyframesOp.bl_idname)

        box.operator(LPF_OT_ShiftFcurveValuesOp.bl_idname)

        box.operator(LPF_OT_LocRotScaleOp.bl_idname)
        



class LPF_PT_PanelShiftKeyframesCurve(LoopifyPanelBase, bpy.types.Panel):
 
    bl_idname = "LPF_PT_panel_utils2_Curve"
    bl_label = "Instance/Shift Curve Mapping"
    bl_description = "Curve mapping for shifting operators"
    # bl_parent_id = 'LPF_PT_panel_utils2'
    bl_parent_id = 'LPF_PT_PanelInstanceOperations'
    bl_options = {'DEFAULT_CLOSED'}
    def draw(self, context):
        

        node_group_name = 'shift_keyframes_group'
        curve_node_name = 'shift_keyframes_node'
    
        ng = bpy.data.node_groups[node_group_name]
        nodes = ng.nodes     
        node = nodes.get(curve_node_name)
        
        layout = self.layout        


        layout.template_curve_mapping(node, "mapping")



def follow_path_panel(self, context):
    layout = self.layout
    layout.operator(LPF_OT_FixBoneFollowPathOp.bl_idname, text = 'LPF Fix Offset')



class LoopifyPanelNLA(bpy.types.Panel):
    bl_idname = "LoopifyPanelNLA"
    bl_space_type = "NLA_EDITOR"
    bl_category = 'Loopify'
    bl_label = "Loopify"
    bl_region_type = 'UI'
    def draw(self, context):
        layout = self.layout
        

        props = context.scene.loopify_props
        layout.prop(props,'nla_repeat')
        # layout.prop(props,'nla_offset')
        # layout.prop(props,'nla_global_offset')
        layout.operator(LPF_OT_NLA_Loop_Op.bl_idname)


class KeyFrameItem(bpy.types.PropertyGroup):

    key: bpy.props.FloatVectorProperty(size = 2)
    handle_left: bpy.props.FloatVectorProperty(size = 2)
    handle_right: bpy.props.FloatVectorProperty(size = 2)


class LoopifyPropertyGroup(bpy.types.PropertyGroup):
    add_to_existing: bpy.props.BoolProperty(name="add to existing",default = False)
    offset: bpy.props.IntProperty(name="offset",default = 25)
    global_offset: bpy.props.IntProperty(name="global offset",default = 0)
    selected_only: bpy.props.BoolProperty(name="selected only",default = False)
    fit_timeline: bpy.props.BoolProperty(name="fit timeline",default = True)  
    num_instances: bpy.props.IntProperty(name="num instances",default = 10) 
    frames_list: bpy.props.CollectionProperty(type=KeyFrameItem)
    nla_repeat: bpy.props.IntProperty(name = 'Repeat', default = 2,min = 1)
    nla_offset: bpy.props.FloatProperty(name = 'Offset', default = 0)
    nla_global_offset: bpy.props.IntProperty(name = 'Global Offset', default = 0)
    duplicate_linked: bpy.props.BoolProperty(name = 'Duplicate Linked', default = False,description = 'If Linked, object data will not be copied')
classes = [
LPF_OT_InstantiateOp,
LPF_OT_InstantiateCollectionOp,
LPF_OT_InstanceFixLoopOp,

LPF_PT_PanelInstanceOperations,
LPF_PT_PanelInstanceBase,

LPF_OT_ShiftKeyframesOp,
LPF_PT_PanelShiftKeyframesBase,
LPF_PT_PanelShiftKeyframesCurve,
LPF_PT_PanelInstanceTweak,


LPF_OT_ShiftFcurveValuesOp,

LPF_OT_LocRotScaleOp,


LPF_OT_MakeLoopOp,
LPF_OT_MakeLoopOutToInOp,
LPF_OT_LoopNoiseOp,
LPF_OT_RandomizeNoiseSeedOp,
LPF_OT_RemoveAllModifiersOp,
LPF_OT_RemoveNoiseLoopOp,



LPF_OT_LoopRotationOp,

LPF_OT_PingPongOp,
LPF_OT_FixCycleLoopOp,


# LPF_PT_PanelUtils1Base,
LPF_PT_PanelCopyPaste,
LPF_PT_PanelMatchStartEnd,
LPF_PT_PanelRepeater,
LPF_PT_PanelNoise,
LPF_PT_PanelRotation,


LPF_OT_FixBoneFollowPathOp,

LPF_OT_CopyOffsetsOp,
LPF_OT_PasteOffsetsOp,

LPF_OT_CopyKeyframesOp,
LPF_OT_PasteKeyframesOp,

LPF_OT_SetKeyframesValueOp,

KeyFrameItem,
LoopifyPropertyGroup,


LPF_OT_NLA_Loop_Op,
LoopifyPanelNLA,
]

from bpy.app.handlers import persistent
@persistent
def CreateProfileCurve(dummy):
    node_group_name = 'shift_keyframes_group'
    curve_node_name = 'shift_keyframes_node'
    
    if node_group_name not in bpy.data.node_groups:
        ng = bpy.data.node_groups.new(node_group_name, 'ShaderNodeTree')
        ng.use_fake_user = True
    else:
        ng = bpy.data.node_groups[node_group_name]
    nodes = ng.nodes
    
    node = nodes.get(curve_node_name)
    if node == None:
        node = nodes.new('ShaderNodeRGBCurve')
        node.name = curve_node_name
    return node



def register():
    bpy.app.handlers.load_post.append(CreateProfileCurve)

    for cls in classes:
        bpy.utils.register_class(cls)

    bpy.types.Scene.loopify_props = bpy.props.PointerProperty(type=LoopifyPropertyGroup)
    
    
    bpy.types.BONE_PT_bFollowPathConstraint.append(follow_path_panel)    
   
def unregister():
    del bpy.types.Scene.loopify_props
      
    for cls in classes:
        bpy.utils.unregister_class(cls)

    bpy.types.BONE_PT_bFollowPathConstraint.remove(follow_path_panel)
if __name__ == '__main__':
    register()

