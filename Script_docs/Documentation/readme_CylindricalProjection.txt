# ------------------------------------------------------------------------------
# Available at: http://mari.ideascale.com/
# ------------------------------------------------------------------------------
# Cylindrical Prjection
# Copyright (c) 2014 Jens Kafitz. All Rights Reserved.
# ------------------------------------------------------------------------------
# Author: Jens Kafitz | Mari Ideascale
# Web: www.campi3d.com
# Web: www.mari.ideascale.com
# Email: info@campi3d.com
# ------------------------------------------------------------------------------
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
# ------------------------------------------------------------------------------

CONTENTS:
- Information
- Requirements
- Installation
- Node Tutorials
- Node Reference Guide
- where to find the node
- Release History



Information: ==============================================================

The cylindrical projection node is a new projection type useful for any cylindrical
object such as trees, pipes, weapons etc.


Requirements: ==============================================================

- Mari 2.5 or above
- Ideascale MARI Function Library 1.07.05 or higher


Installation: ==============================================================

Take scripts and put them into your user preference script directory. Or any startup
script path that Mari has set. Once these are in place, Mari on startup will run through
the scripts folder and load the procedural library. Going to the Python tab and showing
the console will allow you to see the modules loading up. This is where if in any case
the loading fails it will let you know. 


Example:
	• On Linux+Mac: ~/Mari/Scripts/
	• On Windows: Documents/Mari/Scripts/	


Node Tutorials: ==============================================================

A full demo video is available here: https://vimeo.com/94145101
A Quick Demo on how to position the projection is available here: https://vimeo.com/93711136

or refer to the readme_CylindricalProjection_QuickStart.jpg in your Script_Docs/Documentation Folder for a 
visual guide how to place a projection accurately in seconds even on objects with complex rotations/offsets.



Node Reference Guide: ==============================================================


-- TEXTURE MAP --

Debug Pattern:
A procedurally generated grid pattern to give quick feedback for UV Size and Projection Alignment

Texture Map:
The Map you want to project

Rotate Map:
Rotates the Map before projecting it

Slide: 	    Slides the texture along Z (Length) of cylinder

-- CYLINDER DIMENSION --

Lock UV Scale: 	
With LockUV Scale turned on, UV Scale will be adjusted for changes in Length and Radius to remain consistent.

Length:
Length of the Projection Cylinder.

Radius:
Radius of the Projection Cylinder. This determines mainly the end of the projection from the Cylinder Outwards.
Projection Clipping is currently square for performance reasons

Squash:		Will squash the cylinder around X (negative values) or y (positive values)

-- UV SIZE --

RepeatU		Texture repeat around the cylinder
RepeatV		Texture repeat along the length of the cylinder
UV Scale	A Multiplier for Repeat U and Repeat V.


-- Cylinder Pivot --

The cylinder Pivot is the most important setting to correctly align the Cylinder in Space. The Point defined here represents the center of
cylinder cap.


Display Object Position as RGB Value: 	Will show each point on the object in form on RGB Colors. You can sample those with the Pixel Analyzer Tool
					with "CPaint Buffer Clamping" turned of in the "Painting" Palette to get the XYZ values of any point you click on

X Offset				X Coordinate of Pivot
Offset					A Slider with a smaller Range to make fine adjustments to the X Offset

Y Offset				Y Coordinate of Pivot
Offset					A Slider with a smaller Range to make fine adjustments to the Y Offset

Z Offset				Z Coordinate of Pivot
Offset					A Slider with a smaller Range to make fine adjustments to the Z Offset


-- Transform Rotate (around pivot) --

Will swing the Cylinder around the Pivot defined under CYLINDER PIVOT Group.

Rotate X/Y	Will rotate the Cylinder around X or Y of the Pivot. By Default a standing Cylinder (Rotation Y: 90`) is generated.
Rotate Z	Will spin the cylinder around its own axis. Useful for example to rotate the one main seam or precisely position your texture.
Flip Z		Will flip the cylinder 180 degrees around Z of the Pivot. This can be useful if the cylinder is facing the wrong direction from the pivot.


-- Pie Clip --

Plane Slice Clip Start			Will slice the cylinder from the pivot downwards
Offet					A Slider with a smaller range to make fine adjustents to Plane Slice Clip Start
Plane Slice Clip End			Will slice the Cylinder from its end (defined by the length) upwards
Offet					A Slider with a smaller range to make fine adjustents to Plane Slice Clip Ende


Pie Slice Clip Start		        Will slice the cylinder cake style. In degrees of the cylinder
Offet					A Slider with a smaller range to make fine adjustents to Pie Slice Clip Start
Pie Slice Clip End		        Will slice the cylinder cake style. In degrees of the cylinder
Offet					A Slider with a smaller range to make fine adjustents to Pie Slice Clip End


-- Transform Helpers --

Most sliders of the node are sized to work with large objects such as Trees, Towers etc.. The following Multipliers can help with smaller scene sizes

Global Multiplier			Multiplies against all Transform Helpers. Sort of like one slider to rule them all.


Length/Radius Multiplier		By setting the value lower you can get more adjust the Slider of the Length + Radius Setting to your scene needs

Transform Offset Multiplier		Will multiply against the Transform Offsets. Please note this only affects the secondary Offsets. The main transform sliders
					X Offset, Y Offset and Z Offset will remain unaffected by this.

Clip Offset Multiplier			Will multiply against the Pie Clip Offsets. Please note this only affects the secondary Offsets. The main transform sliders
					("Start", "End") will remain unaffected by this.
	
		

		




Where to find the nodes: ============================================================

The new node is located under  Adjustments /Custom/


History: ============================================================================

# History:
# - 05/06/14		1.0 Release for Mari 2.5,2,6


Credits: ============================================================================

Based on work done for ColorToMask by the foundry.

 
        