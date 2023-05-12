# loopify-blender
Addon for making perfect animation loops and to simplify common animation tasks

To install the addon, open Blender, go to "Edit/Preferences/Addons" and press "Install" on the upper right corner. Locate the zip file and don't forget to enable it on the addon list and save preferences, restart Blender. 
It was tested on Windows and Mac only, so please write me, if it works on Linux. 

You'll find main interface of the addon on the right side of the graph editor. This means that the add-on is mainly designed to work with animation f-curves.

The addon can screw up your animation, so make sure that you save a copy of your project before using the addon. Its performance depends on the amount of data you use it with. Try starting with simple tasks that involve fewer objects and animation data, and do more complex operations after understanding how different operators work. I'm planning to upgrade this addon, add more functionality, and make it more consistent, so stay tuned!

Its user interface is divided into several categories:

1. "Instancing Operations" category

    Instancing operations category is a tool, that creates copies of animated objects or collections, to evenly distribute their animation f-curves across the timeline and to make seamless loop out of their animation.
    In terms of sorting objects or bones, their order in the outliner depends on their name. Therefore, if you want to reorder them, you can simply rename them accordingly to use them with Loopify.
    1.Instantiate Object: This operator creates multiple instances of an active object with animation offset. The offset allows you to create copies of an object with an offset in time so that they don't all animate at the same time. Later, you can use "Shift" operators to perform subsequent operations on those instances.
    2.Instantiate Collection: This operator creates multiple instances of an active collection. This is similar to the "Instantiate Object" operator but it creates instances of an entire collection. For better use of it, it's better to create an Armature object or another type of object, that drives the animation of other objects in collection. This operator finds all animated objects in duplicated collections, and puts them in separated collection for convenience. You can use those objects, to offset their animations on the timeline with Loopify.
    3.Shift Keyframes X: This operator allows you to offset the selected animated objects or bones keyframes on the X-axis, based on their index. This means that you can shift the timing of the keyframes. This operator only works with one armature object with selected bones.
    4.Shift Fcurves Y: This operator allows you to offset the selected animated objects or bones fcurves values on the Y-axis, based on their index. This means that you can shift the values of the keyframes. This operator only works with one armature object with selected bones.
    5.Shift Loc/Rot/Scale: This operator allows you to offset the selected objects or bones transforms, based on their index. You can choose to offset the location, rotation, or scale of the selected objects or bones. This operator only works with one armature object with selected bones.
    6.Instance/Shift Curve Mapping:
    Curve mapping for shifting operators. You make uneven offset
    by tweaking the curve.
    7.Fix Looping: This operator fixes the animation looping of instances. It works better with a uniform offset, meaning that if you have multiple instances of an object with different offsets, it may not work perfectly.

2. "Copy/Paste/Tweak" category

    1.Copy Keyframes: This operator copies all keyframes of selected fcurves. This means that you can duplicate the animation.
    2.Paste Keyframes:
    This operator pastes all copied keyframes with Copy Keyframes operator to the selected fcurves.
    3.Copy Offsets:
    This operator copies the initial values of the selected fcurves. It is useful when you want to copy the starting position of an animation and apply it to other frames. For example, you can copy the offset of a walk cycle and paste it to create another walk cycle with the same start position.
    4.Paste Offsets:
    This operator pastes copied offsets to the selected fcurves. It is useful when you want to make same offset for another motion.
    5.Set Value:
    This operator sets the exact value to all selected keyframes. It is useful when you want to type exact value to keyframe. You can tweak the value in the redo window on the left bottom corner. 

3. "Match Start/End" category

    1.Match Start/End 1: This operator sets the values and positions of the last pair of keyframes on selected fcurves, relative to the first pair of keyframes to make seamless loop of the animation. You need a minimum of 4 keyframes to use this operator.
    2.Match Start/End 2: This operator sets the value of the last keyframe the same as the first keyframe on selected fcurves to make seamless loop of the animation.
 
4. "Repeater" category

    1.Repeat/Ping Pong: This operator loops the animation on selected fcurves using a repeat or ping pong method.
    This means that you can create a looping animation that repeats or goes back and forth. It adds the "Cycles" modifier to the fcurves. 
    2.Fix Repeater Looping: This operator fixes repeater/ping pong looping. This means that if you have an animation that is set to repeat or ping pong, this operator will try to fix any issues with the looping.   

5. "Noise Modifier" category

    1.Loop Noise: This operator loops the noise modifier on selected fcurves. It creates second noise modifier, and blends those two noises, to make a loop.
    2.Remove Noise Loop: This operator removes the created noise loop on selected fcurves. This means that you can undo the loop created by the "Loop Noise" operator.
    3.Randomize Noise Seed: This operator randomizes the seed of the noise modifier on selected fcurves. This means that you can create different noise seed for each f-curve.
    4.Remove All Modifiers: This operator removes all modifiers on selected fcurves. This means that you can remove any modifiers that are affecting the animation.

6. "Rotation" category

    1.Loop Rotation: This operator loops the rotation of selected fcurves.You can specify amount of 360-degree rotations, to make a seamless loop.

7. Additional operators

    1.Fix Offset: This operator fixes the bone offset,when creating 'Follow Path' constraint. The button of the operator is in the constraint ui
    2.NLA editor operators
    3.Loop Strips: This operator repeats the active NLA strip, to fit them in the timeline


