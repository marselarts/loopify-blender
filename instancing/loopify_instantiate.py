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



collection_helper = ImportFromAddonDir('collection_helper','functions')   

collection = collection_helper.collection
link = collection_helper.link
move = collection_helper.move

LPFinstances = ImportFromAddonDir('lpf_instances','instancing').LPFinstances   

def duplicate(obj, data=True, actions=True,name = "_copy",coll = None):
    obj_copy = bpy.data.objects.get(name)
    if obj_copy == None:
        obj_copy = obj.copy()
        if data:
            obj_copy.data = obj_copy.data.copy()
        if actions and obj_copy.animation_data:
            obj_copy.animation_data.action = obj_copy.animation_data.action.copy()

        obj_copy.name = name
    link(obj_copy,coll)

    return obj_copy     

def generate_copies(active_ob,number_of_copies,suffix,coll,linked):
    copies = []
    # print('generating:')
    for i in range(number_of_copies):
        name = active_ob.name+"_lpf_instance_" + suffix + '.'+ str(i).zfill(3) 
        
        new_ob = duplicate(
                obj=active_ob,
                data=not linked,
                actions=True,
                name = name,
                coll = coll
            )
        
        # print(new_ob.name)
        copies.append(new_ob)
    return copies


def generate_name():
    import string
    import random
    N = 7
    res = ''.join(random.choices(string.ascii_lowercase +
                                string.digits, k=N))
    return res        

class LPF_OT_InstantiateOp(bpy.types.Operator):
    """Creates multiple instances of an active object with animation offset.
For subsequent operations on instances, use 'Shift' operators"""
    bl_idname = "loopify.instantiate"
    bl_label = "loopify instantiate"
    bl_options = {'REGISTER', 'UNDO'}

    
    offset: bpy.props.IntProperty(default = 25, name = 'Offset',min = 1)
    global_offset: bpy.props.IntProperty(default =  0, name = 'Global Offset')
    fit_timeline: bpy.props.BoolProperty(default = True,options={'HIDDEN'})
    num_instances: bpy.props.IntProperty(default = 10, name = 'Number of Copies') 
    offset_from_first: bpy.props.BoolProperty(default = False,name = 'Offset From First')

    fix_looping: bpy.props.BoolProperty(default = False, name = 'Fix Looping')
    
    def execute(self, context):
        
        context.space_data.dopesheet.filter_text = ""


        if len(context.selected_objects) > 1:
            self.report({'ERROR'}, 'Only one object must be selected, to instantiate it' )
            return {'CANCELLED'}                 

        offset = self.offset
        global_offset = self.global_offset
        num_instances = self.num_instances  
        fit_timeline = self.fit_timeline    
        offset_from_first = self.offset_from_first
        fix_looping = self.fix_looping


        if fit_timeline:
            self.num_instances = 0

        scene = context.scene
        props = scene.loopify_props
        props.num_instances = num_instances
        props.fit_timeline = fit_timeline
        only_selected_curves = props.selected_only
        linked = props.duplicate_linked


        start_frame = scene.frame_start
        end_frame = scene.frame_end
        frame_range =  end_frame-start_frame

        
        main_ob = context.object

        copies_coll = collection(main_ob.name + ' LPF Instances')
        copies_coll.hide_viewport = False
        
        link(copies_coll,scene.collection)

        if fit_timeline:
            num_instances = frame_range/offset 
            num_instances*= 2

        num_instances = int(num_instances)

        if len(copies_coll.all_objects) > num_instances:
            for i in reversed(range(num_instances,len(copies_coll.all_objects))):
                bpy.data.objects.remove(copies_coll.all_objects[i])
            
        objs = generate_copies(main_ob,num_instances,'',copies_coll,linked)
        first_fcurves = main_ob.animation_data.action.fcurves
        all_fcurves = []
        for ob in objs:
            ob.hide_viewport = False
            ob.hide_render = False
            ob.select_set(True)
            fcurves = ob.animation_data.action.fcurves
            for fcu,first_fcu in zip(fcurves,first_fcurves):
                fcu.select = first_fcu.select
                # if fcu.select:
                #     all_fcurves.append(fcu)
                
                
            # fcurves.update()
        
        instances = LPFinstances(context,objs,only_selected_curves)

        if instances.message != 'Good':
            self.report({'ERROR'}, instances.message )
            return {'CANCELLED'}                 
        
        

        if only_selected_curves:
            first_fcurves = [fcu for fcu in first_fcurves if fcu in context.selected_editable_fcurves]
                
        instances.set_position(first_fcurves)
        print('-----------------')
       
        if not offset_from_first:       
     
            first_key = instances.objects[0]['fcurves'][0].keyframe_points[0].co[0]
            second_key = instances.objects[0]['fcurves'][0].keyframe_points[-1].co[0]
            curve_len = second_key-first_key

            fcu_range = (num_instances-1)*offset
            last_key = first_key+fcu_range #+ curve_len
            fcu_mid = last_key-fcu_range/2

            timeline_mid = end_frame - frame_range/2
            global_offset+=timeline_mid-fcu_mid
            global_offset -= curve_len/2

   
        
        
        instances.offset(offset,global_offset,True)   

        if fix_looping:
            instances.fix_looping(context)

        # try:
        #     bpy.ops.graph.select_all(action='SELECT')
        # except:
        #     pass
        bpy.ops.graph.select_all(action='SELECT')


        
#################################################

        main_ob.hide_viewport = True
        main_ob.hide_render = True

        context.view_layer.objects.active = objs[0]



        for fcu in all_fcurves:
            fcu.select = True
            for p in fcu.keyframe_points:
                p.select_control_point = True
                p.select_left_handle = True
                p.select_right_handle = True
            

        
        return {'FINISHED'}


    def invoke(self, context, event):
       
 
        scene = context.scene
        props = scene.loopify_props
        # self.offset = props.offset
        self.num_instances = props.num_instances
        self.fit_timeline = props.fit_timeline

        return self.execute(context)

classes = [
LPF_OT_InstantiateOp, 
]
def register():
    for cls in classes:
        bpy.utils.register_class(cls)
def unregister():
    for cls in classes:
        bpy.utils.unregister_class(cls)
if __name__ == '__main__':
    register()
