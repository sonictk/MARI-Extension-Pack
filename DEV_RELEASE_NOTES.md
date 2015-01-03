#Release Notes for MARI EXTENSION PACK 2.0
Copyright (c) 2015 www.mari.ideascale.com. All Rights Reserved.

##Release Date
TBA

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

- "Color Range to Mask" now has a basic Grade Module for selected colors. Due to the size + expense 
  of the node baking or caching is recommended in bigger layer stacks.

- "Enhance Selection" Mode in Color Range to Mask was improved

#####GEOMETRY PROCEDURALS

- Polysurface Curvature now has a "Hard Edged" Mode that will clip grey values

- Polysurface Curvature now has a "Attentuate by Ambient Occlusion" Mode


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

- Jens Kafitz *www.campi3d.com // MariIdeas@campi3d.com*
- Miguel A Santiago Jr. *www.digiteck3d.com // miguel@digiteck3d.com*
- Nicholas Breslow *www.nbreslow.com // nick@nbreslow.com*
- Antoni Kujawa
- Orlando Esponda
- Antonio Neto


#####SHADER DEVELOPMENT

- Miguel A Santiago Jr. *www.digiteck3d.com // miguel@digiteck3d.com*
- Nicholas Breslow *www.nbreslow.com // nick@nbreslow.com*


#####MAC QA

- Yasin Hasanian
- Dave Girard
