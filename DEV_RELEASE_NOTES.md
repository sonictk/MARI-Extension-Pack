#Release Notes for MARI EXTENSION PACK 2.2
Copyright (c) 2015 www.mari.ideascale.com. All Rights Reserved.

##New Features:

###Nodes & Shaders:

#####General:

######Nodes ready for Nodegraph

MARI Extension Pack Nodes have been reworked for best experience in the Nodegraph.
Nodes now have their most useful paramenters exposed as Node Handles to allow node-driven paramenters
(Octaves driven by another Noise etc.).
While Node Handles are unmapped, Node Sliders are used.
While Node Handles are mapped, Node Sliders are ignored.

#####Adjustment Layers:

######Historgram Scan

A node similar to a default Contrast Node but mimicking behavior of Substance Designers 'Histogram Scan' Node.

######RGB to HSV + HSV to RGB

Two new nodes were added to Layerstack & Nodegraph to convert values between RGB + HSV (Hue/Saturation/Value).

######RGB to HSL + HSL to RGB

Two new nodes were added to Layerstack & Nodegraph to convert values between RGB + HSL (Hue/Saturation/Lightness).


#####Geometry Procedurals:

######Transform Coordinates 3D
A node to transform object coordinates such as Position + Normal.
All Extension Pack Procedurals now have a 'Transform Coordinate' Handle
in the Nodegraph to attach this to.

Many Extension Pack Procedurals already have Scale/offset/Rotatuion options
built in but this can be used as a central control hub to modify multiple nodes at once.

######Transform Coordinates UV
A node to transform object UV Coordinates.
All Extension Pack Procedurals now have a 'Transform Coordinate' Handle
in the Nodegraph to attach this to.

Many Extension Pack Procedurals already have Scale/offset/Rotatuion options
built in but this can be used as a central control hub to modify multiple nodes at once.
Attaching this Node to a procedural will give the same effect as activating 'UV Space' in
the Procedural Options.


#####Layer Nodes (Nodegraph only):

######Transition Node
A node to add detail to mask edges.
This Node is only available in the Nodegraph.

######Mix Node
Very simple mix node to mix two colors by a mask. This is very similar to the 'merge' node but
a LOT lighter and faster in performance since you don't need to carry around blend modes, advanced blendmodes
etc. when you don't need them. For convenience a color A and color B can be set on the node. They will be ignored
if the corresponding handles are mapped in the nodegraph.
The Mix Slider will always be evaluated regardless of the Mix Noodle being mapped (in which case it's an added multiplier)

#####Material Nodes (Nodegraph only):

######Material Regions - WIP

New nodes were added as part of the implementation of 'Material Regions'.
Material Region Base, Material Region, Material Region Pass Through and
Material Region Value Selector.

Different Material Region Presets for different workflows (Roughness/Reflectance, Metallness/Roughness, Glossiness) are available.

Material Regions are a powerful way to layer different materials on top of each other, provide a logical grouping in the Nodegraph and giving the user maximum control over each part of the material. Other than Layered Shaders
performance is kept high by only passing a 'finished' channel to one shader
instead of layereing multiple shaders on top of each other.

Material Regions are only available in the Nodegraph.


###Tools:

#####Selection Groups:

######Material ID from Selection Group

A new tool was added to the 'Selection Group' Palette that will allow you to easily create a materialID channel from your selection groups


##Feature Improvements:

###Nodes & Shaders:


######Adjustments - General

Adjustments are now categorized in subfolders (Color Correction, Utilities etc.)

######Procedurals - General

ATTENTION: Some of the following changes will change the look of existing procedurals when converting Projects
           that use the old ones.

The 'Transform Scale' Settings (Scale X,Y,Z) have been refactored so that larger numbers now mean larger scale.
Previously procedurals would scale up in size the closer the value got to 0.0.
At default setting of 1.0 the result is identical as before.

Clamping options have been added to various procedurals where they were missing.
Clamping is now generaly performed on the result of the noise computation but before applying Color A / B.
This ensures that color mixing behaves relieably but it is still possible to set color values outside of 0-1 range.

Various Slider ranges have been refactored to a 0-1 range to make it easier to map attributes in the nodegraph with
paintable nodes or other procedurals.

Procedurals in the MainWindow/Layers/ Menu no longer appear under a
'CustomProcedurals' Folder but are merged into the main Procedurals,Geometry,
Environment etc. Folders


######Polysurface Curvature

Polysurface Curvature now has a 'Min Curvature' Attribute

The Polysurface Curvature Node now has an additional 'Normal Map Mix'.
When a Normal Map (for example a 'Normal Map' Channel) is attached to the
handle in the Nodegraph you are able to mix or add edges from a normalmap
into the final calculation of the curvature.


######Paintable Gabor Noise

Paintable Gabor Noise no longer appears under 'Adjustments'
and has been moved to Procedurals/Custom/Gabor/


######Custom Object Normal

Custom Obect Normal has been renamed to Custom Surface Normal to be in line
wit Maris Vocabulary.

######FBM+
FBM+ now uses a different algorithm, giving more predicatable results with less
overall 'flowing' of features across the surface when changing sliders


###Tools:


######Tools - General

We've continued adding improved performance to more tools such as ConvertToPaintable, ExportSelectedChannels, Duplicate-Flatten etc.
by surpressing viewport updates during their runtime.
This can lead to speed improvements of 40-50% in some cases.


######Duplicate/Flatten Channel

Duplicate/Flatten Channel will no longer create channel duplicates of channelLayers (shared channels) if the
duplicate/flattened channel contained channel layers


######Mask From Selection / Mask from Selection (inverted)

Layer/AddLayerMask/Mask From Selection + Mask From Selection (inverted) have been removed from MARI Extension Pack
since MARI 3 now ships natively with its own implementation.


######Patch Bake to Image Manager

'Patch Bake to Image Manager' now use Mari 3s new OCIO color management when loading images into the image manager.
The colorspace to load images in are determined by the selected channel when executing the tool.


######Unproject Channel to Image Manager / Unproject Layer to Image Manager

'Unproject Channel/Layer to Image Manager' now uses Mari 3s new OCIO color management on projectors and when loading
images into the image manager. The colorspace to unproject the image in is determined by the selected channel when executing the tool

'Unproject Channel/Layer to Image Manager' will now unproject images at 2x PaintBuffer Resolution or maximum 16k.

'Unproject Channel/Layer to Image Manager' will set the scale of the Projector based on the X Dimennsion of the Paintbuffer.
Unrpojected Images will always be square with a 1:1 Pixel Aspect Ratio.

'Unproject Channel/Layer to Image Manager' will unproject at appropriate bitDepth based on the selected channel/layer.
8bit Images are saved in PNG, 16bit/32bit in exr format.

'Unproject Channel/Layer to Image Manager' will now timestamp imported images and images will have the correct layer / channel name.


##Developer Notes:

######New Category handling

RegisterCustomShaders now uses the new mari.gl_render.registerCustomNodeFromXMLFile for
adjustments and procedurals.

As a result categories in Adjustment & Procedural Node XML Files now need to be specified explicitely including
their initial path (/Filters/, '/Procedurals/').
The path is no longer derrived from the TAGS attribute such as _adjustment.

Adjustments now need to be placed manually under adjustments by specifying
the path '/Filter/' in the CATEGORY section of the xml file

This allows for placement of adjustment files in other locations as the
Adjustment Layer Submenu.

######New Functions

Luminance function was updated

DT3D Noise Functions have been amended with clamping variable. Doc needs updating
col2mask function ?





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
