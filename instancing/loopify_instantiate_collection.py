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

def duplicate_coll(context,linked):
    for window in context.window_manager.windows:
        screen = window.screen

        for area in screen.areas:
            if area.type == 'OUTLINER':
                override = {'window': window, 'screen': screen, 'area': area}
                if linked:
                    bpy.ops.outliner.collection_duplicate_linked(override)
                else:
                    bpy.ops.outliner.collection_duplicate(override)
                break


def generate_copies(context,num_instances,linked):
    scene = context.scene

    active_coll = context.collection


    for coll in bpy.data.collections:
        if active_coll.name in coll.children:
            parent = coll
            break
    if active_coll.name in scene.collection.children:
        parent = scene.collection

    lpf_main_coll = collection(active_coll.name + ' LPF Instances')
    try:
        link(lpf_main_coll,parent)
    except:
        pass
    dupl_coll = collection(active_coll.name + '_duplicates')
    link(dupl_coll,lpf_main_coll)


    for ch in dupl_coll.children:
        bpy.data.collections.remove(ch)
    


    for i in range(num_instances):
        
        duplicate_coll(context,linked)

    new_collections = []
    for coll in parent.children:
        if coll == active_coll or coll == lpf_main_coll:
            continue
        
        new_collections.append(coll)

    new_collections.reverse()
    for coll in new_collections:

        move(coll,parent,dupl_coll)
        if linked:
            for ob in coll.all_objects:
                try:
                    action_copy = ob.animation_data.action.copy()
                    ob.animation_data.action = action_copy
                except:
                    pass

    anim_coll = collection(active_coll.name + '_anim')
    link(anim_coll,lpf_main_coll)

    for ob in anim_coll.objects:
        bpy.data.objects.remove(ob)

    anim_objects = []
    for coll in new_collections:
        for ob in coll.all_objects:
            try:
                action = ob.animation_data.action
                if action != None:
                    link(ob,anim_coll)    
                    anim_objects.append(ob)
            except:
                pass
    for ob in anim_objects:
        name = ob.name[:-4] + '_lpf_instance' + ob.name[-4:]
        ob.name = name
    
    # active_coll.hide_viewport = True
    # active_coll.hide_render = True

    return anim_objects

class LPF_OT_InstantiateCollectionOp(bpy.types.Operator):
    """Creates multiple instances of an active collection.
For subsequent operations on instances, use 'Shift' operators"""
    bl_idname = "loopify.instantiate_collection"
    bl_label = "loopify instantiate collection"
    bl_options = {'REGISTER', 'UNDO'}

    
    
    def execute(self, context):
        
     


        if len(context.selected_objects) > 1:
            self.report({'ERROR'}, 'Only one object must be selected, to instantiate it' )
            return {'CANCELLED'}                 

       


        scene = context.scene
        props = scene.loopify_props
  
        num_instances = props.num_instances 
  
        num_instances = int(num_instances)
        linked = props.duplicate_linked
     
        objs = generate_copies(context,num_instances,linked)
  
        
        return {'FINISHED'}


    def invoke(self, context, event):
       
 
        scene = context.scene
        props = scene.loopify_props
        # self.offset = props.offset
        self.num_instances = props.num_instances
        self.fit_timeline = props.fit_timeline

        return self.execute(context)
