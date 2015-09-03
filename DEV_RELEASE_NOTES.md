#Release Notes for MARI EXTENSION PACK 3.0
Copyright (c) 2015 www.mari.ideascale.com. All Rights Reserved.

##New Features:

###Installation & Deployment:

Extension Pack 3.0 has a new File+Folder Structure within your SCRIPT Directory to make
it a compact. easy to update package.
Please refer to HELP/INSTALLATION/ for install instructions

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

#####Basic Nodes:

######Normal Color

A simple node generating a default tangent space normal color in sRGB or linear colorspace


#####Geometry Nodes:

######Transform Coordinates 3D
A node to transform object coordinates such as Position + Normal.
All Extension Pack Procedurals now have a 'Transform Coordinate' Handle
in the Nodegraph to attach this to.

Many Extension Pack Procedurals already have Scale/offset/Rotatuion options
built in but this can be used as a central control hub to modify multiple nodes at once.

######Transform Coordinates UV
A node to transform object UV Coordinates.
All Extension Pack Noises now have a 'Transform Coordinate' Handle
in the Nodegraph to attach this to.

Many Extension Pack Procedurals already have Scale/offset/Rotatuion options
built in but this can be used as a central control hub to modify multiple nodes at once.
Attaching this Node to a procedural will give the same effect as activating 'UV Space' in
the Procedural Options.


#####Environment Nodes:

######Image Node

The 'Image Node' will allow you to load an image with similar options as you have on the
default Mari 'Tiled' Node. However this node does not contain any UV transformation options (repeat, offset).
By attaching a 'Transform Coordinates UV' Node to the 'Image' Node Input you get the same options as a tiled node has
but with the advantage of being able to use different  tiling images in different channels while having only a single set
of controls for repeat, offset etc.


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


#####Region Nodes (Advanced Nodegraph only):

######Material Regions

New nodes were added as part of the implementation of 'Material Regions'.
Region Base, Region and Region Output

Different Material Region Presets for different workflows (Roughness/Reflectance, Metallness/Roughness, SpecularGlossiness) are available.

Material Regions are a powerful way to layer different materials on top of each other, provide a logical grouping in the Nodegraph and giving the user maximum control over each part of the material. Other than Layered Shaders
performance is kept high by only passing a 'finished' channel to one shader
instead of layereing multiple shaders on top of each other.

Material Regions are only available in the advanced Nodegraph (Preferences/Nodegraph/Enable Advanced Nodegraph)

######PBR Workflow Conversion Nodes

Two new nodes were added to convert Outputs from a Metal-Roughness workflow to a Reflectance/Roughness or Specular/Glossiness workflow.


###Tools:

#####File:

######Project Paths

'Project Paths' allows you to configure default paths (Texture Export+Import,Camera Locations, Image Manager defaults etc.)
and file templates for your project. Paths can be set relative to a project base path, folder creation is supported and
settings are saved between sessions.


#####Selection:

######Isolate Selection

A new menu item was added to the Selection menu and the right-click viewport menu ('Visibility' submenu) that allows you to isolate
the visibility of your current selection. Unselected parts of your model will be hidden. Once you toggle back, your original visibility
states will be restored. A default shortcut CTRL+1, indentical to Mayas 'Isolate Select' has been set as default but can be modifed
via the Shortcut Editor.

Currently only Face & Patch Selections are supported. Isolate Selection cannot be run to toggle visibilities in object mode.


#####Selection Groups:

######Material ID from Selection Group

A new tool was added to the 'Selection Group' Palette that will allow you to easily create a materialID channel from your selection groups


#####Objects:

######Export Object

It is now possible to export your geometry from inside Mari to an OBJ File.
Export Geometry can export either subdivided or unsubdivided geometry if OpenSubd is applied.

When launched via the 'Object' Menu you are able to select what geometry to export.
When launched via the right mouse click menu in the object palette, the selected geometry will be exported.

######Subdivision / Set all to Highest + Set all to Lowest

A new submenu was added to the Object menu and right click object dropdown to toggle all objects in your scene
to their highest or lowest available subdivision levels.
Locked Objects are respected.

######Subdivision / Set all Visible to Highest + Set all Visible to Lowest

A new submenu was added to the Object menu and right click object dropdown to toggle all visible objects in your scene
to their highest or lowest available subdivision levels.
Locked Objects are respected.



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


######Export Custom Channel Selection

'Export Custom Channel Selection' now separates the File Path and the File Export Template in its UI
to avoid having to retype the template everytime you change the path.
Path & Template Field support the usual MARI Variables such as $ENTITY,$CHANNEL etc.
If a $Variable is defined as a subfolder, folders will be auto-created. Otherwise a user prompt will appear.

'Export Custom Channel Selection' will now remember your last settings for checkbox options and Export File Template, an option was
added to reset the Export File Template to Project Default

'Export Custom Channel Selection' now uses the default Operation System Dialog for Path Selections instead of the
 limited MARI Default one.

'DISABLE SMALL TEXTURES' Checkbox is now a 'ENABLE SMALL TEXTURES' checkbox to not have double negatives

'Export Custom Channel Selection' now differentiates if it is being launched from 'Export' or 'Export Flattened' Submenu.
 On ExportFlattened, 'Export Flattened' checkbox is enabled by default and the File Template defaults to the
 template defined for flattened Textures. When launched from 'Export' submenu, 'Export Flattened' is off by default
 and file Template defaults to template defined for non-flattened Textures.
 Templates can be modified by using the new 'Project Paths' tool.


######Export UV Mask

'Export UV Mask' now uses a similar interface as 'Export Custom Channel Selection'

'Export UV Mask' now lets the user choose the Export File Template.
Path & Template Field support the usual MARI Variables such as $ENTITY,$CHANNEL etc.
If a $Variable is defined as a subfolder, folders will be auto-created. Otherwise a user prompt will appear.

Template Entries are saved between sessions

When launched via the 'Object' Menu you are able to select what geometry to export from.
When launched via the right mouse click menu in the object palette, the UV Masks from the selected geometry will be exported.

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


##Bugfixes:

###Tools:


######Pause Viewport Update

The icon for 'Pause Viewport Update' would not be found on MARI Configurations with multiple Script Paths.


######Export Custom Channel Selection

'Export Custom Channel Selection' errored in MARI 3.0 during Export.

'Export Custom Channel Selection' when used with 'Only Modified Textures' previously would error if the UDIM
Count increased (for example by adding geometry versions) or if users mistakenly removed the channel user attributes
used to determine changes in textures.

'Export Custom Channel Selection' when used with 'Only Modified Textures' previously would error with certain
 maskStack configurations.

'Export Custom Channel Selection' when used with 'Only Modified Textures' would not register changes to a channel
caused by a Channel Layer in the Layerstack.

 Metadata added to Channels to determine what textures have changed between exports are no longer visible to the user
 in the 'Channel' Info Section

######Clone & Merge Layers

'Clone & Merge Layers' when executed on a selection containing a locked layer would duplicate the selection in the stack
but error when merging. 'Clone & Merge Layers' will now unlock any locked layers after duplication so it can run correctly.


######Add Channel Mask / Add Channel Mask (grouped)

'Add Channel Mask' would cause a program crash in Mari 3.0

'Add Channel Mask (grouped) would error and stop working in Mari 3.0


######Create Channel from custom Channel Resolution

'Create new Channel from custom Resolution' UI Action under 'Scripts/'Channel'/'Templae' was calling the wrong tool
in Mari Extension Pack 2.1

######Save/Load Custom Channel Resolution

'Save Custom Channel Resolution' + 'Load Custom Channel Resolution' would error in Mari 3.0


######Image Manager/ Export Selection

'Image Manager'/'Export Selection' would error in Mari 3.0

'Image Manager'/'Export Selection' will now use the standard OS Folder Selection Dialog

'Image Manager'/'Export Selection' will now default to the Project Path for Reference Images defined by
 mari.resources.DEFAULT_IMAGE

Image Manager'/'Export Selection' cancel button will now more reliably cancel exports since the export thread
is now checking for a user executed cancel after every image export.



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
