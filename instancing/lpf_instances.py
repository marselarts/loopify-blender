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
import re
from mathutils import Vector
import warnings

##test
def move_point(p,frame):
    dist_left = p.co[0] - p.handle_left[0]
    dist_right = p.co[0] - p.handle_right[0]
    p.co[0] = frame
    p.handle_left[0] = frame - dist_left
    p.handle_right[0] = frame - dist_right   

def move_point_value(p,value):
    dist_left = p.co[1] - p.handle_left[1]
    dist_right = p.co[1] - p.handle_right[1]
    p.co[1] = value
    p.handle_left[1] = value - dist_left
    p.handle_right[1] = value - dist_right   

def get_min_val_index(sequence):
    if sequence == []:
        m = None
        i = None
        return m,i
    
    (m,i) = min((abs(v),i) for i,v in enumerate(sequence))
    return m,i

def compare_two_lists(list1,list2):
    if len(list1) > len(list2):
        longer_list = list1
        shorter_list = list2
    else:
        longer_list = list2
        shorter_list = list1
    list1 = list1[:len(shorter_list)]
    list2 = list2[:len(shorter_list)]
    result_list = [elem for i, elem in enumerate(longer_list) if i >= len(shorter_list)]

    return list1,list2,result_list

def fcu_in_frame(objects,frame):
    f_objects = []
    for ob in objects:
        fcurves = ob["fcurves"]
        for fcu in fcurves:
            first_co = fcu.keyframe_points[0].co[0]
            end_co = fcu.keyframe_points[-1].co[0]
            fcu_range = range(int(first_co),int(end_co))
            if frame in fcu_range:
                fcu.select = True
                if not ob in f_objects:
                    f_objects.append(ob)
    return f_objects

def map_range(value, in_min, in_max, out_min, out_max):
    in_span = in_max - in_min
    out_span = out_max - out_min
    in_scaled = float(value - in_min) / float(in_span)
    out = out_min + (in_scaled * out_span)
    return out

class LPFinstances:
    def __init__(self,context,selection,only_selected_curves):
        
        if only_selected_curves and len(context.selected_editable_fcurves) == 0:
            self.message = '"Only Selected Fcurves" option is on, but no curves are selected'
            return            

        if len(selection) == 0:
            self.message = 'At least two objects must be selected'
            return    
        try:
            selection[0].animation_data.action.fcurves
        except:
            self.message = 'Objects must be animated'
            return

 

        single = False
        armature = False
        if len(selection) == 1:
            ob = selection[0]
            single = True
        if single and ob.type == 'ARMATURE':
            armature = True

        

        
        selection = sorted(selection,key=lambda ob: ob.name)
        
        def selected_fcurves(fcurves):
            fcurves = [f for f in fcurves if f in context.selected_editable_fcurves]
            return fcurves
    
        objects = []
        if not armature:
            for ob in selection:
                # print(ob.name)
                fcurves = ob.animation_data.action.fcurves
                if only_selected_curves:
                    fcurves = selected_fcurves(fcurves)
                ob_data = {'object': ob,'fcurves': fcurves}
                
                objects.append(ob_data)
                
            self.type = 'OBJECTS'
        else:

            bones = context.selected_pose_bones
            bones = sorted(bones,key=lambda b: b.name)
            ob = selection[0]
            ob_fcurves = ob.animation_data.action.fcurves
            if bones != None:
                
                for b in bones:
                    print("aaa",b.name)
                    fcurves = []
                    for fcu in ob_fcurves:
                        n = re.findall('"([^"]*)"',fcu.data_path)[0]
                     
                        if n == b.name:

                            print('PATH ', fcu.data_path)
                            print(n)
                            
                            fcurves.append(fcu)
                    if only_selected_curves:
                        fcurves = selected_fcurves(fcurves)
                    ob_data = {'object': b,'fcurves': fcurves}
                    objects.append(ob_data)
                
            self.type = 'BONES'
        
        if len(objects) <= 1 and armature:
            self.message = 'At least two bones must be selected in Pose Mode'
            return
        if len(objects) <= 1 and not armature:
            self.message = 'At least two objects must be selected'
            return
        
        self.objects = objects

        
        self.message = 'Good'
        
    def set_position(self,ref_fcurves):
        
        objs = self.objects
        for ob in objs:
            fcurves = ob['fcurves']
            for fcu,first_fcu in zip(fcurves,ref_fcurves):
                for p,first_p in zip(fcu.keyframe_points,first_fcu.keyframe_points):
                    frame = first_p.co[0]      
                    move_point(p,frame)
        
    def offset(self,amount,global_amount,reset_curves):
        if self.message != 'Good':
            warnings.warn(self.message)
            return
       


        map = bpy.data.node_groups['shift_keyframes_group'].nodes[0].mapping
        map.update()

        objs = self.objects
        first_ob = objs[0]
        first_fcurves = first_ob['fcurves']
        

        for i,ob in enumerate(objs):
            curve_v = map.evaluate(map.curves[3],map_range(i,0,len(objs)-1,0,1))
           
            curve_v = map_range(curve_v,0,1,0,len(objs)-1)
            
            offs = curve_v * amount
            # offs = i * amount
            
            fcurves = ob['fcurves']
            for fcu,first_fcu in zip(fcurves,first_fcurves):
                for p,first_p in zip(fcu.keyframe_points,first_fcu.keyframe_points):
                    if reset_curves:
                        frame = first_p.co[0]      
                    else:
                        frame = p.co[0]              
                    # frame += (i)*amount
                    frame += offs
                    # frame = int(frame)
                    move_point(p,frame)

        all_fcurves = []   
        for i,ob in enumerate(objs):
            fcurves = ob['fcurves']
            for fcu in fcurves:
                for p in fcu.keyframe_points:
                    frame = p.co[0]
                    frame += global_amount
                    move_point(p,frame)
                all_fcurves.append(fcu)





    def offset_value(self,amount,global_amount,reset_curves):
        if self.message != 'Good':
            warnings.warn(self.message)
            return
       

        map = bpy.data.node_groups['shift_keyframes_group'].nodes[0].mapping
        map.update()

        objs = self.objects
        first_ob = objs[0]
        first_fcurves = first_ob['fcurves']
        


        for i,ob in enumerate(objs):
            curve_v = map.evaluate(map.curves[3],map_range(i,0,len(objs)-1,0,1))
           
            curve_v = map_range(curve_v,0,1,0,len(objs)-1)
            
            offs = curve_v * amount
            
            fcurves = ob['fcurves']
            for fcu,first_fcu in zip(fcurves,first_fcurves):
                for p,first_p in zip(fcu.keyframe_points,first_fcu.keyframe_points):
                    if reset_curves:
                        value = first_p.co[1]      
                    else:
                        value = p.co[1]              

                    value += offs
  
                    move_point_value(p,value)

        all_fcurves = []   
        for i,ob in enumerate(objs):
            fcurves = ob['fcurves']
            for fcu in fcurves:
                for p in fcu.keyframe_points:
                    frame = p.co[0]
                    frame += global_amount
                    move_point(p,frame)
                all_fcurves.append(fcu)
    

   
            
    def fix_looping(self,context):


        scene = context.scene
        start_frame = scene.frame_start
        end_frame = scene.frame_end
        start_offsets = []
        end_offsets = []
        all_fcurves = []

        objects = self.objects
 
        for ob in objects:
            fcurves = ob['fcurves']
            for fcu in fcurves:
                all_fcurves.append(fcu)

            k = fcurves[0].keyframe_points[0].co[0]

            offs_from_start = start_frame - k
            offs_from_end = end_frame - k
            end_offsets.append(offs_from_end)
            start_offsets.append(offs_from_start)

        start_offsets = [abs(offs) for offs in start_offsets if offs >=0]
        start_offs,ind_start = get_min_val_index(start_offsets)
        if start_offs == None:
            return False
 
        end_offsets_abs = [offs for offs in end_offsets if offs >=0 ]
        end_offs,ind_end = get_min_val_index(end_offsets_abs)
        end_offs_prev = end_offsets_abs[ind_end-1]

        step = end_offs_prev-end_offs

        diff = start_offs - end_offs

        frame_range = end_frame-start_frame

        new_range = frame_range + diff -1

        if end_offs > start_offs:
            new_range+=step

        

        ratio = frame_range/new_range
        ratio = round(ratio, 4)
        for i,ob in enumerate(objects):
            fcurves = ob['fcurves']  
            for fcu in fcurves:
                first_point = fcu.keyframe_points[0]
                fcu_start = first_point.co[0]
                fcu_start_new = fcu_start * ratio
                dist = fcu_start_new - fcu_start
                for k in fcu.keyframe_points:
                    co = k.co[0]
                    handle_left = k.handle_left[0]
                    handle_right = k.handle_right[0]

                    co += dist
                    handle_left += dist
                    handle_right += dist

                    k.co[0] = co
                    k.handle_left[0] = handle_left
                    k.handle_right[0] = handle_right

        # self.fix_fcurves_start_end(context)
    
    def fix_fcurves_start_end(self,context):
        objects = self.objects
        scene = context.scene
        start_frame = scene.frame_start
        end_frame = scene.frame_end

        start_objects = fcu_in_frame(objects,start_frame)
        end_objects = fcu_in_frame(objects,end_frame)
     

               
        if len(start_objects)!=len(end_objects):
            start_objects,end_objects,residue = compare_two_lists(start_objects,end_objects)
            if self.type == "OBJECTS":
                for ob in residue:
                    ob_ob = ob['object']
                    ob_ob.hide_viewport = True
                    ob_ob.hide_render = True
            else:
                self.message = 'Bones count at start and end frame not matching'
                return    
        # if len(start_objects)!=len(end_objects):
        #     self.message = 'Objects count at start and end frame not matching'
        #     return    
            
                            
        for start_ob,end_ob in zip(start_objects,end_objects):
            start_fcurves = start_ob["fcurves"]
            end_fcurves = end_ob["fcurves"] 
            for start_fcu,end_fcu in zip(start_fcurves,end_fcurves):
                print('-----')
                print(start_fcu.data_path)
                print(end_fcu.data_path)
                for start_key,end_key in zip(start_fcu.keyframe_points,end_fcu.keyframe_points):
                    diff = start_frame - start_key.co[0]
                    diff_handle_left = start_frame - start_key.handle_left[0]
                    diff_handle_right = start_frame - start_key.handle_right[0]
                    
                    co = end_frame - diff
                    co_handle_left = end_frame - diff_handle_left
                    co_handle_right = end_frame - diff_handle_right

                    end_key.co[0] = co + 1
                    end_key.handle_left[0] = co_handle_left + 1
                    end_key.handle_right[0] = co_handle_right + 1

                    end_key.co[1] = start_key.co[1]
                    end_key.handle_left[1] = start_key.handle_left[1]
                    end_key.handle_right[1] = start_key.handle_right[1]
        



    
    def print_fcurves_coords(self):
        objects = self.objects

        for i,ob in enumerate(objects):
            print('object:', i)
            fcurves = ob['fcurves']
            for j,fcu in enumerate(fcurves):
                print('fcurve:', j)
                for k in fcu.keyframe_points:
                    print(k.co[0])
    
     


    
class LPFinstancesNoAnim:
    def __init__(self,context,selection):

        if len(selection) == 0:
            self.message = 'At least two objects must be selected'
            return    

 

        single = False
        armature = False
        if len(selection) == 1:
            ob = selection[0]
            single = True
        if single and ob.type == 'ARMATURE':
            armature = True

 
        
        selection = sorted(selection,key=lambda ob: ob.name)
        
   
        objects = []
        if not armature:
            for ob in selection:
         
                ob_data = {'object': ob}
                
                objects.append(ob_data)
            self.type = 'OBJECTS'
        else:

            bones = context.selected_pose_bones

            if bones != None:
                
                for b in bones:
                  
                    ob_data = {'object': b}
                    objects.append(ob_data)
                
            self.type = 'BONES'
        
        if len(objects) <= 1 and armature:
            self.message = 'At least two bones must be selected in Pose Mode'
            return
        if len(objects) <= 1 and not armature:
            self.message = 'At least two objects must be selected'
            return
        
        self.objects = objects

        
        self.message = 'Good'

    def loc_rot_scale(self,add_to_existing,loc,rot,scl_min,scl_max):
        # if self.message != 'Good' or self.message != 'Objects must be animated':
        #     warnings.warn(self.message)
        #     return
        objs = self.objects
        
        map = bpy.data.node_groups['shift_keyframes_group'].nodes[0].mapping
        map.update()   

        for i,ob_ in enumerate(objs):
            curve_v = map.evaluate(map.curves[3],map_range(i,0,len(objs)-1,0,1))
           
            curve_v_ob = map_range(curve_v,0,1,0,len(objs)-1)    
            
            if type(loc) != Vector:
                loc = Vector(loc)

            if type(rot) != Vector:
                rot = Vector(rot)       
 

            print(type(rot))
            
            new_loc =  loc * curve_v_ob

            new_rot = rot * curve_v_ob

            curve_v_scl = map_range(curve_v,0,1,scl_min,scl_max)  
            
            new_scl = [curve_v_scl,curve_v_scl,curve_v_scl]
            new_scl = Vector(new_scl)

            ob = ob_["object"]      

            print(new_loc)
            if not add_to_existing:
                ob.location = new_loc
                ob.rotation_euler = new_rot
                ob.scale = new_scl
            else:
                ob.location += new_loc
                euler = ob.rotation_euler
                euler = Vector(euler)
                euler += new_rot
                ob.rotation_euler = new_rot
                ob.scale += new_scl
  
        

     


    

                            
        
        
                            
        
        