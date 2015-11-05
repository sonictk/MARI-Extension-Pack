#Release Notes for MARI EXTENSION PACK 2.1
Copyright (c) 2015 www.mari.ideascale.com. All Rights Reserved.


##New Features:

#####SHADING MENU & LIGHTING TOOLBAR

######Pause Viewport Update

A new icon was added to the 'Lighting' Toolbar. When pressed the Mari Viewport
will be paused. This allows for operations such as Layer-reordering
do be done at significantly increased speed without having to wait for a viewport
update each time.


#####GEOMETRY PROCEDURALS

######Selection Fill

A new node that will fill the current selection (object, patches, faces) with the
color specified. The node needs to be converted to a paintable layer after use
since it will update the selection based on the current.


#####ADJUSTMENT LAYERS

######SV Lookup

Remap Saturation and Value along a Curve

######Edge from Normal Map

Similar to the 'Polysurface Curvature' Node this node will run an edge/curvature detection.
Other than 'Polysurface Curvature' this nodes takes into account the underlying layers (Normal Map)
instead of running the detection on your objects normals.
Due to Maris lack of filtering this node needs to be converted to a paintable one after use (by merging or using 'CLone & Merge')
and should get a gaussian blur applied for best use.

######Color Temperature

Adjustment Layer to change the color temperature in familiar way using Kelvin


#####SHADERS


######UNREAL Advanced

BRDF compatible with Unreal Engine. Some additional features over Mari's
Unreal Engine Shader include:

- PBS Warnings when painting illegal values
- Sliders for Values (will be overwritten when value slot is mapped)
- Emmissive Color
- Flat+Basic Lighting Modes will return BaseColor instead of black when metallic is 1



##Feature Improvements:

#####ADJUSTMENT LAYERS

######Set Range

The OldMin/OldMax and NewMin/NewMax Options have been converted from the previous range-locked sliders to textboxes to allow for easy input of values
below 0.0 and over 1.0.

The previous behavior of being able to control values per color channel
have been removed and replaced with per channel checkboxes.

######Illegal Value Warning

Illegal Value Warning now differentiates its color warning between values that are above the upper limit and ones that are below the lower limit


#####ENVIRONMENT PROCEDURALS

######Axis Projection

A new option 'Suppress Alpha' was added to optionally ignore the Alpha of the loaded image

Overall performance of the Node was increased significantly


#####CHANNELS

######Export Selected Channels + Duplicate Flatten Channels

The currently active channel will be pre-selected in the interface

Objects + Channels are now sorted alphabetically to be in line with Mari's Object and Channels Palettes.

Only channels from the current object will be displayed by default now.
A new checkbox 'List all Objects' was added  to return to the previous behavior.
The current object's channels will be bumped to the top of the list.

Channels created by layeredShader stacks (with cryptic channel names) will no longer appear in the list


#####LAYERS MENU



######Channel Layer / Channel Layer Mask / Channel Layer Mask (grouped)

Channel Layer Selection has a new Interface, with alphabetical channel sorting and channel filtering options

Multi Selections of Channel Layer are now possible. For each selected channel in the interface one channel layer will be added.

"Channel Layer" + "Channel Layer Mask" now works with layeredShaders

"Channel Layer Mask" now respects existing masks or mask stacks on creation by converting simple masks
into a mask stack and adding the channel mask or in case of existing mask stacks adding to it.

"Channel Layer Mask (grouped)" will now work with multiple selected layers, grouping layers under a single group with a Channel Mask added to the group node

"Channel Layer Mask" will now work with multiple selected layers, adding one ChannelMask per Layer.


######Convert to Paintable

Convert to Paintable can now be used on Channel Layers. Masks,Mask- and Adjustment Stacks will remain intact.


######Clone & Merge

Clone & Merge now has added logic to prevent it from duplicating channels when executed on a selection that included channel layers.
This includes cases where channel layers are used in (possibly nested) maskStacks & Adjustment Stacks.


######Mask from Selection

'Mask from Selection' now works with layeredShaders

'Mask from Selection' now works with multiple layer selection, adding one
mask per layer

'Mask from Selection' now respects existing masks or mask stacks  on creation by converting simple masks
into a mask stack and adding the channel mask or in case of existing mask stacks adding to it.


######Toggle Unselected Visibility / Toggle Unselected Lock

'Toggle Unselected Visibility' & 'Toggle Unselected Lock' will now work hierchary based:

    - selecting a group layer or a layer outside of a group will toggle only unselected layers and groups on the same hierchary depth.
    - selecting a layer within a group will only toggle unselected layers & groups in the same group.




##Bugfixes:

#####PATCHES

######Patch to Image Manager

'Patch to Image Manager' would not remove temporary layers when invalid
UDIM Numbers were found (for example when a plane is touching the
UV borders)

Added logic to prevent PatchToImageManager to create channel duplicates if
selected channel included channel layers

#####LAYERS

######Channel Layer / ChannelLayerMask / ChannelLayerMask (grouped)

Channel Layer+Masks now work correctly with pinned, floating or docked
Channels that are not selected in the Channel Palette but accessible in the interface

Channel Layer+Masks no longer show the cryptic channels generated by
layeredShaders in the channel selection dropdown


######Clone & Merge

'Clone & Merge' previously did not work correctly when executed in mask stacks

'Clone & Merge' now works correctly with pinned, floating or docked
Channels that are not selected in the Channel Palette but accessible in the interface


######Toggle Visibility / Toggle Lock
Toggling Layer Visibility or Lock for multiple selections previously did not work in mask & adjustment stacks

Toggle Unselected Visibility previously ignored groups

Toggling Layer Visibility or Lock now works correctly with pinned, floating or docked
Channels that are not selected in the Channel Palette but accessible in the interface



######Mask from Selection

'Mask From Selection' now works correctly with pinned, floating or docked
Channels that are not selected in the Channel Palette but accessible in the interface



######Convert to Paintable

'Convert to Paintable' now works correctly with pinned, floating or docked
Channels that are not selected in the Channel Palette but accessible in the interface




##Dev Notes:

######New functions to document:

// Kelvin to RGB
vec3 Kelvin2Rgb(float Kelvin);


//Luminance
// Returns Luminance of Image
float Luminance(vec3 color);


// sRgb to Linear Conversion
// vec3 + vec4 functions to convert to sRgb to linear
vec4 sRgb2Linear(vec4 Color);
vec3 sRgb2Linear(vec3 Color);


// Linear to sRGB conversion
// vec3 + vec4 functions to convert to linear to sRGB
vec4 linear2sRgb(vec4 Color)
vec3 linear2sRgb(vec3 Color)






----------------------------------------------------------------------

#Release Notes for MARI EXTENSION PACK 2.0
Copyright (c) 2015 www.mari.ideascale.com. All Rights Reserved.

##Release Date
28 January 2015

##Added Features:


#####ENVIRONMENT PROCEDURALS

######Texture Scatter UV
A UV based Texture Bombing Node capable of creating tileable textures on a standard
Maya Plane. Windows Users please refer to "Known Issues & Workarounds" at the bottom of this page
for important information to avoid display driver instability during baking.


######Axis Projection
Axis Projection is similar to a Triplanar Projection but with a lot more control over
rotation of projection in space (for objects that are not perfectly aligned in XYZ)
and isolation of each +/- axis

#####GEOMETRY PROCEDURALS

######Backface Mask
An way to isolate interior faces of objects for example cloth lining. Work off your objects normals

#####NOISE PROCEDURALS

######VoronoiPopcorn
A complex procedural for creating veins, cracks, crumbled paper looks etc.


#####BASIC PROCEDURALS

######Black/White/Grey Constants
Ever realized how many times you create a constant, then set it to black, white or grey ?
If the answer is : "A lot" then this simple addition of the 3 preconfigured constants will come in handy.
Press TAB and type !


#####ADJUSTMENT LAYERS

######Illegal Albedo Warning
Adjustment layer that gives a visual warning when values outisde a custom value range are detected.

######Posterize
Simple Posterize adjustment implementation, specifying how many color/value steps you want


#####IMAGE MANAGER

######Export Selection
A new feature was added to export multiple selected images from the Image Manager.
Existing naming and extensions are respected. If no extension is found "tif" will be used.


#####OBJECT MENU

######Export UV Mask
A new feature was added to the Object Menu that allows you to export Geometry UV Masks


#####CHANNELS MENU

######Duplicate & Flatten
A new feature was added that allows you to easily flatten a duplicated of a selected channel.
Naming of the new channel is inherited from the original, any sharing on the original is maintained.

######Export Custom Selection
A new Export Mode was added that allows you to export a custom selection of channels across multiple geometries

######Save/Load/Create from Channel Resolution
A new feature was added that allows you to transfer mixed UDIM Resolution Layouts between Channels


#####LAYERS MENU

######Clone & Merge
A new feature was added to give similar functionality to Photoshops "Merge Visible".
Clone & Merge will create a merged copy of all selected layers - optionally for selected UDIMs only.

######Toggle Visibility
New options have been added to toggle visibility state of multiple selected/unselected layers

######Toggle Lock
New options have been added to toggle lock state of multiple selected/unselected layers

######Channel Layer
A new option has been added to simplify the use of entire Channels in another Layerstack

######Channel Layer Mask + Grouped Channel Layer Mask
New options have been added to the "Add Mask" Menu to simplify the use of complete channels in a layer mask.
"Add grouped Channel mask" will place the selected layers in a group first and apply the channel mask to the group node.

######Mask from Selection
New options have been added to the "Add Mask" Menu to create Masks from selected patches.


#####PATCHES MENU

######Patch to Image Manager
A new option was added to the Patches Menu that will bake a copy of selected patches
and place the images in the Image Manager


#####CAMERA MENU

######Quick Unproject Channel/Layer
Two new options where added to quickly unproject the currently visibly
channel or layer to the Image Manager


#####VIEW MENU

######Screenshot All Channels
A new option was added to automatically screenshot all Channels in your project
(requires "Incremental" to be turned on under "Screenshot Settings")



##Feature Improvements:


#####ADJUSTMENT LAYERS

######Color Range to Mask

- "Color Range to Mask" now has a basic Grade Module for selected colors. Due to the size + expense
  of the node baking or caching is recommended in bigger layer stacks.

- "Enhance Selection" Mode in Color Range to Mask was improved

#####GEOMETRY PROCEDURALS

######Polysurface Curvature

- Polysurface Curvature now has a "Hard Edged" Mode that will clip grey values

- Polysurface Curvature now has a "Attentuate by Ambient Occlusion" Mode, giving more plausible results on
  hard-surface objects


#####LAYERS MENU

######Convert to Paintable
Convert to Paintable now supports selection of multiple Layers.
Layers will be converted to Paintable ones in the selected order.



##Bugfixes:


#####GENERAL

- svn or git files in the directories could cause the extension pack to not load properly


#####NOISE PROCEDURALS

- Legacy Cloud was broken and not behaving like Mari Cloud in Ideascale Nodepack 1.5



##Known issues & Workarounds:


- (WINDOWS USERS ONLY): Texture Scatter UV will crash your display driver during baking/flattening
  due to an automated windows feature that lets your driver time out after
  a few seconds of inactivity. To work around this you need to set

  - EDIT/PREFERENCES/GPU TAB
  - MAX RENDER SIZE FOR BAKING: 256 (default is 1024)

  to allow Mari to split the processing into smaller chunks

- Voronoi Popcorn is a rather expensive procedural. We recommend converting it to paintable.

- Color Range to Mask is a rather expensive adjustment. We recommend baking it down/merging
  applied grading.




##Credits:

#####PYTHON DEVELOPMENT

- Jorel Latraille, *http://www.jorel-latraille.com*
- Ben Neall *www.bneall.blogspot.co.nz //  bneall@gmail.com*
- Sreenivas Alapati *http://cg-cnu.blogspot.in // sreenivas9alapati@gmail.com*
- Miguel A Santiago Jr. *www.digiteck3d.com // miguel@digiteck3d.com*
- Jens Kafitz, *www.campi3d.com // MariIdeas@campi3d.com*
- Antoni Kujawa


#####NODE DEVELOPMENT

- Miguel A Santiago Jr. *www.digiteck3d.com // miguel@digiteck3d.com*
- Nicholas Breslow *www.nbreslow.com // nick@nbreslow.com*
- Jens Kafitz *www.campi3d.com // MariIdeas@campi3d.com*
- Antoni Kujawa
- Orlando Esponda
- Antonio Neto


#####SHADER DEVELOPMENT

- Miguel A Santiago Jr. *www.digiteck3d.com // miguel@digiteck3d.com*
- Nicholas Breslow *www.nbreslow.com // nick@nbreslow.com*


#####MAC QA

- Yasin Hasanian
- Dave Girard
